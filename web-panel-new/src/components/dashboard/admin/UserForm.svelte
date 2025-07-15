<script lang="ts">
    import { getInstitutions } from "$lib/api/institutions";
    import { getRoles } from "$lib/api/roles";
    import { assignRole, updateUser } from "$lib/api/users";
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
        institution: ["admin_institution", "institution_staff"].includes(
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

    // Validar datos mínimos
    $: hasMinimumData =
        form.first_name &&
        form.last_name &&
        form.email &&
        form.phone &&
        form.role;

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
    $: canUpdate =
        form.first_name &&
        form.last_name &&
        form.email &&
        form.phone &&
        (form.role || !editMode);

    let showMissingFieldsModal = false;
    let missingFields: string[] = [];
    let missingFieldsMessage = "";

    onMount(async () => {
        console.log("🔧 UserForm onMount - Cargando datos...");
        try {
            console.log("🔧 Cargando roles...");
            roles = await getRoles();
            console.log("✅ Roles cargados:", roles.length);
            rolesLoadError = false;
        } catch (err) {
            console.error("❌ Error cargando roles:", err);
            roles = [];
            rolesLoadError = true;
        }
        try {
            console.log("🔧 Cargando instituciones...");
            institutions = await getInstitutions();
            console.log("✅ Instituciones cargadas:", institutions.length);
            institutionsLoadError = false;
        } catch (err) {
            console.error("❌ Error cargando instituciones:", err);
            institutions = [];
            institutionsLoadError = true;
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

        submitting = true;
        error = "";
        debugResult = {};

        try {
            // Guardar usuario (sin el campo 'role')
            const userUpdateData = { ...form };
            delete (userUpdateData as any).role;
            if (!userUpdateData.password)
                delete (userUpdateData as any).password;
            if (!userUpdateData.date_of_birth)
                delete (userUpdateData as any).date_of_birth;

            const updateResult = await updateUser(form.id, userUpdateData);
            debugResult.updateResult = updateResult;

            if (updateResult.error) {
                if (updateResult.error.includes("401")) {
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
                } else if (updateResult.error.includes("403")) {
                    error = "No tienes permisos para editar este usuario.";
                    return;
                } else {
                    error = updateResult.error;
                    return;
                }
            }

            // Si el rol cambió y el usuario es admin, asignar rol
            if (
                editMode &&
                isFieldEditable("role") &&
                form.role &&
                form.role !== initialData.role
            ) {
                const assignResult = await assignRole(form.id, form.role);
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
        form[field] = value;
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
                </div>
                {#if !editMode}
                    <button class="expand-all-btn" on:click={expandAllSections}>
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
                            disabled={!isFieldEditable("last_name")}
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
                            disabled={!isFieldEditable("email")}
                        />
                        {#if errors.email}<span class="error-text"
                                >{errors.email}</span
                            >{/if}
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
                            disabled={!isFieldEditable("phone")}
                        />
                        {#if errors.phone}<span class="error-text"
                                >{errors.phone}</span
                            >{/if}
                    </div>
                    <div class="form-group">
                        <label for="gender">Género</label>
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
                            disabled={!isFieldEditable("gender")}
                        >
                            <option value="">Seleccionar</option>
                            <option value="femenino">Femenino</option>
                            <option value="masculino">Masculino</option>
                            <option value="otro">Otro</option>
                        </select>
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
                            disabled={!isFieldEditable("date_of_birth")}
                        />
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
                            disabled={!isFieldEditable("role")}
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
                            <span class="warning-text"
                                >No se pudieron cargar los roles.</span
                            >
                        {/if}
                        {#if errors.role}<span class="error-text"
                                >{errors.role}</span
                            >{/if}
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
                                disabled={!isFieldEditable(
                                    "professional_license",
                                )}
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
                                disabled={!isFieldEditable("specialization")}
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
                                disabled={!isFieldEditable("experience_years")}
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
                                disabled={!isFieldEditable("hourly_rate")}
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
                                disabled={!isFieldEditable("availability")}
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
                                disabled={!isFieldEditable("institution_id")}
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
            title="Datos obligatorios faltantes"
            on:close={() => (showMissingFieldsModal = false)}
        >
            <p>{missingFieldsMessage}</p>
            <ul>
                {#each missingFields as field}
                    <li>{field}</li>
                {/each}
            </ul>
            <button
                class="btn"
                on:click={() => (showMissingFieldsModal = false)}>Cerrar</button
            >
        </ModalNotification>
    {/if}
</div>

<style>
    .user-form-container {
        width: 100%;
        max-width: 100%;
    }
    .form-section {
        background: var(--color-bg);
        border-radius: var(--border-radius);
        border: 1px solid var(--color-accent);
        margin-bottom: var(--spacing-xl);
        padding: var(--spacing-lg);
        box-sizing: border-box;
        width: 100%;
        max-width: 100%;
    }
    .section-header {
        margin-bottom: var(--spacing-lg);
        padding-bottom: var(--spacing-sm);
        border-bottom: 1px solid var(--color-border);
    }
    .form-grid {
        display: grid;
        grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
        gap: var(--spacing-lg) var(--spacing-md);
        width: 100%;
        box-sizing: border-box;
    }
    .form-group {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-xs);
        margin-bottom: var(--spacing-md);
        width: 100%;
        min-width: 0;
        box-sizing: border-box;
    }
    .form-group label {
        font-weight: 500;
        color: var(--color-text);
        font-size: 0.95rem;
        margin-bottom: 0.2rem;
    }
    .form-group input,
    .form-group select {
        padding: var(--spacing-sm);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        background: var(--color-bg-card);
        color: var(--color-text);
        font-size: 0.95rem;
        transition: all 0.2s;
        width: 100%;
        min-width: 0;
        box-sizing: border-box;
    }
    .form-group input:focus,
    .form-group select:focus {
        outline: none;
        border-color: var(--color-accent);
        box-shadow: 0 0 0 2px rgba(0, 230, 118, 0.1);
        background: var(--color-bg-hover);
        color: var(--color-text);
    }
    .form-group input.error,
    .form-group select.error {
        border-color: var(--color-danger);
    }
    .error-text {
        color: var(--color-danger);
        font-size: 0.85rem;
        margin-top: 2px;
    }
    @media (max-width: 900px) {
        .form-grid {
            grid-template-columns: 1fr;
        }
    }
    @media (max-width: 600px) {
        .form-section {
            padding: var(--spacing-md);
        }
        .form-header {
            flex-direction: column;
            align-items: flex-start;
            gap: var(--spacing-md);
        }
    }
    .form-actions {
        display: flex;
        justify-content: flex-end;
        gap: var(--spacing-md);
        margin-top: var(--spacing-lg);
    }
    .form-actions .btn-primary {
        background: var(--color-accent);
        color: #fff;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.7rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.18s;
        box-shadow: 0 1.5px 6px rgba(0, 0, 0, 0.08);
    }
    .form-actions .btn-primary:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
    .form-actions .btn-primary:hover:not(:disabled) {
        background: var(--color-accent-dark, #00c060);
    }
</style>
