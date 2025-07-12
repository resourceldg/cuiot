<script lang="ts">
    import { getRoles } from "$lib/api/roles";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let loading = false;
    export let submitting = false;
    export let error = "";

    // Datos mínimos
    let form = {
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        password: "",
        confirm_password: "",
        role: "",
        is_active: true,
    };

    let roles: any[] = [];
    let errors: Record<string, string> = {};

    // Cargar roles al montar
    onMount(async () => {
        try {
            roles = await getRoles();
        } catch (err) {
            error = "Error al cargar roles";
        }
    });

    // Actualizar el campo role cuando los roles se cargan
    $: if (form && Array.isArray(form.roles)) {
        form.role = form.roles.length > 0 ? form.roles[0] : "";
    }

    function validateForm() {
        errors = {};

        if (!form.first_name.trim()) errors.first_name = "Nombre requerido";
        if (!form.last_name.trim()) errors.last_name = "Apellido requerido";
        if (!form.email.trim()) {
            errors.email = "Email requerido";
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
            errors.email = "Email inválido";
        }
        if (!form.phone.trim()) errors.phone = "Teléfono requerido";
        if (!form.password) {
            errors.password = "Contraseña requerida";
        } else if (form.password.length < 8) {
            errors.password = "Mínimo 8 caracteres";
        }
        if (form.password !== form.confirm_password) {
            errors.confirm_password = "Las contraseñas no coinciden";
        }
        if (!form.role) errors.role = "Rol requerido";

        return Object.keys(errors).length === 0;
    }

    function handleSubmit() {
        if (!validateForm()) return;
        dispatch("submit", form);
    }

    function updateField(field: string, value: any) {
        form[field] = value;
        form = { ...form };
    }
</script>

<div class="minimal-form">
    <div class="form-header">
        <h2>Crear Usuario - Datos Mínimos</h2>
        <p>Complete los campos esenciales para crear el usuario</p>
    </div>

    {#if error}
        <div class="error-banner">{error}</div>
    {/if}

    <form on:submit|preventDefault={handleSubmit}>
        <div class="form-grid">
            <div class="form-group">
                <label for="first_name">Nombre *</label>
                <input
                    id="first_name"
                    type="text"
                    bind:value={form.first_name}
                    class:error={errors.first_name}
                    placeholder="Ingrese nombre"
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
                    placeholder="Ingrese apellido"
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
                <label for="password">Contraseña *</label>
                <input
                    id="password"
                    type="password"
                    bind:value={form.password}
                    class:error={errors.password}
                    placeholder="Mínimo 8 caracteres"
                />
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

            <div class="form-group">
                <label for="role">Rol *</label>
                <select
                    id="role"
                    bind:value={form.role}
                    class:error={errors.role}
                >
                    <option value="">Seleccionar rol</option>
                    {#each roles as role}
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

        <div class="form-actions">
            <button
                type="button"
                class="btn-secondary"
                on:click={() => dispatch("cancel")}
            >
                Cancelar
            </button>
            <button type="submit" class="btn-primary" disabled={submitting}>
                {submitting ? "Creando..." : "Crear Usuario"}
            </button>
        </div>
    </form>
</div>

<style>
    .minimal-form {
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

    .form-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: var(--spacing-md);
        margin-bottom: var(--spacing-xl);
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
        background: var(--color-bg-hover);
        color: var(--color-text);
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
        justify-content: center;
        gap: var(--spacing-md);
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
        .minimal-form {
            padding: var(--spacing-md);
        }

        .form-grid {
            grid-template-columns: 1fr;
        }

        .form-actions {
            flex-direction: column;
        }

        .btn-primary,
        .btn-secondary {
            width: 100%;
        }
    }
</style>
