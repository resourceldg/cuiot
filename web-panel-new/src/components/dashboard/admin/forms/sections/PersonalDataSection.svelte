<script lang="ts">
    import type { UserFormData } from "$lib/validations/userValidations";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let formData: UserFormData;
    export let errors: Record<string, string> = {};
    export let disabled = false;

    function updateField(field: keyof UserFormData, value: any) {
        formData[field] = value;
        dispatch("update", { field, value });
    }

    function handleInput(field: keyof UserFormData) {
        return (e: Event) => {
            const target = e.target as HTMLInputElement;
            updateField(field, target.value);
        };
    }

    function handleSelect(field: keyof UserFormData) {
        return (e: Event) => {
            const target = e.target as HTMLSelectElement;
            updateField(field, target.value);
        };
    }
</script>

<div class="section">
    <div class="section-header">
        <h3>Datos Personales</h3>
        <p>Información básica del usuario</p>
    </div>

    <div class="form-grid">
        <div class="form-group">
            <label for="first_name">Nombre *</label>
            <input
                id="first_name"
                type="text"
                value={formData.first_name}
                on:input={handleInput("first_name")}
                class:error={errors.first_name}
                placeholder="Ingrese nombre"
                {disabled}
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
                value={formData.last_name}
                on:input={handleInput("last_name")}
                class:error={errors.last_name}
                placeholder="Ingrese apellido"
                {disabled}
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
                value={formData.email}
                on:input={(e) => updateField("email", e.target.value)}
                class:error={errors.email}
                placeholder="usuario@ejemplo.com"
                {disabled}
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
                on:input={(e) => updateField("phone", e.target.value)}
                class:error={errors.phone}
                placeholder="+54 11 1234-5678"
                {disabled}
            />
            {#if errors.phone}
                <span class="error-text">{errors.phone}</span>
            {/if}
        </div>

        <div class="form-group">
            <label for="date_of_birth">Fecha de Nacimiento</label>
            <input
                id="date_of_birth"
                type="date"
                value={formData.date_of_birth}
                on:input={(e) => updateField("date_of_birth", e.target.value)}
                class:error={errors.date_of_birth}
                {disabled}
            />
            {#if errors.date_of_birth}
                <span class="error-text">{errors.date_of_birth}</span>
            {/if}
        </div>

        <div class="form-group">
            <label for="gender">Género</label>
            <select
                id="gender"
                value={formData.gender}
                on:change={(e) => updateField("gender", e.target.value)}
                class:error={errors.gender}
                {disabled}
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

<style>
    .section {
        background: var(--color-bg);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        padding: var(--spacing-lg);
        margin-bottom: var(--spacing-lg);
    }

    .section-header {
        margin-bottom: var(--spacing-lg);
    }

    .section-header h3 {
        margin: 0 0 var(--spacing-xs) 0;
        color: var(--color-text);
        font-size: 1.2rem;
        font-weight: 600;
    }

    .section-header p {
        margin: 0;
        color: var(--color-text-muted);
        font-size: 0.9rem;
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

    .form-group label {
        font-weight: 500;
        color: var(--color-text);
        font-size: 0.9rem;
    }

    .form-group input,
    .form-group select {
        background: var(--color-bg);
        color: var(--color-text);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        font-size: 0.9rem;
        transition: all 0.2s;
    }

    .form-group input:focus,
    .form-group select:focus {
        background: var(--color-bg-hover);
        color: var(--color-text);
        border-color: var(--color-accent);
        box-shadow: 0 0 0 2px rgba(0, 230, 118, 0.1);
    }

    .form-group input.error,
    .form-group select.error {
        border-color: var(--color-danger);
    }

    .form-group input:disabled,
    .form-group select:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .error-text {
        color: var(--color-danger);
        font-size: 0.8rem;
        margin-top: 2px;
    }

    @media (max-width: 768px) {
        .section {
            padding: var(--spacing-md);
        }

        .form-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
