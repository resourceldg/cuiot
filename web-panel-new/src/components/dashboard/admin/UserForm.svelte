<script lang="ts">
    import { getInstitutions } from "$lib/api/institutions";
    import { getPackages } from "$lib/api/packages";
    import { getRoles } from "$lib/api/roles";
    import CheckIcon from "$lib/ui/icons/CheckIcon.svelte";
    import PlusIcon from "$lib/ui/icons/PlusIcon.svelte";
    import { createEventDispatcher, onMount } from "svelte";
    import InstitutionSection from "./form-sections/InstitutionSection.svelte";
    import LegalSection from "./form-sections/LegalSection.svelte";
    import PersonalDataSection from "./form-sections/PersonalDataSection.svelte";
    import ProfessionalSection from "./form-sections/ProfessionalSection.svelte";
    import ValidationSection from "./form-sections/ValidationSection.svelte";

    const dispatch = createEventDispatcher();

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

    // Datos de referencia
    let roles: Role[] = [];
    let institutions: Institution[] = [];
    let packages: Package[] = [];

    // Formulario
    let form = {
        // Datos básicos (mínimos necesarios)
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        password: "",
        confirm_password: "",
        role: "",
        is_active: true,

        // Datos adicionales (expandibles)
        date_of_birth: "",
        gender: "",
        institution_id: null as number | null,
        package_id: null as string | null,
        professional_license: "",
        specialization: "",
        experience_years: 0,
        is_freelance: false,
        hourly_rate: 0,
        availability: "",
        legal_representative_id: null as string | null,
        legal_capacity_verified: false,
        terms_accepted: false,
    };

    // Validaciones
    let errors: Record<string, string> = {};

    // Secciones expandibles
    let expandedSections = {
        personal: false,
        security: false,
        role: false,
        institution: false,
        professional: false,
        legal: false,
        validation: false,
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
        form.password &&
        form.role;

    onMount(async () => {
        await Promise.all([loadRoles(), loadInstitutions(), loadPackages()]);
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

    async function loadPackages() {
        try {
            packages = await getPackages();
        } catch (err) {
            error = "Error al cargar paquetes";
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

    function validateMinimumData(): boolean {
        errors = {};

        if (!form.first_name.trim()) errors.first_name = "Nombre es requerido";
        if (!form.last_name.trim()) errors.last_name = "Apellido es requerido";
        if (!form.email.trim()) {
            errors.email = "Email es requerido";
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
            errors.email = "Email inválido";
        }
        if (!form.phone.trim()) {
            errors.phone = "Teléfono es requerido";
        } else if (!/^\+?[\d\s\-\(\)]+$/.test(form.phone)) {
            errors.phone = "Teléfono inválido";
        }
        if (!form.password) {
            errors.password = "Contraseña es requerida";
        } else if (form.password.length < 8) {
            errors.password = "Contraseña debe tener al menos 8 caracteres";
        }
        if (form.password !== form.confirm_password) {
            errors.confirm_password = "Las contraseñas no coinciden";
        }
        if (!form.role) {
            errors.role = "Rol es requerido";
        }

        return Object.keys(errors).length === 0;
    }

    function validateFullForm(): boolean {
        if (!validateMinimumData()) return false;

        // Validaciones adicionales
        if (form.date_of_birth) {
            const age = calculateAge(form.date_of_birth);
            if (age < 18) {
                errors.date_of_birth = "Debe ser mayor de 18 años";
            }
        }

        if (isCaregiver) {
            if (!form.professional_license.trim()) {
                errors.professional_license =
                    "Licencia profesional es requerida para cuidadores";
            }
            if (form.experience_years < 0) {
                errors.experience_years =
                    "Años de experiencia no pueden ser negativos";
            }
            if (form.hourly_rate < 0) {
                errors.hourly_rate = "Tarifa por hora no puede ser negativa";
            }
        }

        if (requiresRepresentative && !form.legal_representative_id) {
            errors.legal_representative_id =
                "Representante legal es requerido para cuidado delegado";
        }

        if (!form.terms_accepted) {
            errors.terms_accepted = "Debe aceptar los términos y condiciones";
        }

        return Object.keys(errors).length === 0;
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

    function handleSubmit() {
        const isValid = expandedSections.validation
            ? validateFullForm()
            : validateMinimumData();

        if (!isValid) return;

        submitting = true;
        error = "";

        try {
            dispatch("submit", form);
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
    }
</script>

<div class="user-form-container">
    {#if loading}
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p>Cargando datos...</p>
        </div>
    {:else}
        {#if error}
            <div class="error-message">
                <span>{error}</span>
            </div>
        {/if}

        <div class="form-header">
            <div class="form-info">
                <h2>Crear Usuario</h2>
                <p>
                    Complete los datos mínimos requeridos o expanda las
                    secciones para información adicional
                </p>
            </div>
            <button class="expand-all-btn" on:click={expandAllSections}>
                <PlusIcon size={16} />
                Expandir Todo
            </button>
        </div>

        <form on:submit|preventDefault={handleSubmit} class="user-form">
            <!-- Datos Mínimos (siempre visibles) -->
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
                            value={form.first_name}
                            on:input={(e) =>
                                updateForm("first_name", e.target.value)}
                            class:error={errors.first_name}
                            placeholder="Ingrese el nombre"
                        />
                        {#if errors.first_name}
                            <span class="error-text">{errors.first_name}</span>
                        {/if}
                    </div>

                    <div class="form-group">
                        <label for="last_name">Apellido *</label>
                        <input
                            id="last_name"
                            type="text"
                            value={form.last_name}
                            on:input={(e) =>
                                updateForm("last_name", e.target.value)}
                            class:error={errors.last_name}
                            placeholder="Ingrese el apellido"
                        />
                        {#if errors.last_name}
                            <span class="error-text">{errors.last_name}</span>
                        {/if}
                    </div>

                    <div class="form-group">
                        <label for="email">Email *</label>
                        <input
                            id="email"
                            type="email"
                            value={form.email}
                            on:input={(e) =>
                                updateForm("email", e.target.value)}
                            class:error={errors.email}
                            placeholder="usuario@ejemplo.com"
                        />
                        {#if errors.email}
                            <span class="error-text">{errors.email}</span>
                        {/if}
                    </div>

                    <div class="form-group">
                        <label for="phone">Teléfono *</label>
                        <input
                            id="phone"
                            type="tel"
                            value={form.phone}
                            on:input={(e) =>
                                updateForm("phone", e.target.value)}
                            class:error={errors.phone}
                            placeholder="+54 11 1234-5678"
                        />
                        {#if errors.phone}
                            <span class="error-text">{errors.phone}</span>
                        {/if}
                    </div>

                    <div class="form-group">
                        <label for="password">Contraseña *</label>
                        <input
                            id="password"
                            type="password"
                            value={form.password}
                            on:input={(e) =>
                                updateForm("password", e.target.value)}
                            class:error={errors.password}
                            placeholder="Mínimo 8 caracteres"
                        />
                        {#if errors.password}
                            <span class="error-text">{errors.password}</span>
                        {/if}
                    </div>

                    <div class="form-group">
                        <label for="confirm_password"
                            >Confirmar Contraseña *</label
                        >
                        <input
                            id="confirm_password"
                            type="password"
                            value={form.confirm_password}
                            on:input={(e) =>
                                updateForm("confirm_password", e.target.value)}
                            class:error={errors.confirm_password}
                            placeholder="Repita la contraseña"
                        />
                        {#if errors.confirm_password}
                            <span class="error-text"
                                >{errors.confirm_password}</span
                            >
                        {/if}
                    </div>

                    <div class="form-group">
                        <label for="role">Rol *</label>
                        <select
                            id="role"
                            value={form.role}
                            on:change={(e) =>
                                updateForm("role", e.target.value)}
                            class:error={errors.role}
                        >
                            <option value="">Seleccionar rol</option>
                            {#each availableRoles as role}
                                <option value={role.name}>{role.name}</option>
                            {/each}
                        </select>
                        {#if errors.role}
                            <span class="error-text">{errors.role}</span>
                        {/if}
                    </div>

                    <div class="form-group">
                        <label for="is_active">Estado</label>
                        <div class="checkbox-group">
                            <input
                                id="is_active"
                                type="checkbox"
                                checked={form.is_active}
                                on:change={(e) =>
                                    updateForm("is_active", e.target.checked)}
                            />
                            <label for="is_active">Usuario activo</label>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Datos Personales Adicionales -->
            <div class="form-section expandable">
                <div
                    class="section-header"
                    on:click={() => toggleSection("personal")}
                >
                    <h3>👤 Datos Personales Adicionales</h3>
                    <button
                        type="button"
                        class="expand-btn"
                        class:expanded={expandedSections.personal}
                    >
                        <PlusIcon size={16} />
                    </button>
                </div>
                {#if expandedSections.personal}
                    <PersonalDataSection
                        {form}
                        {errors}
                        on:update={(e) =>
                            updateForm(e.detail.field, e.detail.value)}
                    />
                {/if}
            </div>

            <!-- Institución y Paquete -->
            <div class="form-section expandable">
                <div
                    class="section-header"
                    on:click={() => toggleSection("institution")}
                >
                    <h3>🏥 Institución y Paquete</h3>
                    <button
                        type="button"
                        class="expand-btn"
                        class:expanded={expandedSections.institution}
                    >
                        <PlusIcon size={16} />
                    </button>
                </div>
                {#if expandedSections.institution}
                    <InstitutionSection
                        {form}
                        {institutions}
                        {packages}
                        on:update={(e) =>
                            updateForm(e.detail.field, e.detail.value)}
                    />
                {/if}
            </div>

            <!-- Datos Profesionales (solo para cuidadores) -->
            {#if isCaregiver}
                <div class="form-section expandable">
                    <div
                        class="section-header"
                        on:click={() => toggleSection("professional")}
                    >
                        <h3>💼 Datos Profesionales</h3>
                        <button
                            type="button"
                            class="expand-btn"
                            class:expanded={expandedSections.professional}
                        >
                            <PlusIcon size={16} />
                        </button>
                    </div>
                    {#if expandedSections.professional}
                        <ProfessionalSection
                            {form}
                            {errors}
                            on:update={(e) =>
                                updateForm(e.detail.field, e.detail.value)}
                        />
                    {/if}
                </div>
            {/if}

            <!-- Representante Legal (solo para cuidado delegado) -->
            {#if requiresRepresentative}
                <div class="form-section expandable">
                    <div
                        class="section-header"
                        on:click={() => toggleSection("legal")}
                    >
                        <h3>⚖️ Representante Legal</h3>
                        <button
                            type="button"
                            class="expand-btn"
                            class:expanded={expandedSections.legal}
                        >
                            <PlusIcon size={16} />
                        </button>
                    </div>
                    {#if expandedSections.legal}
                        <LegalSection
                            {form}
                            {errors}
                            on:update={(e) =>
                                updateForm(e.detail.field, e.detail.value)}
                        />
                    {/if}
                </div>
            {/if}

            <!-- Validaciones -->
            <div class="form-section expandable">
                <div
                    class="section-header"
                    on:click={() => toggleSection("validation")}
                >
                    <h3>✅ Validaciones y Términos</h3>
                    <button
                        type="button"
                        class="expand-btn"
                        class:expanded={expandedSections.validation}
                    >
                        <PlusIcon size={16} />
                    </button>
                </div>
                {#if expandedSections.validation}
                    <ValidationSection
                        {form}
                        {errors}
                        on:update={(e) =>
                            updateForm(e.detail.field, e.detail.value)}
                    />
                {/if}
            </div>

            <!-- Botones -->
            <div class="form-actions">
                <div class="form-status">
                    {#if hasMinimumData}
                        <div class="status-valid">
                            <CheckIcon size={16} />
                            <span>Datos mínimos completos</span>
                        </div>
                    {:else}
                        <div class="status-incomplete">
                            <span>Complete los datos mínimos requeridos</span>
                        </div>
                    {/if}
                </div>
                <button
                    type="submit"
                    class="btn-primary"
                    disabled={submitting || !hasMinimumData}
                >
                    {submitting ? "Creando..." : "Crear Usuario"}
                </button>
            </div>
        </form>
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
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: var(--spacing-md);
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

    @media (max-width: 768px) {
        .user-form-container {
            padding: var(--spacing-md);
        }

        .form-header {
            flex-direction: column;
            align-items: stretch;
            gap: var(--spacing-md);
        }

        .form-grid {
            grid-template-columns: 1fr;
        }

        .form-actions {
            flex-direction: column;
            gap: var(--spacing-md);
        }

        .btn-primary {
            width: 100%;
        }
    }
</style>
