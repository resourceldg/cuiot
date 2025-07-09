<script lang="ts">
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let password = "";
    export let confirmPassword = "";
    export let errors: Record<string, string> = {};
    export let disabled = false;

    function updatePassword(value: string) {
        password = value;
        dispatch("update", { field: "password", value });
    }

    function updateConfirmPassword(value: string) {
        confirmPassword = value;
        dispatch("update", { field: "confirm_password", value });
    }
</script>

<div class="section">
    <div class="section-header">
        <h3>Seguridad</h3>
        <p>Configuración de contraseña</p>
    </div>

    <div class="form-grid">
        <div class="form-group">
            <label for="password">Contraseña *</label>
            <input
                id="password"
                type="password"
                value={password}
                on:input={(e) => updatePassword(e.target.value)}
                class:error={errors.password}
                placeholder="Mínimo 8 caracteres"
                {disabled}
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
                value={confirmPassword}
                on:input={(e) => updateConfirmPassword(e.target.value)}
                class:error={errors.confirm_password}
                placeholder="Repita la contraseña"
                {disabled}
            />
            {#if errors.confirm_password}
                <span class="error-text">{errors.confirm_password}</span>
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

    .form-group input {
        padding: var(--spacing-sm);
        background: var(--color-bg);
        color: var(--color-text);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        font-size: 0.9rem;
        transition: all 0.2s;
    }

    .form-group input:focus {
        outline: none;
        background: var(--color-bg-hover);
        color: var(--color-text);
        border-color: var(--color-accent);
        box-shadow: 0 0 0 2px rgba(0, 230, 118, 0.1);
    }

    .form-group input.error {
        border-color: var(--color-danger);
    }

    .form-group input:disabled {
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
