<script lang="ts">
    import { userService } from "$lib/api.js";
    import { createEventDispatcher, onMount } from "svelte";
    let current = "";
    let password = "";
    let confirm = "";
    let loading = false;
    let error = null;
    let success = null;
    let userId = null;
    const dispatch = createEventDispatcher();

    function validate() {
        if (!password || password.length < 8)
            return "La contraseña debe tener al menos 8 caracteres.";
        if (password !== confirm) return "Las contraseñas no coinciden.";
        return null;
    }

    onMount(() => {
        const token = localStorage.getItem("authToken");
        if (token) {
            try {
                const payload = JSON.parse(atob(token.split(".")[1]));
                userId = payload.sub ? parseInt(payload.sub) : null;
            } catch {}
        }
    });

    async function handleChange() {
        error = null;
        success = null;
        const validation = validate();
        if (validation) {
            error = validation;
            return;
        }
        loading = true;
        try {
            if (!userId) throw new Error("No se pudo obtener el ID de usuario");
            await userService.changePassword(userId, current, password);
            success = "Contraseña cambiada correctamente.";
            current = password = confirm = "";
        } catch (e) {
            error = e.message || "Error al cambiar la contraseña.";
        } finally {
            loading = false;
        }
    }
</script>

<div class="card">
    <div class="card-header">
        <h2 class="text-2xl font-bold text-gray-800">Cambiar Contraseña</h2>
        <p class="text-gray-600 mt-1">
            Actualiza tu contraseña para mantener tu cuenta segura
        </p>
    </div>

    <form on:submit|preventDefault={handleChange} class="space-y-6">
        <div class="section">
            <div class="grid grid-cols-1 gap-6">
                <!-- Contraseña Actual -->
                <div class="form-group">
                    <label for="current_password" class="form-label"
                        >Contraseña Actual *</label
                    >
                    <div class="relative">
                        <input
                            id="current_password"
                            type="password"
                            bind:value={current}
                            class="form-input pr-12"
                            required
                            placeholder="Tu contraseña actual"
                        />
                        <button
                            type="button"
                            class="absolute inset-y-0 right-0 pr-3 flex items-center"
                        >
                            <svg
                                class="h-5 w-5 text-gray-400"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                                ></path>
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                                ></path>
                            </svg>
                        </button>
                    </div>
                </div>

                <!-- Nueva Contraseña -->
                <div class="form-group">
                    <label for="new_password" class="form-label"
                        >Nueva Contraseña *</label
                    >
                    <div class="relative">
                        <input
                            id="new_password"
                            type="password"
                            bind:value={password}
                            class="form-input pr-12"
                            required
                            placeholder="Mínimo 8 caracteres"
                        />
                        <button
                            type="button"
                            class="absolute inset-y-0 right-0 pr-3 flex items-center"
                        >
                            <svg
                                class="h-5 w-5 text-gray-400"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                                ></path>
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                                ></path>
                            </svg>
                        </button>
                    </div>
                    <p class="form-help">
                        La contraseña debe tener al menos 8 caracteres
                    </p>
                </div>

                <!-- Confirmar Nueva Contraseña -->
                <div class="form-group">
                    <label for="confirm_password" class="form-label"
                        >Confirmar Nueva Contraseña *</label
                    >
                    <div class="relative">
                        <input
                            id="confirm_password"
                            type="password"
                            bind:value={confirm}
                            class="form-input pr-12"
                            required
                            placeholder="Repite la nueva contraseña"
                        />
                        <button
                            type="button"
                            class="absolute inset-y-0 right-0 pr-3 flex items-center"
                        >
                            <svg
                                class="h-5 w-5 text-gray-400"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                                ></path>
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                                ></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Acciones -->
        <div class="flex justify-end space-x-4 pt-6 border-t border-gray-200">
            <button type="submit" class="btn-primary" disabled={loading}>
                {#if loading}
                    <div
                        class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"
                    ></div>
                {/if}
                Cambiar Contraseña
            </button>
        </div>
    </form>
</div>

<style>
    .btn {
        @apply px-4 py-2 rounded font-semibold;
    }
    .btn-primary {
        @apply bg-blue-500 text-white hover:bg-green-500 transition;
    }
    .input {
        @apply border rounded px-3 py-2;
    }
    .input-bordered {
        @apply border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200;
    }
</style>
