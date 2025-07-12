<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { onMount } from "svelte";
    import { getRoles } from "$lib/api/roles";
    import { getInstitutions } from "$lib/api/institutions";
    import { getPackages } from "$lib/api/packages";
    import { createUser, type UserCreateData } from "$lib/api/users";
    import SectionHeader from "../../shared/ui/SectionHeader.svelte";
    import UserIcon from "$lib/ui/icons/UserIcon.svelte";
    import XIcon from "$lib/ui/icons/XIcon.svelte";
    import CheckIcon from "$lib/ui/icons/CheckIcon.svelte";
    import AlertIcon from "$lib/ui/icons/AlertIcon.svelte";

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
    let success = "";

    // Datos de referencia
    let roles: Role[] = [];
    let institutions: Institution[] = [];
    let packages: Package[] = [];

    // Formulario
    let form = {
        // Datos básicos
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        password: "",
        confirm_password: "",
        date_of_birth: "",
        gender: "",
        
        // Rol y estado
        role: "",
        is_active: true,
        
        // Institución (opcional)
        institution_id: null as number | null,
        
        // Paquete (opcional)
        package_id: null as string | null,
        
        // Datos profesionales (solo para cuidadores)
        professional_license: "",
        specialization: "",
        experience_years: 0,
        is_freelance: false,
        hourly_rate: 0,
        availability: "",
        
        // Representante legal (solo para cuidado delegado)
        legal_representative_id: null as string | null,
        
        // Validaciones
        legal_capacity_verified: false,
        terms_accepted: false
    };

    // Validaciones
    let errors: Record<string, string> = {};
    let showPassword = false;

    // Filtros según rol seleccionado
    $: availableRoles = roles.filter(role => !role.is_system || role.name === 'sysadmin');
    $: isCaregiver = form.role === 'caregiver';
    $: isDelegatedCare = form.role === 'cared_person_delegated';
    $: requiresRepresentative = isDelegatedCare;

    onMount(async () => {
        await Promise.all([
            loadRoles(),
            loadInstitutions(),
            loadPackages()
        ]);
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

    function validateForm(): boolean {
        errors = {};

        // Validaciones básicas
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

        if (!form.date_of_birth) {
            errors.date_of_birth = "Fecha de nacimiento es requerida";
        } else {
            const age = calculateAge(form.date_of_birth);
            if (age < 18) {
                errors.date_of_birth = "Debe ser mayor de 18 años";
            }
        }

        if (!form.gender) {
            errors.gender = "Género es requerido";
        }

        if (!form.role) {
            errors.role = "Rol es requerido";
        }

        // Validaciones específicas por rol
        if (isCaregiver) {
            if (!form.professional_license.trim()) {
                errors.professional_license = "Licencia profesional es requerida para cuidadores";
            }
            if (form.experience_years < 0) {
                errors.experience_years = "Años de experiencia no pueden ser negativos";
            }
            if (form.hourly_rate < 0) {
                errors.hourly_rate = "Tarifa por hora no puede ser negativa";
            }
        }

        if (requiresRepresentative && !form.legal_representative_id) {
            errors.legal_representative_id = "Representante legal es requerido para cuidado delegado";
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
        
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
            age--;
        }
        
        return age;
    }

    async function handleSubmit() {
        if (!validateForm()) return;

        submitting = true;
        error = "";
        success = "";

        const userData: UserCreateData = {
            first_name: form.first_name,
            last_name: form.last_name,
            email: form.email,
            phone: form.phone,
            password: form.password,
            date_of_birth: form.date_of_birth,
            gender: form.gender,
            role: form.role,
            is_active: form.is_active,
            institution_id: form.institution_id,
            package_id: form.package_id,
            professional_license: form.professional_license,
            specialization: form.specialization,
            experience_years: form.experience_years,
            is_freelance: form.is_freelance,
            hourly_rate: form.hourly_rate,
            availability: form.availability,
            legal_representative_id: form.legal_representative_id,
            legal_capacity_verified: form.legal_capacity_verified
        };

        const { data, error: apiError } = await createUser(userData);
        if (apiError) {
            error = apiError;
            submitting = false;
            return;
        }
        success = "Usuario creado exitosamente";
        
        // Limpiar formulario
        resetForm();
        
        // Cerrar modal después de un delay
        setTimeout(() => {
            dispatch('userCreated');
            closeModal();
        }, 1500);
        submitting = false;
    }

    function resetForm() {
        form = {
            first_name: "",
            last_name: "",
            email: "",
            phone: "",
            password: "",
            confirm_password: "",
            date_of_birth: "",
            gender: "",
            role: "",
            is_active: true,
            institution_id: null,
            package_id: null,
            professional_license: "",
            specialization: "",
            experience_years: 0,
            is_freelance: false,
            hourly_rate: 0,
            availability: "",
            legal_representative_id: null,
            legal_capacity_verified: false,
            terms_accepted: false
        };
        errors = {};
    }

    function closeModal() {
        dispatch('close');
    }

    function togglePassword() {
        showPassword = !showPassword;
    }
</script>

<div class="modal-overlay" on:click={closeModal}>
    <div class="modal-content" on:click|stopPropagation>
        <div class="modal-header">
            <SectionHeader
                title="Crear Nuevo Usuario"
                subtitle="Registro completo de usuario en el sistema"
            >
                <span slot="icon">
                    <UserIcon size={24} />
                </span>
            </SectionHeader>
            <button class="close-btn" on:click={closeModal}>
                <XIcon size={20} />
            </button>
        </div>

        {#if loading}
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <p>Cargando datos...</p>
            </div>
        {:else}
            <div class="modal-body">
                {#if error}
                    <div class="error-message">
                        <AlertIcon size={16} />
                        <span>{error}</span>
                    </div>
                {/if}

                {#if success}
                    <div class="success-message">
                        <CheckIcon size={16} />
                        <span>{success}</span>
                    </div>
                {/if}

                <form on:submit|preventDefault={handleSubmit} class="user-form">
                    <!-- Datos Personales -->
                    <div class="form-section">
                        <h3>📋 Datos Personales</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="first_name">Nombre *</label>
                                <input
                                    id="first_name"
                                    type="text"
                                    bind:value={form.first_name}
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
                                    bind:value={form.last_name}
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
                                    bind:value={form.email}
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
                                    bind:value={form.phone}
                                    class:error={errors.phone}
                                    placeholder="+54 11 1234-5678"
                                />
                                {#if errors.phone}
                                    <span class="error-text">{errors.phone}</span>
                                {/if}
                            </div>

                            <div class="form-group">
                                <label for="date_of_birth">Fecha de Nacimiento *</label>
                                <input
                                    id="date_of_birth"
                                    type="date"
                                    bind:value={form.date_of_birth}
                                    class:error={errors.date_of_birth}
                                />
                                {#if errors.date_of_birth}
                                    <span class="error-text">{errors.date_of_birth}</span>
                                {/if}
                            </div>

                            <div class="form-group">
                                <label for="gender">Género *</label>
                                <select
                                    id="gender"
                                    bind:value={form.gender}
                                    class:error={errors.gender}
                                >
                                    <option value="">Seleccionar género</option>
                                    <option value="male">Masculino</option>
                                    <option value="female">Femenino</option>
                                    <option value="other">Otro</option>
                                    <option value="prefer_not_to_say">Prefiero no decir</option>
                                </select>
                                {#if errors.gender}
                                    <span class="error-text">{errors.gender}</span>
                                {/if}
                            </div>
                        </div>
                    </div>

                    <!-- Seguridad -->
                    <div class="form-section">
                        <h3>🔐 Seguridad</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="password">Contraseña *</label>
                                <div class="password-input">
                                    <input
                                        id="password"
                                        type={showPassword ? "text" : "password"}
                                        bind:value={form.password}
                                        class:error={errors.password}
                                        placeholder="Mínimo 8 caracteres"
                                    />
                                    <button type="button" class="password-toggle" on:click={togglePassword}>
                                        {showPassword ? "👁️" : "👁️‍🗨️"}
                                    </button>
                                </div>
                                {#if errors.password}
                                    <span class="error-text">{errors.password}</span>
                                {/if}
                            </div>

                            <div class="form-group">
                                <label for="confirm_password">Confirmar Contraseña *</label>
                                <input
                                    id="confirm_password"
                                    type="password"
                                    bind:value={form.confirm_password}
                                    class:error={errors.confirm_password}
                                    placeholder="Repita la contraseña"
                                />
                                {#if errors.confirm_password}
                                    <span class="error-text">{errors.confirm_password}</span>
                                {/if}
                            </div>
                        </div>
                    </div>

                    <!-- Rol y Estado -->
                    <div class="form-section">
                        <h3>👤 Rol y Estado</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="role">Rol *</label>
                                <select
                                    id="role"
                                    bind:value={form.role}
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
                                        bind:checked={form.is_active}
                                    />
                                    <label for="is_active">Usuario activo</label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Institución y Paquete -->
                    <div class="form-section">
                        <h3>🏥 Institución y Paquete</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="institution">Institución</label>
                                <select
                                    id="institution"
                                    bind:value={form.institution_id}
                                >
                                    <option value={null}>Sin institución</option>
                                    {#each institutions as institution}
                                        <option value={institution.id}>{institution.name}</option>
                                    {/each}
                                </select>
                            </div>

                            <div class="form-group">
                                <label for="package">Paquete</label>
                                <select
                                    id="package"
                                    bind:value={form.package_id}
                                >
                                    <option value={null}>Sin paquete</option>
                                    {#each packages as package}
                                        <option value={package.id}>{package.name} - ${package.price_monthly}/mes</option>
                                    {/each}
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Datos Profesionales (solo para cuidadores) -->
                    {#if isCaregiver}
                        <div class="form-section">
                            <h3>💼 Datos Profesionales</h3>
                            <div class="form-grid">
                                <div class="form-group">
                                    <label for="professional_license">Licencia Profesional *</label>
                                    <input
                                        id="professional_license"
                                        type="text"
                                        bind:value={form.professional_license}
                                        class:error={errors.professional_license}
                                        placeholder="Número de licencia"
                                    />
                                    {#if errors.professional_license}
                                        <span class="error-text">{errors.professional_license}</span>
                                    {/if}
                                </div>

                                <div class="form-group">
                                    <label for="specialization">Especialización</label>
                                    <input
                                        id="specialization"
                                        type="text"
                                        bind:value={form.specialization}
                                        placeholder="Ej: Geriatría, Pediatría"
                                    />
                                </div>

                                <div class="form-group">
                                    <label for="experience_years">Años de Experiencia</label>
                                    <input
                                        id="experience_years"
                                        type="number"
                                        bind:value={form.experience_years}
                                        class:error={errors.experience_years}
                                        min="0"
                                        max="50"
                                    />
                                    {#if errors.experience_years}
                                        <span class="error-text">{errors.experience_years}</span>
                                    {/if}
                                </div>

                                <div class="form-group">
                                    <label for="hourly_rate">Tarifa por Hora (ARS)</label>
                                    <input
                                        id="hourly_rate"
                                        type="number"
                                        bind:value={form.hourly_rate}
                                        class:error={errors.hourly_rate}
                                        min="0"
                                        step="100"
                                    />
                                    {#if errors.hourly_rate}
                                        <span class="error-text">{errors.hourly_rate}</span>
                                    {/if}
                                </div>

                                <div class="form-group">
                                    <label for="is_freelance">Tipo de Trabajo</label>
                                    <div class="checkbox-group">
                                        <input
                                            id="is_freelance"
                                            type="checkbox"
                                            bind:checked={form.is_freelance}
                                        />
                                        <label for="is_freelance">Freelance/Independiente</label>
                                    </div>
                                </div>

                                <div class="form-group full-width">
                                    <label for="availability">Disponibilidad</label>
                                    <textarea
                                        id="availability"
                                        bind:value={form.availability}
                                        placeholder="Horarios disponibles, días de trabajo, etc."
                                        rows="3"
                                    ></textarea>
                                </div>
                            </div>
                        </div>
                    {/if}

                    <!-- Representante Legal (solo para cuidado delegado) -->
                    {#if requiresRepresentative}
                        <div class="form-section">
                            <h3>⚖️ Representante Legal</h3>
                            <div class="form-group">
                                <label for="legal_representative">Representante Legal *</label>
                                <select
                                    id="legal_representative"
                                    bind:value={form.legal_representative_id}
                                    class:error={errors.legal_representative_id}
                                >
                                    <option value="">Seleccionar representante legal</option>
                                    <!-- Aquí se cargarían los usuarios familiares disponibles -->
                                    <option value="temp_id">Usuario Familiar (ejemplo)</option>
                                </select>
                                {#if errors.legal_representative_id}
                                    <span class="error-text">{errors.legal_representative_id}</span>
                                {/if}
                                <small class="help-text">
                                    Las personas bajo cuidado delegado deben tener un representante legal vinculado.
                                </small>
                            </div>
                        </div>
                    {/if}

                    <!-- Validaciones -->
                    <div class="form-section">
                        <h3>✅ Validaciones</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <div class="checkbox-group">
                                    <input
                                        id="legal_capacity_verified"
                                        type="checkbox"
                                        bind:checked={form.legal_capacity_verified}
                                    />
                                    <label for="legal_capacity_verified">Capacidad legal verificada</label>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="checkbox-group">
                                    <input
                                        id="terms_accepted"
                                        type="checkbox"
                                        bind:checked={form.terms_accepted}
                                        class:error={errors.terms_accepted}
                                    />
                                    <label for="terms_accepted">Acepto los términos y condiciones *</label>
                                </div>
                                {#if errors.terms_accepted}
                                    <span class="error-text">{errors.terms_accepted}</span>
                                {/if}
                            </div>
                        </div>
                    </div>

                    <!-- Botones -->
                    <div class="form-actions">
                        <button type="button" class="btn-secondary" on:click={closeModal}>
                            Cancelar
                        </button>
                        <button type="submit" class="btn-primary" disabled={submitting}>
                            {submitting ? "Creando..." : "Crear Usuario"}
                        </button>
                    </div>
                </form>
            </div>
        {/if}
    </div>
</div>

<style>
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        padding: var(--spacing-md);
    }

    .modal-content {
        background: var(--color-bg);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-xl);
        max-width: 800px;
        width: 100%;
        max-height: 90vh;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--spacing-lg);
        border-bottom: 1px solid var(--color-border);
        background: var(--color-bg-card);
    }

    .close-btn {
        background: none;
        border: none;
        cursor: pointer;
        padding: var(--spacing-sm);
        border-radius: var(--border-radius);
        color: var(--color-text-muted);
        transition: all 0.2s;
    }

    .close-btn:hover {
        background: var(--color-bg-hover);
        color: var(--color-text);
    }

    .modal-body {
        padding: var(--spacing-lg);
        overflow-y: auto;
        flex: 1;
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
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .error-message,
    .success-message {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        padding: var(--spacing-md);
        border-radius: var(--border-radius);
        margin-bottom: var(--spacing-lg);
        font-weight: 500;
    }

    .error-message {
        background: var(--color-danger-bg);
        color: var(--color-danger);
        border: 1px solid var(--color-danger);
    }

    .success-message {
        background: var(--color-success-bg);
        color: var(--color-success);
        border: 1px solid var(--color-success);
    }

    .user-form {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-xl);
    }

    .form-section {
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        padding: var(--spacing-lg);
        background: var(--color-bg-card);
    }

    .form-section h3 {
        margin: 0 0 var(--spacing-md) 0;
        color: var(--color-text);
        font-size: 1.1rem;
        font-weight: 600;
    }

    .form-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: var(--spacing-md);
    }

    .form-group {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-xs);
    }

    .form-group.full-width {
        grid-column: 1 / -1;
    }

    .form-group label {
        font-weight: 500;
        color: var(--color-text);
        font-size: 0.9rem;
    }

    .form-group input,
    .form-group select,
    .form-group textarea {
        padding: var(--spacing-sm);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        background: var(--color-bg);
        color: var(--color-text);
        font-size: 0.9rem;
        transition: all 0.2s;
    }

    .form-group input:focus,
    .form-group select:focus,
    .form-group textarea:focus {
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

    .help-text {
        color: var(--color-text-muted);
        font-size: 0.8rem;
        margin-top: 4px;
    }

    .password-input {
        position: relative;
        display: flex;
        align-items: center;
    }

    .password-toggle {
        position: absolute;
        right: var(--spacing-sm);
        background: none;
        border: none;
        cursor: pointer;
        padding: 4px;
        border-radius: var(--border-radius);
        color: var(--color-text-muted);
    }

    .password-toggle:hover {
        background: var(--color-bg-hover);
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
        justify-content: flex-end;
        gap: var(--spacing-md);
        padding-top: var(--spacing-lg);
        border-top: 1px solid var(--color-border);
    }

    .btn-primary,
    .btn-secondary {
        padding: var(--spacing-sm) var(--spacing-lg);
        border: none;
        border-radius: var(--border-radius);
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 0.9rem;
    }

    .btn-primary {
        background: var(--color-accent);
        color: white;
    }

    .btn-primary:hover:not(:disabled) {
        background: var(--color-accent-dark);
    }

    .btn-primary:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .btn-secondary {
        background: var(--color-bg-hover);
        color: var(--color-text);
        border: 1px solid var(--color-border);
    }

    .btn-secondary:hover {
        background: var(--color-border);
    }

    @media (max-width: 768px) {
        .modal-content {
            margin: var(--spacing-md);
            max-height: calc(100vh - 2 * var(--spacing-md));
        }

        .form-grid {
            grid-template-columns: 1fr;
        }

        .form-actions {
            flex-direction: column-reverse;
        }

        .btn-primary,
        .btn-secondary {
            width: 100%;
        }
    }
</style> 