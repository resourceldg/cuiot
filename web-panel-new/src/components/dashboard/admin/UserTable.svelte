<script lang="ts">
    import { goto } from "$app/navigation";
    import { getInstitutions } from "$lib/api/institutions";
    import {
        getPackages,
        getUserPackageSubscriptions,
    } from "$lib/api/packages";
    import {
        createRole,
        deleteRole,
        getRoles,
        updateRole,
    } from "$lib/api/roles";
    import {
        createUser,
        deleteUser,
        getUsers,
        updateUser,
    } from "$lib/api/users";
    import { user as sessionUser } from "$lib/sessionStore.js";
    import CalendarIcon from "$lib/ui/icons/CalendarIcon.svelte";
    import CheckIcon from "$lib/ui/icons/CheckIcon.svelte";
    import ClockIcon from "$lib/ui/icons/ClockIcon.svelte";
    import DollarIcon from "$lib/ui/icons/DollarIcon.svelte";
    import PackageIcon from "$lib/ui/icons/PackageIcon.svelte";
    import RefreshIcon from "$lib/ui/icons/RefreshIcon.svelte";
    import TargetIcon from "$lib/ui/icons/TargetIcon.svelte";
    import WarningIcon from "$lib/ui/icons/WarningIcon.svelte";
    import XIcon from "$lib/ui/icons/XIcon.svelte";
    import { onMount } from "svelte";
    import EditUserModal from "./EditUserModal.svelte";

    // Tipos explícitos para usuarios y roles
    interface Role {
        id: string;
        name: string;
        description?: string;
        permissions: Record<string, any>;
        is_system?: boolean;
    }
    interface User {
        id: string;
        email: string;
        username?: string;
        first_name: string;
        last_name?: string;
        phone?: string;
        date_of_birth?: string;
        gender?: string;
        professional_license?: string;
        specialization?: string;
        experience_years?: number;
        is_freelance: boolean;
        hourly_rate?: number;
        availability?: string;
        is_verified: boolean;
        institution_id?: number;
        is_active: boolean;
        last_login?: string;
        created_at: string;
        updated_at: string;
        roles?: string[];
    }

    // Estados
    let users: User[] = [];
    let roles: any[] = [];
    let loading = false;
    let rolesLoading = false;
    let error = "";
    let rolesError = "";

    let showDeleteModal = false;
    let showRoleModal = false;
    // Cambia la declaración de selectedUser para aceptar null
    let selectedUser: User | null = null;
    let deleting = false;
    let showDeleteNotification = false;
    let deleteNotificationType: "success" | "error" = "success";
    let deleteNotificationMessage = "";
    let deleteNotificationSubtitle = "";

    // Filtros
    let searchTerm = "";
    let statusFilter = "";
    let roleFilter = "";
    let packageFilter = "";
    let institutionFilter = "";
    let filterTimeout: number;

    function getFilterParams() {
        const params: any = {};

        // Search filter
        if (searchTerm && searchTerm.trim()) {
            params.search = searchTerm.trim();
        }

        // Status filter - convert to boolean for API
        if (statusFilter) {
            if (statusFilter === "todos") {
                // No aplicar filtro de estado
                delete params.is_active;
            } else {
                params.is_active = statusFilter === "activo";
            }
        } else {
            // Por defecto, solo mostrar usuarios activos
            params.is_active = true;
        }

        // Role filter
        if (roleFilter && roleFilter.trim()) {
            params.role = roleFilter.trim();
        }

        // Institution filter
        if (institutionFilter) {
            if (
                institutionFilter === "sin_institucion" ||
                institutionFilter === "none"
            ) {
                params.no_institution = true;
            } else {
                const institutionId = Number(institutionFilter);
                if (!isNaN(institutionId)) {
                    params.institution_id = institutionId;
                } else {
                    params.institution_name = institutionFilter;
                }
            }
        }

        // Package filter
        if (packageFilter) {
            // Los IDs de paquetes son UUIDs (strings), no números
            params.package_id = packageFilter;
        }

        return params;
    }

    $: if (
        searchTerm !== undefined ||
        statusFilter !== undefined ||
        roleFilter !== undefined ||
        packageFilter !== undefined ||
        institutionFilter !== undefined
    ) {
        clearTimeout(filterTimeout);
        filterTimeout = setTimeout(() => {
            loadUsers();
        }, 300);
    }

    let form = {
        name: "",
        email: "",
        password: "",
        role: "",
        status: "activo",
    };
    let roleForm = {
        name: "",
        description: "",
        permissions: {} as Record<string, any>,
        is_system: false,
    };
    let editablePermissions: Record<string, Record<string, boolean>> = {};
    let isNewRole = false;

    // Estado para modal de historial
    let showHistoryModal = false;
    let historyUser: User | null = null;
    let userHistory: any[] = [];
    let historyLoading = false;
    let historyError = "";

    // Estado para modal de paquetes
    let showPackageModal = false;
    let packageUser: User | null = null;
    let currentPackage: any = null;
    let packageHistory: any[] = [];
    let allPackages: any[] = [];
    let packageLoading = false;
    let packageError = "";

    // Estados para notificaciones de roles
    let showRoleNotification = false;
    let roleNotificationType: "success" | "error" = "success";
    let roleNotificationMessage = "";
    let roleNotificationSubtitle = "";

    // Estados para notificaciones de eliminación de roles
    let showDeleteRoleNotification = false;
    let deleteRoleNotificationType: "success" | "error" = "success";
    let deleteRoleNotificationMessage = "";
    let deleteRoleNotificationSubtitle = "";

    // Estados para notificaciones de usuarios creados
    let showUserCreatedNotification = false;
    let userCreatedNotificationMessage = "";
    let userCreatedNotificationSubtitle = "";

    // Modo debug visual
    let debugMode = false;
    let debugData: any = null;

    // Toggle para modo debug
    function toggleDebugMode() {
        debugMode = !debugMode;
        console.log("🔧 Debug mode:", debugMode ? "ON" : "OFF");
    }

    // --- Mapeo de nombres de roles a versión amigable ---
    const ROLE_LABELS = {
        // Roles del sistema
        admin: "Administrador",
        sysadmin: "Sysadmin",
        sin_rol: "Sin Rol",

        // Roles de cuidado (estándar)
        cared_person_self: "Sujeto de Cuidado (Autocuidado)",
        caredperson: "Sujeto de Cuidado (Delegado)",
        family_member: "Familiar",
        caregiver: "Cuidador",
        freelance_caregiver: "Cuidador Freelance",

        // Roles institucionales
        institution_admin: "Admin Institución",
        institution_staff: "Staff Institución",
        medical_staff: "Staff Médico",

        // Roles legados (mantener compatibilidad)
        "cuidador profesional": "Cuidador Profesional",
        familiar: "Familiar",
        "sujeto del cuidado": "Sujeto de Cuidado",
        "admin institución": "Admin Institución",

        // Roles inconsistentes (mantener compatibilidad)
        caredpersonself: "Sujeto de Cuidado (Autocuidado)",
    };

    // Manejo de errores para 'err' de tipo unknown
    function getErrorMessage(err: unknown): string {
        if (err instanceof Error) return err.message;
        if (typeof err === "string") return err;
        return "Error desconocido";
    }

    // Catálogos para filtros - SIMPLIFICADO
    let institutions: any[] = [];
    let packages: any[] = [];
    let loadingCatalogs = false;
    let catalogsError = "";

    // Cargar datos al montar el componente - CON VERIFICACIÓN DE AUTH
    onMount(async () => {
        console.log("🔧 UserTable onMount - Iniciando carga...");

        // Verificar si hay un usuario recién creado
        const newlyCreatedUserId = sessionStorage.getItem("newlyCreatedUserId");
        if (newlyCreatedUserId) {
            console.log(
                "🎉 UserTable onMount: Detectado usuario recién creado:",
                newlyCreatedUserId,
            );

            // Mostrar notificación de éxito
            userCreatedNotificationMessage = "Usuario creado exitosamente";
            userCreatedNotificationSubtitle =
                "El usuario ha sido registrado en el sistema y aparece en la primera línea de la tabla.";
            showUserCreatedNotification = true;

            // Limpiar el sessionStorage
            sessionStorage.removeItem("newlyCreatedUserId");
        }

        await loadUsers();
        await loadRoles();
    });

    // Función para cargar datos solo si está autenticado
    async function loadDataIfAuthenticated() {
        const token = localStorage.getItem("authToken");
        if (!token) {
            console.log("🔧 UserTable - No hay token, saltando carga de datos");
            return;
        }

        loadingCatalogs = true;
        catalogsError = "";
        try {
            let [insts, pkgs, rls] = await Promise.all([
                getInstitutions(),
                getPackages(),
                getRoles(),
            ]);
            // Deduplicar por nombre
            institutions = insts.filter(
                (inst: any, idx: number, arr: any[]) =>
                    arr.findIndex((i: any) => i.name === inst.name) === idx,
            );
            packages = pkgs.filter(
                (pkg: any, idx: number, arr: any[]) =>
                    arr.findIndex((p: any) => p.name === pkg.name) === idx,
            );
            roles = rls;
        } catch (err) {
            catalogsError = "Error al cargar catálogos";
            console.error("Error al cargar catálogos", err);
        } finally {
            loadingCatalogs = false;
        }
        await loadUsers();
    }

    // Función pública para recargar datos (puede ser llamada desde el padre)
    export function reloadData() {
        loadDataIfAuthenticated();
    }

    async function loadUsers() {
        loading = true;
        error = "";
        const { data, error: apiError } = await getUsers(getFilterParams());
        if (apiError) {
            error = apiError;
            users = [];
        } else if (data) {
            // Solo transformar roles, preservar el resto de los campos
            users = Array.isArray(data)
                ? data.map((user) => ({
                      ...user,
                      roles: Array.isArray(user.roles) ? user.roles : [],
                  }))
                : [];

            // Ordenar usuarios por fecha de creación descendente (más recientes primero)
            users.sort((a, b) => {
                const dateA = new Date(a.created_at || 0);
                const dateB = new Date(b.created_at || 0);
                return dateB.getTime() - dateA.getTime();
            });
        } else {
            users = [];
        }
        loading = false;
    }

    function clearFilters() {
        searchTerm = "";
        statusFilter = "";
        roleFilter = "";
        packageFilter = "";
        institutionFilter = "";
        loadUsers();
    }

    async function loadRoles() {
        rolesLoading = true;
        rolesError = "";
        try {
            roles = await getRoles();
            console.log("🔧 loadRoles - Roles cargados:", roles.length);
            console.log(
                "🔧 loadRoles - Roles activos:",
                roles.filter((r) => r.is_active !== false).length,
            );
            console.log(
                "🔧 loadRoles - Roles inactivos:",
                roles.filter((r) => r.is_active === false).length,
            );
            if (roles.some((r) => r.is_active === false)) {
                console.log(
                    "🔧 loadRoles - Roles inactivos encontrados:",
                    roles
                        .filter((r) => r.is_active === false)
                        .map((r) => r.name),
                );
            }
        } catch (err) {
            rolesError = getErrorMessage(err);
        } finally {
            rolesLoading = false;
        }
    }

    function openDeleteModal(user: User) {
        selectedUser = user;
        showDeleteModal = true;
    }

    function closeDeleteModal() {
        showDeleteModal = false;
        selectedUser = null;
    }

    // --- Validaciones para roles ---
    let roleErrors = { name: "", description: "" };
    let roleSuccess = "";

    function validateRoleForm() {
        roleErrors = { name: "", description: "" };
        roleSuccess = "";
        if (!roleForm.name.trim()) {
            roleErrors.name = "El nombre del rol es requerido.";
        } else if (
            roles.some(
                (r) =>
                    r.name === roleForm.name &&
                    (isNewRole || r.name !== roleForm.name),
            )
        ) {
            roleErrors.name = "Ya existe un rol con ese nombre.";
        }
        if (!roleForm.description || roleForm.description.trim().length < 5) {
            roleErrors.description =
                "La descripción debe tener al menos 5 caracteres.";
        }
        return !roleErrors.name && !roleErrors.description;
    }

    const PERMISSION_CATEGORIES = {
        users: { read: false, write: false, delete: false },
        roles: { read: false, write: false, delete: false },
        institutions: { read: false, write: false, delete: false },
        packages: { read: false, write: false, delete: false },
        alerts: { read: false, write: false, delete: false },
        events: { read: false, write: false, delete: false },
        reports: { read: false, write: false, delete: false },
    };

    function openNewRoleModal() {
        roleForm = {
            name: "",
            description: "",
            permissions: {},
            is_system: false,
        };
        isNewRole = true;
        editablePermissions = JSON.parse(JSON.stringify(PERMISSION_CATEGORIES));
        showRoleModal = true;
        roleErrors = { name: "", description: "" };
        roleSuccess = "";
    }

    function openRoleModal(role: Role) {
        roleForm = {
            id: role.id,
            name: role.name,
            description: role.description || "",
            permissions: role.permissions,
            is_system: role.is_system || false,
        };
        // Inicializar editablePermissions con los permisos actuales del rol, rellenando faltantes
        let perms = role.permissions;
        if (typeof perms === "string") {
            try {
                perms = JSON.parse(perms);
            } catch {
                perms = {};
            }
        }
        // Asegurar que perms no sea null
        if (!perms || typeof perms !== "object") {
            perms = {};
        }
        editablePermissions = {};
        for (const cat in PERMISSION_CATEGORIES) {
            editablePermissions[cat] = {
                ...PERMISSION_CATEGORIES[
                    cat as keyof typeof PERMISSION_CATEGORIES
                ],
                ...(perms[cat] || {}),
            };
        }
        isNewRole = false;
        showRoleModal = true;
        roleErrors = { name: "", description: "" };
        roleSuccess = "";
    }

    function closeRoleModal() {
        showRoleModal = false;
        roleForm = {
            name: "",
            description: "",
            permissions: {},
            is_system: false,
        };
        editablePermissions = {};
        isNewRole = false;
        rolesError = "";
    }

    function handlePermissionChange(
        category: string,
        permission: string,
        value: boolean,
    ) {
        if (
            editablePermissions &&
            editablePermissions[category as keyof typeof PERMISSION_CATEGORIES]
        ) {
            editablePermissions[category as keyof typeof PERMISSION_CATEGORIES][
                permission
            ] = value;
            roleForm.permissions = editablePermissions;
        }
    }

    async function saveUser() {
        error = "";
        if (selectedUser) {
            // Actualizar usuario existente
            const updateData = {
                email: form.email,
                first_name: form.name.split(" ")[0] || "",
                last_name: form.name.split(" ").slice(1).join(" ") || "",
                is_active: form.status === "activo",
            };

            const { error: updateError } = await updateUser(
                selectedUser.id,
                updateData,
            );
            if (updateError) {
                error = updateError;
                return;
            }
        } else {
            // Crear nuevo usuario
            const createData = {
                email: form.email,
                first_name: form.name.split(" ")[0] || "",
                last_name: form.name.split(" ").slice(1).join(" ") || "",
                password: form.password,
                is_active: form.status === "activo",
            };

            const { error: createError } = await createUser(createData);
            if (createError) {
                error = createError;
                return;
            }
        }
        await loadUsers();
    }

    async function deleteUserHandler() {
        error = "";
        if (!selectedUser?.id) {
            error = "Usuario no seleccionado";
            console.error("❌ deleteUserHandler: Usuario no seleccionado");
            return;
        }

        deleting = true;
        showDeleteNotification = false; // Reset notification state
        deleteNotificationType = "success"; // Default to success
        deleteNotificationMessage = "";
        deleteNotificationSubtitle = "";

        console.log("🔧 deleteUserHandler: Iniciando eliminación de usuario", {
            userId: selectedUser.id,
            userName:
                `${selectedUser.first_name} ${selectedUser.last_name || ""}`.trim(),
        });

        try {
            const result = await deleteUser(selectedUser.id);
            console.log(
                "✅ deleteUserHandler: Usuario eliminado exitosamente",
                result,
            );

            await loadUsers();
            deleteNotificationMessage = "Usuario desactivado";
            deleteNotificationSubtitle = `El usuario ${selectedUser.first_name} ${selectedUser.last_name || ""} ha sido desactivado del sistema.`;
            showDeleteNotification = true;
        } catch (err) {
            const errorMessage = getErrorMessage(err);
            console.error("❌ deleteUserHandler: Error al eliminar usuario", {
                userId: selectedUser.id,
                error: err,
                errorMessage,
            });

            // Manejar errores específicos
            let userFriendlyMessage = "Error al eliminar usuario";
            let userFriendlySubtitle = errorMessage;

            if (errorMessage.includes("No puedes eliminar tu propia cuenta")) {
                userFriendlyMessage = "No puedes eliminar tu propia cuenta";
                userFriendlySubtitle =
                    "Por seguridad, no puedes eliminar la cuenta con la que estás conectado.";
            } else if (errorMessage.includes("404")) {
                userFriendlyMessage = "Usuario no encontrado";
                userFriendlySubtitle =
                    "El usuario que intentas eliminar ya no existe en el sistema.";
            } else if (errorMessage.includes("403")) {
                userFriendlyMessage = "Sin permisos";
                userFriendlySubtitle =
                    "No tienes permisos para eliminar usuarios.";
            } else if (errorMessage.includes("500")) {
                userFriendlyMessage = "Error del servidor";
                userFriendlySubtitle =
                    "Ocurrió un error interno. Intenta nuevamente.";
            }

            error = errorMessage;
            deleteNotificationType = "error";
            deleteNotificationMessage = userFriendlyMessage;
            deleteNotificationSubtitle = userFriendlySubtitle;
            showDeleteNotification = true;
        } finally {
            deleting = false;
            closeDeleteModal();
        }
    }

    async function saveRole() {
        if (!validateRoleForm()) return;

        console.log("🔧 saveRole: Iniciando guardado de rol", {
            isNewRole,
            roleName: roleForm.name,
            roleId: roleForm.id,
        });

        // Asegurar que editablePermissions no sea null
        const permissionsToSave = editablePermissions || {};

        // Actualizar permisos antes de enviar
        const dataToSend = {
            ...roleForm,
            permissions: JSON.stringify(permissionsToSave),
        };

        console.log("🔧 saveRole: Datos a enviar", dataToSend);

        try {
            if (isNewRole) {
                const result = await createRole(dataToSend);
                console.log("✅ saveRole: Rol creado exitosamente", result);
                roleNotificationMessage = "Rol creado exitosamente";
                roleNotificationSubtitle =
                    "El nuevo rol ha sido agregado al sistema.";
            } else {
                const result = await updateRole(roleForm.id, dataToSend);
                console.log(
                    "✅ saveRole: Rol actualizado exitosamente",
                    result,
                );
                roleNotificationMessage = "Rol actualizado exitosamente";
                roleNotificationSubtitle =
                    "Los cambios han sido guardados correctamente.";
            }
            await loadRoles();
            await loadUsers(); // Recargar usuarios para actualizar los roles
            roleNotificationType = "success";
            showRoleNotification = true;
        } catch (err) {
            const errorMessage = getErrorMessage(err);
            console.error("❌ saveRole: Error al procesar rol", {
                isNewRole,
                roleName: roleForm.name,
                roleId: roleForm.id,
                error: err,
                errorMessage,
            });

            rolesError = errorMessage;
            roleNotificationType = "error";
            roleNotificationMessage = "Error al procesar el rol";
            roleNotificationSubtitle = errorMessage;
            showRoleNotification = true;
        }
    }

    async function deleteRoleHandler(roleId: string) {
        console.log("🔧 deleteRoleHandler: Iniciando eliminación de rol", {
            roleId,
        });

        try {
            const result = await deleteRole(roleId);
            console.log(
                "✅ deleteRoleHandler: Rol desactivado exitosamente",
                result,
            );

            await loadRoles();
            await loadUsers(); // Recargar usuarios para actualizar los roles
            deleteRoleNotificationType = "success";
            deleteRoleNotificationMessage = "Rol desactivado exitosamente";
            deleteRoleNotificationSubtitle = `El rol ha sido desactivado del sistema. ${result.users_affected || 0} usuarios afectados.`;
            showDeleteRoleNotification = true;
        } catch (err) {
            const errorMessage = getErrorMessage(err);
            console.error("❌ deleteRoleHandler: Error al eliminar rol", {
                roleId,
                error: err,
                errorMessage,
            });

            // Manejar errores específicos
            let userFriendlyMessage = "Error al eliminar rol";
            let userFriendlySubtitle = errorMessage;

            if (
                errorMessage.includes("No se puede eliminar un rol de sistema")
            ) {
                userFriendlyMessage = "No se puede eliminar un rol de sistema";
                userFriendlySubtitle =
                    "Los roles de sistema están protegidos y no pueden ser eliminados.";
            } else if (errorMessage.includes("404")) {
                userFriendlyMessage = "Rol no encontrado";
                userFriendlySubtitle =
                    "El rol que intentas eliminar ya no existe en el sistema.";
            } else if (errorMessage.includes("403")) {
                userFriendlyMessage = "Sin permisos";
                userFriendlySubtitle =
                    "No tienes permisos para eliminar roles.";
            } else if (errorMessage.includes("400")) {
                userFriendlyMessage = "Error de validación";
                userFriendlySubtitle =
                    "No se puede eliminar este rol debido a restricciones del sistema.";
            }

            rolesError = errorMessage;
            deleteRoleNotificationType = "error";
            deleteRoleNotificationMessage = userFriendlyMessage;
            deleteRoleNotificationSubtitle = userFriendlySubtitle;
            showDeleteRoleNotification = true;
        }
    }

    async function openHistoryModal(user: User) {
        historyUser = user;
        showHistoryModal = true;
        historyLoading = true;
        historyError = "";
        userHistory = [];
        try {
            // Aquí deberías hacer fetch real de historial (mockup)
            userHistory = [
                {
                    type: "evento",
                    date: "2024-07-10",
                    desc: "Evento importante",
                },
                { type: "alarma", date: "2024-07-09", desc: "Alarma activada" },
                {
                    type: "reporte",
                    date: "2024-07-08",
                    desc: "Reporte médico cargado",
                },
                {
                    type: "recordatorio",
                    date: "2024-07-07",
                    desc: "Recordatorio enviado",
                },
            ];
        } catch (err) {
            historyError = getErrorMessage(err);
        } finally {
            historyLoading = false;
        }
    }
    function closeHistoryModal() {
        showHistoryModal = false;
        historyUser = null;
        userHistory = [];
        historyError = "";
    }

    async function openPackageModal(user: any) {
        console.log("🔧 openPackageModal - INICIANDO FUNCIÓN");
        console.log("🔧 openPackageModal - Usuario:", user);
        console.log("🔧 openPackageModal - User ID:", user.id);
        console.log("🔧 openPackageModal - User email:", user.email);

        // Verificar si el usuario puede tener paquetes
        if (!userCanHavePackages(user)) {
            console.log(
                "🔧 openPackageModal - Usuario no puede tener paquetes",
            );
            return;
        }

        selectedUser = user;
        userPackageSubscriptions = [];
        packageModalError = "";
        loadingPackages = true;

        console.log("🔧 openPackageModal - Variables inicializadas");

        try {
            console.log(
                "🔧 openPackageModal - Llamando getUserPackageSubscriptions...",
            );
            userPackageSubscriptions = await getUserPackageSubscriptions(
                user.id,
            );
            console.log(
                "🔧 openPackageModal - Respuesta:",
                userPackageSubscriptions,
            );
        } catch (e: any) {
            console.error("❌ openPackageModal - Error:", e);
            packageModalError =
                e.message || "Error al cargar las suscripciones de paquetes.";
        } finally {
            loadingPackages = false;
            showPackageModal = true;
            console.log(
                "🔧 openPackageModal - Modal abierto, loadingPackages:",
                loadingPackages,
            );
        }
    }
    function closePackageModal() {
        showPackageModal = false;
        packageUser = null;
        currentPackage = null;
        packageHistory = [];
        allPackages = [];
        packageError = "";
    }

    let showEditModal = false;
    let sessionUserRole = "";
    $: sessionUserRole =
        Array.isArray($sessionUser?.roles) && $sessionUser.roles.length > 0
            ? $sessionUser.roles[0]
            : "";

    let editAnchorRect: DOMRect | null = null;

    function openEditModal(user: User, event?: MouseEvent) {
        selectedUser = user;
        if (event && event.currentTarget) {
            const rect = (
                event.currentTarget as HTMLElement
            ).getBoundingClientRect();
            editAnchorRect = rect;
        } else {
            editAnchorRect = null;
        }
        showEditModal = true;
    }
    function closeEditModal() {
        showEditModal = false;
        selectedUser = null;
        editAnchorRect = null;
    }
    // Reemplaza handleEditSave para refrescar usuarios y cerrar el modal
    async function handleEditSave() {
        // Recargar usuarios desde la API
        await loadUsers();
        closeEditModal();
    }

    // Utilidad para obtener solo el rol activo (deduplicado)
    function getActiveRole(user) {
        if (!user || !Array.isArray(user.roles)) return null;

        // Deduplicar roles y obtener el más relevante
        const uniqueRoles = [...new Set(user.roles)];

        if (uniqueRoles.length === 0) return null;

        // Priorizar roles específicos
        const priorityRoles = [
            "admin",
            "institution_admin",
            "medical_staff",
            "cared_person_self",
        ];
        for (const priorityRole of priorityRoles) {
            if (uniqueRoles.includes(priorityRole)) {
                return priorityRole;
            }
        }

        // Si no hay roles prioritarios, devolver el primero
        return uniqueRoles[0];
    }

    // Utilidad para obtener solo el paquete activo
    function getActivePackage(user) {
        const packages =
            user && Array.isArray(user.package_subscriptions)
                ? user.package_subscriptions
                : [];
        // Si hay más de uno, muestra warning (opcional)
        if (packages.length > 1) {
            console.warn(
                `Usuario ${user.email} tiene más de un paquete activo`,
                packages,
            );
        }
        // Devuelve el primero si existe
        return packages[0] || null;
    }

    // --- Confirmación de borrado de rol ---
    let showDeleteRoleModal = false;
    let roleToDelete: Role | null = null;
    let deleteRoleSuccess = "";

    function confirmDeleteRole(role: Role) {
        roleToDelete = role;
        showDeleteRoleModal = true;
        deleteRoleSuccess = "";
    }
    function closeDeleteRoleModal() {
        showDeleteRoleModal = false;
        roleToDelete = null;
        deleteRoleSuccess = "";
    }
    let deletingRole = false;

    async function handleDeleteRole() {
        if (!roleToDelete) return;
        deletingRole = true;
        try {
            const result = await deleteRole(roleToDelete.id);

            // Pequeño delay para asegurar que el backend procese la eliminación
            await new Promise((resolve) => setTimeout(resolve, 500));

            await loadRoles();
            await loadUsers(); // Recargar usuarios para actualizar los roles

            // Mostrar notificación de éxito
            deleteRoleNotificationType = "success";
            deleteRoleNotificationMessage = "Rol desactivado exitosamente";
            deleteRoleNotificationSubtitle = `El rol ha sido desactivado del sistema. ${result.users_affected || 0} usuarios afectados.`;
            showDeleteRoleNotification = true;

            deletingRole = false;
        } catch (err) {
            const errorMessage = getErrorMessage(err);
            let userFriendlyMessage = "Error al desactivar el rol";
            let userFriendlySubtitle = "Ha ocurrido un error inesperado";

            // Mensajes específicos según el tipo de error
            if (
                errorMessage.includes("No se puede eliminar un rol de sistema")
            ) {
                userFriendlyMessage = "Rol de sistema protegido";
                userFriendlySubtitle =
                    "Los roles de sistema no pueden ser eliminados por seguridad";
            } else if (errorMessage.includes("Rol no encontrado")) {
                userFriendlyMessage = "Rol no encontrado";
                userFriendlySubtitle =
                    "El rol que intentas eliminar ya no existe";
            } else if (errorMessage.includes("Sin permisos")) {
                userFriendlyMessage = "Sin permisos";
                userFriendlySubtitle = "No tienes permisos para eliminar roles";
            } else if (errorMessage.includes("Error de validación")) {
                userFriendlyMessage = "Error de validación";
                userFriendlySubtitle = "Los datos del rol no son válidos";
            }

            deleteRoleNotificationType = "error";
            deleteRoleNotificationMessage = userFriendlyMessage;
            deleteRoleNotificationSubtitle = userFriendlySubtitle;
            showDeleteRoleNotification = true;

            deletingRole = false;
        }
    }

    // ... existing code ...
    $: if (showRoleNotification) {
        setTimeout(() => {
            showRoleNotification = false;
            closeRoleModal();
        }, 1300); // duración de la animación + margen
    }

    // ... existing code ...
    $: if (showDeleteNotification) {
        setTimeout(() => {
            showDeleteNotification = false;
            closeDeleteModal();
        }, 1300);
    }

    // ... existing code ...
    $: if (showDeleteRoleNotification) {
        setTimeout(() => {
            showDeleteRoleNotification = false;
            closeDeleteRoleModal();
        }, 1300);
    }

    // Timeout para notificación de usuario creado
    $: if (showUserCreatedNotification) {
        setTimeout(() => {
            showUserCreatedNotification = false;
        }, 3000); // Mostrar por 3 segundos
    }

    let notification = "";

    $: if (institutionFilter === "none") {
        institutionFilter = "";
        notification =
            "No puedes seleccionar una institución y 'sin institución' a la vez.";
    }

    $: if (roleFilter === "admin") {
        if (institutionFilter) institutionFilter = "";
        if (packageFilter) packageFilter = "";
        notification =
            "El rol 'admin' no puede combinarse con institución ni paquete.";
    }

    $: if (roleFilter === "institution") {
        if (statusFilter) statusFilter = "";
        if (packageFilter) packageFilter = "";
        notification =
            "El rol 'institution' no puede combinarse con estado ni paquete.";
    }

    $: if (
        users.length === 0 &&
        (roleFilter || institutionFilter || packageFilter || statusFilter)
    ) {
        notification =
            "No hay usuarios que cumplan con todos los filtros seleccionados. Prueba ajustando los criterios.";
    }

    function clearNotification() {
        notification = "";
    }

    // --- PAGINACIÓN ---
    let currentPage = 1;
    const pageSize = 6;
    $: totalPages = Math.ceil(users.length / pageSize);
    $: pagedUsers = users.slice(
        (currentPage - 1) * pageSize,
        currentPage * pageSize,
    );
    function nextPage() {
        if (currentPage < totalPages) currentPage++;
    }
    function prevPage() {
        if (currentPage > 1) currentPage--;
    }
    $: if (users.length && currentPage > totalPages)
        currentPage = totalPages || 1;

    // Roles que pueden tener paquetes (individuales o institucionales)
    const ROLES_WITH_PACKAGE = [
        "cared_person_self", // Paquetes individuales
        "family_member", // Paquetes individuales
        "institution_admin", // Paquetes institucionales
    ];

    let sessionUserRoles: string[] = Array.isArray($sessionUser?.roles)
        ? $sessionUser.roles
        : [];

    function canContractPackage() {
        const allowed = [
            "admin_institution",
            "institution_admin",
            "cared_person_self",
            "family_member",
        ];
        return sessionUserRoles.some((r) => allowed.includes(r));
    }
    function isInstitutionStaffOnly() {
        return (
            sessionUserRoles.includes("institution_staff") &&
            !sessionUserRoles.some((r) =>
                ["admin_institution", "institution_admin"].includes(r),
            )
        );
    }

    let userPackageSubscriptions = [];
    let loadingPackages = false;
    let packageModalError = "";

    // Corrección de acceso a roles en usuarios
    function getUserRoles(user: User | { roles?: string[] }): string[] {
        return user && Array.isArray(user.roles) ? user.roles : [];
    }

    // Función para verificar si un usuario puede tener paquetes
    function userCanHavePackages(user: User): boolean {
        const userRoles = getUserRoles(user).map((role) =>
            role.trim().toLowerCase(),
        );
        const allowedRoles = ROLES_WITH_PACKAGE.map((role) =>
            role.trim().toLowerCase(),
        );
        const canHave = userRoles.some((role) => allowedRoles.includes(role));
        return canHave;
    }

    // Función para verificar si un usuario tiene suscripciones reales
    function userHasPackageSubscriptions(user: User): boolean {
        // Por ahora, solo verificamos si el usuario puede tener paquetes
        // En el futuro, podríamos hacer una llamada a la API para verificar suscripciones reales
        return userCanHavePackages(user);
    }

    // Función para obtener las suscripciones de un usuario (para mostrar en el modal)
    async function getUserPackageSubscriptionsForModal(user: User) {
        if (!userHasPackageSubscriptions(user)) {
            return [];
        }

        try {
            const response = await getUserPackageSubscriptions(user.id);
            console.log(
                "🔧 getUserPackageSubscriptionsForModal - Respuesta:",
                response,
            );
            return response || [];
        } catch (error) {
            console.error("🔧 Error al obtener suscripciones:", error);
            return [];
        }
    }

    function asignarNuevoPaquete(user) {
        alert(
            `Asignar paquete a: ${user.first_name} ${user.last_name || ""} (${user.email})`,
        );
        // Aquí irá el flujo real de asignación/creación de paquete
    }
</script>

<div class="user-table-section">
    <div class="section-header">
        <div class="header-content">
            <h2>👥 Gestión de Usuarios</h2>
            <p>Administra usuarios, roles y permisos del sistema</p>
        </div>
        <div class="header-actions">
            <button class="btn-secondary debug-btn" on:click={toggleDebugMode}>
                {debugMode ? "🔧 Debug ON" : "🔧 Debug OFF"}
            </button>
        </div>
    </div>

    <!-- Botones de acción principales -->
    <div class="main-actions">
        <div class="action-group">
            <button
                class="btn-primary action-btn"
                on:click={() => goto("/dashboard/users/create")}
            >
                <svg
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                >
                    <path d="M12 5v14M5 12h14" />
                </svg>
                <span>Nuevo Usuario</span>
            </button>
            <button
                class="btn-secondary action-btn"
                on:click={openNewRoleModal}
            >
                <svg
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                >
                    <path d="M12 5v14M5 12h14" />
                </svg>
                <span>Nuevo Rol</span>
            </button>
        </div>
    </div>

    <!-- Sección de Roles -->
    <div class="roles-section">
        <div class="roles-header">
            <h3>Roles del Sistema</h3>
        </div>
        {#if rolesLoading}
            <div class="loading">Cargando roles...</div>
        {:else if rolesError}
            <div class="error">{rolesError}</div>
        {:else if roles.length === 0}
            <div class="empty">No hay roles definidos.</div>
        {/if}
        <div class="roles-grid">
            {#each roles.filter((role) => role.is_active !== false) as role (role.id)}
                <div class="role-card {role.is_active ? 'active' : 'inactive'}">
                    <div class="role-header">
                        <h4>
                            {ROLE_LABELS[
                                role.name as keyof typeof ROLE_LABELS
                            ] || role.name}
                        </h4>
                        <div class="role-badges">
                            {#if role.is_system}
                                <span class="system-badge">Sistema</span>
                            {/if}
                            {#if !role.is_active}
                                <span class="inactive-badge">Inactivo</span>
                            {/if}
                        </div>
                    </div>
                    <p class="role-description">
                        {role.description || "Sin descripción"}
                    </p>
                    <div class="role-actions">
                        {#if !role.is_system && role.name !== "admin" && role.name !== "sin_rol"}
                            <button
                                class="delete-btn"
                                on:click={() => confirmDeleteRole(role)}
                                title="Eliminar rol"
                            >
                                <svg
                                    width="20"
                                    height="20"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="1.8"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                >
                                    <path d="M3 6h18" />
                                    <path
                                        d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                                    />
                                    <path
                                        d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0v12m4-12v12"
                                    />
                                </svg>
                            </button>
                        {/if}
                        {#if !role.is_system}
                            <button
                                class="edit-btn"
                                on:click={() => openRoleModal(role)}
                                title="Editar rol"
                            >
                                <svg
                                    width="20"
                                    height="20"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="1.8"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    ><path d="M12 20h9" /><path
                                        d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19.5 3 21l1.5-4L16.5 3.5z"
                                    /></svg
                                >
                            </button>
                        {/if}
                    </div>
                </div>
            {/each}
        </div>
    </div>

    <!-- Filtros de usuarios -->
    <div class="user-filters">
        <input
            type="text"
            placeholder="Buscar por nombre o email..."
            class="filter-input"
            bind:value={searchTerm}
        />
        <select class="filter-select" bind:value={statusFilter}>
            <option value="">Solo activos (por defecto)</option>
            <option value="activo">Solo activos</option>
            <option value="inactivo">Solo inactivos</option>
            <option value="todos">Todos los estados</option>
        </select>
        <select class="filter-select" bind:value={roleFilter}>
            <option value="">Todos los roles</option>
            {#each roles.filter((role) => role.is_active !== false) as role}
                <option value={role.name}>{role.name}</option>
            {/each}
        </select>
        <select class="filter-select" bind:value={packageFilter}>
            <option value="">Todos los paquetes</option>
            {#each packages as pkg}
                <option value={pkg.id}>{pkg.name}</option>
            {/each}
        </select>
        <select class="filter-select" bind:value={institutionFilter}>
            <option value="">Todas las instituciones</option>
            <option value="none">Sin institución</option>
            {#each institutions as inst}
                <option value={inst.id}>{inst.name}</option>
            {/each}
        </select>
        <button
            class="btn-secondary"
            on:click={() => {
                searchTerm = "";
                statusFilter = "";
                roleFilter = "";
                packageFilter = "";
                institutionFilter = "";
                loadUsers();
            }}>Limpiar filtros</button
        >
    </div>

    <!-- Sección de Usuarios -->
    <div class="users-section">
        <div class="section-header-with-stats">
            <h3>Usuarios</h3>
            {#if users.length > 0}
                <div class="stats-info">
                    <span class="stat-item">
                        📊 {users.length} usuarios encontrados
                    </span>
                    {#if searchTerm || statusFilter || roleFilter || packageFilter || institutionFilter}
                        <span class="stat-item filters-applied">
                            🔍 Filtros aplicados
                        </span>
                    {/if}
                </div>
            {/if}
        </div>
        {#if loading}
            <div class="loading">Cargando usuarios...</div>
        {:else if error}
            <div class="error">{error}</div>
        {:else if Array.isArray(users) && users.length === 0}
            <div class="empty">No hay usuarios registrados.</div>
        {:else}
            <table class="user-table">
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Email</th>
                        <th>Rol</th>
                        <th>Paquete</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {#each pagedUsers as user}
                        <tr>
                            <td>{user.first_name} {user.last_name}</td>
                            <td>{user.email}</td>
                            <td>
                                {#if Array.isArray(user.roles) && user.roles.length > 0}
                                    {@const activeRole = getActiveRole(user)}
                                    {@const roleLabel =
                                        ROLE_LABELS[activeRole] || activeRole}
                                    <span class="role-badge" title={activeRole}>
                                        {roleLabel}
                                    </span>
                                    {#if user.roles.length > 1}
                                        <span
                                            class="role-count"
                                            title="{user.roles
                                                .length} roles asignados"
                                        >
                                            +{user.roles.length - 1}
                                        </span>
                                    {/if}
                                {:else}
                                    <span class="error-text">Sin rol</span>
                                {/if}
                            </td>
                            <td>
                                {#if userCanHavePackages(user)}
                                    {#if (user.package_subscriptions ?? []).length > 0}
                                        {getActivePackage(user)?.package_name ||
                                            "Sin paquete activo"}
                                    {:else}
                                        <span class="error-text"
                                            >Sin paquete</span
                                        >
                                    {/if}
                                {:else}
                                    <span
                                        title="Este rol no requiere paquetes"
                                        style="display:inline-flex;align-items:center;gap:0.2em;color:var(--color-text-secondary);"
                                    >
                                        No aplica
                                    </span>
                                {/if}
                            </td>
                            <td>{user.is_active ? "Activo" : "Inactivo"}</td>
                            <td>
                                <div class="actions-grid">
                                    <button
                                        class="history-btn"
                                        on:click={() => openHistoryModal(user)}
                                        title="Ver historial del usuario"
                                    >
                                        <svg
                                            width="18"
                                            height="18"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor"
                                            stroke-width="1.8"
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            ><circle
                                                cx="12"
                                                cy="12"
                                                r="10"
                                            /><polyline
                                                points="12 6 12 12 16 14"
                                            /></svg
                                        >
                                    </button>
                                    {#if userCanHavePackages(user)}
                                        <button
                                            class="package-btn"
                                            on:click={() => {
                                                console.log(
                                                    "🔧 CLICK - Botón de paquete clickeado para usuario:",
                                                    user.email,
                                                );
                                                openPackageModal(user);
                                            }}
                                            title="Ver suscripciones de paquetes"
                                        >
                                            <svg
                                                width="17"
                                                height="17"
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                stroke-width="1.8"
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                ><path
                                                    d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"
                                                /><polyline
                                                    points="3.27 6.96 12 12.01 20.73 6.96"
                                                /></svg
                                            >
                                        </button>
                                    {/if}
                                    <button
                                        class="action-btn"
                                        title="Editar usuario"
                                        on:click={(e) => openEditModal(user, e)}
                                    >
                                        <svg
                                            width="20"
                                            height="20"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor"
                                            stroke-width="1.8"
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            ><path d="M12 20h9" /><path
                                                d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19.5 3 21l1.5-4L16.5 3.5z"
                                            /></svg
                                        >
                                    </button>
                                    <button
                                        class="action-btn delete"
                                        title="Eliminar usuario"
                                        on:click={() => openDeleteModal(user)}
                                    >
                                        <svg
                                            width="20"
                                            height="20"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor"
                                            stroke-width="1.8"
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            ><path d="M3 6h18" /><path
                                                d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                                            /><path
                                                d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0v12m4-12v12"
                                            /></svg
                                        >
                                    </button>
                                </div>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        {/if}
    </div>

    <!-- Modal de Confirmación de Eliminación de Usuario -->
    {#if showDeleteModal}
        <div class="modal-backdrop" on:click={closeDeleteModal}></div>
        <div
            class="modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="delete-modal-title"
        >
            <button
                class="modal-close"
                on:click={closeDeleteModal}
                title="Cerrar"
                disabled={deleting}>&times;</button
            >
            <h3 id="delete-modal-title">Eliminar usuario</h3>

            {#if !showDeleteNotification}
                <p>
                    ¿Estás seguro que deseas eliminar el usuario <strong
                        >{selectedUser
                            ? `${selectedUser.first_name} ${selectedUser.last_name || ""}`.trim()
                            : ""}</strong
                    >?
                </p>
                {#if error}
                    <div class="form-error">{error}</div>
                {/if}
                {#if debugMode && debugData}
                    <details class="debug-details">
                        <summary>🔧 DEBUG: Datos de la operación</summary>
                        <pre class="debug-data">{JSON.stringify(
                                debugData,
                                null,
                                2,
                            )}</pre>
                    </details>
                {/if}
            {/if}

            <div class="modal-actions">
                {#if !showDeleteNotification}
                    <button
                        class="btn-danger"
                        on:click={deleteUserHandler}
                        disabled={deleting}
                    >
                        {#if deleting}
                            <span class="loading-spinner"></span> Eliminando...
                        {:else}
                            Eliminar
                        {/if}
                    </button>
                {/if}
                <button
                    class="btn-secondary"
                    on:click={closeDeleteModal}
                    disabled={deleting}
                >
                    {showDeleteNotification ? "Cerrar" : "Cancelar"}
                </button>
            </div>

            <!-- Componente de notificación -->
            {#if showDeleteNotification}
                <div class="simple-success-notification">
                    <svg class="checkmark" viewBox="0 0 52 52">
                        <circle
                            class="checkmark-circle"
                            cx="26"
                            cy="26"
                            r="25"
                            fill="none"
                        />
                        <path
                            class="checkmark-check"
                            fill="none"
                            d="M14 27l7 7 16-16"
                        />
                    </svg>
                    <div class="simple-success-text">
                        <h2>{deleteNotificationMessage}</h2>
                        <p>{deleteNotificationSubtitle}</p>
                    </div>
                </div>
            {/if}
        </div>
    {/if}

    <!-- Modal de Rol (profesional, permisos editables para nuevos roles) -->
    {#if showRoleModal}
        <div class="modal-backdrop" on:click={closeRoleModal}></div>
        <div
            class="modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="role-modal-title"
        >
            <button class="modal-close" on:click={closeRoleModal} title="Cerrar"
                >&times;</button
            >
            <h3 id="role-modal-title">
                {isNewRole ? "Nuevo rol" : "Editar rol"}
            </h3>

            <form
                class="modal-form"
                on:submit|preventDefault={saveRole}
                autocomplete="off"
            >
                <!-- Información sobre roles activos -->
                {#if isNewRole}
                    <div class="info-message">
                        <svg
                            width="20"
                            height="20"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                        >
                            <circle cx="12" cy="12" r="10" />
                            <path d="M12 16v-4" />
                            <path d="M12 8h.01" />
                        </svg>
                        <div>
                            <strong>Rol activo por defecto</strong>
                            <p>
                                Los nuevos roles se crean automáticamente como
                                activos y pueden ser asignados a usuarios
                                inmediatamente.
                            </p>
                        </div>
                    </div>
                {/if}
                <label>
                    Nombre del Rol
                    <input
                        type="text"
                        bind:value={roleForm.name}
                        placeholder="admin, caregiver, etc."
                        required
                        disabled={roleForm.is_system}
                    />
                    {#if roleErrors.name}<span class="form-error"
                            >{roleErrors.name}</span
                        >{/if}
                </label>
                <label>
                    Descripción
                    <textarea
                        bind:value={roleForm.description}
                        placeholder="Descripción del rol"
                        rows="3"
                        disabled={roleForm.is_system}
                    ></textarea>
                    {#if roleErrors.description}<span class="form-error"
                            >{roleErrors.description}</span
                        >{/if}
                </label>
                {#if roleForm.is_system}
                    <div class="form-info">Rol de sistema. No editable.</div>
                {/if}
                <label>
                    Permisos
                    <div class="permissions-editor">
                        <h4>Permisos del Rol</h4>
                        <div class="permissions-grid">
                            <div class="perm-category">
                                <h5>Usuarios</h5>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.users.read
                                        }
                                    />
                                    Leer usuarios
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.users.write
                                        }
                                    />
                                    Crear/editar usuarios
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.users.delete
                                        }
                                    />
                                    Eliminar usuarios
                                </label>
                            </div>
                            <div class="perm-category">
                                <h5>Roles</h5>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.roles.read
                                        }
                                    />
                                    Leer roles
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.roles.write
                                        }
                                    />
                                    Crear/editar roles
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.roles.delete
                                        }
                                    />
                                    Eliminar roles
                                </label>
                            </div>
                            <div class="perm-category">
                                <h5>Instituciones</h5>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.institutions
                                                .read
                                        }
                                    />
                                    Leer instituciones
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.institutions
                                                .write
                                        }
                                    />
                                    Crear/editar instituciones
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.institutions
                                                .delete
                                        }
                                    />
                                    Eliminar instituciones
                                </label>
                            </div>
                            <div class="perm-category">
                                <h5>Paquetes</h5>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.packages.read
                                        }
                                    />
                                    Leer paquetes
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.packages.write
                                        }
                                    />
                                    Crear/editar paquetes
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.packages.delete
                                        }
                                    />
                                    Eliminar paquetes
                                </label>
                            </div>
                            <div class="perm-category">
                                <h5>Alertas</h5>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.alerts.read
                                        }
                                    />
                                    Leer alertas
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.alerts.write
                                        }
                                    />
                                    Crear/editar alertas
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.alerts.delete
                                        }
                                    />
                                    Eliminar alertas
                                </label>
                            </div>
                            <div class="perm-category">
                                <h5>Eventos</h5>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.events.read
                                        }
                                    />
                                    Leer eventos
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.events.write
                                        }
                                    />
                                    Crear/editar eventos
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.events.delete
                                        }
                                    />
                                    Eliminar eventos
                                </label>
                            </div>
                            <div class="perm-category">
                                <h5>Reportes</h5>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.reports.read
                                        }
                                    />
                                    Leer reportes
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.reports.write
                                        }
                                    />
                                    Crear/editar reportes
                                </label>
                                <label class="checkbox-label">
                                    <input
                                        type="checkbox"
                                        bind:checked={
                                            editablePermissions.reports.delete
                                        }
                                    />
                                    Eliminar reportes
                                </label>
                            </div>
                        </div>
                    </div>
                </label>
                {#if rolesError && !showRoleNotification}
                    <div class="form-error">{rolesError}</div>
                {/if}
                <div class="modal-actions">
                    {#if !roleForm.is_system}
                        <button type="submit" class="btn-primary"
                            >{isNewRole
                                ? "Crear rol"
                                : "Guardar cambios"}</button
                        >
                    {/if}
                    <button
                        type="button"
                        class="btn-secondary"
                        on:click={closeRoleModal}>Cerrar</button
                    >
                </div>

                <!-- Notificación de éxito simple con check animado -->
                {#if showRoleNotification}
                    <div class="simple-success-notification">
                        <svg class="checkmark" viewBox="0 0 52 52">
                            <circle
                                class="checkmark-circle"
                                cx="26"
                                cy="26"
                                r="25"
                                fill="none"
                            />
                            <path
                                class="checkmark-check"
                                fill="none"
                                d="M14 27l7 7 16-16"
                            />
                        </svg>
                        <div class="simple-success-text">
                            <h2>{roleNotificationMessage}</h2>
                            <p>{roleNotificationSubtitle}</p>
                        </div>
                    </div>
                {/if}
            </form>
        </div>
    {/if}

    <!-- Modal de historial -->
    {#if showHistoryModal}
        <div class="modal-backdrop" on:click={closeHistoryModal}></div>
        <div
            class="modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="history-modal-title"
        >
            <button
                class="modal-close"
                on:click={closeHistoryModal}
                title="Cerrar">&times;</button
            >
            <h3 id="history-modal-title">Historial de {historyUser?.name}</h3>
            {#if historyLoading}
                <div class="loading">Cargando historial...</div>
            {:else if historyError}
                <div class="form-error">{historyError}</div>
            {:else if userHistory.length === 0}
                <div class="empty">Sin historial disponible.</div>
            {:else}
                <div class="timeline-vertical">
                    {#each userHistory as item}
                        <div class="timeline-item">
                            <div class="timeline-dot"></div>
                            <div class="timeline-content">
                                <span class="timeline-date">{item.date}</span>
                                <span class="timeline-type">{item.type}</span>
                                <span class="timeline-desc">{item.desc}</span>
                            </div>
                        </div>
                    {/each}
                </div>
                {#if userHistory.length > 4}
                    <button class="btn-secondary">Ampliar historial</button>
                {/if}
            {/if}
        </div>
    {/if}

    <!-- Modal de paquetes mejorado -->
    {#if showPackageModal}
        <div
            class="modal-backdrop"
            on:click={() => (showPackageModal = false)}
        ></div>
        <div
            class="modal package-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="package-modal-title"
        >
            <button
                class="modal-close"
                on:click={() => (showPackageModal = false)}
                title="Cerrar">&times;</button
            >

            <div class="modal-header">
                <div class="modal-title-section">
                    <h3 id="package-modal-title">
                        <PackageIcon size={24} /> Suscripciones de paquetes
                    </h3>
                    <p class="modal-subtitle">
                        {selectedUser?.first_name}
                        {selectedUser?.last_name || ""}
                        <span class="user-email">({selectedUser?.email})</span>
                    </p>
                </div>
            </div>

            {#if loadingPackages}
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <p>Cargando suscripciones...</p>
                </div>
            {:else if packageModalError}
                <div class="error-container">
                    <div class="error-icon">
                        <WarningIcon size={48} />
                    </div>
                    <h4>Error al cargar suscripciones</h4>
                    <p>{packageModalError}</p>
                </div>
            {:else if userPackageSubscriptions.length === 0}
                <div class="empty-container">
                    <div class="empty-icon">
                        <PackageIcon size={48} />
                    </div>
                    <h4>Sin suscripciones</h4>
                    <p>
                        Este usuario no tiene suscripciones de paquetes activas.
                    </p>
                    {#if userCanHavePackages(selectedUser)}
                        <button
                            class="btn-primary"
                            style="margin-top:1.2rem;"
                            on:click={() => asignarNuevoPaquete(selectedUser)}
                        >
                            <svg
                                width="18"
                                height="18"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                ><path d="M12 5v14M5 12h14" /></svg
                            >
                            Asignar nuevo paquete
                        </button>
                    {/if}
                </div>
            {:else}
                <div class="package-subscriptions">
                    {#each userPackageSubscriptions as sub (sub.id || sub.package_id)}
                        <div class="package-card">
                            <div class="package-header">
                                <h4 class="package-name">
                                    {sub.package?.name || "Paquete sin nombre"}
                                </h4>
                                <span class="package-status {sub.status}">
                                    {#if sub.status === "active"}
                                        <span class="status-dot active"></span> Activo
                                    {:else if sub.status === "expired"}
                                        <span class="status-dot expired"></span>
                                        Expirado
                                    {:else}
                                        {sub.status}
                                    {/if}
                                </span>
                            </div>

                            <div class="package-details">
                                <div class="detail-row">
                                    <span class="detail-label">
                                        <RefreshIcon size={16} />
                                        Ciclo de facturación:
                                    </span>
                                    <span class="detail-value">
                                        {sub.billing_cycle === "monthly"
                                            ? "Mensual"
                                            : "Anual"}
                                    </span>
                                </div>
                                <div class="detail-row">
                                    <span class="detail-label">
                                        <CalendarIcon size={16} />
                                        Fecha inicio:
                                    </span>
                                    <span class="detail-value">
                                        {sub.start_date
                                            ? new Date(
                                                  sub.start_date,
                                              ).toLocaleDateString("es-ES", {
                                                  year: "numeric",
                                                  month: "long",
                                                  day: "numeric",
                                              })
                                            : "-"}
                                    </span>
                                </div>
                                <div class="detail-row">
                                    <span class="detail-label">
                                        <ClockIcon size={16} />
                                        Próxima facturación:
                                    </span>
                                    <span class="detail-value">
                                        {sub.next_billing_date
                                            ? new Date(
                                                  sub.next_billing_date,
                                              ).toLocaleDateString("es-ES", {
                                                  year: "numeric",
                                                  month: "long",
                                                  day: "numeric",
                                              })
                                            : "-"}
                                    </span>
                                </div>
                                <div class="detail-row">
                                    <span class="detail-label">
                                        <DollarIcon size={16} />
                                        Monto actual:
                                    </span>
                                    <span class="detail-value amount">
                                        ${(sub.current_amount / 100).toFixed(2)}
                                        ARS
                                    </span>
                                </div>
                                <div class="detail-row">
                                    <span class="detail-label">
                                        <RefreshIcon size={16} />
                                        Auto renovación:
                                    </span>
                                    <span class="detail-value">
                                        {#if sub.auto_renew}
                                            <CheckIcon size={16} /> Sí
                                        {:else}
                                            <XIcon size={16} /> No
                                        {/if}
                                    </span>
                                </div>
                            </div>

                            {#if sub.selected_features && sub.selected_features.length > 0}
                                <div class="package-features">
                                    <span class="features-label">
                                        <TargetIcon size={16} />
                                        Características seleccionadas:
                                    </span>
                                    <div class="features-list">
                                        {#each sub.selected_features as feature}
                                            <span
                                                class="feature-badge"
                                                title={feature}
                                            >
                                                {feature}
                                            </span>
                                        {/each}
                                    </div>
                                </div>
                            {:else}
                                <div class="package-features">
                                    <span class="features-label">
                                        <TargetIcon size={16} />
                                        Características seleccionadas:
                                    </span>
                                    <div class="no-features">
                                        No hay características seleccionadas
                                        para este paquete
                                    </div>
                                </div>
                            {/if}
                        </div>
                    {/each}
                </div>
            {/if}
        </div>
    {/if}

    <!-- Elimina el modal clásico de usuario -->
    <!-- Mantén solo el modal avanzado: -->
    <EditUserModal
        user={selectedUser}
        open={showEditModal}
        {loading}
        {sessionUserRole}
        anchorRect={editAnchorRect}
        on:save={handleEditSave}
        on:cancel={closeEditModal}
    />

    <!-- DEBUG: Estado del modal de edición -->
    <details>
        <summary>DEBUG: Modal edición</summary>
        <div style="background:#222;color:#0f0;padding:1em;font-size:0.9em;">
            <div><b>showEditModal:</b> {showEditModal ? "true" : "false"}</div>
            <div><b>selectedUser:</b></div>
            <pre>{selectedUser
                    ? JSON.stringify(selectedUser, null, 2)
                    : "null"}</pre>
        </div>
    </details>

    {#if showDeleteRoleModal}
        <div class="modal-backdrop" />
        <div class="modal" role="dialog" aria-modal="true">
            <button
                class="modal-close"
                on:click={closeDeleteRoleModal}
                title="Cerrar"
                disabled={deletingRole}>&times;</button
            >

            <!-- Notificación de éxito/error -->
            {#if showDeleteRoleNotification}
                <div
                    class="simple-success-notification {deleteRoleNotificationType}"
                >
                    <svg class="checkmark" viewBox="0 0 52 52">
                        <circle
                            class="checkmark-circle"
                            cx="26"
                            cy="26"
                            r="25"
                            fill="none"
                        />
                        <path
                            class="checkmark-check"
                            fill="none"
                            d="M14 27l7 7 16-16"
                        />
                    </svg>
                    <div class="simple-success-text">
                        <h2>{deleteRoleNotificationMessage}</h2>
                        <p>{deleteRoleNotificationSubtitle}</p>
                    </div>
                </div>
            {:else}
                <h3>¿Desactivar rol?</h3>

                <!-- Información del rol -->
                <div class="role-info-card">
                    <div class="role-info-header">
                        <h4>{roleToDelete?.name}</h4>
                        {#if roleToDelete?.is_system}
                            <span class="system-badge">Sistema</span>
                        {/if}
                    </div>
                    <p class="role-info-description">
                        {roleToDelete?.description || "Sin descripción"}
                    </p>
                </div>

                <!-- Advertencias -->
                <div class="warning-section">
                    {#if roleToDelete?.is_system}
                        <div class="warning-message system-warning">
                            <svg
                                width="20"
                                height="20"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                            >
                                <circle cx="12" cy="12" r="10" />
                                <path d="M12 6v6m0 0v6" />
                            </svg>
                            <div>
                                <strong>Rol de sistema protegido</strong>
                                <p>
                                    Los roles de sistema no pueden ser
                                    eliminados por seguridad.
                                </p>
                            </div>
                        </div>
                    {:else}
                        <div class="warning-message">
                            <svg
                                width="20"
                                height="20"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                            >
                                <path
                                    d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
                                />
                                <line x1="12" y1="9" x2="12" y2="13" />
                                <line x1="12" y1="17" x2="12.01" y2="17" />
                            </svg>
                            <div>
                                <strong>Acción irreversible</strong>
                                <p>
                                    Al desactivar este rol, todos los usuarios
                                    que lo tengan asignado serán reasignados al
                                    rol "sin_rol".
                                </p>
                            </div>
                        </div>
                    {/if}
                </div>

                <!-- Acciones -->
                <div class="modal-actions">
                    <button
                        class="btn-secondary"
                        on:click={closeDeleteRoleModal}
                        disabled={deletingRole}>Cancelar</button
                    >
                    {#if !roleToDelete?.is_system}
                        <button
                            class="btn-danger"
                            on:click={handleDeleteRole}
                            disabled={deletingRole}
                        >
                            {#if deletingRole}
                                <span class="loading-spinner"></span> Desactivando...
                            {:else}
                                Desactivar Rol
                            {/if}
                        </button>
                    {/if}
                </div>
            {/if}
        </div>
    {/if}

    {#if totalPages > 1}
        <div class="pagination">
            <button on:click={prevPage} disabled={currentPage === 1}
                >Anterior</button
            >
            <span>Página {currentPage} de {totalPages}</span>
            <button on:click={nextPage} disabled={currentPage === totalPages}
                >Siguiente</button
            >
        </div>
    {/if}

    <!-- Notificación de usuario creado exitosamente -->
    {#if showUserCreatedNotification}
        <div class="simple-success-notification user-created-notification">
            <svg class="checkmark" viewBox="0 0 52 52">
                <circle
                    class="checkmark-circle"
                    cx="26"
                    cy="26"
                    r="25"
                    fill="none"
                />
                <path
                    class="checkmark-check"
                    fill="none"
                    d="M14 27l7 7 16-16"
                />
            </svg>
            <div class="simple-success-text">
                <h2>{userCreatedNotificationMessage}</h2>
                <p>{userCreatedNotificationSubtitle}</p>
            </div>
        </div>
    {/if}
</div>

<style>
    .user-table-section {
        background: var(--color-bg-card);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-md);
        padding: 1.5rem;
        margin-bottom: 2rem;
    }

    .user-table-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .header-actions {
        display: flex;
        gap: 1rem;
    }

    .new-user-btn,
    .new-role-btn {
        background: var(--color-primary);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: var(--border-radius);
        cursor: pointer;
        font-weight: 500;
        transition: background-color 0.2s;
    }

    .new-user-btn:hover,
    .new-role-btn:hover {
        background: var(--color-primary-dark);
    }

    .new-role-btn {
        background: var(--color-secondary);
    }

    .new-role-btn:hover {
        background: var(--color-secondary-dark);
    }

    .roles-section,
    .users-section {
        margin-bottom: 2rem;
    }

    .roles-section h3,
    .users-section h3 {
        margin-bottom: 1rem;
        color: var(--color-text-primary);
        font-size: 1.25rem;
    }

    .section-header-with-stats {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .section-header-with-stats h3 {
        margin: 0;
    }

    .stats-info {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .stat-item {
        font-size: 0.9rem;
        color: var(--color-text-secondary);
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        background: var(--color-bg-secondary);
    }

    .stat-item.filters-applied {
        color: var(--color-accent);
        background: rgba(var(--color-accent-rgb), 0.1);
        border: 1px solid rgba(var(--color-accent-rgb), 0.2);
    }

    .roles-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .role-card {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 110px;
        border: 1px solid var(--color-border);
        border-radius: 0.6rem;
        background: var(--color-bg-primary);
        padding: 0.7rem 0.8rem 0.7rem 0.8rem;
        margin-bottom: 0.3rem;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
        position: relative;
        transition: all 0.2s ease;
    }

    .role-card.active {
        border-color: #28a745;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.1);
    }

    .role-card.inactive {
        border-color: #dc3545;
        background: #f8f9fa;
        opacity: 0.7;
    }

    .role-card.inactive:hover {
        opacity: 1;
    }
    .role-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0;
        padding-right: 0.5rem;
    }

    .role-badges {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }
    .roles-header {
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--color-border);
    }

    .roles-header h3 {
        margin: 0;
        color: var(--color-text-primary);
        font-size: 1.25rem;
        font-weight: 600;
    }
    .btn-primary {
        padding: 0.45em 1.2em;
        font-size: 1em;
        border-radius: 0.4em;
        margin: 0 0.2em 0 0;
    }
    .role-header h4 {
        margin: 0;
        color: var(--color-text-primary);
        font-size: 0.98rem;
        font-weight: 600;
    }
    .system-badge {
        background: transparent;
        color: var(--color-accent);
        border: 1px solid var(--color-accent);
        border-radius: 6px;
        font-size: 0.78em;
        padding: 0.08em 0.5em;
        font-weight: 500;
        height: 1.3em;
        display: flex;
        align-items: center;
    }

    .inactive-badge {
        background: #dc3545;
        color: white;
        border: 1px solid #dc3545;
        border-radius: 6px;
        font-size: 0.78em;
        padding: 0.08em 0.5em;
        font-weight: 500;
        height: 1.3em;
        display: flex;
        align-items: center;
    }
    .role-description {
        margin: 0.2rem 0 0.7rem 0;
        color: var(--color-text-secondary);
        font-size: 0.97rem;
        min-height: 1em;
    }
    .role-actions {
        display: flex;
        gap: 0.4rem;
        justify-content: flex-end;
        align-items: center;
        margin-top: 0.3rem;
        padding-top: 0.2rem;
        border-top: none;
    }
    .edit-btn,
    .delete-btn {
        background: none;
        border: none;
        border-radius: 0.35rem;
        padding: 0.12rem 0.18rem;
        display: flex;
        align-items: center;
        cursor: pointer;
        transition: color 0.18s;
        color: var(--color-text-secondary);
        font-size: 1rem;
        outline: none;
        box-shadow: none;
    }
    .edit-btn svg,
    .delete-btn svg {
        width: 18px;
        height: 18px;
        margin: 0;
        padding: 0;
    }
    .edit-btn:hover,
    .delete-btn:hover {
        color: var(--color-accent);
    }
    .edit-btn[title],
    .delete-btn[title] {
        position: relative;
    }
    .edit-btn[title]:hover:after,
    .delete-btn[title]:hover:after {
        content: attr(title);
        position: absolute;
        left: 50%;
        top: 110%;
        transform: translateX(-50%);
        background: var(--color-bg-secondary);
        color: var(--color-text-primary);
        border: 1px solid var(--color-border);
        border-radius: 0.25rem;
        padding: 0.18rem 0.5rem;
        font-size: 0.82em;
        white-space: nowrap;
        z-index: 10;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .user-table {
        width: 100%;
        min-width: 900px;
        border-collapse: separate;
        border-spacing: 0;
        overflow-x: auto;
    }

    .user-table-section {
        overflow-x: auto;
        width: 100%;
    }

    .user-table th,
    .user-table td {
        padding: 0.75rem;
        text-align: left;
        border-bottom: 1px solid var(--color-border);
    }

    .user-table th {
        background: var(--color-bg-secondary);
        font-weight: 600;
        color: var(--color-text-primary);
    }

    .user-roles {
        display: flex;
        flex-wrap: wrap;
        gap: 0.25rem;
    }

    .role-badge {
        background: transparent;
        color: #d1d5db;
        padding: 0.2rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-block;
        border: 1px solid #d1d5db;
    }

    .role-count {
        background: var(--color-text-secondary);
        color: white;
        padding: 0.1rem 0.3rem;
        border-radius: 0.2rem;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 0.25rem;
        display: inline-block;
    }

    .no-role {
        color: var(--color-text-secondary);
        font-size: 0.875rem;
        font-style: italic;
    }

    .user-status {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .user-status.activo {
        background: transparent;
        color: #27ae60;
        border: 1.5px solid #27ae60;
    }

    .user-status.inactivo {
        background: var(--color-danger);
        color: white;
    }

    .action-btn {
        background: none;
        border: none;
        cursor: pointer;
        padding: 0.25rem;
        margin-right: 0.5rem;
        border-radius: 0.25rem;
        transition: background-color 0.2s;
    }

    .action-btn:hover {
        background: var(--color-bg-secondary);
    }

    .action-btn.delete:hover {
        background: var(--color-danger-light);
    }

    .delete-btn {
        background: none;
        border: none;
        color: var(--color-text-secondary);
        padding: 0.12rem 0.18rem;
        font-size: 1rem;
        transition: color 0.18s;
    }
    .delete-btn:hover {
        color: var(--color-accent);
        background: none;
    }

    .delete-btn.small {
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
    }

    .delete-btn:hover {
        background: var(--color-danger-dark);
    }

    .loading,
    .error,
    .empty {
        text-align: center;
        padding: 2rem;
        color: var(--color-text-secondary);
    }

    .error {
        color: var(--color-danger);
    }

    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 1000;
    }

    .modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: var(--color-bg-card);
        padding: 1.5rem 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        z-index: 1001;
        min-width: 320px;
        max-width: 420px;
        width: 100%;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        box-sizing: border-box;
    }

    /* Modal específico para roles - más grande */
    .modal[aria-labelledby="role-modal-title"] {
        max-width: 600px;
        max-height: 80vh;
        overflow-y: auto;
    }
    @media (max-width: 600px) {
        .modal {
            min-width: 0;
            max-width: 98vw;
            width: 98vw;
            padding: 0.7rem 0.5rem;
        }
    }
    .modal-close {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: none;
        border: none;
        font-size: 1.5rem;
        color: var(--color-text-secondary);
        cursor: pointer;
        z-index: 10;
        transition: color 0.2s;
    }
    .modal-close:hover {
        color: var(--color-accent);
    }
    .modal-close:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    .modal h3 {
        margin-top: 0;
        margin-bottom: 1.5rem;
        color: var(--color-text-primary);
    }
    .modal label {
        display: block;
        margin-bottom: 1rem;
        color: var(--color-text-primary);
        font-weight: 500;
    }
    .modal input,
    .modal select,
    .modal textarea {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        background: var(--color-bg-secondary);
        color: var(--color-text-primary);
        margin-top: 0.25rem;
        font-size: 1rem;
    }
    .modal textarea {
        resize: vertical;
        min-height: 80px;
    }
    .checkbox-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .checkbox-label input[type="checkbox"] {
        width: auto;
        margin: 0;
    }
    .modal-actions {
        display: flex;
        gap: 1rem;
        justify-content: flex-end;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid var(--color-border);
        position: sticky;
        bottom: 0;
        background: var(--color-bg-card);
    }
    .modal-actions button {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: var(--border-radius);
        cursor: pointer;
        font-weight: 500;
        transition: background-color 0.2s;
    }
    .modal-actions button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
    .modal-actions button[type="submit"] {
        background: var(--color-primary);
        color: white;
    }

    .modal-actions button[type="submit"]:hover {
        background: var(--color-primary-dark);
    }

    .modal-actions button.delete {
        background: var(--color-danger);
        color: white;
    }

    .modal-actions button.delete:hover {
        background: var(--color-danger-dark);
    }

    .modal-actions button[type="button"] {
        background: var(--color-bg-secondary);
        color: var(--color-text-primary);
        border: 1px solid var(--color-border);
    }

    .modal-actions button[type="button"]:hover {
        background: var(--color-border);
    }

    .action-btn svg,
    .delete-btn svg {
        color: var(--color-text-secondary);
        stroke: currentColor;
        opacity: 0.85;
        transition: color 0.2s;
    }
    .action-btn:hover svg,
    .delete-btn:hover svg {
        color: var(--color-accent);
    }
    .form-error {
        color: var(--color-danger);
        margin-bottom: 1rem;
        font-size: 0.95em;
    }
    .btn-primary {
        background: var(--color-accent);
        color: #fff;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 0.25rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s;
    }
    .btn-primary:hover {
        background: var(--color-accent-dark, #1e7e34);
    }
    .btn-secondary {
        background: var(--color-bg-secondary);
        color: var(--color-text-primary);
        border: 1px solid var(--color-border);
        padding: 0.6rem 1.5rem;
        border-radius: 0.25rem;
        font-weight: 500;
        cursor: pointer;
        transition:
            background 0.2s,
            color 0.2s;
    }
    .btn-secondary:hover {
        background: var(--color-border);
    }
    .btn-danger {
        background: var(--color-danger);
        color: #fff;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 0.25rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s;
    }
    .btn-danger:hover {
        background: var(--color-danger-dark, #c82333);
    }

    @media (max-width: 768px) {
        .user-table-header {
            flex-direction: column;
            gap: 1rem;
            align-items: stretch;
        }

        .header-actions {
            justify-content: center;
        }

        .main-actions {
            padding: 1rem;
        }

        .action-group {
            flex-direction: column;
            align-items: stretch;
        }

        .action-btn {
            min-width: auto;
            width: 100%;
        }

        .roles-grid {
            grid-template-columns: 1fr;
        }

        .user-table {
            font-size: 0.875rem;
        }

        .user-table th,
        .user-table td {
            padding: 0.5rem;
        }

        .modal {
            min-width: 90vw;
            margin: 1rem;
        }
    }
    .permissions-list {
        background: var(--color-bg-secondary);
        border-radius: 0.25rem;
        padding: 0.75rem 1rem;
        margin-top: 0.25rem;
        font-size: 0.97em;
        color: var(--color-text-primary);
        max-height: 200px;
        overflow-y: auto;
    }
    .perm-group {
        margin-bottom: 0.5rem;
    }
    .perm-yes {
        color: #27ae60;
        font-weight: 500;
    }
    .perm-no {
        color: #c82333;
        font-weight: 500;
    }
    .perm-none {
        color: var(--color-text-secondary);
        font-style: italic;
    }
    .form-info {
        color: var(--color-accent);
        margin-bottom: 1rem;
        font-size: 0.97em;
    }
    .user-filters {
        display: flex;
        gap: 1rem;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    .filter-input {
        flex: 1 1 200px;
        padding: 0.5rem 1rem;
        border: 1px solid var(--color-border);
        border-radius: 0.25rem;
        background: var(--color-bg-secondary);
        color: var(--color-text-primary);
        font-size: 1rem;
    }
    .filter-select {
        padding: 0.5rem 1rem;
        border: 1px solid var(--color-border);
        border-radius: 0.25rem;
        background: var(--color-bg-secondary);
        color: var(--color-text-primary);
        font-size: 1rem;
    }
    .permissions-editor {
        background: var(--color-bg-secondary);
        border-radius: 0.25rem;
        padding: 1rem;
        margin-top: 0.25rem;
        max-height: 400px;
        overflow-y: auto;
    }
    .permissions-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 0.5rem;
    }
    .perm-category {
        margin-bottom: 1rem;
    }
    .perm-category h4 {
        margin: 0 0 0.5rem 0;
        color: var(--color-text-primary);
        font-size: 1rem;
    }
    .checkbox-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.25rem 0;
        font-size: 0.95em;
        color: var(--color-text-primary);
    }
    .checkbox-label input[type="checkbox"] {
        margin: 0;
    }
    .history-btn {
        background: none;
        border: none;
        color: var(--color-text-secondary);
        padding: 0.12rem 0.18rem;
        font-size: 1rem;
        transition: color 0.18s;
        display: flex;
        align-items: center;
        cursor: pointer;
    }
    .history-btn:hover {
        color: var(--color-accent);
    }
    .timeline-vertical {
        display: flex;
        flex-direction: column;
        gap: 1.1rem;
        margin: 1.2rem 0 0.5rem 0;
        position: relative;
    }
    .timeline-item {
        display: flex;
        align-items: flex-start;
        gap: 0.7rem;
        position: relative;
    }
    .timeline-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: var(--color-accent);
        margin-top: 0.2rem;
        flex-shrink: 0;
    }
    .timeline-content {
        display: flex;
        flex-direction: column;
        gap: 0.1rem;
    }
    .timeline-date {
        font-size: 0.93em;
        color: var(--color-text-secondary);
    }
    .timeline-type {
        font-size: 0.93em;
        color: var(--color-accent);
        font-weight: 500;
    }
    .timeline-desc {
        font-size: 1em;
        color: var(--color-text-primary);
    }
    .package-header-btn {
        background: none;
        border: none;
        color: var(--color-accent);
        padding: 0.12rem 0.18rem;
        font-size: 1rem;
        transition: color 0.18s;
        display: flex;
        align-items: center;
        cursor: pointer;
        margin-left: auto;
    }
    .package-header-btn:hover {
        color: var(--color-text-primary);
    }
    .package-section {
        margin-top: 1rem;
    }
    .package-card {
        background: var(--color-bg-secondary);
        border-radius: 0.4rem;
        padding: 0.7rem 1rem;
        margin-bottom: 0.5rem;
        border: 1px solid var(--color-border);
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
    }
    .package-card.actual {
        border: 2px solid var(--color-accent);
    }
    .package-history-list {
        list-style: none;
        padding: 0;
        margin: 0 0 1rem 0;
    }
    .package-history-list li {
        margin-bottom: 0.3rem;
        font-size: 0.97em;
    }
    .package-list {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 0.5rem;
    }
    .package-header {
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    .package-badge {
        display: inline-block;
        background: var(--color-bg-secondary);
        color: var(--color-accent);
        border: 1px solid var(--color-accent);
        border-radius: 0.5em;
        padding: 0.18em 0.7em;
        font-size: 0.97em;
        font-weight: 500;
        margin-right: 0.2em;
    }
    .package-badge.empty {
        color: var(--color-text-secondary);
        border: 1px solid var(--color-border);
        background: none;
    }
    @media (max-width: 1100px) {
        .user-table {
            min-width: 700px;
        }
    }
    @media (max-width: 800px) {
        .user-table {
            min-width: 500px;
            font-size: 0.95em;
        }
        .package-badge {
            font-size: 0.93em;
            padding: 0.13em 0.5em;
        }
    }
    /* Estilos para el botón de paquete */
    .package-btn {
        background: none;
        border: none;
        color: var(--color-accent);
        padding: 0.12rem 0.18rem;
        font-size: 1rem;
        transition: color 0.18s;
        display: flex;
        align-items: center;
        cursor: pointer;
    }
    .package-btn:hover {
        color: var(--color-text-primary);
    }
    /* Estilos para el grid de acciones */
    .actions-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(2, 1fr);
        gap: 0.3rem 0.5rem;
        justify-items: center;
        align-items: center;
        min-width: 60px;
        min-height: 60px;
    }

    .loading-spinner {
        display: inline-block;
        width: 18px;
        height: 18px;
        border: 2px solid rgba(0, 0, 0, 0.15);
        border-top: 2px solid var(--color-accent);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 8px;
        vertical-align: middle;
    }
    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    /* Estilos temporales para notificaciones */
    .modal-notification {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1002;
        background: rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
    }

    .notification-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        margin-right: 1rem;
        background: white;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }

    .notification-icon svg {
        width: 30px;
        height: 30px;
    }

    .notification-content {
        background: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        min-width: 300px;
        position: relative;
    }

    .notification-content h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
        font-weight: 600;
        color: #333;
    }

    .notification-content p {
        margin: 0;
        color: #666;
        font-size: 0.95rem;
    }

    .notification-close {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        background: none;
        border: none;
        cursor: pointer;
        padding: 0.25rem;
        border-radius: 0.25rem;
        color: #999;
        transition: color 0.2s;
    }

    .notification-close:hover {
        color: #333;
        background: rgba(0, 0, 0, 0.05);
    }

    /* Estilos para la notificación animada */
    .modal-animated-notification {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1002;
        background: rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        padding: 1rem;
    }

    .circle-bg {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        margin-right: 1rem;
        background: white;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }

    .notification-animated-content {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        color: #333;
    }

    .notification-animated-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: 50%;
        margin-right: 1rem;
        background: white;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }

    .notification-animated-text {
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
        font-size: 1rem;
        color: #333;
    }

    .notification-animated-icon svg {
        width: 30px;
        height: 30px;
    }

    .notification-animated-text h4 {
        margin: 0;
        font-size: 1.2rem;
        font-weight: 600;
        color: #333;
    }

    .notification-animated-text p {
        margin: 0;
        color: #666;
        font-size: 0.95rem;
    }

    .notification-animated-icon.success {
        border: 3px solid #28a745;
    }

    .notification-animated-icon.error {
        border: 3px solid #dc3545;
    }

    .notification-animated-content.grow {
        transform: scale(1.1);
        transition: transform 0.3s ease-in-out;
    }

    .expanding-notification-overlay {
        position: absolute;
        inset: 0;
        z-index: 2000;
        pointer-events: all;
        overflow: hidden;
    }
    .expanding-circle {
        position: absolute;
        inset: 0;
        margin: auto;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        transform: scale(0);
        opacity: 0.7;
        z-index: 2001;
        transition:
            transform 4s cubic-bezier(0.4, 0, 0.2, 1),
            opacity 1.2s;
        box-shadow:
            0 0 0 6px rgba(255, 255, 255, 0.25),
            0 8px 32px rgba(40, 167, 69, 0.12);
        border: 3px solid rgba(255, 255, 255, 0.45);
    }
    .expanding-circle.success {
        background: radial-gradient(
            circle,
            rgba(40, 167, 69, 0.55) 0%,
            rgba(40, 167, 69, 0.38) 100%
        );
    }
    .expanding-circle.success.expand {
        background: radial-gradient(
            circle,
            rgba(40, 167, 69, 0.75) 0%,
            rgba(40, 167, 69, 0.45) 100%
        );
        transform: scale(2.7);
        opacity: 0.98;
    }
    .expanding-circle.error {
        background: radial-gradient(
            circle,
            rgba(220, 53, 69, 0.55) 0%,
            rgba(220, 53, 69, 0.38) 100%
        );
    }
    .expanding-circle.error.expand {
        background: radial-gradient(
            circle,
            rgba(220, 53, 69, 0.75) 0%,
            rgba(220, 53, 69, 0.45) 100%
        );
        transform: scale(2.7);
        opacity: 0.98;
    }
    .expanding-notification-content.centered {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 2002;
        color: #fff;
        text-align: center;
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.9s 2.2s;
    }
    .expanding-notification-content.centered.fade-in {
        opacity: 1;
    }
    .expanding-icon {
        margin-bottom: 1.2rem;
        background: rgba(255, 255, 255, 0.18);
        border-radius: 50%;
        padding: 0.5rem;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    }
    .expanding-text h2 {
        margin: 0 0 0.5rem 0;
        font-size: 1.7rem;
        font-weight: 700;
        color: #fff;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.18);
    }
    .expanding-text p {
        margin: 0;
        font-size: 1.15rem;
        color: #f0f0f0;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
    }

    .simple-success-notification {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 2002;
        color: #28a745;
        text-align: center;
        background: none;
        pointer-events: none;
    }
    .checkmark {
        width: 72px;
        height: 72px;
        display: block;
        stroke: #28a745;
        stroke-width: 4;
        stroke-linecap: round;
        stroke-linejoin: round;
        margin-bottom: 1.2rem;
    }
    .checkmark-circle {
        stroke-dasharray: 157;
        stroke-dashoffset: 0;
        stroke: #e6f9ed;
        animation: circle-appear 0.5s ease-in;
    }
    .checkmark-check {
        stroke-dasharray: 36;
        stroke-dashoffset: 36;
        animation: check-draw 0.7s 0.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }
    @keyframes check-draw {
        to {
            stroke-dashoffset: 0;
        }
    }
    @keyframes circle-appear {
        from {
            stroke-dashoffset: 157;
        }
        to {
            stroke-dashoffset: 0;
        }
    }
    .simple-success-text h2 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
        font-weight: 600;
    }
    .simple-success-text p {
        margin: 0;
        font-size: 1.05rem;
        color: #333;
    }

    /* Estilos para el modal de eliminación de roles */
    .role-info-card {
        background: var(--color-bg-primary);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        padding: 1rem;
        margin: 1rem 0;
    }

    .role-info-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .role-info-header h4 {
        margin: 0;
        color: var(--color-text-primary);
        font-size: 1.1rem;
        font-weight: 600;
    }

    .role-info-description {
        margin: 0;
        color: var(--color-text-secondary);
        font-size: 0.9rem;
        line-height: 1.4;
    }

    .warning-section {
        margin: 1rem 0;
    }

    .warning-message {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 1rem;
        border-radius: var(--border-radius);
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }

    .warning-message.system-warning {
        background: #f8d7da;
        border-color: #f5c6cb;
        color: #721c24;
    }

    .warning-message svg {
        flex-shrink: 0;
        margin-top: 0.1rem;
    }

    .warning-message strong {
        display: block;
        margin-bottom: 0.25rem;
        font-weight: 600;
    }

    .warning-message p {
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.4;
    }

    .info-message {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 1rem;
        border-radius: var(--border-radius);
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin-bottom: 1rem;
    }

    .info-message svg {
        flex-shrink: 0;
        margin-top: 0.1rem;
    }

    .info-message strong {
        display: block;
        margin-bottom: 0.25rem;
        font-weight: 600;
    }

    .info-message p {
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.4;
    }

    /* Estilos específicos para el formulario de roles */
    .modal-form {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .permissions-editor {
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        padding: 1rem;
        background: var(--color-bg-secondary);
    }

    .permissions-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }

    .perm-category h5 {
        margin: 0 0 0.5rem 0;
        color: var(--color-text-primary);
        font-size: 0.9rem;
        font-weight: 600;
    }

    .checkbox-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }

    .pagination {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    .pagination button {
        padding: 0.5rem 1.2rem;
        border-radius: 0.25rem;
        border: 1px solid var(--color-border);
        background: var(--color-bg-secondary);
        color: var(--color-text-primary);
        font-weight: 500;
        cursor: pointer;
        transition: background 0.2s;
    }
    .pagination button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .debug-details {
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        overflow: hidden;
    }

    .debug-details summary {
        background: #f8f9fa;
        padding: 0.75rem 1rem;
        cursor: pointer;
        font-weight: 500;
        color: #495057;
        border-bottom: 1px solid #e0e0e0;
    }

    .debug-details summary:hover {
        background: #e9ecef;
    }

    .debug-data {
        background: #f8f9fa;
        padding: 1rem;
        margin: 0;
        font-family: "Courier New", monospace;
        font-size: 0.85rem;
        line-height: 1.4;
        color: #495057;
        overflow-x: auto;
        max-height: 300px;
        overflow-y: auto;
        border-radius: 0 0 8px 8px;
    }

    .debug-details[open] summary {
        border-bottom: 1px solid #dee2e6;
    }

    .section-header {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        margin-bottom: 1.2rem;
    }

    /* Botones de acción principales */
    .main-actions {
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: var(--color-bg-card);
        border-radius: var(--border-radius);
        border: 1px solid var(--color-border);
        box-shadow: var(--shadow-sm);
    }

    .action-group {
        display: flex;
        gap: 1rem;
        align-items: center;
        flex-wrap: wrap;
    }

    .action-btn {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        border-radius: var(--border-radius);
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        min-width: 140px;
        justify-content: center;
    }

    .action-btn:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }

    .action-btn svg {
        flex-shrink: 0;
    }

    .debug-btn {
        font-size: 0.85rem;
        padding: 0.5rem 1rem;
        opacity: 0.8;
    }

    .debug-btn:hover {
        opacity: 1;
    }
    .roles-section {
        padding-top: 0.5rem;
    }

    /* Estilos mejorados para el modal de paquetes */
    .package-subscriptions {
        max-height: 70vh;
        overflow-y: auto;
        padding: 1rem 0;
    }

    .package-subscriptions::-webkit-scrollbar {
        width: 6px;
    }

    .package-subscriptions::-webkit-scrollbar-track {
        background: var(--color-bg-secondary);
        border-radius: 3px;
    }

    .package-subscriptions::-webkit-scrollbar-thumb {
        background: var(--color-border);
        border-radius: 3px;
    }

    .package-subscriptions::-webkit-scrollbar-thumb:hover {
        background: var(--color-text-secondary);
    }

    .package-card {
        background: var(--color-bg-card);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius-lg);
        padding: var(--spacing-lg);
        margin-bottom: var(--spacing-lg);
        box-shadow: var(--shadow-md);
        transition: all var(--transition-normal);
        position: relative;
        overflow: hidden;
    }

    .package-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--color-accent);
        border-radius: var(--border-radius-lg) var(--border-radius-lg) 0 0;
    }

    .package-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        border-color: var(--color-accent);
    }

    .package-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--spacing-lg);
        padding-bottom: var(--spacing-md);
        border-bottom: 2px solid var(--color-border);
    }

    .package-name {
        margin: 0;
        font-size: var(--font-size-xl);
        font-weight: 700;
        color: var(--color-text);
    }

    .package-status {
        display: flex;
        align-items: center;
        gap: var(--spacing-xs);
        padding: var(--spacing-sm) var(--spacing-md);
        border-radius: 20px;
        font-size: var(--font-size-sm);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: var(--shadow-sm);
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }

    .status-dot.active {
        background: var(--color-success);
        box-shadow: 0 0 0 2px rgba(0, 230, 118, 0.3);
    }

    .status-dot.expired {
        background: var(--color-error);
        box-shadow: 0 0 0 2px rgba(255, 77, 109, 0.3);
    }

    .package-status.active {
        background: rgba(0, 230, 118, 0.1);
        color: var(--color-success);
        border: 1px solid var(--color-success);
    }

    .package-status.expired {
        background: rgba(255, 77, 109, 0.1);
        color: var(--color-error);
        border: 1px solid var(--color-error);
    }

    .package-details {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: var(--spacing-md);
        margin-bottom: var(--spacing-lg);
    }

    .detail-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--spacing-md);
        background: var(--color-bg-hover);
        border-radius: var(--border-radius);
        border: 1px solid var(--color-border);
    }

    .detail-label {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        font-weight: 600;
        color: var(--color-text-secondary);
        font-size: var(--font-size-sm);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .detail-value {
        display: flex;
        align-items: center;
        gap: var(--spacing-xs);
        color: var(--color-text);
        font-size: var(--font-size-sm);
        font-weight: 500;
        text-align: right;
    }

    .detail-value.amount {
        font-weight: 700;
        color: var(--color-success);
        font-size: var(--font-size-base);
    }

    .package-features {
        margin-top: var(--spacing-lg);
        padding-top: var(--spacing-lg);
        border-top: 2px solid var(--color-border);
    }

    .features-label {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        font-weight: 600;
        color: var(--color-text-secondary);
        font-size: var(--font-size-sm);
        margin-bottom: var(--spacing-md);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .features-list {
        display: flex;
        flex-wrap: wrap;
        gap: var(--spacing-sm);
    }

    .feature-badge {
        background: var(--color-accent);
        color: var(--color-bg);
        padding: var(--spacing-xs) var(--spacing-md);
        border-radius: 20px;
        font-size: var(--font-size-xs);
        font-weight: 600;
        border: none;
        box-shadow: var(--shadow-sm);
        transition: all var(--transition-normal);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .feature-badge:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
        opacity: 0.9;
    }

    .no-features {
        color: var(--color-text-secondary);
        font-style: italic;
        font-size: var(--font-size-sm);
        padding: var(--spacing-md);
        text-align: center;
        background: var(--color-bg-hover);
        border-radius: var(--border-radius);
        border: 1px dashed var(--color-border);
    }

    /* Estilos adicionales para el modal de paquetes */
    .package-modal {
        max-width: 800px;
        width: 90vw;
    }

    .modal-header {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        margin-bottom: var(--spacing-xl);
        padding-bottom: var(--spacing-lg);
        border-bottom: 2px solid var(--color-border);
        padding-right: 3rem; /* Espacio para el botón de cerrar */
    }

    .modal-title-section h3 {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        margin: 0 0 var(--spacing-sm) 0;
        font-size: var(--font-size-2xl);
        font-weight: 700;
        color: var(--color-text);
    }

    .modal-subtitle {
        margin: 0;
        color: var(--color-text-secondary);
        font-size: var(--font-size-base);
    }

    .user-email {
        color: var(--color-accent);
        font-weight: 500;
    }

    .modal-icon {
        color: var(--color-accent);
        opacity: 0.8;
    }

    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: var(--spacing-2xl) var(--spacing-md);
        text-align: center;
    }

    .loading-container p {
        margin: var(--spacing-md) 0 0 0;
        color: var(--color-text-secondary);
        font-size: var(--font-size-base);
    }

    .error-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: var(--spacing-2xl) var(--spacing-md);
        text-align: center;
        background: rgba(255, 77, 109, 0.1);
        border-radius: var(--border-radius-lg);
        border: 1px solid rgba(255, 77, 109, 0.2);
    }

    .error-icon {
        margin-bottom: var(--spacing-md);
        color: var(--color-error);
    }

    .error-container h4 {
        margin: 0 0 var(--spacing-sm) 0;
        color: var(--color-error);
        font-size: var(--font-size-lg);
        font-weight: 600;
    }

    .error-container p {
        margin: 0;
        color: var(--color-text-secondary);
        font-size: var(--font-size-sm);
    }

    .empty-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: var(--spacing-2xl) var(--spacing-md);
        text-align: center;
        background: var(--color-bg-hover);
        border-radius: var(--border-radius-lg);
        border: 1px dashed var(--color-border);
    }

    .empty-icon {
        margin-bottom: var(--spacing-md);
        opacity: 0.6;
        color: var(--color-text-secondary);
    }

    .empty-container h4 {
        margin: 0 0 var(--spacing-sm) 0;
        color: var(--color-text);
        font-size: var(--font-size-lg);
        font-weight: 600;
    }

    .empty-container p {
        margin: 0;
        color: var(--color-text-secondary);
        font-size: var(--font-size-sm);
    }

    @media (max-width: 768px) {
        .modal-header {
            flex-direction: column;
            gap: var(--spacing-md);
            padding-right: 0;
        }

        .package-details {
            grid-template-columns: 1fr;
        }

        .package-header {
            flex-direction: column;
            align-items: flex-start;
            gap: var(--spacing-sm);
        }

        .detail-label {
            font-size: var(--font-size-xs);
        }

        .detail-value {
            font-size: var(--font-size-xs);
        }

        .feature-badge {
            font-size: var(--font-size-xs);
            padding: var(--spacing-xs) var(--spacing-sm);
        }
    }

    .warning-text {
        color: var(--color-warning, #e67e22);
        font-weight: bold;
        margin-right: 0.3em;
    }
    .error-text {
        color: var(--color-danger, #e74c3c);
        font-weight: bold;
        margin-right: 0.3em;
    }

    /* Estilos específicos para notificación de usuario creado */
    .user-created-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        transform: none;
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(40, 167, 69, 0.3);
        pointer-events: auto;
        animation: slideInRight 0.5s ease-out;
        z-index: 3000;
    }

    .user-created-notification .checkmark {
        stroke: white;
        width: 48px;
        height: 48px;
        margin-bottom: 1rem;
    }

    .user-created-notification .checkmark-circle {
        stroke: rgba(255, 255, 255, 0.3);
    }

    .user-created-notification .simple-success-text h2 {
        color: white;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }

    .user-created-notification .simple-success-text p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.95rem;
    }

    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
</style>
