<script lang="ts">
    import { createEventDispatcher } from "svelte";
    export let user = {};
    export let show = false;
    export let loading = false;
    const dispatch = createEventDispatcher();

    let formData = {
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        date_of_birth: "",
        specialization: "",
        years_experience: "",
        certifications: "",
    };

    $: if (user && show) {
        formData = {
            first_name: user.first_name || "",
            last_name: user.last_name || "",
            email: user.email || "",
            phone: user.phone || "",
            date_of_birth: user.date_of_birth
                ? user.date_of_birth.split("T")[0]
                : "",
            specialization: user.specialization || "",
            years_experience: user.years_experience || "",
            certifications: user.certifications || "",
        };
    }

    function handleSubmit() {
        dispatch("submit", formData);
    }

    function handleClose() {
        dispatch("close");
    }

    function handleDelete() {
        dispatch("delete");
    }

    function handleBackdropClick(event) {
        if (event.target === event.currentTarget) {
            handleClose();
        }
    }
</script>

{#if show}
    <div
        class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 p-4"
        on:click={handleBackdropClick}
    >
        <div
            class="bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto p-8"
        >
            <div class="mb-6">
                <h2 class="text-2xl font-bold text-gray-900 mb-1">
                    Editar Perfil
                </h2>
                <p class="text-gray-500 text-sm">
                    Actualiza tu información personal y profesional
                </p>
            </div>

            <form on:submit|preventDefault={handleSubmit} class="space-y-8">
                <!-- Información Personal -->
                <div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">
                        Información Personal
                    </h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label
                                class="block text-xs text-gray-500 mb-1"
                                for="first_name"
                            >
                                Nombre *
                            </label>
                            <input
                                id="first_name"
                                type="text"
                                bind:value={formData.first_name}
                                class="form-input"
                                required
                            />
                        </div>

                        <div>
                            <label
                                class="block text-xs text-gray-500 mb-1"
                                for="last_name"
                            >
                                Apellido *
                            </label>
                            <input
                                id="last_name"
                                type="text"
                                bind:value={formData.last_name}
                                class="form-input"
                                required
                            />
                        </div>

                        <div>
                            <label
                                class="block text-xs text-gray-500 mb-1"
                                for="email"
                            >
                                Email *
                            </label>
                            <input
                                id="email"
                                type="email"
                                bind:value={formData.email}
                                class="form-input"
                                required
                            />
                        </div>

                        <div>
                            <label
                                class="block text-xs text-gray-500 mb-1"
                                for="phone"
                            >
                                Teléfono
                            </label>
                            <input
                                id="phone"
                                type="tel"
                                bind:value={formData.phone}
                                class="form-input"
                            />
                        </div>

                        <div>
                            <label
                                class="block text-xs text-gray-500 mb-1"
                                for="date_of_birth"
                            >
                                Fecha de Nacimiento
                            </label>
                            <input
                                id="date_of_birth"
                                type="date"
                                bind:value={formData.date_of_birth}
                                class="form-input"
                            />
                        </div>
                    </div>
                </div>

                <!-- Información Profesional -->
                <div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">
                        Información Profesional
                    </h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label
                                class="block text-xs text-gray-500 mb-1"
                                for="specialization"
                            >
                                Especialidad
                            </label>
                            <select
                                id="specialization"
                                bind:value={formData.specialization}
                                class="form-select"
                            >
                                <option value=""
                                    >Selecciona una especialidad</option
                                >
                                <option value="Cuidado de ancianos"
                                    >Cuidado de ancianos</option
                                >
                                <option value="Enfermería geriátrica"
                                    >Enfermería geriátrica</option
                                >
                                <option value="Fisioterapia"
                                    >Fisioterapia</option
                                >
                                <option value="Psicología geriátrica"
                                    >Psicología geriátrica</option
                                >
                                <option value="Medicina geriátrica"
                                    >Medicina geriátrica</option
                                >
                                <option value="Acompañamiento"
                                    >Acompañamiento</option
                                >
                                <option value="Otro">Otro</option>
                            </select>
                        </div>

                        <div>
                            <label
                                class="block text-xs text-gray-500 mb-1"
                                for="years_experience"
                            >
                                Años de Experiencia
                            </label>
                            <input
                                id="years_experience"
                                type="number"
                                bind:value={formData.years_experience}
                                class="form-input"
                                min="0"
                                max="50"
                            />
                        </div>

                        <div class="md:col-span-2">
                            <label
                                class="block text-xs text-gray-500 mb-1"
                                for="certifications"
                            >
                                Certificaciones
                            </label>
                            <textarea
                                id="certifications"
                                bind:value={formData.certifications}
                                class="form-textarea"
                                rows="2"
                                placeholder="Lista tus certificaciones, títulos y cursos relevantes..."
                            ></textarea>
                        </div>
                    </div>
                </div>

                <!-- Acciones -->
                <div
                    class="flex flex-col md:flex-row justify-between items-center gap-4 pt-6 border-t border-gray-200 mt-8"
                >
                    <button
                        type="button"
                        on:click={handleClose}
                        class="btn-secondary w-full md:w-auto"
                        disabled={loading}
                    >
                        Cancelar
                    </button>
                    <div class="flex gap-4 w-full md:w-auto">
                        <button
                            type="submit"
                            class="btn-primary flex items-center gap-2 w-full md:w-auto"
                            disabled={loading}
                        >
                            {#if loading}
                                <div
                                    class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"
                                ></div>
                            {/if}
                            <svg
                                class="w-4 h-4"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M5 13l4 4L19 7"
                                />
                            </svg>
                            Guardar Cambios
                        </button>
                        <button
                            type="button"
                            class="btn-warning flex items-center gap-2 w-full md:w-auto"
                            on:click={handleDelete}
                        >
                            <svg
                                class="w-4 h-4"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12"
                                />
                            </svg>
                            Eliminar cuenta
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
{/if}

<style>
    .btn {
        @apply px-4 py-2 rounded font-semibold;
    }
    .btn-primary {
        @apply bg-blue-500 text-white hover:bg-green-500 transition;
    }
    .btn-ghost {
        @apply bg-transparent text-blue-700 hover:bg-blue-100;
    }
    .input {
        @apply border rounded px-3 py-2;
    }
    .input-bordered {
        @apply border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200;
    }
</style>
