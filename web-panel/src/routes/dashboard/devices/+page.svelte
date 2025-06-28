<script lang="ts">
    import { goto } from "$app/navigation";
    import {
        authService,
        deviceService,
        elderlyPersonService,
    } from "$lib/api.js";
    import { Edit, Plus, Trash2 } from "lucide-svelte";
    import { onMount } from "svelte";
    import DeviceForm from "../../../components/DeviceForm.svelte";

    type Device = {
        id: string;
        name: string;
        location: string;
        device_id: string;
        elderly_person_id: string;
        is_active: boolean;
        status?: string;
        type?: string;
        created_at?: string;
        updated_at?: string;
    };
    type ElderlyPerson = {
        id: string;
        first_name: string;
        last_name: string;
    };

    let devices: Device[] = [];
    let elderlyPersons: ElderlyPerson[] = [];
    let deviceFormVisible: boolean = false;
    let deviceFormLoading: boolean = false;
    let deviceFormError: string = "";
    let editingDevice: Device | null = null;
    let deviceFormTitle: string = "Agregar Dispositivo";
    let deviceFormKey: number = Date.now();
    let debugData: any = {};

    onMount(async () => {
        if (!authService.isAuthenticated()) {
            goto("/login");
            return;
        }
        await loadDevicesAndElderly();
    });

    async function loadDevicesAndElderly() {
        try {
            deviceFormLoading = true;
            const [devicesData, elderlyData] = await Promise.all([
                deviceService.getAll(),
                elderlyPersonService.getAll(),
            ]);
            devices = Array.isArray(devicesData)
                ? devicesData.sort((a, b) => {
                      const dateA = new Date(
                          a.updated_at || a.created_at,
                      ).getTime();
                      const dateB = new Date(
                          b.updated_at || b.created_at,
                      ).getTime();
                      return dateB - dateA;
                  })
                : [];
            elderlyPersons = Array.isArray(elderlyData) ? elderlyData : [];
            debugData.devices = devicesData;
            debugData.elderlyPersons = elderlyData;
        } catch (err) {
            deviceFormError = err?.message || "Error al cargar dispositivos";
        } finally {
            deviceFormLoading = false;
        }
    }

    function openAddDeviceForm() {
        editingDevice = null;
        deviceFormTitle = "Agregar Dispositivo";
        deviceFormError = "";
        deviceFormVisible = true;
        deviceFormKey = Date.now();
    }

    function openEditDeviceForm(device: Device) {
        editingDevice = device;
        deviceFormTitle = "Editar Dispositivo";
        deviceFormError = "";
        deviceFormVisible = true;
        deviceFormKey = Date.now();
    }

    function closeDeviceForm() {
        deviceFormVisible = false;
        editingDevice = null;
        deviceFormError = "";
        deviceFormKey = Date.now();
    }

    async function handleDeviceFormSubmit(e: CustomEvent) {
        deviceFormLoading = true;
        deviceFormError = "";
        try {
            const data = e.detail;
            if (!data.name || !data.device_id || !data.elderly_person_id) {
                deviceFormError =
                    "Nombre, ID de dispositivo y adulto mayor son obligatorios";
                return;
            }
            if (editingDevice) {
                await deviceService.update(editingDevice.id, data);
            } else {
                await deviceService.create(data);
            }
            deviceFormVisible = false;
            await loadDevicesAndElderly();
        } catch (err) {
            deviceFormError =
                err?.message || (err && err.toString()) || "Error al guardar";
        } finally {
            deviceFormLoading = false;
        }
    }

    async function handleDeleteDevice(device: Device) {
        if (
            confirm(
                `¿Seguro que deseas eliminar el dispositivo '${device.name}'?`,
            )
        ) {
            try {
                await deviceService.delete(device.id);
                await loadDevicesAndElderly();
            } catch (err) {
                alert(err?.message || "Error al eliminar dispositivo");
            }
        }
    }
</script>

<h1 class="text-2xl font-bold text-blue-900 mb-6">Gestión de Dispositivos</h1>

<section class="">
    <div class="flex items-center justify-between mb-6">
        <h2 class="text-lg font-semibold text-gray-700">Dispositivos</h2>
        <button
            class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded shadow flex items-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
            on:click={openAddDeviceForm}
            disabled={deviceFormLoading}
            title="Agregar un nuevo dispositivo"
        >
            <Plus class="w-5 h-5" /> Agregar Dispositivo
        </button>
    </div>
    {#if deviceFormLoading}
        <div class="text-center text-gray-500 py-8">
            Cargando dispositivos...
        </div>
    {:else if devices.length === 0}
        <div class="flex flex-col items-center justify-center py-16">
            <h3 class="text-xl font-semibold text-gray-600 mb-2">
                No hay dispositivos registrados
            </h3>
            <p class="text-gray-400">
                Agrega el primer dispositivo para comenzar el monitoreo
            </p>
        </div>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            {#each devices as device}
                <div
                    class="bg-white rounded-xl shadow-md border border-gray-200 p-5 flex flex-col hover:shadow-lg transition-shadow"
                >
                    <div class="flex items-center justify-between mb-2">
                        <h3 class="text-lg font-bold text-blue-900">
                            {device.name}
                        </h3>
                        <span class="text-xs text-blue-600 font-mono"
                            >ID: {device.device_id}</span
                        >
                    </div>
                    <div class="mb-2 flex flex-wrap gap-2 items-center">
                        <span
                            class="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold"
                            class:bg-green-100={device.status === "ready"}
                            class:text-green-800={device.status === "ready"}
                            class:bg-yellow-100={device.status === "offline"}
                            class:text-yellow-800={device.status === "offline"}
                            class:bg-red-100={device.status === "error"}
                            class:text-red-800={device.status === "error"}
                            class:bg-gray-200={device.status === "off"}
                            class:text-gray-700={device.status === "off"}
                        >
                            {#if device.status === "ready"}🟢 Ready{/if}
                            {#if device.status === "offline"}🟡 Offline{/if}
                            {#if device.status === "error"}🔴 Error{/if}
                            {#if device.status === "off"}⚪ Off{/if}
                        </span>
                        {#if device.type}
                            <span
                                class="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-blue-100 text-blue-800"
                            >
                                {device.type
                                    .replace("_", " ")
                                    .replace(/\b\w/g, (l) => l.toUpperCase())}
                            </span>
                        {/if}
                    </div>
                    <div class="mb-2">
                        <p class="text-sm text-gray-700">
                            <strong>Ubicación:</strong>
                            {device.location || "N/A"}
                        </p>
                        <p class="text-sm text-gray-700">
                            <strong>Adulto Mayor:</strong>
                            {#if device.elderly_person_id}{elderlyPersons.find(
                                    (p) => p.id === device.elderly_person_id,
                                )?.first_name || ""}
                                {elderlyPersons.find(
                                    (p) => p.id === device.elderly_person_id,
                                )?.last_name || ""}{:else}N/A{/if}
                        </p>
                    </div>
                    <div class="flex gap-2 mt-2">
                        <button
                            class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-3 py-1 rounded flex items-center gap-1 text-sm shadow"
                            on:click={() => openEditDeviceForm(device)}
                            title="Editar dispositivo"
                        >
                            <Edit class="w-4 h-4" /> Editar
                        </button>
                        <button
                            class="bg-red-500 hover:bg-red-600 text-white font-semibold px-3 py-1 rounded flex items-center gap-1 text-sm shadow"
                            on:click={() => handleDeleteDevice(device)}
                            title="Eliminar dispositivo"
                        >
                            <Trash2 class="w-4 h-4" /> Eliminar
                        </button>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</section>

<DeviceForm
    visible={deviceFormVisible}
    initialData={editingDevice}
    {elderlyPersons}
    loading={deviceFormLoading}
    error={deviceFormError}
    title={deviceFormTitle}
    key={deviceFormKey}
    on:submit={handleDeviceFormSubmit}
    on:close={closeDeviceForm}
/>

<!-- Debug monitor visual -->
{#if Object.keys(debugData).length > 0}
    <div class="debug-monitor">
        <h4>Debug API Monitor</h4>
        <pre>{JSON.stringify(debugData, null, 2)}</pre>
    </div>
{/if}

<style>
    .devices .device-card {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    .device-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .device-header h3 {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    .device-id {
        background: #f3f4f6;
        color: #2563eb;
        padding: 0.2rem 0.7rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .device-details p {
        margin: 0.2rem 0;
        font-size: 0.95rem;
        color: var(--text-secondary);
    }
    .device-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: auto;
    }
    .debug-monitor {
        background: #f3f4f6;
        color: #374151;
        border: 1px solid #d1d5db;
        border-radius: 0.375rem;
        padding: 1rem;
        margin-bottom: 1rem;
        font-size: 0.95rem;
        max-height: 300px;
        overflow: auto;
    }
</style>
