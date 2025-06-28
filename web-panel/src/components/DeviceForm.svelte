<script lang="ts">
    import { createEventDispatcher } from "svelte";
    export let initialData: any = null;
    export let elderlyPersons: Array<{
        id: string;
        first_name: string;
        last_name: string;
    }> = [];
    export let loading: boolean = false;
    export let error: string = "";
    export let visible: boolean = false;
    export let title: string = "Agregar Dispositivo";

    const dispatch = createEventDispatcher();

    type DeviceForm = {
        name: string;
        location: string;
        device_id: string;
        elderly_person_id: string;
        is_active: boolean;
    };

    let form: DeviceForm = {
        name: "",
        location: "",
        device_id: "",
        elderly_person_id: "",
        is_active: true,
    };

    $: if (visible && initialData) {
        form = {
            name: initialData.name || "",
            location: initialData.location || "",
            device_id: initialData.device_id || "",
            elderly_person_id: initialData.elderly_person_id || "",
            is_active:
                initialData.is_active !== undefined
                    ? initialData.is_active
                    : true,
        };
    }
    $: if (visible && !initialData) {
        form = {
            name: "",
            location: "",
            device_id: "",
            elderly_person_id: "",
            is_active: true,
        };
    }

    function handleSubmit() {
        if (!form.name || !form.device_id || !form.elderly_person_id) {
            dispatch("error", {
                message:
                    "Nombre, ID de dispositivo y adulto mayor son obligatorios",
            });
            return;
        }
        dispatch("submit", { ...form });
    }

    function handleClose() {
        dispatch("close");
    }
</script>

{#if visible}
    <div
        class="fixed inset-0 bg-black bg-opacity-40 z-40 flex items-center justify-center"
        on:click={handleClose}
    ></div>
    <div
        class="fixed z-50 bg-white rounded-xl shadow-2xl p-6 w-full max-w-md mx-auto top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
    >
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold text-blue-900">{title}</h2>
            <button
                class="text-2xl text-gray-400 hover:text-gray-700"
                on:click={handleClose}>&times;</button
            >
        </div>
        <form on:submit|preventDefault={handleSubmit} class="space-y-4">
            {#if error}
                <div class="bg-red-100 text-red-700 px-3 py-2 rounded text-sm">
                    {error}
                </div>
            {/if}
            <div class="flex flex-col gap-1">
                <label class="font-medium text-gray-700">Nombre *</label>
                <input
                    type="text"
                    bind:value={form.name}
                    required
                    disabled={loading}
                    class="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>
            <div class="flex flex-col gap-1">
                <label class="font-medium text-gray-700">Ubicación</label>
                <input
                    type="text"
                    bind:value={form.location}
                    disabled={loading}
                    class="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>
            <div class="flex flex-col gap-1">
                <label class="font-medium text-gray-700"
                    >ID de Dispositivo *</label
                >
                <input
                    type="text"
                    bind:value={form.device_id}
                    required
                    disabled={loading}
                    class="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>
            <div class="flex flex-col gap-1">
                <label class="font-medium text-gray-700">Adulto Mayor *</label>
                <select
                    bind:value={form.elderly_person_id}
                    required
                    disabled={loading}
                    class="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                    <option value="" disabled selected
                        >Selecciona un adulto mayor</option
                    >
                    {#each elderlyPersons as person}
                        <option value={person.id}
                            >{person.first_name} {person.last_name}</option
                        >
                    {/each}
                </select>
            </div>
            <div class="flex items-center gap-2">
                <input
                    type="checkbox"
                    bind:checked={form.is_active}
                    disabled={loading}
                    class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <label class="text-gray-700">Activo</label>
            </div>
            <div class="flex justify-end gap-2 mt-4">
                <button
                    type="submit"
                    class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded shadow disabled:opacity-60 disabled:cursor-not-allowed"
                    disabled={loading}
                >
                    {#if loading}Guardando...{:else}Guardar{/if}
                </button>
                <button
                    type="button"
                    class="bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold px-4 py-2 rounded shadow"
                    on:click={handleClose}
                    disabled={loading}>Cancelar</button
                >
            </div>
        </form>
    </div>
{/if}
