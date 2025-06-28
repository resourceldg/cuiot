<script>
    import { goto } from "$app/navigation";
    import { authService, authStore } from "$lib/api.js";
    import { Activity, Heart, Shield } from "lucide-svelte";
    import { onMount } from "svelte";

    let email = "";
    let password = "";
    let loading = false;
    let error = "";

    onMount(() => {
        // Redirigir si ya está autenticado
        if (authService.isAuthenticated()) {
            goto("/dashboard");
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
            goto("/dashboard");
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

    function goToHome() {
        goto("/");
    }
</script>

<svelte:head>
    <title>Iniciar Sesión - CUIOT</title>
</svelte:head>

<div class="login-container">
    <div class="login-background">
        <div class="login-overlay"></div>
    </div>

    <div class="login-content">
        <div class="login-card">
            <div class="login-header">
                <button on:click={goToHome} class="back-button">
                    ← Volver al inicio
                </button>

                <div class="brand-section">
                    <div class="brand-icon">
                        <Shield class="w-8 h-8" />
                    </div>
                    <h1>CUIOT</h1>
                    <p class="brand-subtitle">Tecnologías para el Cuidado</p>
                </div>

                <p class="login-subtitle">Inicia sesión en tu cuenta</p>
            </div>

            <form on:submit|preventDefault={handleLogin} class="login-form">
                {#if error}
                    <div class="error-message">
                        <Activity class="w-4 h-4" />
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
                        <div class="loading-spinner"></div>
                        Iniciando sesión...
                    {:else}
                        <Heart class="w-4 h-4" />
                        Iniciar Sesión
                    {/if}
                </button>
            </form>

            <div class="login-footer">
                <p>
                    ¿No tienes cuenta? <a href="/register">Regístrate aquí</a>
                </p>
                <p class="demo-info">
                    <Shield class="w-4 h-4 inline" />
                    Plataforma segura para el cuidado de personas
                </p>
            </div>
        </div>
    </div>
</div>

<style>
    .login-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(
            135deg,
            #1e3a8a 0%,
            #3b82f6 50%,
            #1e40af 100%
        );
        padding: 1rem;
        position: relative;
    }

    .login-background {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: radial-gradient(
                circle at 20% 80%,
                rgba(120, 119, 198, 0.3) 0%,
                transparent 50%
            ),
            radial-gradient(
                circle at 80% 20%,
                rgba(255, 119, 198, 0.3) 0%,
                transparent 50%
            );
    }

    .login-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.1);
    }

    .login-content {
        position: relative;
        z-index: 10;
        width: 100%;
        max-width: 450px;
    }

    .login-card {
        background: white;
        border-radius: 16px;
        box-shadow:
            0 25px 50px -12px rgba(0, 0, 0, 0.25),
            0 0 0 1px rgba(255, 255, 255, 0.1);
        padding: 2.5rem;
        backdrop-filter: blur(10px);
    }

    .back-button {
        background: none;
        border: none;
        color: #6b7280;
        font-size: 0.875rem;
        cursor: pointer;
        padding: 0.5rem 0;
        margin-bottom: 1rem;
        transition: color 0.2s;
    }

    .back-button:hover {
        color: #374151;
    }

    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .brand-section {
        margin-bottom: 1.5rem;
    }

    .brand-icon {
        width: 64px;
        height: 64px;
        background: linear-gradient(135deg, #3b82f6, #1e40af);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        color: white;
    }

    .brand-section h1 {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1f2937;
        margin: 0;
        letter-spacing: -0.025em;
    }

    .brand-subtitle {
        color: #6b7280;
        font-size: 1rem;
        font-weight: 500;
        margin: 0.25rem 0 0 0;
    }

    .login-subtitle {
        color: #6b7280;
        font-size: 0.875rem;
        margin: 0;
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
        font-weight: 600;
        color: #374151;
        font-size: 0.875rem;
    }

    .form-group input {
        padding: 0.875rem;
        border: 2px solid #e5e7eb;
        border-radius: 0.75rem;
        font-size: 0.875rem;
        transition: all 0.2s ease-in-out;
        background: #f9fafb;
    }

    .form-group input:focus {
        outline: none;
        border-color: #3b82f6;
        background: white;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }

    .form-group input:disabled {
        background-color: #f3f4f6;
        cursor: not-allowed;
        opacity: 0.7;
    }

    .login-button {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        padding: 0.875rem;
        border: none;
        border-radius: 0.75rem;
        font-weight: 600;
        font-size: 0.875rem;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
    }

    .login-button:hover:not(:disabled) {
        transform: translateY(-1px);
        box-shadow: 0 8px 15px -3px rgba(59, 130, 246, 0.3);
    }

    .login-button:disabled {
        opacity: 0.7;
        cursor: not-allowed;
        transform: none;
    }

    .loading-spinner {
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top: 2px solid white;
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
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #dc2626;
        padding: 0.875rem;
        border-radius: 0.75rem;
        font-size: 0.875rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .login-footer {
        margin-top: 2rem;
        text-align: center;
    }

    .login-footer p {
        color: #6b7280;
        font-size: 0.875rem;
        margin: 0.5rem 0;
    }

    .login-footer a {
        color: #3b82f6;
        text-decoration: none;
        font-weight: 500;
    }

    .login-footer a:hover {
        text-decoration: underline;
    }

    .demo-info {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        color: #9ca3af;
        font-size: 0.75rem;
        margin-top: 1rem;
    }

    @media (max-width: 640px) {
        .login-card {
            padding: 2rem;
        }

        .brand-section h1 {
            font-size: 2rem;
        }
    }
</style>
