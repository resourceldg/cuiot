<script>
    import { goto } from "$app/navigation";
    import { authService } from "$lib/api.js";
    import { onMount } from "svelte";

    let formData = {
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        phone: "",
    };
    let loading = false;
    let error = "";
    let success = "";

    onMount(() => {
        // Redirigir si ya está autenticado
        if (authService.isAuthenticated()) {
            goto("/");
        }
    });

    async function handleRegister() {
        if (
            !formData.email ||
            !formData.password ||
            !formData.first_name ||
            !formData.last_name
        ) {
            error = "Por favor completa todos los campos requeridos";
            return;
        }

        if (formData.password.length < 6) {
            error = "La contraseña debe tener al menos 6 caracteres";
            return;
        }

        loading = true;
        error = "";
        success = "";

        try {
            await authService.register(formData);
            success = "¡Registro exitoso! Redirigiendo al login...";
            setTimeout(() => {
                goto("/login");
            }, 2000);
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
                error = "Error al registrar usuario";
            }
        } finally {
            loading = false;
        }
    }

    function handleKeyPress(event) {
        if (event.key === "Enter") {
            handleRegister();
        }
    }
</script>

<svelte:head>
    <title>Registro - Sistema Integral de Monitoreo</title>
</svelte:head>

<div class="register-container">
    <div class="register-card">
        <div class="register-header">
            <h1>👴 Registro</h1>
            <p>Crea tu cuenta</p>
        </div>

        <form on:submit|preventDefault={handleRegister} class="register-form">
            {#if error}
                <div class="error-message">
                    {error}
                </div>
            {/if}

            {#if success}
                <div class="success-message">
                    {success}
                </div>
            {/if}

            <div class="form-row">
                <div class="form-group">
                    <label for="first_name">Nombre *</label>
                    <input
                        type="text"
                        id="first_name"
                        bind:value={formData.first_name}
                        on:keypress={handleKeyPress}
                        placeholder="Tu nombre"
                        required
                        disabled={loading}
                    />
                </div>

                <div class="form-group">
                    <label for="last_name">Apellido *</label>
                    <input
                        type="text"
                        id="last_name"
                        bind:value={formData.last_name}
                        on:keypress={handleKeyPress}
                        placeholder="Tu apellido"
                        required
                        disabled={loading}
                    />
                </div>
            </div>

            <div class="form-group">
                <label for="email">Email *</label>
                <input
                    type="email"
                    id="email"
                    bind:value={formData.email}
                    on:keypress={handleKeyPress}
                    placeholder="tu@email.com"
                    required
                    disabled={loading}
                />
            </div>

            <div class="form-group">
                <label for="phone">Teléfono</label>
                <input
                    type="tel"
                    id="phone"
                    bind:value={formData.phone}
                    on:keypress={handleKeyPress}
                    placeholder="+34 123 456 789"
                    disabled={loading}
                />
            </div>

            <div class="form-group">
                <label for="password">Contraseña *</label>
                <input
                    type="password"
                    id="password"
                    bind:value={formData.password}
                    on:keypress={handleKeyPress}
                    placeholder="Mínimo 6 caracteres"
                    required
                    disabled={loading}
                />
            </div>

            <button type="submit" class="register-button" disabled={loading}>
                {#if loading}
                    Registrando...
                {:else}
                    Crear Cuenta
                {/if}
            </button>
        </form>

        <div class="register-footer">
            <p>¿Ya tienes cuenta? <a href="/login">Inicia sesión aquí</a></p>
        </div>
    </div>
</div>

<style>
    .register-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
    }

    .register-card {
        background: white;
        border-radius: 12px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04);
        padding: 2.5rem;
        width: 100%;
        max-width: 500px;
    }

    .register-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .register-header h1 {
        font-size: 1.875rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }

    .register-header p {
        color: #6b7280;
        font-size: 0.875rem;
    }

    .register-form {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
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

    .register-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem;
        border: none;
        border-radius: 0.375rem;
        font-weight: 500;
        cursor: pointer;
        transition: opacity 0.15s ease-in-out;
    }

    .register-button:hover:not(:disabled) {
        opacity: 0.9;
    }

    .register-button:disabled {
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

    .success-message {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #16a34a;
        padding: 0.75rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
    }

    .register-footer {
        text-align: center;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e5e7eb;
    }

    .register-footer p {
        color: #6b7280;
        font-size: 0.875rem;
    }

    .register-footer a {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
    }

    .register-footer a:hover {
        text-decoration: underline;
    }

    @media (max-width: 640px) {
        .form-row {
            grid-template-columns: 1fr;
        }
    }
</style>
