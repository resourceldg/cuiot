<script lang="ts">
    import { getInstitutions } from "$lib/api/institutions";
    import { getPackages } from "$lib/api/packages";
    import { getRoles } from "$lib/api/roles";
    import { UserUseCases } from "$lib/useCases/userUseCases";
    import type { UserFormData } from "$lib/validations/userValidations";
    import {
        validateFullUser,
        validateMinimalUser,
    } from "$lib/validations/userValidations";
    import { onMount } from "svelte";

    export let currentUserRole = "sysadmin";
    export let onSubmit: (user: any) => void = () => {};
    export let onCancel: () => void = () => {};

    // Estado del formulario
    let formData: UserFormData = {
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        password: "",
        confirm_password: "",
        role: "",
        date_of_birth: "",
        gender: "",
        institution_id: null,
        package_id: null,
        professional_license: "",
        experience_years: undefined,
        hourly_rate: undefined,
        legal_representative_id: null,
        terms_accepted: false,
        is_active: true,
    };

    let errors: Record<string, string> = {};
    let loading = false;
    let submitting = false;
    let error = "";

    // Datos de referencia
    let roles: any[] = [];
    let institutions: any[] = [];
    let packages: any[] = [];
    let availableRoles: string[] = [];

    // Estado de secciones
    let expandedSections = {
        personal: true,
        security: true,
        role: true,
        professional: false,
        legal: false,
    };

    onMount(async () => {
        loading = true;
        try {
            // Cargar datos de referencia
            [roles, institutions, packages] = await Promise.all([
                getRoles(),
                getInstitutions(),
                getPackages(),
            ]);

            // Obtener roles disponibles según usuario actual
            availableRoles = UserUseCases.getAvailableRoles(currentUserRole);
        } catch (err) {
            error = "Error al cargar datos de referencia";
        } finally {
            loading = false;
        }
    });

    function updateField(field: keyof UserFormData, value: any) {
        formData[field] = value;
        formData = { ...formData };

        // Validar en tiempo real
        validateForm();
    }

    function validateForm() {
        // Validar según secciones expandidas
        if (
            expandedSections.personal &&
            expandedSections.security &&
            expandedSections.role
        ) {
            errors = validateMinimalUser(formData);
        } else {
            errors = validateFullUser(formData);
        }
    }

    async function handleSubmit() {
        validateForm();

        if (Object.keys(errors).length > 0) {
            return;
        }

        submitting = true;
        try {
            const user = await UserUseCases.createFullUser(
                formData,
                currentUserRole,
            );
            onSubmit(user);
        } catch (err: any) {
            error = err.message || "Error al crear usuario";
        } finally {
            submitting = false;
        }
    }

    function toggleSection(section: keyof typeof expandedSections) {
        expandedSections[section] = !expandedSections[section];
        expandedSections = { ...expandedSections };
    }

    function expandAll() {
        expandedSections = {
            personal: true,
            security: true,
            role: true,
            professional: true,
            legal: true,
        };
    }

    function collapseAll() {
        expandedSections = {
            personal: true,
            security: true,
            role: true,
            professional: false,
            legal: false,
        };
    }
</script>

<div class="simplified-form">
    <div class="form-header">
        <h2>Crear Usuario</h2>
        <p>Complete la información del nuevo usuario</p>
    </div>

    {#if error}
        <div class="error-banner">{error}</div>
    {/if}

    {#if loading}
        <div class="loading">Cargando datos...</div>
    {:else}
        <form on:submit|preventDefault={handleSubmit}>
            <!-- Datos Personales -->
            <div class="section">
                <div
                    class="section-toggle"
                    on:click={() => toggleSection("personal")}
                >
                    <h3>Datos Personales</h3>
                    <span class="toggle-icon"
                        >{expandedSections.personal ? "−" : "+"}</span
                    >
                </div>

                {#if expandedSections.personal}
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="first_name">Nombre *</label>
                            <input
                                id="first_name"
                                type="text"
                                value={formData.first_name}
                                on:input={(e) =>
                                    updateField("first_name", e.target.value)}
                                class:error={errors.first_name}
                                placeholder="Ingrese nombre"
                            />
                            {#if errors.first_name}
                                <span class="error-text"
                                    >{errors.first_name}</span
                                >
                            {/if}
                        </div>

                        <div class="form-group">
                            <label for="last_name">Apellido *</label>
                            <input
                                id="last_name"
                                type="text"
                                value={formData.last_name}
                                on:input={(e) =>
                                    updateField("last_name", e.target.value)}
                                class:error={errors.last_name}
                                placeholder="Ingrese apellido"
                            />
                            {#if errors.last_name}
                                <span class="error-text"
                                    >{errors.last_name}</span
                                >
                            {/if}
                        </div>

                        <div class="form-group">
                            <label for="email">Email *</label>
                            <input
                                id="email"
                                type="email"
                                value={formData.email}
                                on:input={(e) =>
                                    updateField("email", e.target.value)}
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
                                value={formData.phone}
                                on:input={(e) =>
                                    updateField("phone", e.target.value)}
                                class:error={errors.phone}
                                placeholder="+54 11 1234-5678"
                            />
                            {#if errors.phone}
                                <span class="error-text">{errors.phone}</span>
                            {/if}
                        </div>
                    </div>
                {/if}
            </div>

            <!-- Seguridad -->
            <div class="section">
                <div
                    class="section-toggle"
                    on:click={() => toggleSection("security")}
                >
                    <h3>Seguridad</h3>
                    <span class="toggle-icon"
                        >{expandedSections.security ? "−" : "+"}</span
                    >
                </div>

                {#if expandedSections.security}
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="password">Contraseña *</label>
                            <input
                                id="password"
                                type="password"
                                value={formData.password}
                                on:input={(e) =>
                                    updateField("password", e.target.value)}
                                class:error={errors.password}
                                placeholder="Mínimo 8 caracteres"
                            />
                            {#if errors.password}
                                <span class="error-text">{errors.password}</span
                                >
                            {/if}
                        </div>

                        <div class="form-group">
                            <label for="confirm_password"
                                >Confirmar Contraseña *</label
                            >
                            <input
                                id="confirm_password"
                                type="password"
                                value={formData.confirm_password}
                                on:input={(e) =>
                                    updateField(
                                        "confirm_password",
                                        e.target.value,
                                    )}
                                class:error={errors.confirm_password}
                                placeholder="Repita la contraseña"
                            />
                            {#if errors.confirm_password}
                                <span class="error-text"
                                    >{errors.confirm_password}</span
                                >
                            {/if}
                        </div>
                    </div>
                {/if}
            </div>

            <!-- Rol y Estado -->
            <div class="section">
                <div
                    class="section-toggle"
                    on:click={() => toggleSection("role")}
                >
                    <h3>Rol y Estado</h3>
                    <span class="toggle-icon"
                        >{expandedSections.role ? "−" : "+"}</span
                    >
                </div>

                {#if expandedSections.role}
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="role">Rol *</label>
                            <select
                                id="role"
                                value={formData.role}
                                on:change={(e) =>
                                    updateField("role", e.target.value)}
                                class:error={errors.role}
                            >
                                <option value="">Seleccionar rol</option>
                                {#each availableRoles as roleName}
                                    <option value={roleName}>{roleName}</option>
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
                                    checked={formData.is_active}
                                    on:change={(e) =>
                                        updateField(
                                            "is_active",
                                            e.target.checked,
                                        )}
                                />
                                <label for="is_active">Usuario activo</label>
                            </div>
                        </div>
                    </div>
                {/if}
            </div>

            <!-- Controles de secciones -->
            <div class="section-controls">
                <button
                    type="button"
                    class="btn-secondary"
                    on:click={expandAll}
                >
                    Expandir Todo
                </button>
                <button
                    type="button"
                    class="btn-secondary"
                    on:click={collapseAll}
                >
                    Colapsar Todo
                </button>
            </div>

            <!-- Acciones del formulario -->
            <div class="form-actions">
                <button type="button" class="btn-secondary" on:click={onCancel}>
                    Cancelar
                </button>
                <button type="submit" class="btn-primary" disabled={submitting}>
                    {submitting ? "Creando..." : "Crear Usuario"}
                </button>
            </div>
        </form>
    {/if}
</div>

<style>
    .simplified-form {
        max-width: 800px;
        margin: 0 auto;
        padding: var(--spacing-lg);
    }

    .form-header {
        text-align: center;
        margin-bottom: var(--spacing-xl);
    }

    .form-header h2 {
        margin: 0 0 var(--spacing-sm) 0;
        color: var(--color-text);
        font-size: 1.5rem;
    }

    .form-header p {
        margin: 0;
        color: var(--color-text-muted);
    }

    .error-banner {
        background: var(--color-danger-bg);
        color: var(--color-danger);
        padding: var(--spacing-md);
        border-radius: var(--border-radius);
        margin-bottom: var(--spacing-lg);
        text-align: center;
    }

    .loading {
        text-align: center;
        padding: var(--spacing-xl);
        color: var(--color-text-muted);
    }

    .section {
        background: var(--color-bg);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        margin-bottom: var(--spacing-md);
        overflow: hidden;
    }

    .section-toggle {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--spacing-md);
        background: var(--color-bg-hover);
        cursor: pointer;
        transition: background 0.2s;
    }

    .section-toggle:hover {
        background: var(--color-border);
    }

    .section-toggle h3 {
        margin: 0;
        color: var(--color-text);
        font-size: 1.1rem;
        font-weight: 600;
    }

    .toggle-icon {
        font-size: 1.2rem;
        font-weight: bold;
        color: var(--color-text-muted);
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

    .section-controls {
        display: flex;
        justify-content: center;
        gap: var(--spacing-md);
        margin: var(--spacing-lg) 0;
    }

    .form-actions {
        display: flex;
        justify-content: center;
        gap: var(--spacing-md);
        margin-top: var(--spacing-xl);
    }

    .btn-primary,
    .btn-secondary {
        padding: var(--spacing-sm) var(--spacing-xl);
        border: none;
        border-radius: var(--border-radius);
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 1rem;
        min-width: 120px;
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
        .simplified-form {
            padding: var(--spacing-md);
        }

        .form-grid {
            grid-template-columns: 1fr;
            padding: var(--spacing-md);
        }

        .section-controls,
        .form-actions {
            flex-direction: column;
        }

        .btn-primary,
        .btn-secondary {
            width: 100%;
        }
    }
</style>
