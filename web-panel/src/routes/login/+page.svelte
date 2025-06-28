<script>
    import { goto } from "$app/navigation";
    import { authService, authStore } from "$lib/api.js";
    import { onMount } from "svelte";

    let email = "";
    let password = "";
    let loading = false;
    let error = "";

    onMount(() => {
        // Redirigir si ya está autenticado
        if (authService.isAuthenticated()) {
            goto("/");
        }
    });

    async function handleLogin() {
        if (!email || !password) {
            error = "Por favor completa todos los campos";
            return;
        }

        loading = true;
        error = "";

        try {
            await authService.login(email, password);
            authStore.update((state) => ({
                ...state,
                isAuthenticated: true,
            }));
            goto("/");
        } catch (err) {
            // Manejo de errores legibles
            if (err && typeof err.message === "object" && err.message.detail) {
                if (Array.isArray(err.message.detail)) {
                    error = err.message.detail.map((e) => e.msg).join(" | ");
                } else {
                    error = err.message.detail;
                }
            } else if (typeof err.message === "string") {
                error = err.message;
            } else {
                error = "Error al iniciar sesión";
            }
        } finally {
            loading = false;
        }
    }

    function handleKeyPress(event) {
        if (event.key === "Enter") {
            handleLogin();
        }
    }
</script>

<svelte:head>
    <title>Login - Viejos Son Los Trapos</title>
</svelte:head>

<div class="login-container">
    <div class="login-card">
        <div class="login-header">
            <h1>👴 Viejos Son Los Trapos</h1>
            <p>Inicia sesión en tu cuenta</p>
        </div>

        <form on:submit|preventDefault={handleLogin} class="login-form">
            {#if error}
                <div class="error-message">
                    {error}
                </div>
            {/if}

            <div class="form-group">
                <label for="email">Email</label>
                <input
                    type="email"
                    id="email"
                    bind:value={email}
                    on:keypress={handleKeyPress}
                    placeholder="tu@email.com"
                    required
                    disabled={loading}
                />
            </div>

            <div class="form-group">
                <label for="password">Contraseña</label>
                <input
                    type="password"
                    id="password"
                    bind:value={password}
                    on:keypress={handleKeyPress}
                    placeholder="Tu contraseña"
                    required
                    disabled={loading}
                />
            </div>

            <button type="submit" class="login-button" disabled={loading}>
                {#if loading}
                    Iniciando sesión...
                {:else}
                    Iniciar Sesión
                {/if}
            </button>
        </form>

        <div class="login-footer">
            <p>¿No tienes cuenta? <a href="/register">Regístrate aquí</a></p>
        </div>
    </div>
</div>

<style>
    .login-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
    }

    .login-card {
        background: white;
        border-radius: 12px;
        box-shadow:
            0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04);
        padding: 2.5rem;
        width: 100%;
        max-width: 400px;
    }

    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .login-header h1 {
        font-size: 1.875rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }

    .login-header p {
        color: #6b7280;
        font-size: 0.875rem;
    }

    .login-form {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .form-group {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .form-group label {
        font-weight: 500;
        color: #374151;
        font-size: 0.875rem;
    }

    .form-group input {
        padding: 0.75rem;
        border: 1px solid #d1d5db;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        transition: border-color 0.15s ease-in-out;
    }

    .form-group input:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    .form-group input:disabled {
        background-color: #f9fafb;
        cursor: not-allowed;
    }

    .login-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem;
        border: none;
        border-radius: 0.375rem;
        font-weight: 500;
        cursor: pointer;
        transition: opacity 0.15s ease-in-out;
    }

    .login-button:hover:not(:disabled) {
        opacity: 0.9;
    }

    .login-button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .error-message {
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        color: #dc2626;
        padding: 0.75rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
    }

    .login-footer {
        text-align: center;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e5e7eb;
    }

    .login-footer p {
        color: #6b7280;
        font-size: 0.875rem;
    }

    .login-footer a {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
    }

    .login-footer a:hover {
        text-decoration: underline;
    }
</style>
