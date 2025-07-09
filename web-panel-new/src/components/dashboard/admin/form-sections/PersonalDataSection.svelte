<script lang="ts">
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let form: any;
    export let errors: Record<string, string> = {};

    function updateField(field: string, value: any) {
        dispatch("update", { field, value });
    }
</script>

<div class="form-section">
    <h3>📋 Datos Personales</h3>
    <div class="form-grid">
        <div class="form-group">
            <label for="first_name">Nombre *</label>
            <input
                id="first_name"
                type="text"
                value={form.first_name}
                on:input={(e) => updateField("first_name", e.target.value)}
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
                on:input={(e) => updateField("last_name", e.target.value)}
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
                on:input={(e) => updateField("email", e.target.value)}
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
                on:input={(e) => updateField("phone", e.target.value)}
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
                value={form.date_of_birth}
                on:input={(e) => updateField("date_of_birth", e.target.value)}
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
                value={form.gender}
                on:change={(e) => updateField("gender", e.target.value)}
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

<style>
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

    @media (max-width: 768px) {
        .form-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
