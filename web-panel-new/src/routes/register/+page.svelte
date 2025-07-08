<script>
    import { goto } from "$app/navigation";
    let email = "";
    let password = "";
    let confirmPassword = "";
    let error = "";
    let loading = false;
    let success = false;

    async function handleSubmit(e) {
        e.preventDefault();
        if (!email || !password || !confirmPassword) {
            error = "Completa todos los campos";
            return;
        }
        if (password !== confirmPassword) {
            error = "Las contraseñas no coinciden";
            return;
        }
        error = "";
        loading = true;
        success = false;
        try {
            const res = await fetch("/api/v1/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });
            if (!res.ok) {
                let msg = "Error de registro";
                try {
                    const data = await res.json();
                    msg = data.detail || msg;
                } catch {}
                throw new Error(msg);
            }
            loading = false;
            success = true;
            setTimeout(() => goto("/login"), 1800);
        } catch (e) {
            error = e.message || "Error de registro";
            loading = false;
        }
    }
</script>

<div class="register-form-container">
    <form class="register-form" on:submit={handleSubmit} autocomplete="on">
        <h2 class="register-title">Registro</h2>
        {#if error}
            <div class="register-error">
                <span class="register-error-icon">❌</span>
                {error}
            </div>
        {/if}
        {#if success}
            <div class="register-success">
                <span class="register-success-icon">✅</span>
                ¡Registro exitoso! Redirigiendo al login...
            </div>
        {/if}
        <label>
            Email
            <input
                type="email"
                bind:value={email}
                placeholder="tu@email.com"
                required
                disabled={loading || success}
                autocomplete="username"
            />
        </label>
        <label>
            Contraseña
            <input
                type="password"
                bind:value={password}
                placeholder="Tu contraseña"
                required
                disabled={loading || success}
                autocomplete="new-password"
            />
        </label>
        <label>
            Confirmar contraseña
            <input
                type="password"
                bind:value={confirmPassword}
                placeholder="Repite tu contraseña"
                required
                disabled={loading || success}
                autocomplete="new-password"
            />
        </label>
        <button
            type="submit"
            class="register-btn"
            disabled={loading || success}
        >
            {#if loading}
                <span class="register-spinner">⏳</span> Registrando...
            {:else}
                <span class="register-btn-icon">📝</span> Registrarse
            {/if}
        </button>
        <div class="register-footer">
            ¿Ya tienes cuenta? <a href="/login">Inicia sesión aquí</a>
        </div>
    </form>
</div>

<style>
    .register-form-container {
        min-height: 60vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: none;
        padding: 2rem 0;
    }
    .register-form {
        background: var(--color-bg-card);
        border-radius: 16px;
        box-shadow: 0 2px 16px rgba(0, 0, 0, 0.18);
        padding: 2.5rem 2rem;
        min-width: 320px;
        max-width: 370px;
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        border: 1.5px solid var(--color-border);
    }
    .register-title {
        margin: 0 0 1rem 0;
        color: var(--color-accent);
        font-size: 1.5rem;
        text-align: center;
        font-weight: 700;
    }
    .register-error {
        background: rgba(255, 77, 109, 0.08);
        color: var(--color-danger);
        border: 1.5px solid var(--color-danger);
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-size: 1rem;
        text-align: center;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        justify-content: center;
    }
    .register-error-icon {
        font-size: 1.2rem;
    }
    label {
        display: flex;
        flex-direction: column;
        font-size: 1rem;
        color: var(--color-text-secondary);
        gap: 0.3rem;
    }
    input[type="email"],
    input[type="password"] {
        padding: 0.7rem;
        border: 1.5px solid var(--color-border);
        border-radius: 7px;
        font-size: 1rem;
        background: var(--color-bg);
        color: var(--color-text);
        transition: border 0.2s;
    }
    input[type="email"]:focus,
    input[type="password"]:focus {
        outline: none;
        border-color: var(--color-accent);
        background: var(--color-bg-card);
    }
    .register-btn {
        background: var(--color-accent);
        color: var(--color-bg-card);
        border: none;
        border-radius: 7px;
        padding: 0.8rem;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    .register-btn:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }
    .register-btn-icon {
        font-size: 1.2rem;
    }
    .register-spinner {
        font-size: 1.2rem;
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
    .register-footer {
        margin-top: 1.2rem;
        text-align: center;
        font-size: 0.98rem;
        color: var(--color-text-secondary);
    }
    .register-footer a {
        color: var(--color-accent);
        text-decoration: underline;
        font-weight: 500;
    }
    .register-success {
        background: rgba(77, 255, 109, 0.08);
        color: var(--color-success, #2ecc40);
        border: 1.5px solid var(--color-success, #2ecc40);
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-size: 1rem;
        text-align: center;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        justify-content: center;
        margin-bottom: 0.5rem;
    }
    .register-success-icon {
        font-size: 1.2rem;
    }
</style>
