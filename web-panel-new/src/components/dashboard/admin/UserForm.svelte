<script lang="ts">
    import { getInstitutions } from "$lib/api/institutions";
    import { getRoles } from "$lib/api/roles";
    import { assignRole, createUser, updateUser } from "$lib/api/users";
    import PlusIcon from "$lib/ui/icons/PlusIcon.svelte";
    import { validateFullUser } from "$lib/validations/userValidations";
    import { createEventDispatcher, onMount } from "svelte";
    import ModalNotification from "../../shared/ui/ModalNotification.svelte";

    const dispatch = createEventDispatcher();

    // Props
    export let disabled = false;
    export let initialData: any = null;
    export let editMode: boolean = false;
    export let sessionUserRole: string = "";

    // Tipos
    interface Role {
        id: string;
        name: string;
        description?: string;
        is_system?: boolean;
        is_active?: boolean;
    }

    interface Institution {
        id: number;
        name: string;
        institution_type: string;
    }

    interface Package {
        id: string;
        name: string;
        description: string;
        price_monthly: number;
        price_yearly: number;
        max_users: number;
        max_devices: number;
    }

    // Estados
    let loading = false;
    let submitting = false;
    let error = "";
    let debugResult: Record<string, any> | null = null;

    // Datos de referencia
    let roles: Role[] = [];
    let institutions: Institution[] = [];
    let rolesLoadError = false;
    let institutionsLoadError = false;
    let emailChecking = false;
    let emailExists = false;

    // Inicialización robusta SOLO cuando cambia initialData y editMode
    let form = {
        id: undefined as number | undefined,
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        password: "",
        confirm_password: "",
        role: "",
        is_active: true,
        date_of_birth: "",
        gender: "",
        institution_id: undefined as number | undefined,
        professional_license: "",
        specialization: "",
        experience_years: 0,
        is_freelance: false,
        hourly_rate: 0,
        availability: "",
        legal_representative_id: undefined as string | null | undefined,
        legal_capacity_verified: false,
        terms_accepted: false,
        is_verified: false,
    };
    let institutionIdString = "";
    $: institutionIdString = form.institution_id
        ? String(form.institution_id)
        : "";

    let dateOfBirthString = "";
    $: dateOfBirthString = form.date_of_birth ? String(form.date_of_birth) : "";

    // Precarga robusta SOLO al abrir en modo edición
    $: if (editMode && initialData && initialData.id !== form.id) {
        form = { ...form, ...initialData };
        // Mapear roles para compatibilidad
        if (Array.isArray(initialData.roles) && initialData.roles.length > 0) {
            form.role = initialData.roles[0];
        } else if (initialData.role) {
            form.role = initialData.role;
        } else {
            form.role = "";
        }
        // Asegura que el id esté presente en el form
        if (initialData.id) {
            form.id = initialData.id;
        }
        // Asignar género por defecto si falta
        if (!form.gender) {
            form.gender = "Otro";
        }
    }

    // Validaciones
    let errors: Record<string, string> = {};

    function validateForm() {
        errors = validateFullUser(form, "edit");
    }

    // Función para verificar si el email ya existe
    async function checkEmailExists(email: string) {
        if (!email || email.length < 3 || !email.includes("@")) {
            emailExists = false;
            return;
        }

        emailChecking = true;
        try {
            const response = await fetch(
                `/api/v1/auth/check-email?email=${encodeURIComponent(email)}`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                },
            );

            if (response.ok) {
                const data = await response.json();
                emailExists = data.exists;
            } else {
                emailExists = false;
            }
        } catch (error) {
            emailExists = false;
        } finally {
            emailChecking = false;
        }
    }

    // Verificar email cuando cambie (con debounce)
    let emailCheckTimeout: number;
    $: if (form.email && form.email.length > 2 && form.email.includes("@")) {
        clearTimeout(emailCheckTimeout);
        emailCheckTimeout = setTimeout(() => {
            if (!editMode || form.email !== initialData?.email) {
                checkEmailExists(form.email);
            }
        }, 500);
    }

    // Secciones expandibles
    let expandedSections: {
        [key: string]: boolean;
        personal: boolean;
        security: boolean;
        role: boolean;
        institution: boolean;
        professional: boolean;
        legal: boolean;
        validation: boolean;
    } = {
        personal: false,
        security: false,
        role: false,
        institution: false,
        professional: false,
        legal: false,
        validation: false,
    };

    // Expandir todas las secciones automáticamente en modo edición
    $: if (editMode) {
        expandedSections = {
            personal: true,
            security: true,
            role: true,
            institution: true,
            professional: true,
            legal: true,
            validation: true,
        };
    }

    // --- NUEVO: lógica de visibilidad de secciones por rol ---
    $: visibleSections = {
        personal: true,
        security: true,
        role: true,
        professional: [
            "caregiver",
            "freelance_caregiver",
            "medical_staff",
        ].includes(form.role),
        legal: form.role === "family_member",
        institution: ["institution_admin", "institution_staff"].includes(
            form.role,
        ),
        validation: true,
    };

    // Filtros según rol seleccionado
    $: availableRoles = roles.filter(
        (role) => !role.is_system || role.name === "sysadmin",
    );
    $: isCaregiver = form.role === "caregiver";
    $: isDelegatedCare = form.role === "cared_person_delegated";
    $: requiresRepresentative = isDelegatedCare;

    // Validar datos mínimos según reglas de negocio
    $: hasMinimumData =
        form.first_name?.trim() &&
        form.last_name?.trim() &&
        form.email?.trim() &&
        form.phone?.trim() &&
        form.role &&
        !emailExists && // No permitir emails duplicados
        !emailChecking && // Esperar a que termine la verificación
        (editMode ||
            (form.password?.trim() && form.password === form.confirm_password)); // Password requerido y coincidente para creación

    // Validación específica por rol
    $: roleSpecificValidation = {
        caregiver: form.professional_license?.trim(),
        freelance_caregiver:
            form.professional_license?.trim() && form.hourly_rate > 0,
        medical_staff: form.professional_license?.trim(),
        institution_admin: form.institution_id,
        institution_staff: form.institution_id,
        family_member: true, // Solo requiere datos básicos
        cared_person_self: true, // Solo requiere datos básicos
        caredperson: true, // Solo requiere datos básicos
    };

    $: hasRoleSpecificData = form.role
        ? roleSpecificValidation[
              form.role as keyof typeof roleSpecificValidation
          ]
        : true;

    // --- Lógica de edición por rol ---
    function isFieldEditable(field: string): boolean {
        // Si el usuario logueado es admin o sysadmin, todo editable
        if (sessionUserRole === "admin" || sessionUserRole === "sysadmin")
            return true;
        // Si no hay rol, todo editable (modo desarrollo)
        if (!form.role) return true;
        // Caregiver: solo datos personales y profesionales
        if (form.role === "caregiver") {
            return [
                "first_name",
                "last_name",
                "email",
                "phone",
                "gender",
                "date_of_birth",
                "professional_license",
                "specialization",
                "experience_years",
                "is_freelance",
                "hourly_rate",
                "availability",
                "is_active",
                "is_verified",
            ].includes(field);
        }
        // Family: solo personales y legales
        if (form.role === "family") {
            return [
                "first_name",
                "last_name",
                "email",
                "phone",
                "gender",
                "date_of_birth",
                "legal_representative_id",
                "legal_capacity_verified",
                "terms_accepted",
                "is_active",
                "is_verified",
            ].includes(field);
        }
        // Institution: solo institucionales y paquetes
        if (form.role === "institution") {
            return ["institution_id", "is_active", "is_verified"].includes(
                field,
            );
        }
        // Cared person: solo personales y salud
        if (form.role === "cared_person") {
            return [
                "first_name",
                "last_name",
                "email",
                "phone",
                "gender",
                "date_of_birth",
                "is_active",
                "is_verified",
            ].includes(field);
        }
        // Por defecto, editable
        return true;
    }

    // --- Ajuste del botón Actualizar ---
    $: canUpdate = hasMinimumData && hasRoleSpecificData;

    // Debug para el botón
    $: buttonDebug = {
        hasMinimumData,
        hasRoleSpecificData,
        canUpdate,
        role: form.role,
        firstName: form.first_name?.trim(),
        lastName: form.last_name?.trim(),
        email: form.email?.trim(),
        phone: form.phone?.trim(),
        // Debug detallado de validación
        firstNameValid: !!form.first_name?.trim(),
        lastNameValid: !!form.last_name?.trim(),
        emailValid: !!form.email?.trim(),
        phoneValid: !!form.phone?.trim(),
        roleValid: !!form.role,
        passwordValid: editMode || !!form.password?.trim(),
        passwordMatch: editMode || form.password === form.confirm_password,
        // Valores exactos para debugging
        firstNameValue: form.first_name,
        lastNameValue: form.last_name,
        emailValue: form.email,
        phoneValue: form.phone,
        roleValue: form.role,
        passwordValue: form.password ? "***" : "",
        confirmPasswordValue: form.confirm_password ? "***" : "",
    };

    let showMissingFieldsModal = false;
    let missingFields: string[] = [];
    let missingFieldsMessage = "";

    onMount(async () => {
        console.log("🔧 UserForm onMount - Cargando datos...");
        try {
            console.log("🔧 Cargando roles...");
            const rolesData = await getRoles();
            console.log("✅ Roles cargados:", rolesData);
            roles = Array.isArray(rolesData) ? rolesData : [];
            console.log("✅ Roles procesados:", roles.length);
            console.log(
                "✅ Roles activos:",
                roles.filter((r) => r.is_active !== false).length,
            );
            rolesLoadError = false;
        } catch (err) {
            console.error("❌ Error cargando roles:", err);
            roles = [];
            rolesLoadError = true;
            error = `Error cargando roles: ${err instanceof Error ? err.message : "Error desconocido"}`;
        }
        try {
            console.log("🔧 Cargando instituciones...");
            const institutionsData = await getInstitutions();
            console.log("✅ Instituciones cargadas:", institutionsData);
            institutions = Array.isArray(institutionsData)
                ? institutionsData
                : [];
            console.log("✅ Instituciones procesadas:", institutions.length);
            institutionsLoadError = false;
        } catch (err) {
            console.error("❌ Error cargando instituciones:", err);
            institutions = [];
            institutionsLoadError = true;
            error = `${error ? error + "; " : ""}Error cargando instituciones: ${err instanceof Error ? err.message : "Error desconocido"}`;
        }
    });

    async function loadRoles() {
        try {
            roles = await getRoles();
        } catch (err) {
            error = err instanceof Error ? err.message : "Error desconocido";
        }
    }

    async function loadInstitutions() {
        try {
            institutions = await getInstitutions();
        } catch (err) {
            error = "Error al cargar instituciones";
            console.error(err);
        }
    }

    function toggleSection(section: string) {
        expandedSections[section] = !expandedSections[section];
        expandedSections = { ...expandedSections };
    }

    function expandAllSections() {
        expandedSections = {
            personal: true,
            security: true,
            role: true,
            institution: true,
            professional: true,
            legal: true,
            validation: true,
        };
    }

    function calculateAge(birthDate: string): number {
        const today = new Date();
        const birth = new Date(birthDate);
        let age = today.getFullYear() - birth.getFullYear();
        const monthDiff = today.getMonth() - birth.getMonth();

        if (
            monthDiff < 0 ||
            (monthDiff === 0 && today.getDate() < birth.getDate())
        ) {
            age--;
        }

        return age;
    }

    // --- Guardar usuario y rol ---
    async function handleSubmit() {
        validateForm();
        if (Object.keys(errors).length > 0) {
            console.log(
                "❌ UserForm handleSubmit: Errores de validación",
                errors,
            );
            return;
        }

        // Validación preventiva de email duplicado
        if (!editMode && form.email) {
            console.log(
                "🔍 UserForm handleSubmit: Verificando email antes del envío...",
            );
            try {
                const response = await fetch(
                    `/api/v1/auth/check-email?email=${encodeURIComponent(form.email)}`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                        },
                    },
                );

                if (response.ok) {
                    const data = await response.json();
                    if (data.exists) {
                        error =
                            "❌ El email ya está registrado en el sistema. Por favor, use un email diferente.";
                        console.log(
                            "❌ UserForm handleSubmit: Email duplicado detectado preventivamente",
                        );
                        return;
                    }
                }
            } catch (error) {
                console.error(
                    "❌ UserForm handleSubmit: Error verificando email:",
                    error,
                );
                // Continuar con el envío si hay error en la verificación
            }
        }

        submitting = true;
        error = "";
        debugResult = {};
        let assignRoleNeeded = false;
        let previousRole =
            initialData &&
            (Array.isArray(initialData.roles)
                ? initialData.roles[0]
                : initialData.role);

        try {
            let result;

            if (editMode) {
                // Modo edición: actualizar usuario existente
                const userUpdateData = { ...form };
                delete (userUpdateData as any).role;
                if (!userUpdateData.password)
                    delete (userUpdateData as any).password;
                if (!userUpdateData.date_of_birth)
                    delete (userUpdateData as any).date_of_birth;
                else {
                    // Convertir fecha a formato datetime para el backend
                    const dateValue = userUpdateData.date_of_birth;
                    if (typeof dateValue === "string" && dateValue) {
                        // Agregar tiempo (00:00:00) a la fecha para convertirla a datetime
                        userUpdateData.date_of_birth = `${dateValue}T00:00:00`;
                    }
                }

                result = await updateUser(String(form.id), userUpdateData);
                debugResult.updateResult = result;
            } else {
                // Modo creación: crear nuevo usuario
                const userCreateData = { ...form };
                delete (userCreateData as any).role;
                delete (userCreateData as any).id;
                delete (userCreateData as any).confirm_password; // Eliminar confirm_password

                // Para creación, password es requerido
                if (!userCreateData.password) {
                    error =
                        "La contraseña es requerida para crear un nuevo usuario";
                    return;
                }

                if (!userCreateData.date_of_birth)
                    delete (userCreateData as any).date_of_birth;
                else {
                    // Convertir fecha a formato datetime para el backend
                    const dateValue = userCreateData.date_of_birth;
                    if (typeof dateValue === "string" && dateValue) {
                        // Agregar tiempo (00:00:00) a la fecha para convertirla a datetime
                        userCreateData.date_of_birth = `${dateValue}T00:00:00`;
                    }
                }

                result = await createUser(userCreateData);
                debugResult.createResult = result;
            }

            if (result.error) {
                if (result.error.includes("401")) {
                    // Forzar logout y redirigir
                    if (typeof window !== "undefined") {
                        localStorage.removeItem("token");
                        sessionStorage.setItem(
                            "sessionMessage",
                            "Sesión expirada, por favor vuelve a iniciar sesión.",
                        );
                        window.location.href = "/login";
                    }
                    return;
                } else if (result.error.includes("403")) {
                    error = editMode
                        ? "No tienes permisos para editar este usuario."
                        : "No tienes permisos para crear usuarios.";
                    return;
                } else if (
                    result.error.includes("Email already registered") ||
                    result.error.includes("already registered")
                ) {
                    error =
                        "❌ El email ya está registrado en el sistema. Por favor, use un email diferente.";
                    return;
                } else {
                    error = result.error;
                    return;
                }
            }

            // Obtener el ID del usuario (nuevo o existente)
            const userId = editMode ? String(form.id) : result.data?.id;

            // Siempre asignar el rol seleccionado tras guardar (si hay rol y usuario)
            if (form.role && userId) {
                // En modo creación, siempre asignar el rol
                // En modo edición, solo asignar si cambió
                if (!editMode || !previousRole || form.role !== previousRole) {
                    assignRoleNeeded = true;
                }
            }

            if (assignRoleNeeded && userId) {
                const assignResult = await assignRole(userId, form.role);
                debugResult.assignResult = assignResult;
                if (assignResult.error) {
                    // Intentar parsear error JSON
                    try {
                        const errObj = JSON.parse(assignResult.error);
                        if (errObj.missing_fields) {
                            missingFields = errObj.missing_fields;
                            missingFieldsMessage =
                                errObj.message ||
                                "Faltan datos obligatorios para el rol seleccionado.";
                            showMissingFieldsModal = true;
                            return;
                        }
                    } catch (e) {}
                    error = assignResult.error;
                    return;
                }
            }
            // Mensaje de éxito
            error = "";
            dispatch("submit", { ...form, debugResult });
        } catch (err) {
            const errorMessage =
                err instanceof Error
                    ? err.message
                    : "Error al procesar formulario";
            error = errorMessage;
        } finally {
            submitting = false;
        }
    }

    function updateForm(field: keyof typeof form, value: any) {
        (form as any)[field] = value;
        validateForm();
    }
</script>

<div class="user-form-container">
    {#if loading}
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p>Cargando datos...</p>
        </div>
    {:else}
        <form on:submit|preventDefault={handleSubmit} class="user-form">
            <div class="form-header">
                <div class="form-info">
                    <h2>{editMode ? "Editar usuario" : "Crear Usuario"}</h2>
                    <p>
                        {editMode
                            ? "Modifica los datos necesarios y actualiza el usuario."
                            : "Complete los datos mínimos requeridos o expanda las secciones para información adicional"}
                    </p>
                    {#if !editMode}
                        <div class="form-progress">
                            <div class="progress-bar">
                                <div
                                    class="progress-fill"
                                    style="width: {hasMinimumData
                                        ? hasRoleSpecificData
                                            ? '100%'
                                            : '75%'
                                        : '50%'}"
                                ></div>
                            </div>
                            <span class="progress-text">
                                {hasMinimumData
                                    ? hasRoleSpecificData
                                        ? "✅ Completado"
                                        : "⚠️ Datos básicos completos"
                                    : "📝 Datos básicos requeridos"}
                            </span>
                        </div>
                    {/if}
                </div>
                {#if !editMode}
                    <button
                        class="expand-all-btn"
                        on:click={expandAllSections}
                        {disabled}
                    >
                        <PlusIcon size={16} />
                        Expandir Todo
                    </button>
                {/if}
            </div>
            <div class="form-section required">
                <div class="section-header">
                    <h3>📋 Datos Mínimos Requeridos</h3>
                    <span class="required-badge">Obligatorio</span>
                </div>
                <div class="form-grid">
                    <div class="form-group">
                        <label for="first_name">Nombre *</label>
                        <input
                            id="first_name"
                            type="text"
                            bind:value={form.first_name}
                            on:input={(e) => {
                                const t = e.target as HTMLInputElement | null;
                                updateForm("first_name", t ? t.value : "");
                            }}
                            class:error={errors.first_name}
                            class:debug-not-editable={!isFieldEditable(
                                "first_name",
                            )}
                            placeholder="Ingrese el nombre"
                            disabled={disabled ||
                                !isFieldEditable("first_name")}
                        />
                        {#if !isFieldEditable("first_name")}
                            <span style="color:red;font-weight:bold;"
                                >NO EDITABLE POR PERMISOS</span
                            >
                        {/if}
                        {#if errors.first_name}<span class="error-text"
                                >{errors.first_name}</span
                            >{/if}
                    </div>
                    <div class="form-group">
                        <label for="last_name">Apellido *</label>
                        <input
                            id="last_name"
                            type="text"
                            bind:value={form.last_name}
                            on:input={(e) => {
                                const t = e.target as HTMLInputElement | null;
                                updateForm("last_name", t ? t.value : "");
                            }}
                            placeholder="Ingrese el apellido"
                            disabled={disabled || !isFieldEditable("last_name")}
                        />
                        {#if errors.last_name}<span class="error-text"
                                >{errors.last_name}</span
                            >{/if}
                    </div>
                    <div class="form-group">
                        <label for="email">Email *</label>
                        <input
                            id="email"
                            type="email"
                            bind:value={form.email}
                            on:input={(e) => {
                                const t = e.target as HTMLInputElement | null;
                                updateForm("email", t ? t.value : "");
                            }}
                            placeholder="usuario@ejemplo.com"
                            disabled={disabled || !isFieldEditable("email")}
                            class:error={errors.email || emailExists}
                        />
                        {#if emailChecking}
                            <span class="info-text"
                                >🔍 Verificando email...</span
                            >
                        {:else if emailExists}
                            <span class="error-text"
                                >❌ Este email ya está registrado en el sistema</span
                            >
                        {:else if errors.email}
                            <span class="error-text">{errors.email}</span>
                        {/if}
                    </div>
                    <div class="form-group">
                        <label for="phone">Teléfono *</label>
                        <input
                            id="phone"
                            type="tel"
                            bind:value={form.phone}
                            on:input={(e) => {
                                const t = e.target as HTMLInputElement | null;
                                updateForm("phone", t ? t.value : "");
                            }}
                            placeholder="+54 11 1234-5678"
                            disabled={disabled || !isFieldEditable("phone")}
                        />
                        {#if errors.phone}<span class="error-text"
                                >{errors.phone}</span
                            >{/if}
                    </div>
                    {#if !editMode}
                        <div class="form-group">
                            <label for="password">Contraseña *</label>
                            <input
                                id="password"
                                type="password"
                                bind:value={form.password}
                                on:input={(e) => {
                                    const t =
                                        e.target as HTMLInputElement | null;
                                    updateForm("password", t ? t.value : "");
                                }}
                                placeholder="Ingrese la contraseña"
                                class:error={errors.password}
                                disabled={disabled ||
                                    !isFieldEditable("password")}
                            />
                            {#if errors.password}<span class="error-text"
                                    >{errors.password}</span
                                >{/if}
                        </div>
                        <div class="form-group">
                            <label for="confirm_password"
                                >Confirmar Contraseña *</label
                            >
                            <input
                                id="confirm_password"
                                type="password"
                                bind:value={form.confirm_password}
                                on:input={(e) => {
                                    const t =
                                        e.target as HTMLInputElement | null;
                                    updateForm(
                                        "confirm_password",
                                        t ? t.value : "",
                                    );
                                }}
                                placeholder="Confirme la contraseña"
                                class:error={errors.confirm_password}
                                disabled={disabled ||
                                    !isFieldEditable("confirm_password")}
                            />
                            {#if errors.confirm_password}<span
                                    class="error-text"
                                    >{errors.confirm_password}</span
                                >{/if}
                            {#if form.password && form.confirm_password && form.password !== form.confirm_password}
                                <span class="error-text"
                                    >❌ Las contraseñas no coinciden</span
                                >
                            {/if}
                        </div>
                    {:else}
                        <div class="form-group">
                            <label for="password"
                                >Nueva Contraseña (opcional)</label
                            >
                            <input
                                id="password"
                                type="password"
                                bind:value={form.password}
                                on:input={(e) => {
                                    const t =
                                        e.target as HTMLInputElement | null;
                                    updateForm("password", t ? t.value : "");
                                }}
                                placeholder="Dejar vacío para mantener la actual"
                                class:error={errors.password}
                                disabled={disabled ||
                                    !isFieldEditable("password")}
                            />
                            {#if errors.password}<span class="error-text"
                                    >{errors.password}</span
                                >{/if}
                        </div>
                    {/if}
                    <div class="form-group">
                        <label for="gender">Género *</label>
                        <select
                            id="gender"
                            value={form.gender ?? ""}
                            on:change={(e) => {
                                const t = e.target as HTMLSelectElement | null;
                                updateForm(
                                    "gender",
                                    t && t.value ? t.value : "",
                                );
                            }}
                            class:error={errors.gender}
                            disabled={disabled || !isFieldEditable("gender")}
                        >
                            <option value="">Seleccionar género</option>
                            <option value="female">Femenino</option>
                            <option value="male">Masculino</option>
                            <option value="other">Otro</option>
                            <option value="prefer_not_to_say"
                                >Prefiero no decir</option
                            >
                        </select>
                        {#if errors.gender}<span class="error-text"
                                >{errors.gender}</span
                            >{/if}
                    </div>
                    <div class="form-group">
                        <label for="date_of_birth">Fecha de nacimiento</label>
                        <input
                            id="date_of_birth"
                            type="date"
                            bind:value={dateOfBirthString}
                            on:input={(e) => {
                                const t = e.target as HTMLInputElement | null;
                                updateForm("date_of_birth", t ? t.value : "");
                            }}
                            disabled={disabled ||
                                !isFieldEditable("date_of_birth")}
                        />
                        {#if errors.date_of_birth}
                            <span class="error-text"
                                >{errors.date_of_birth}</span
                            >
                        {/if}
                    </div>
                    <div class="form-group">
                        <label for="role">Rol *</label>
                        <select
                            id="role"
                            value={form.role ?? ""}
                            on:change={(e) => {
                                const t = e.target as HTMLSelectElement | null;
                                updateForm("role", t && t.value ? t.value : "");
                            }}
                            class:error={errors.role}
                            disabled={disabled || !isFieldEditable("role")}
                        >
                            {#if roles.length === 0}
                                <option value="">Sin datos</option>
                            {:else}
                                <option value="">Seleccionar rol</option>
                                {#each roles as role}
                                    <option value={role.name}
                                        >{role.name}</option
                                    >
                                {/each}
                            {/if}
                        </select>
                        {#if rolesLoadError}
                            <div class="error-section">
                                <span class="error-text"
                                    >❌ No se pudieron cargar los roles.
                                    Verifique la conexión.</span
                                >
                                <button
                                    class="retry-btn"
                                    on:click={loadRoles}
                                    disabled={loading}
                                >
                                    🔄 Reintentar
                                </button>
                            </div>
                        {:else if roles.length === 0}
                            <span class="warning-text"
                                >⚠️ No hay roles disponibles en el sistema.</span
                            >
                        {/if}
                        {#if errors.role}<span class="error-text"
                                >{errors.role}</span
                            >{/if}
                        {#if form.role && !hasRoleSpecificData}
                            <span class="warning-text">
                                ⚠️ Este rol requiere información adicional.
                                Complete las secciones expandibles.
                            </span>
                        {/if}
                    </div>
                    <div class="form-group">
                        <label for="is_active">Estado</label>
                        <input
                            id="is_active"
                            type="checkbox"
                            checked={form.is_active}
                            on:change={(e) =>
                                updateForm(
                                    "is_active",
                                    (e.target as HTMLInputElement).checked,
                                )}
                        />
                        <span>Usuario activo</span>
                    </div>
                </div>
            </div>
            {#if visibleSections.professional}
                <div class="form-section">
                    <div class="section-header">
                        <h3>🧑‍💼 Datos Profesionales</h3>
                    </div>
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="professional_license"
                                >Licencia profesional *</label
                            >
                            <input
                                id="professional_license"
                                type="text"
                                bind:value={form.professional_license}
                                on:input={(e) => {
                                    const t =
                                        e.target as HTMLInputElement | null;
                                    updateForm(
                                        "professional_license",
                                        t ? t.value : "",
                                    );
                                }}
                                class:error={errors.professional_license}
                                placeholder="Ingrese la licencia profesional"
                                disabled={disabled ||
                                    !isFieldEditable("professional_license")}
                            />
                            {#if errors.professional_license}
                                <span class="error-text"
                                    >{errors.professional_license}</span
                                >
                            {/if}
                        </div>
                        <div class="form-group">
                            <label for="specialization">Especialización</label>
                            <input
                                id="specialization"
                                type="text"
                                bind:value={form.specialization}
                                on:input={(e) => {
                                    const t =
                                        e.target as HTMLInputElement | null;
                                    updateForm(
                                        "specialization",
                                        t ? t.value : "",
                                    );
                                }}
                                disabled={disabled ||
                                    !isFieldEditable("specialization")}
                            />
                        </div>
                        <div class="form-group">
                            <label for="experience_years"
                                >Años de experiencia</label
                            >
                            <input
                                id="experience_years"
                                type="number"
                                min="0"
                                bind:value={form.experience_years}
                                on:input={(e) => {
                                    const t =
                                        e.target as HTMLInputElement | null;
                                    updateForm(
                                        "experience_years",
                                        t ? t.value : "",
                                    );
                                }}
                                disabled={disabled ||
                                    !isFieldEditable("experience_years")}
                            />
                        </div>
                        <div class="form-group">
                            <label for="is_freelance">¿Freelance?</label>
                            <input
                                id="is_freelance"
                                type="checkbox"
                                checked={form.is_freelance}
                                on:change={(e) =>
                                    updateForm(
                                        "is_freelance",
                                        (e.target as HTMLInputElement).checked,
                                    )}
                            />
                        </div>
                        <div class="form-group">
                            <label for="hourly_rate">Tarifa por hora</label>
                            <input
                                id="hourly_rate"
                                type="number"
                                min="0"
                                bind:value={form.hourly_rate}
                                on:input={(e) => {
                                    const t =
                                        e.target as HTMLInputElement | null;
                                    updateForm("hourly_rate", t ? t.value : "");
                                }}
                                disabled={disabled ||
                                    !isFieldEditable("hourly_rate")}
                            />
                        </div>
                        <div class="form-group">
                            <label for="availability">Disponibilidad</label>
                            <input
                                id="availability"
                                type="text"
                                bind:value={form.availability}
                                on:input={(e) => {
                                    const t =
                                        e.target as HTMLInputElement | null;
                                    updateForm(
                                        "availability",
                                        t ? t.value : "",
                                    );
                                }}
                                disabled={disabled ||
                                    !isFieldEditable("availability")}
                            />
                        </div>
                        <div class="form-group">
                            <label for="is_verified">¿Verificado?</label>
                            <input
                                id="is_verified"
                                type="checkbox"
                                checked={form.is_verified}
                                on:change={(e) =>
                                    updateForm(
                                        "is_verified",
                                        (e.target as HTMLInputElement).checked,
                                    )}
                            />
                        </div>
                    </div>
                </div>
            {/if}
            {#if visibleSections.institution}
                <div class="form-section">
                    <div class="section-header">
                        <h3>🏢 Institución</h3>
                    </div>
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="institution_id">Institución</label>
                            <select
                                id="institution_id"
                                value={form.institution_id !== undefined &&
                                form.institution_id !== null
                                    ? String(form.institution_id)
                                    : ""}
                                on:change={(e) => {
                                    const t =
                                        e.target as HTMLSelectElement | null;
                                    const val =
                                        t && t.value
                                            ? t.value !== ""
                                                ? Number(t.value)
                                                : undefined
                                            : undefined;
                                    updateForm("institution_id", val);
                                }}
                                disabled={disabled ||
                                    !isFieldEditable("institution_id")}
                            >
                                {#if institutions.length === 0}
                                    <option value="">Sin datos</option>
                                {:else}
                                    <option value="">Sin institución</option>
                                    {#each institutions as inst}
                                        <option value={String(inst.id)}
                                            >{inst.name}</option
                                        >
                                    {/each}
                                {/if}
                            </select>
                            {#if institutionsLoadError}
                                <span class="warning-text"
                                    >No se pudieron cargar instituciones.</span
                                >
                            {/if}
                        </div>
                    </div>
                </div>
            {/if}
            <div class="form-actions">
                <!-- Debug info para el botón -->
                {#if !editMode}
                    <div class="button-debug">
                        <details>
                            <summary>🔍 Debug del botón</summary>
                            <div class="debug-content">
                                <h4>Estado de Validación:</h4>
                                <ul>
                                    <li>
                                        ✅ Nombre: {buttonDebug.firstNameValid
                                            ? "Válido"
                                            : "❌ Faltante"}
                                    </li>
                                    <li>
                                        ✅ Apellido: {buttonDebug.lastNameValid
                                            ? "Válido"
                                            : "❌ Faltante"}
                                    </li>
                                    <li>
                                        ✅ Email: {buttonDebug.emailValid
                                            ? "Válido"
                                            : "❌ Faltante"}
                                    </li>
                                    <li>
                                        ✅ Teléfono: {buttonDebug.phoneValid
                                            ? "Válido"
                                            : "❌ Faltante"}
                                    </li>
                                    <li>
                                        ✅ Rol: {buttonDebug.roleValid
                                            ? "Válido"
                                            : "❌ Faltante"}
                                    </li>
                                    <li>
                                        🔒 Contraseña: {buttonDebug.passwordValid
                                            ? "Válida"
                                            : "❌ Faltante"}
                                    </li>
                                    {#if !editMode}
                                        <li>
                                            🔐 Confirmación: {buttonDebug.passwordMatch
                                                ? "✅ Coincide"
                                                : "❌ No coincide"}
                                        </li>
                                    {/if}
                                </ul>

                                <h4>Estado Final:</h4>
                                <ul>
                                    <li>
                                        📋 Datos mínimos: {buttonDebug.hasMinimumData
                                            ? "✅ Completos"
                                            : "❌ Incompletos"}
                                    </li>
                                    <li>
                                        🎯 Datos específicos del rol: {buttonDebug.hasRoleSpecificData
                                            ? "✅ Completos"
                                            : "❌ Incompletos"}
                                    </li>
                                    <li>
                                        🚀 Botón habilitado: {buttonDebug.canUpdate
                                            ? "✅ Sí"
                                            : "❌ No"}
                                    </li>
                                </ul>

                                <h4>Valores Actuales:</h4>
                                <pre>{JSON.stringify(
                                        buttonDebug,
                                        null,
                                        2,
                                    )}</pre>
                            </div>
                        </details>
                    </div>
                {/if}

                <button
                    type="submit"
                    class="btn-primary"
                    disabled={disabled || submitting || !canUpdate}
                >
                    {#if submitting}
                        <span class="loading-spinner-small"></span>
                        {editMode ? "Actualizando..." : "Creando..."}
                    {:else}
                        {editMode ? "Actualizar" : "Crear Usuario"}
                    {/if}
                </button>
            </div>
            {#if error}
                <div class="error-banner">{error}</div>
            {/if}
        </form>
    {/if}
    {#if editMode && !form.role}
        <div class="warning-text">
            (Modo desarrollo) El usuario no tiene rol asignado. Todos los campos
            son editables.
        </div>
    {/if}
    {#if editMode && form.role === ""}
        <div class="error-text">
            Debe asignar un rol para guardar cambios en producción.
        </div>
    {/if}
    {#if debugResult}
        <details>
            <summary>DEBUG: Respuesta de la API</summary>
            <pre
                style="background: #f0f0f0; padding: 10px; border-radius: 4px; font-size: 12px; overflow: auto; max-height: 200px;">{JSON.stringify(
                    debugResult,
                    null,
                    2,
                )}</pre>
        </details>
    {/if}
    {#if showMissingFieldsModal}
        <ModalNotification
            type="error"
            message={missingFieldsMessage}
            subtitle={missingFields.length > 0
                ? `Campos faltantes: ${missingFields.join(", ")}`
                : ""}
            show={showMissingFieldsModal}
            on:close={() => (showMissingFieldsModal = false)}
        />
    {/if}
</div>

<style>
    .user-form-container {
        width: 100%;
        margin: 0 auto;
        padding: 0;
    }

    .user-form {
        background: var(--color-bg-card);
        border-radius: 16px;
        border: 1px solid var(--color-border);
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        width: 100%;
        box-sizing: border-box;
    }

    .form-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid var(--color-border);
        gap: 1rem;
    }

    .form-info h2 {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--color-text);
        margin: 0 0 0.5rem 0;
    }

    .form-info p {
        color: var(--color-text-secondary);
        font-size: 1rem;
        line-height: 1.5;
        margin: 0;
    }

    .expand-all-btn {
        background: var(--color-accent);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        white-space: nowrap;
    }

    .expand-all-btn:hover {
        background: var(--color-accent-dark);
        transform: translateY(-1px);
    }

    .form-section {
        background: var(--color-bg);
        border-radius: 12px;
        border: 1px solid var(--color-border);
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        box-sizing: border-box;
        width: 100%;
        transition: all 0.2s;
    }

    .form-section:hover {
        border-color: var(--color-accent);
        box-shadow: 0 2px 8px rgba(0, 230, 118, 0.1);
    }

    .form-section.required {
        border-left: 4px solid var(--color-accent);
    }

    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--color-border);
    }

    .section-header h3 {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--color-text);
        margin: 0;
    }

    .required-badge {
        background: var(--color-accent);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }

    .form-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        width: 100%;
        box-sizing: border-box;
    }

    .form-group {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-bottom: 1rem;
        width: 100%;
        min-width: 0;
        box-sizing: border-box;
    }

    .form-group label {
        font-weight: 600;
        color: var(--color-text);
        font-size: 0.95rem;
        margin-bottom: 0.25rem;
    }

    .form-group input,
    .form-group select,
    .form-group textarea {
        padding: 0.875rem;
        border: 2px solid var(--color-border);
        border-radius: 8px;
        background: var(--color-bg-card);
        color: var(--color-text);
        font-size: 1rem;
        transition: all 0.2s;
        width: 100%;
        min-width: 0;
        box-sizing: border-box;
    }

    .form-group input:focus,
    .form-group select:focus,
    .form-group textarea:focus {
        outline: none;
        border-color: var(--color-accent);
        box-shadow: 0 0 0 3px rgba(0, 230, 118, 0.15);
        background: var(--color-bg-hover);
        color: var(--color-text);
        transform: translateY(-1px);
    }

    .form-group input:disabled,
    .form-group select:disabled,
    .form-group textarea:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        background: var(--color-bg-disabled);
        color: var(--color-text-disabled);
    }

    .form-group input:disabled:focus,
    .form-group select:disabled:focus,
    .form-group textarea:disabled:focus {
        border-color: var(--color-border);
        box-shadow: none;
        transform: none;
    }

    .form-group input.error,
    .form-group select.error,
    .form-group textarea.error {
        border-color: var(--color-danger);
        box-shadow: 0 0 0 3px rgba(255, 77, 109, 0.15);
    }

    .error-text {
        color: var(--color-danger);
        font-size: 0.85rem;
        margin-top: 0.25rem;
        font-weight: 500;
    }

    .warning-text {
        color: #f59e0b;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        padding: 0.75rem;
        background: rgba(245, 158, 11, 0.1);
        border-radius: 8px;
        border-left: 4px solid #f59e0b;
    }

    .error-section {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-top: 0.5rem;
    }

    .retry-btn {
        background: var(--color-accent);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }

    .retry-btn:hover:not(:disabled) {
        background: var(--color-accent-dark);
        transform: translateY(-1px);
    }

    .retry-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .form-actions {
        display: flex;
        justify-content: flex-end;
        gap: 1rem;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 2px solid var(--color-border);
    }

    .form-actions .btn-primary {
        background: var(--color-accent);
        color: #fff;
        border: none;
        border-radius: 10px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(0, 230, 118, 0.3);
        min-width: 160px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .form-actions .btn-primary:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }

    .form-actions .btn-primary:hover:not(:disabled) {
        background: var(--color-accent-dark);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 230, 118, 0.4);
    }

    .form-actions .btn-primary:active:not(:disabled) {
        transform: translateY(0);
    }

    .loading-spinner-small {
        width: 16px;
        height: 16px;
        border: 2px solid transparent;
        border-top: 2px solid currentColor;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    .form-progress {
        margin-top: 1.5rem;
        padding: 1rem;
        background: rgba(0, 230, 118, 0.05);
        border-radius: 8px;
        border: 1px solid rgba(0, 230, 118, 0.2);
    }

    .progress-bar {
        width: 100%;
        height: 10px;
        background: var(--color-border);
        border-radius: 5px;
        overflow: hidden;
        margin-bottom: 0.75rem;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(
            90deg,
            var(--color-accent),
            var(--color-accent-dark)
        );
        transition: width 0.4s ease;
        border-radius: 5px;
    }

    .progress-text {
        font-size: 0.9rem;
        color: var(--color-text);
        font-weight: 600;
        text-align: center;
    }

    .error-banner {
        background: rgba(255, 77, 109, 0.1);
        color: var(--color-danger);
        border: 1px solid var(--color-danger);
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
        font-weight: 600;
        text-align: center;
    }

    .button-debug {
        margin-bottom: 1rem;
    }

    .button-debug details {
        background: rgba(0, 0, 0, 0.05);
        border-radius: 8px;
        padding: 0.5rem;
    }

    .button-debug summary {
        cursor: pointer;
        font-weight: 600;
        color: var(--color-text);
        padding: 0.5rem;
    }

    .button-debug pre {
        background: rgba(0, 0, 0, 0.1);
        padding: 1rem;
        border-radius: 6px;
        font-size: 0.8rem;
        overflow-x: auto;
        margin: 0.5rem 0 0 0;
    }

    .debug-content {
        padding: 1rem;
        background: rgba(0, 0, 0, 0.05);
        border-radius: 8px;
        margin-top: 0.5rem;
    }

    .debug-content h4 {
        margin: 0 0 0.5rem 0;
        color: var(--color-text);
        font-size: 0.9rem;
        font-weight: 600;
    }

    .debug-content ul {
        margin: 0 0 1rem 0;
        padding-left: 1.5rem;
    }

    .debug-content li {
        margin-bottom: 0.25rem;
        font-size: 0.85rem;
        color: var(--color-text);
    }

    /* Responsividad mejorada */
    @media (max-width: 1200px) {
        .user-form {
            padding: 1.5rem;
        }
    }

    @media (max-width: 900px) {
        .form-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .form-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 1rem;
        }

        .user-form {
            padding: 1.5rem;
        }
    }

    @media (max-width: 600px) {
        .form-section {
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .form-header {
            margin-bottom: 1.5rem;
        }

        .form-info h2 {
            font-size: 1.5rem;
        }

        .form-actions {
            flex-direction: column;
            gap: 0.75rem;
        }

        .form-actions .btn-primary {
            width: 100%;
            min-width: auto;
        }

        .user-form {
            padding: 1rem;
        }
    }

    @media (max-width: 480px) {
        .form-grid {
            gap: 0.75rem;
        }

        .form-group {
            margin-bottom: 0.75rem;
        }

        .form-group input,
        .form-group select,
        .form-group textarea {
            padding: 0.75rem;
            font-size: 0.95rem;
        }

        .user-form {
            padding: 0.75rem;
        }

        .form-section {
            padding: 0.75rem;
        }
    }
</style>
