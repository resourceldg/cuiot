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
            await userService.changePassword('me', current, password);
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
.form-group {
    margin-bottom: 1.2rem;
}
.form-label {
    font-size: 0.98rem;
    color: #64748b;
    font-weight: 500;
    margin-bottom: 0.2rem;
    display: block;
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
.btn-primary {
    display: inline-block;
    padding: 0.5rem 1.2rem;
    border-radius: 0.5rem;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    cursor: pointer;
    background: #2563eb;
    color: #fff;
    transition: background 0.2s, color 0.2s;
}
.btn-primary:hover {
    background: #1e40af;
}
.flex {
    display: flex;
}
.justify-end {
    justify-content: flex-end;
}
.pt-6 {
    padding-top: 1.5rem;
}
.border-t {
    border-top: 1px solid #e5e7eb;
}
.space-x-4 > * + * {
    margin-left: 1rem;
}
.animate-spin {
    animation: spin 1s linear infinite;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
@media (max-width: 900px) {
    .card {
        padding: 1.2rem 0.7rem 1rem 0.7rem;
    }
}
</style>
