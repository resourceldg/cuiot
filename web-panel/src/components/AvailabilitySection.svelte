<script lang="ts">
    import { userService } from "$lib/api.js";
    import { createEventDispatcher, onMount } from "svelte";
    // Disponibilidad horaria simple (puedes extender a un calendario real)
    export let availability = {};
    export let loading = false;
    let userId = null;
    let feedback = { success: null, error: null };
    const dispatch = createEventDispatcher();

    const defaultAvailability = {
        monday: { available: true, start: "09:00", end: "17:00" },
        tuesday: { available: true, start: "09:00", end: "17:00" },
        wednesday: { available: true, start: "09:00", end: "17:00" },
        thursday: { available: true, start: "09:00", end: "17:00" },
        friday: { available: true, start: "09:00", end: "17:00" },
        saturday: { available: false, start: "09:00", end: "17:00" },
        sunday: { available: false, start: "09:00", end: "17:00" },
    };

    function normalizeAvailability(av) {
        const result = {};
        for (const day of Object.keys(defaultAvailability)) {
            const val = av && av[day];
            if (typeof val === "object" && val !== null && "available" in val) {
                result[day] = {
                    available: !!val.available,
                    start: val.start || defaultAvailability[day].start,
                    end: val.end || defaultAvailability[day].end,
                };
            } else {
                result[day] = { ...defaultAvailability[day] };
            }
        }
        return result;
    }

    let formData = normalizeAvailability(availability);

    $: formData = normalizeAvailability(availability);

    onMount(() => {
        const token = localStorage.getItem("authToken");
        if (token) {
            try {
                const payload = JSON.parse(atob(token.split(".")[1]));
                userId = payload.sub ? parseInt(payload.sub) : null;
            } catch {}
        }
    });

    async function saveAvailability() {
        feedback = { success: null, error: null };
        try {
            if (!userId) throw new Error("No se pudo obtener el ID de usuario");
            await userService.update(userId, {
                availability: JSON.stringify(availability),
            });
            feedback.success = "Disponibilidad guardada correctamente.";
        } catch (e) {
            feedback.error = e.message || "Error al guardar disponibilidad.";
        }
    }

    function toggle(day) {
        availability[day] = !availability[day];
    }

    function handleSubmit() {
        dispatch("submit", formData);
    }

    function handleReset() {
        formData = { ...defaultAvailability };
    }

    const days = [
        { key: "monday", label: "Lunes" },
        { key: "tuesday", label: "Martes" },
        { key: "wednesday", label: "Miércoles" },
        { key: "thursday", label: "Jueves" },
        { key: "friday", label: "Viernes" },
        { key: "saturday", label: "Sábado" },
        { key: "sunday", label: "Domingo" },
    ];
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
            form="availability-form"
            class="btn-primary"
            disabled={loading}
        >
            Guardar Disponibilidad
        </button>
    </div>
    <div class="card-header">
        <h2 class="text-2xl font-bold text-gray-800">Disponibilidad</h2>
        <p class="text-gray-600 mt-1">
            Define tus horarios de trabajo y disponibilidad
        </p>
    </div>

    <form
        id="availability-form"
        on:submit|preventDefault={handleSubmit}
        class="space-y-6"
    >
        <div class="section">
            <div class="space-y-4">
                {#each days as day}
                    <div
                        class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                    >
                        <div class="flex items-center space-x-4">
                            <label
                                class="relative inline-flex items-center cursor-pointer"
                            >
                                <input
                                    type="checkbox"
                                    bind:checked={formData[day.key].available}
                                    class="form-checkbox"
                                />
                                <span
                                    class="ml-3 text-sm font-medium text-gray-700"
                                    >{day.label}</span
                                >
                            </label>
                        </div>

                        {#if formData[day.key].available}
                            <div class="flex items-center space-x-3">
                                <div class="form-group">
                                    <label class="text-xs text-gray-500"
                                        >Inicio</label
                                    >
                                    <input
                                        type="time"
                                        bind:value={formData[day.key].start}
                                        class="form-input text-sm"
                                    />
                                </div>
                                <span class="text-gray-400">-</span>
                                <div class="form-group">
                                    <label class="text-xs text-gray-500"
                                        >Fin</label
                                    >
                                    <input
                                        type="time"
                                        bind:value={formData[day.key].end}
                                        class="form-input text-sm"
                                    />
                                </div>
                            </div>
                        {:else}
                            <span class="text-sm text-gray-400"
                                >No disponible</span
                            >
                        {/if}
                    </div>
                {/each}
            </div>
        </div>

        <!-- Información Adicional -->
        <div class="section">
            <h3 class="section-title">Información Adicional</h3>
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <svg
                            class="h-5 w-5 text-blue-400"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                        >
                            <path
                                fill-rule="evenodd"
                                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                                clip-rule="evenodd"
                            ></path>
                        </svg>
                    </div>
                    <div class="ml-3">
                        <h3 class="text-sm font-medium text-blue-800">
                            Horarios Flexibles
                        </h3>
                        <div class="mt-2 text-sm text-blue-700">
                            <p>
                                Puedes ajustar tus horarios según tus
                                necesidades. Los cambios se reflejarán
                                inmediatamente en tu perfil para que los
                                clientes puedan ver tu disponibilidad
                                actualizada.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </form>
</div>
