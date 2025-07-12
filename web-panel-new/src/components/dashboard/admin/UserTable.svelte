<script lang="ts">
    import { goto } from "$app/navigation";
    import { createRole, deleteRole, getRoles } from "$lib/api/roles";
    import {
        createUser,
        deleteUser,
        getUsers,
        updateUser,
    } from "$lib/api/users";
    import { user as sessionUser } from "$lib/sessionStore.js";
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
    }

    // Estados
    let users: User[] = [];
    let roles: Role[] = [];
    let loading = false;
    let rolesLoading = false;
    let error = "";
    let rolesError = "";
    let showModal = false;
    let showDeleteModal = false;
    let showRoleModal = false;
    // Cambia la declaración de selectedUser para aceptar null
    let selectedUser: User | null = null;

    // Filtros
    let searchTerm = "";
    let statusFilter = "";
    let roleFilter = "";
    let filterTimeout: number;

    // Aplicar filtros con debounce
    $: if (
        searchTerm !== undefined ||
        statusFilter !== undefined ||
        roleFilter !== undefined
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

    // --- Cambiar nombres de roles a versión corta ---
    const ROLE_LABELS = {
        sysadmin: "Sysadmin",
        "cuidador profesional": "Cuidador profesional",
        familiar: "Familiar",
        "sujeto del cuidado": "Sujeto del cuidado",
        "admin institución": "Admin institución",
    };

    // Manejo de errores para 'err' de tipo unknown
    function getErrorMessage(err: unknown): string {
        if (err instanceof Error) return err.message;
        if (typeof err === "string") return err;
        return "Error desconocido";
    }

    // Cargar datos al montar el componente
    onMount(async () => {
        await Promise.all([loadUsers(), loadRoles()]);
    });

    async function loadUsers() {
        loading = true;
        error = "";
        const { data, error: apiError } = await getUsers({
            search: searchTerm || undefined,
            status: statusFilter || undefined,
            role: roleFilter || undefined,
        });
        console.log("Respuesta getUsers:", data);
        if (apiError) {
            error = apiError;
            users = [];
        } else if (data) {
            // Mapear roles para compatibilidad
            users = Array.isArray(data)
                ? data.map((user) => ({
                      ...user,
                      role:
                          Array.isArray(user.roles) && user.roles.length > 0
                              ? user.roles[0]
                              : "",
                  }))
                : [];
        } else {
            users = [];
        }
        loading = false;
    }

    async function loadRoles() {
        rolesLoading = true;
        rolesError = "";
        try {
            roles = await getRoles();
        } catch (err) {
            rolesError = getErrorMessage(err);
            console.error("Error loading roles:", err);
        } finally {
            rolesLoading = false;
        }
    }

    function openModal(user: User | null = null) {
        selectedUser = user;
        if (user) {
            form = {
                name: `${user.first_name} ${user.last_name || ""}`.trim(),
                email: user.email || "",
                password: "",
                role: "", // Los roles se manejan por separado
                status: user.is_active ? "activo" : "inactivo",
            };
        } else {
            form = {
                name: "",
                email: "",
                password: "",
                role: roles[0]?.name || "",
                status: "activo",
            };
        }
        showModal = true;
    }

    function closeModal() {
        showModal = false;
        selectedUser = null;
        form = {
            name: "",
            email: "",
            password: "",
            role: "",
            status: "activo",
        };
    }

    function openDeleteModal(user: User) {
        selectedUser = user;
        showDeleteModal = true;
    }

    function closeDeleteModal() {
        showDeleteModal = false;
        selectedUser = null;
    }

    function openNewRoleModal() {
        roleForm = {
            name: "",
            description: "",
            permissions: {},
            is_system: false,
        };
        isNewRole = true;
        editablePermissions = {
            users: { read: false, write: false, delete: false },
            roles: { read: false, write: false, delete: false },
            institutions: { read: false, write: false, delete: false },
            packages: { read: false, write: false, delete: false },
            alerts: { read: false, write: false, delete: false },
            events: { read: false, write: false, delete: false },
            reports: { read: false, write: false, delete: false },
        };
        showRoleModal = true;
    }

    function openRoleModal(role: Role) {
        roleForm = {
            name: role.name,
            description: role.description || "",
            permissions: role.permissions,
            is_system: role.is_system || false,
        };
        isNewRole = false;
        showRoleModal = true;
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
        if (isNewRole && editablePermissions[category]) {
            editablePermissions[category][permission] = value;
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
        closeModal();
    }

    async function deleteUserHandler() {
        error = "";
        if (!selectedUser?.id) {
            error = "Usuario no seleccionado";
            return;
        }

        const { error: delError } = await deleteUser(selectedUser.id);
        if (delError) {
            error = delError;
            return;
        }
        await loadUsers();
        closeDeleteModal();
    }

    async function saveRole() {
        try {
            await createRole(roleForm);
            await loadRoles();
            closeRoleModal();
        } catch (err) {
            rolesError = getErrorMessage(err);
            console.error("Error creating role:", err);
        }
    }

    async function deleteRoleHandler(roleId: string) {
        try {
            await deleteRole(roleId);
            await loadRoles();
        } catch (err) {
            rolesError = getErrorMessage(err);
            console.error("Error deleting role:", err);
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

    async function openPackageModal(user: User = null) {
        packageUser = user;
        showPackageModal = true;
        packageLoading = true;
        packageError = "";
        currentPackage = null;
        packageHistory = [];
        allPackages = [];
        try {
            // Mockup: fetch real de paquetes
            currentPackage = user?.package || null;
            packageHistory = user?.package_history || [];
            allPackages = [
                { name: "Básico", desc: "Funciones esenciales", id: 1 },
                { name: "Premium", desc: "Incluye alertas y reportes", id: 2 },
                {
                    name: "Enterprise",
                    desc: "Soporte y personalización avanzada",
                    id: 3,
                },
            ];
        } catch (err) {
            packageError = getErrorMessage(err);
        } finally {
            packageLoading = false;
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

    function openEditModal(user: User) {
        console.log("openEditModal llamado con:", user);
        selectedUser = user;
        showEditModal = true;
        console.log(
            "showEditModal:",
            showEditModal,
            "selectedUser:",
            selectedUser,
        );
    }
    function closeEditModal() {
        showEditModal = false;
        selectedUser = null;
    }
    // Reemplaza handleEditSave para solo refrescar usuarios y cerrar el modal
    async function handleEditSave() {
        await loadUsers();
        closeEditModal();
    }
</script>

<div class="user-table-section">
    <div class="user-table-header">
        <h2>Gestión de Usuarios</h2>
        <div class="header-actions">
            <button class="new-role-btn" on:click={openNewRoleModal}
                >+ Nuevo rol</button
            >
            <button
                class="new-user-btn"
                on:click={() => goto("/dashboard/users/create")}
            >
                + Nuevo usuario
            </button>
        </div>
    </div>

    <!-- Sección de Roles -->
    <div class="roles-section">
        <h3>Roles del Sistema</h3>
        {#if rolesLoading}
            <div class="loading">Cargando roles...</div>
        {:else if rolesError}
            <div class="error">{rolesError}</div>
        {:else if roles.length === 0}
            <div class="empty">No hay roles definidos.</div>
        {:else}
            <div class="roles-grid">
                {#each roles as role}
                    <div class="role-card">
                        <div class="role-header">
                            <h4>{ROLE_LABELS[role.name] || role.name}</h4>
                            {#if role.is_system}
                                <span class="system-badge">Sistema</span>
                            {/if}
                        </div>
                        <p class="role-description">
                            {role.description || "Sin descripción"}
                        </p>
                        <div class="role-actions">
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
                                <button
                                    class="delete-btn"
                                    on:click={() => deleteRoleHandler(role.id)}
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
                                        ><path d="M3 6h18" /><path
                                            d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                                        /><path
                                            d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0v12m4-12v12"
                                        /></svg
                                    >
                                </button>
                            {/if}
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
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
            <option value="">Todos los estados</option>
            <option value="activo">Activo</option>
            <option value="inactivo">Inactivo</option>
        </select>
        <select class="filter-select" bind:value={roleFilter}>
            <option value="">Todos los roles</option>
            {#each roles as role}
                <option value={role.name}
                    >{ROLE_LABELS[role.name] || role.name}</option
                >
            {/each}
        </select>
        <select class="filter-select">
            <option value="">Todos los paquetes</option>
            <option value="basic">Básico</option>
            <option value="premium">Premium</option>
            <option value="enterprise">Enterprise</option>
        </select>
        <select class="filter-select">
            <option value="">Todas las instituciones</option>
            <option value="inst1">San Martín</option>
            <option value="inst2">Santa María</option>
            <option value="inst3">CUIOT Central</option>
        </select>
        <button
            class="btn-secondary"
            on:click={() => {
                searchTerm = "";
                statusFilter = "";
                roleFilter = "";
                loadUsers();
            }}>Limpiar filtros</button
        >
    </div>

    <!-- Sección de Usuarios -->
    <div class="users-section">
        <h3>Usuarios</h3>
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
                        <th>Acciones</th>
                        <th>Nombre</th>
                        <th>Email</th>
                        <th>Roles</th>
                        <th>Estado</th>
                        <th>Último acceso</th>
                    </tr>
                </thead>
                <tbody>
                    {#each users as user}
                        <tr>
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
                                    <button
                                        class="package-btn"
                                        on:click={() => openPackageModal(user)}
                                        title="Ver detalles del paquete"
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
                                    <button
                                        class="action-btn"
                                        title="Editar usuario"
                                        on:click={() => openEditModal(user)}
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
                            <td
                                >{`${user.first_name} ${user.last_name || ""}`.trim()}</td
                            >
                            <td>{user.email}</td>
                            <td>
                                <div class="user-roles">
                                    <span class="role-badge">Usuario</span>
                                    {#if user.is_freelance}
                                        <span class="role-badge freelance"
                                            >Freelance</span
                                        >
                                    {/if}
                                    {#if user.is_verified}
                                        <span class="role-badge verified"
                                            >Verificado</span
                                        >
                                    {/if}
                                </div>
                            </td>
                            <td>
                                <span
                                    class="user-status {user.is_active
                                        ? 'activo'
                                        : 'inactivo'}"
                                >
                                    {user.is_active ? "Activo" : "Inactivo"}
                                </span>
                            </td>
                            <td>
                                {user.last_login
                                    ? new Date(
                                          user.last_login,
                                      ).toLocaleDateString("es-ES")
                                    : "Nunca"}
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
                title="Cerrar">&times;</button
            >
            <h3 id="delete-modal-title">Eliminar usuario</h3>
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
            <div class="modal-actions">
                <button class="btn-danger" on:click={deleteUserHandler}
                    >Eliminar</button
                >
                <button class="btn-secondary" on:click={closeDeleteModal}
                    >Cancelar</button
                >
            </div>
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
                <label>
                    Nombre del Rol
                    <input
                        type="text"
                        bind:value={roleForm.name}
                        placeholder="admin, caregiver, etc."
                        required
                        disabled={roleForm.is_system}
                    />
                </label>
                <label>
                    Descripción
                    <textarea
                        bind:value={roleForm.description}
                        placeholder="Descripción del rol"
                        rows="3"
                        disabled={roleForm.is_system}
                    ></textarea>
                </label>
                {#if roleForm.is_system}
                    <div class="form-info">Rol de sistema. No editable.</div>
                {/if}
                <label>
                    Permisos
                    {#if isNewRole}
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
                                                editablePermissions.packages
                                                    .read
                                            }
                                        />
                                        Leer paquetes
                                    </label>
                                    <label class="checkbox-label">
                                        <input
                                            type="checkbox"
                                            bind:checked={
                                                editablePermissions.packages
                                                    .write
                                            }
                                        />
                                        Crear/editar paquetes
                                    </label>
                                    <label class="checkbox-label">
                                        <input
                                            type="checkbox"
                                            bind:checked={
                                                editablePermissions.packages
                                                    .delete
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
                                                editablePermissions.alerts
                                                    .delete
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
                                                editablePermissions.events
                                                    .delete
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
                                                editablePermissions.reports
                                                    .write
                                            }
                                        />
                                        Crear/editar reportes
                                    </label>
                                    <label class="checkbox-label">
                                        <input
                                            type="checkbox"
                                            bind:checked={
                                                editablePermissions.reports
                                                    .delete
                                            }
                                        />
                                        Eliminar reportes
                                    </label>
                                </div>
                            </div>
                        </div>
                    {:else}
                        <div class="permissions-list">
                            {#if roleForm.permissions}
                                {#each Object.entries(typeof roleForm.permissions === "string" ? JSON.parse(roleForm.permissions) : roleForm.permissions) as [key, value]}
                                    <div class="perm-group">
                                        <strong>{key}</strong>:
                                        {#if typeof value === "object"}
                                            <ul>
                                                {#each Object.entries(value) as [perm, val]}
                                                    <li>
                                                        {perm}:
                                                        <span
                                                            class={val
                                                                ? "perm-yes"
                                                                : "perm-no"}
                                                            >{val
                                                                ? "Sí"
                                                                : "No"}</span
                                                        >
                                                    </li>
                                                {/each}
                                            </ul>
                                        {:else}
                                            <span
                                                class={value
                                                    ? "perm-yes"
                                                    : "perm-no"}
                                                >{value ? "Sí" : "No"}</span
                                            >
                                        {/if}
                                    </div>
                                {/each}
                            {:else}
                                <span class="perm-none"
                                    >Sin permisos definidos</span
                                >
                            {/if}
                        </div>
                    {/if}
                </label>
                {#if rolesError}
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

    <!-- Modal de paquetes -->
    {#if showPackageModal}
        <div class="modal-backdrop" on:click={closePackageModal}></div>
        <div
            class="modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="package-modal-title"
        >
            <button
                class="modal-close"
                on:click={closePackageModal}
                title="Cerrar">&times;</button
            >
            <h3 id="package-modal-title">
                Información de paquetes {packageUser
                    ? `de ${packageUser.name}`
                    : ""}
            </h3>
            {#if packageLoading}
                <div class="loading">Cargando paquetes...</div>
            {:else if packageError}
                <div class="form-error">{packageError}</div>
            {:else}
                <div class="package-section">
                    <h4>Paquete actual</h4>
                    {#if currentPackage}
                        <div class="package-card actual">
                            <strong>{currentPackage.name}</strong>
                            <span>{currentPackage.desc}</span>
                        </div>
                    {:else}
                        <div class="empty">Sin paquete asignado</div>
                    {/if}
                    <h4>Historial de paquetes</h4>
                    {#if packageHistory.length > 0}
                        <ul class="package-history-list">
                            {#each packageHistory as p}
                                <li>
                                    <strong>{p.name}</strong>
                                    <span>{p.desc}</span>
                                </li>
                            {/each}
                        </ul>
                    {:else}
                        <div class="empty">Sin historial de paquetes</div>
                    {/if}
                    <h4>Todos los paquetes</h4>
                    <div class="package-list">
                        {#each allPackages as p}
                            <div class="package-card">
                                <strong>{p.name}</strong>
                                <span>{p.desc}</span>
                            </div>
                        {/each}
                    </div>
                    <button
                        class="btn-primary"
                        style="margin-top:1.2rem;"
                        on:click={() => goto("/dashboard/packages")}
                        >Nuevo paquete</button
                    >
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
    }
    .role-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.2rem;
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
        margin-left: 0.5em;
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
        background: var(--color-primary);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 500;
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
        padding: 2rem 2.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        z-index: 1001;
        min-width: 350px;
        max-width: 95vw;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
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
    }
    .modal-actions button {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: var(--border-radius);
        cursor: pointer;
        font-weight: 500;
        transition: background-color 0.2s;
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
</style>
