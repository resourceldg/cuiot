<script lang="ts">
    import { userService } from "$lib/api.js";
    import { createEventDispatcher, onMount } from "svelte";
    // Preferencias de notificación y accesibilidad
    export let preferences = {};
    export let loading = false;
    let userId = null;
    let feedback = { success: null, error: null };
    let open = false;

    const dispatch = createEventDispatcher();

    const defaultPreferences = {
        notifications: {
            email: true,
            sms: false,
            push: true,
        },
        privacy: {
            profile_visible: true,
            contact_visible: true,
            location_visible: false,
        },
        language: "es",
        timezone: "Europe/Madrid",
        theme: "light",
    };

    function normalizePreferences(prefs) {
        if (!prefs || typeof prefs !== "object")
            return { ...defaultPreferences };
        return {
            ...defaultPreferences,
            ...prefs,
            notifications: {
                ...defaultPreferences.notifications,
                ...(prefs.notifications || {}),
            },
            privacy: {
                ...defaultPreferences.privacy,
                ...(prefs.privacy || {}),
            },
        };
    }

    let formData = normalizePreferences(preferences);

    $: formData = normalizePreferences(preferences);

    onMount(() => {
        const token = localStorage.getItem("authToken");
        if (token) {
            try {
                const payload = JSON.parse(atob(token.split(".")[1]));
                userId = payload.sub ? parseInt(payload.sub) : null;
            } catch {}
        }
    });

    async function savePreferences() {
        feedback = { success: null, error: null };
        try {
            await userService.update('me', {
                availability: JSON.stringify(preferences),
            });
            feedback.success = "Preferencias guardadas correctamente.";
        } catch (e) {
            feedback.error = e.message || "Error al guardar preferencias.";
        }
    }

    function handleSubmit() {
        dispatch("submit", formData);
    }

    function handleReset() {
        formData = { ...defaultPreferences };
    }

    function toggle() { open = !open; }
</script>

<style>
.card {
    background: #fff;
    border-radius: 1rem;
    box-shadow: 0 2px 12px 0 rgba(37, 99, 235, 0.07);
    padding: 2rem 2rem 1.5rem 2rem;
    border: 1px solid #e5e7eb;
    max-width: 420px;
    margin: 0 auto 2rem auto;
}
.card-header {
    margin-bottom: 1.5rem;
}
.card-header h2 {
    font-size: 1.3rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.3rem;
}
.card-header p {
    color: #64748b;
    font-size: 0.98rem;
}
.space-y-6 > * + * {
    margin-top: 1.5rem;
}
.btn-primary, .btn-secondary {
    display: inline-block;
    padding: 0.5rem 1.2rem;
    border-radius: 0.5rem;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: background 0.2s, color 0.2s;
}
.btn-primary {
    background: #2563eb;
    color: #fff;
}
.btn-primary:hover {
    background: #1e40af;
}
.btn-secondary {
    background: #f1f5f9;
    color: #2563eb;
    border: 1px solid #e5e7eb;
}
.btn-secondary:hover {
    background: #e0e7ef;
    color: #1e40af;
}
.form-group {
    margin-bottom: 1.2rem;
}
.form-input {
    width: 100%;
    padding: 0.5rem 0.8rem;
    border-radius: 0.4rem;
    border: 1px solid #e5e7eb;
    font-size: 1rem;
    color: #222;
    background: #f8fafc;
    margin-top: 0.2rem;
}
@media (max-width: 900px) {
    .card {
        padding: 1.2rem 0.7rem 1rem 0.7rem;
    }
}
.accordion-btn {
    background: none;
    border: none;
    color: #2563eb;
    font-size: 1.5rem;
    font-weight: bold;
    cursor: pointer;
    padding: 0 0.5rem;
    border-radius: 0.3rem;
    transition: background 0.2s, color 0.2s;
}
.accordion-btn:hover {
    background: #f1f5f9;
    color: #1e40af;
}
</style>

<div class="card">
    <div class="card-header" on:click={toggle} style="cursor:pointer;display:flex;align-items:center;justify-content:space-between;">
        <h2>Preferencias</h2>
        <button class="accordion-btn" aria-expanded={open} aria-controls="prefs-content">{open ? '−' : '+'}</button>
    </div>
    {#if open}
    <div id="prefs-content">
        <form
            id="preferences-form"
            on:submit|preventDefault={handleSubmit}
            class="space-y-6"
        >
            <!-- Notificaciones -->
            <div class="section">
                <h3 class="section-title">Notificaciones</h3>
                <div class="space-y-4">
                    <div
                        class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                    >
                        <div>
                            <label class="text-sm font-medium text-gray-700"
                                >Notificaciones por Email</label
                            >
                            <p class="text-sm text-gray-500">
                                Recibe alertas importantes por correo electrónico
                            </p>
                        </div>
                        <label
                            class="relative inline-flex items-center cursor-pointer"
                        >
                            <input
                                type="checkbox"
                                bind:checked={formData.notifications.email}
                                class="form-checkbox"
                            />
                        </label>
                    </div>

                    <div
                        class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                    >
                        <div>
                            <label class="text-sm font-medium text-gray-700"
                                >Notificaciones SMS</label
                            >
                            <p class="text-sm text-gray-500">
                                Recibe alertas urgentes por mensaje de texto
                            </p>
                        </div>
                        <label
                            class="relative inline-flex items-center cursor-pointer"
                        >
                            <input
                                type="checkbox"
                                bind:checked={formData.notifications.sms}
                                class="form-checkbox"
                            />
                        </label>
                    </div>

                    <div
                        class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                    >
                        <div>
                            <label class="text-sm font-medium text-gray-700"
                                >Notificaciones Push</label
                            >
                            <p class="text-sm text-gray-500">
                                Recibe notificaciones en tiempo real en el navegador
                            </p>
                        </div>
                        <label
                            class="relative inline-flex items-center cursor-pointer"
                        >
                            <input
                                type="checkbox"
                                bind:checked={formData.notifications.push}
                                class="form-checkbox"
                            />
                        </label>
                    </div>
                </div>
            </div>

            <!-- Privacidad -->
            <div class="section">
                <h3 class="section-title">Privacidad</h3>
                <div class="space-y-4">
                    <div
                        class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                    >
                        <div>
                            <label class="text-sm font-medium text-gray-700"
                                >Perfil Visible</label
                            >
                            <p class="text-sm text-gray-500">
                                Permite que otros usuarios vean tu perfil
                                profesional
                            </p>
                        </div>
                        <label
                            class="relative inline-flex items-center cursor-pointer"
                        >
                            <input
                                type="checkbox"
                                bind:checked={formData.privacy.profile_visible}
                                class="form-checkbox"
                            />
                        </label>
                    </div>

                    <div
                        class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                    >
                        <div>
                            <label class="text-sm font-medium text-gray-700"
                                >Información de Contacto Visible</label
                            >
                            <p class="text-sm text-gray-500">
                                Permite que otros usuarios vean tu información de
                                contacto
                            </p>
                        </div>
                        <label
                            class="relative inline-flex items-center cursor-pointer"
                        >
                            <input
                                type="checkbox"
                                bind:checked={formData.privacy.contact_visible}
                                class="form-checkbox"
                            />
                        </label>
                    </div>

                    <div
                        class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                    >
                        <div>
                            <label class="text-sm font-medium text-gray-700"
                                >Ubicación Visible</label
                            >
                            <p class="text-sm text-gray-500">
                                Comparte tu ubicación con otros usuarios
                            </p>
                        </div>
                        <label
                            class="relative inline-flex items-center cursor-pointer"
                        >
                            <input
                                type="checkbox"
                                bind:checked={formData.privacy.location_visible}
                                class="form-checkbox"
                            />
                        </label>
                    </div>
                </div>
            </div>

            <!-- Configuración General -->
            <div class="section">
                <h3 class="section-title">Configuración General</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="form-group">
                        <label for="language" class="form-label">Idioma</label>
                        <select
                            id="language"
                            bind:value={formData.language}
                            class="form-select"
                        >
                            <option value="es">Español</option>
                            <option value="en">English</option>
                            <option value="ca">Català</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="timezone" class="form-label">Zona Horaria</label
                        >
                        <select
                            id="timezone"
                            bind:value={formData.timezone}
                            class="form-select"
                        >
                            <option value="Europe/Madrid">Madrid (GMT+1/+2)</option>
                            <option value="Europe/London">Londres (GMT+0/+1)</option
                            >
                            <option value="America/New_York"
                                >Nueva York (GMT-5/-4)</option
                            >
                            <option value="America/Los_Angeles"
                                >Los Ángeles (GMT-8/-7)</option
                            >
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="theme" class="form-label">Tema</label>
                        <select
                            id="theme"
                            bind:value={formData.theme}
                            class="form-select"
                        >
                            <option value="light">Claro</option>
                            <option value="dark">Oscuro</option>
                            <option value="auto">Automático</option>
                        </select>
                    </div>
                </div>
            </div>
            <slot />
        </form>
    </div>
    {/if}
</div>
