<script lang="ts">
    import { getInstitutions } from "$lib/api/institutions";
    import { getRoles } from "$lib/api/roles";
    import { assignRole, updateUser } from "$lib/api/users";
    import PlusIcon from "$lib/ui/icons/PlusIcon.svelte";
    import { validateFullUser } from "$lib/validations/userValidations";
    import { createEventDispatcher, onMount } from "svelte";

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
    let debugResult = null;

    // Datos de referencia
    let roles: Role[] = [];
    let institutions: Institution[] = [];
    let rolesLoadError = false;
    let institutionsLoadError = false;

    // Inicialización robusta SOLO cuando cambia initialData y editMode
    let form = {
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
        institution_id: null,
        professional_license: "",
        specialization: "",
        experience_years: 0,
        is_freelance: false,
        hourly_rate: 0,
        availability: "",
        legal_representative_id: null,
        legal_capacity_verified: false,
        terms_accepted: false,
        is_verified: false,
    };

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

    onMount(async () => {
        try {
            roles = await getRoles();
            rolesLoadError = false;
        } catch (err) {
            roles = [];
            rolesLoadError = true;
        }
        try {
            institutions = await getInstitutions();
            institutionsLoadError = false;
        } catch (err) {
            institutions = [];
            institutionsLoadError = true;
        }
    });

    async function loadRoles() {
        try {
            roles = await getRoles();
        } catch (err) {
            error = "Error al cargar roles";
            console.error(err);
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
            return;
        }
        submitting = true;
        error = "";
        debugResult = {};
        let updateResult, assignResult;
        try {
            // Guardar usuario (sin el campo 'role')
            const userUpdateData = { ...form };
            delete userUpdateData.role;
            // Elimina password si está vacío
            if (!userUpdateData.password) delete userUpdateData.password;
            // Elimina date_of_birth si está vacío
            if (!userUpdateData.date_of_birth)
                delete userUpdateData.date_of_birth;
            updateResult = await updateUser(form.id, userUpdateData);
            debugResult.updateResult = updateResult;
            // Si el rol cambió y el usuario es admin, asignar rol
            if (
                editMode &&
                isFieldEditable("role") &&
                form.role &&
                form.role !== initialData.role
            ) {
                assignResult = await assignRole(form.id, form.role);
                debugResult.assignResult = assignResult;
            }
            dispatch("submit", { ...form, debugResult });
        } catch (err) {
            error =
                err instanceof Error
                    ? err.message
                    : "Error al procesar formulario";
        } finally {
            submitting = false;
        }
    }

    function updateForm(field: string, value: any) {
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
                            on:input={(e) =>
                                updateForm("first_name", e.target.value)}
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
                            on:input={(e) =>
                                updateForm("last_name", e.target.value)}
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
                            on:input={(e) =>
                                updateForm("email", e.target.value)}
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
                            on:input={(e) =>
                                updateForm("phone", e.target.value)}
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
                            bind:value={form.gender}
                            on:change={(e) =>
                                updateForm("gender", e.target.value)}
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
                            bind:value={form.date_of_birth}
                            on:input={(e) =>
                                updateForm("date_of_birth", e.target.value)}
                            disabled={!isFieldEditable("date_of_birth")}
                        />
                    </div>
                    <div class="form-group">
                        <label for="role">Rol *</label>
                        <select
                            id="role"
                            bind:value={form.role}
                            on:change={(e) =>
                                updateForm("role", e.target.value)}
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
                            on:input={(e) =>
                                updateForm(
                                    "professional_license",
                                    e.target.value,
                                )}
                            class:error={errors.professional_license}
                            placeholder="Ingrese la licencia profesional"
                            disabled={!isFieldEditable("professional_license")}
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
                            on:input={(e) =>
                                updateForm("specialization", e.target.value)}
                            disabled={!isFieldEditable("specialization")}
                        />
                    </div>
                    <div class="form-group">
                        <label for="experience_years">Años de experiencia</label
                        >
                        <input
                            id="experience_years"
                            type="number"
                            min="0"
                            bind:value={form.experience_years}
                            on:input={(e) =>
                                updateForm("experience_years", e.target.value)}
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
                            on:input={(e) =>
                                updateForm("hourly_rate", e.target.value)}
                            disabled={!isFieldEditable("hourly_rate")}
                        />
                    </div>
                    <div class="form-group">
                        <label for="availability">Disponibilidad</label>
                        <input
                            id="availability"
                            type="text"
                            bind:value={form.availability}
                            on:input={(e) =>
                                updateForm("availability", e.target.value)}
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
                    <div class="form-group">
                        <label for="institution_id">Institución</label>
                        <select
                            id="institution_id"
                            bind:value={form.institution_id}
                            on:change={(e) =>
                                updateForm("institution_id", e.target.value)}
                            disabled={!isFieldEditable("institution_id")}
                        >
                            {#if institutions.length === 0}
                                <option value="">Sin datos</option>
                            {:else}
                                <option value="">Sin institución</option>
                                {#each institutions as inst}
                                    <option value={inst.id}>{inst.name}</option>
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
            {#if error}
                <div class="error-message">
                    <span>{error}</span>
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
</div>

<style>
    .user-form-container {
        padding: var(--spacing-xl);
    }

    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: var(--spacing-xl);
        gap: var(--spacing-md);
    }

    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid var(--color-border);
        border-top: 4px solid var(--color-accent);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    .loading-spinner-small {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top: 2px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 8px;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    .error-message {
        background: var(--color-danger-bg);
        color: var(--color-danger);
        border: 1px solid var(--color-danger);
        padding: var(--spacing-md);
        border-radius: var(--border-radius);
        margin-bottom: var(--spacing-lg);
        font-weight: 500;
    }

    .form-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--spacing-xl);
        padding-bottom: var(--spacing-lg);
        border-bottom: 1px solid var(--color-border);
    }

    .form-info h2 {
        margin: 0 0 var(--spacing-sm) 0;
        color: var(--color-text);
        font-size: 1.5rem;
    }

    .form-info p {
        margin: 0;
        color: var(--color-text-muted);
        font-size: 0.9rem;
    }

    .expand-all-btn {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        background: var(--color-accent);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: var(--spacing-sm) var(--spacing-md);
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s;
    }

    .expand-all-btn:hover {
        background: var(--color-accent-dark);
    }

    .user-form {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-lg);
    }

    .form-section {
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        background: var(--color-bg-card);
        overflow: hidden;
    }

    .form-section.required {
        border-color: var(--color-accent);
        background: linear-gradient(
            135deg,
            var(--color-bg-card),
            rgba(0, 230, 118, 0.05)
        );
    }

    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--spacing-lg);
        background: var(--color-bg);
        border-bottom: 1px solid var(--color-border);
        cursor: pointer;
        transition: all 0.2s;
    }

    .section-header:hover {
        background: var(--color-bg-hover);
    }

    .section-header h3 {
        margin: 0;
        color: var(--color-text);
        font-size: 1.1rem;
        font-weight: 600;
    }

    .required-badge {
        background: var(--color-accent);
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
    }

    .expand-btn {
        background: none;
        border: none;
        cursor: pointer;
        padding: var(--spacing-sm);
        border-radius: var(--border-radius);
        color: var(--color-text-muted);
        transition: all 0.2s;
    }

    .expand-btn:hover {
        background: var(--color-bg-hover);
        color: var(--color-text);
    }

    .expand-btn.expanded {
        transform: rotate(45deg);
        color: var(--color-accent);
    }

    .form-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        padding: var(--spacing-lg);
    }

    .form-group {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-xs);
    }

    .form-group label {
        font-weight: 500;
        color: var(--color-text);
        font-size: 0.9rem;
    }

    .form-group input,
    .form-group select {
        padding: var(--spacing-sm);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        background: var(--color-bg);
        color: var(--color-text);
        font-size: 0.9rem;
        transition: all 0.2s;
    }

    .form-group input:focus,
    .form-group select:focus {
        outline: none;
        border-color: var(--color-accent);
        box-shadow: 0 0 0 2px rgba(0, 230, 118, 0.1);
    }

    .form-group input.error,
    .form-group select.error {
        border-color: var(--color-danger);
    }

    .error-text {
        color: var(--color-danger);
        font-size: 0.8rem;
        margin-top: 2px;
    }

    .checkbox-group {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
    }

    .checkbox-group input[type="checkbox"] {
        width: auto;
        margin: 0;
    }

    .checkbox-group label {
        margin: 0;
        cursor: pointer;
    }

    .form-actions {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: var(--spacing-lg);
        border-top: 1px solid var(--color-border);
    }

    .form-status {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
    }

    .status-valid {
        display: flex;
        align-items: center;
        gap: var(--spacing-xs);
        color: var(--color-success);
        font-weight: 500;
        font-size: 0.9rem;
    }

    .status-incomplete {
        color: var(--color-text-muted);
        font-size: 0.9rem;
    }

    .btn-primary {
        background: var(--color-accent);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: var(--spacing-md) var(--spacing-xl);
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 1rem;
        min-width: 200px;
    }

    .btn-primary:hover:not(:disabled) {
        background: var(--color-accent-dark);
    }

    .btn-primary:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .user-form {
        max-width: 900px;
        margin: 0 auto;
        padding: 0 1rem 1rem 1rem;
        overflow-y: auto;
        /* Elimina max-height para evitar recorte de campos */
    }
    .form-section {
        margin-bottom: 1.5rem;
        background: var(--color-bg-card);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-sm);
        padding: 1rem;
    }
    @media (max-width: 600px) {
        .user-form {
            max-width: 100vw;
            padding: 0 0.5rem 1rem 0.5rem;
            max-height: 90vh;
        }
        .form-grid {
            grid-template-columns: 1fr;
        }
    }
    .warning-text {
        color: var(--color-text-muted);
        font-size: 0.85rem;
        margin-top: 2px;
        display: block;
    }
    .debug-not-editable {
        border: 2px solid red !important;
        background: #ffeaea;
    }
</style>
