<script lang="ts">
    import { userService } from "$lib/api.js";
    import { createEventDispatcher, onMount } from "svelte";
    // Preferencias de notificación y accesibilidad
    export let preferences = {};
    export let loading = false;
    let userId = null;
    let feedback = { success: null, error: null };

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
            if (!userId) throw new Error("No se pudo obtener el ID de usuario");
            await userService.update(userId, {
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
</script>

<div class="card">
    <div class="flex justify-between items-center mb-4">
        <button
            type="button"
            on:click={handleReset}
            class="btn-secondary"
            disabled={loading}
        >
            Restablecer
        </button>
        <button
            type="submit"
            form="preferences-form"
            class="btn-primary"
            disabled={loading}
        >
            Guardar Preferencias
        </button>
    </div>
    <div class="card-header">
        <h2 class="text-2xl font-bold text-gray-800">Preferencias</h2>
        <p class="text-gray-600 mt-1">
            Personaliza tu experiencia en la plataforma
        </p>
    </div>

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
    </form>
</div>
