<script lang="ts">
    import { goto } from "$app/navigation";
    import {
        alertService,
        authService,
        authStore,
        deviceService,
        elderlyPersonService,
    } from "$lib/api.js";
    import type { ElderlyPerson, SystemStatus } from "$lib/types";
    import {
        Activity,
        AlertTriangle,
        Clock,
        Edit,
        Heart,
        LogOut,
        Plus,
        Settings,
        Trash2,
        Users,
    } from "lucide-svelte";
    import { onMount } from "svelte";
    import DeviceForm from "../components/DeviceForm.svelte";
    import ElderlyPersonForm from "../components/ElderlyPersonForm.svelte";

    // Datos reales del backend
    let elderlyPersons: ElderlyPerson[] = [];
    let systemStatus: SystemStatus = {
        devices: 0,
        activeAlerts: 0,
        totalEvents: 0,
        uptime: "99.8%",
    };
    let loading = true;
    let error = "";
    let errorDetail = "";
    let debugData: any = {};

    // Modal y estado de formulario
    let showForm = false;
    let formLoading = false;
    let formError = "";
    let editingPerson: ElderlyPerson | null = null;
    let formTitle = "Agregar Adulto Mayor";
    let formSuccess = "";
    let formKey = Date.now();

    // Nuevo estado para la sesión
    let sessionExpiring = false;
    let sessionExpired = false;

    // Estado para dispositivos
    let devices: any[] = [];
    let deviceFormVisible = false;
    let deviceFormLoading = false;
    let deviceFormError = "";
    let editingDevice: any = null;
    let deviceFormTitle = "Agregar Dispositivo";
    let deviceFormKey = Date.now();

    onMount(async () => {
        // Verificar autenticación
        if (!authService.isAuthenticated()) {
            goto("/login");
            return;
        }
        await loadDashboardData();
        await loadDevicesAndElderly();
    });

    async function loadDashboardData() {
        try {
            loading = true;
            error = "";
            errorDetail = "";
            debugData = {};
            // Cargar datos en paralelo
            const [elderlyData, alertsDataRaw, devicesDataRaw] =
                await Promise.all([
                    elderlyPersonService.getAll(),
                    alertService.getAll(),
                    deviceService.getAll(),
                ]);
            // Debug monitor
            debugData.elderlyPersons = elderlyData;
            debugData.alerts = alertsDataRaw;
            debugData.devices = devicesDataRaw;
            // Asegurar arrays
            const safeAlertsData = Array.isArray(alertsDataRaw)
                ? alertsDataRaw
                : [];
            const safeDevicesData = Array.isArray(devicesDataRaw)
                ? devicesDataRaw
                : [];
            // Procesar adultos mayores y ordenar por updated_at/created_at descendente
            elderlyPersons = Array.isArray(elderlyData)
                ? elderlyData
                      .map((person: any) => ({
                          ...person,
                          name: `${person.first_name} ${person.last_name}`,
                          age: person.age || "N/A",
                          status: "active", // TODO: Determinar estado real
                          lastActivity: "15 minutos", // TODO: Obtener de eventos
                          location: "Sala de estar", // TODO: Obtener de dispositivos
                          alerts: safeAlertsData.filter(
                              (alert: any) =>
                                  alert.elderly_person_id === person.id,
                          ).length,
                      }))
                      .sort((a: any, b: any) => {
                          const dateA = new Date(
                              a.updated_at || a.created_at,
                          ).getTime();
                          const dateB = new Date(
                              b.updated_at || b.created_at,
                          ).getTime();
                          return dateB - dateA;
                      })
                : [];
            // Actualizar estado del sistema
            systemStatus = {
                devices: safeDevicesData.length,
                activeAlerts: safeAlertsData.filter(
                    (alert: any) => !alert.resolved,
                ).length,
                totalEvents: 156, // TODO: Obtener de eventos
                uptime: "99.8%",
            };
            formSuccess = editingPerson
                ? "Adulto mayor editado con éxito"
                : "Adulto mayor creado con éxito";
            setTimeout(() => {
                formSuccess = "";
            }, 2000);
        } catch (err: any) {
            error = "Error al cargar los datos del dashboard";
            errorDetail = err?.message || JSON.stringify(err);
            console.error("Error loading dashboard data:", err);
        } finally {
            loading = false;
        }
    }

    function handleLogout() {
        authService.logout();
        authStore.update((state: any) => ({
            ...state,
            isAuthenticated: false,
        }));
        goto("/login");
    }

    function openAddForm() {
        editingPerson = null;
        formTitle = "Agregar Adulto Mayor";
        formError = "";
        showForm = true;
        formKey = Date.now();
    }

    function openEditForm(person: ElderlyPerson) {
        editingPerson = person;
        formTitle = "Editar Adulto Mayor";
        formError = "";
        showForm = true;
        formKey = Date.now();
    }

    async function handleFormSubmit(e: any) {
        formLoading = true;
        formError = "";
        try {
            // Validar datos antes de enviar
            const data = e.detail;
            if (!data.first_name || !data.last_name) {
                formError = "Nombre y apellido son obligatorios";
                return;
            }
            // Limpiar campos vacíos
            const payload = {
                first_name: data.first_name.trim(),
                last_name: data.last_name.trim(),
                age: data.age ? Number(data.age) : null,
                address: data.address ? data.address.trim() : "",
                emergency_contacts: Array.isArray(data.emergency_contacts)
                    ? data.emergency_contacts
                    : [],
            };
            if (editingPerson) {
                await elderlyPersonService.update(editingPerson.id, payload);
            } else {
                await elderlyPersonService.create(payload);
            }
            showForm = false;
            await loadDashboardData();
        } catch (err: any) {
            formError =
                err?.message || (err && err.toString()) || "Error al guardar";
        } finally {
            formLoading = false;
        }
    }

    function handleFormClose() {
        showForm = false;
        editingPerson = null;
        formError = "";
        formKey = Date.now();
    }

    async function handleDelete(person: ElderlyPerson) {
        if (
            confirm(
                `¿Seguro que deseas eliminar a ${person.first_name} ${person.last_name}?`,
            )
        ) {
            try {
                await elderlyPersonService.delete(person.id);
                await loadDashboardData();
                formSuccess = "Adulto mayor eliminado con éxito";
                setTimeout(() => {
                    formSuccess = "";
                }, 2000);
            } catch (err: any) {
                alert(err?.message || "Error al eliminar");
            }
        }
    }

    function handleConfigureDevice() {
        alert("Funcionalidad próximamente: configurar dispositivo");
    }

    function handleViewAlerts() {
        alert("Funcionalidad próximamente: ver alertas");
    }

    function handleRenewSession() {
        // Redirige a login para renovar sesión
        goto("/login");
    }

    // Cargar dispositivos y adultos mayores
    async function loadDevicesAndElderly() {
        try {
            deviceFormLoading = true;
            // elderlyPersons ya se carga en loadDashboardData, pero lo recargamos por si acaso
            const [devicesData, elderlyData] = await Promise.all([
                deviceService.getAll(),
                elderlyPersonService.getAll(),
            ]);
            devices = Array.isArray(devicesData)
                ? devicesData.sort((a: any, b: any) => {
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
        } catch (err: any) {
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

    function openEditDeviceForm(device: any) {
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

    async function handleDeviceFormSubmit(e: any) {
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
        } catch (err: any) {
            deviceFormError =
                err?.message || (err && err.toString()) || "Error al guardar";
        } finally {
            deviceFormLoading = false;
        }
    }

    async function handleDeleteDevice(device: any) {
        if (
            confirm(
                `¿Seguro que deseas eliminar el dispositivo '${device.name}'?`,
            )
        ) {
            try {
                await deviceService.delete(device.id);
                await loadDevicesAndElderly();
            } catch (err: any) {
                alert(err?.message || "Error al eliminar dispositivo");
            }
        }
    }
</script>

<svelte:head>
    <title>Viejos Son Los Trapos - Panel de Control</title>
</svelte:head>

<div class="container">
    <header class="header">
        <div class="header-content">
            <h1>👴 Viejos Son Los Trapos</h1>
            <p>Panel de monitoreo para adultos mayores</p>
        </div>
        <button class="logout-button" on:click={handleLogout}>
            <LogOut class="icon-small" />
            Cerrar Sesión
        </button>
    </header>

    {#if error}
        <div class="error-banner">
            <div>
                {error}
                {#if errorDetail}
                    <div class="error-detail">{errorDetail}</div>
                {/if}
            </div>
            <button on:click={loadDashboardData}>Reintentar</button>
        </div>
    {/if}

    <div class="dashboard">
        <!-- Estado del sistema -->
        <section class="system-status">
            <h2>Estado del Sistema</h2>
            {#if loading}
                <div class="loading">Cargando datos...</div>
            {:else}
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div class="card">
                        <div class="stat">
                            <Users class="icon" />
                            <div>
                                <h3>{systemStatus.devices}</h3>
                                <p>Dispositivos Activos</p>
                            </div>
                        </div>
                    </div>
                    <div class="card">
                        <div class="stat">
                            <AlertTriangle class="icon warning" />
                            <div>
                                <h3>{systemStatus.activeAlerts}</h3>
                                <p>Alertas Activas</p>
                            </div>
                        </div>
                    </div>
                    <div class="card">
                        <div class="stat">
                            <Activity class="icon" />
                            <div>
                                <h3>{systemStatus.totalEvents}</h3>
                                <p>Eventos Totales</p>
                            </div>
                        </div>
                    </div>
                    <div class="card">
                        <div class="stat">
                            <Heart class="icon success" />
                            <div>
                                <h3>{systemStatus.uptime}</h3>
                                <p>Tiempo Activo</p>
                            </div>
                        </div>
                    </div>
                </div>
            {/if}
        </section>

        <!-- Adultos mayores -->
        <section class="elderly-persons">
            <div class="section-header">
                <h2>Adultos Mayores</h2>
                <button
                    class="btn btn-primary"
                    on:click={openAddForm}
                    disabled={loading}
                >
                    <Plus class="icon-small" />
                    Agregar
                </button>
            </div>

            {#if loading}
                <div class="loading">Cargando adultos mayores...</div>
            {:else if elderlyPersons.length === 0}
                <div class="empty-state">
                    <Users class="icon-large" />
                    <h3>No hay adultos mayores registrados</h3>
                    <p>
                        Agrega el primer adulto mayor para comenzar el monitoreo
                    </p>
                </div>
            {:else}
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {#each elderlyPersons as person}
                        <div class="card person-card">
                            <div class="person-header">
                                <h3>{person.name}</h3>
                                <span class="age">{person.age} años</span>
                            </div>
                            <div class="person-status">
                                <div class="status-indicator {person.status}">
                                    <Activity class="icon-small" />
                                    <span
                                        >{person.status === "active"
                                            ? "Activo"
                                            : "Inactivo"}</span
                                    >
                                </div>
                                <div class="person-details">
                                    <p>
                                        <Clock class="icon-small" /> Última actividad:
                                        {person.lastActivity}
                                    </p>
                                    <p>
                                        <Settings class="icon-small" /> Ubicación:
                                        {person.location}
                                    </p>
                                    {#if person.alerts > 0}
                                        <p class="alert">
                                            <AlertTriangle class="icon-small" />
                                            {person.alerts} alerta(s)
                                        </p>
                                    {/if}
                                </div>
                            </div>
                            <div class="person-actions">
                                <button
                                    class="btn btn-primary"
                                    on:click={() => openEditForm(person)}
                                >
                                    <Edit class="icon-small" /> Editar
                                </button>
                                <button
                                    class="btn btn-danger"
                                    on:click={() => handleDelete(person)}
                                >
                                    <Trash2 class="icon-small" /> Eliminar
                                </button>
                            </div>
                        </div>
                    {/each}
                </div>
            {/if}
        </section>

        <!-- Acciones rápidas -->
        <section class="quick-actions">
            <h2>Acciones Rápidas</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button
                    class="card action-card"
                    on:click={handleConfigureDevice}
                >
                    <Settings class="icon" />
                    <h3>Configurar Dispositivo</h3>
                    <p>Agregar o configurar un nuevo dispositivo IoT</p>
                </button>
                <button class="card action-card" on:click={openAddForm}>
                    <Users class="icon" />
                    <h3>Agregar Familiar</h3>
                    <p>Registrar un nuevo adulto mayor</p>
                </button>
                <button class="card action-card" on:click={handleViewAlerts}>
                    <AlertTriangle class="icon" />
                    <h3>Ver Alertas</h3>
                    <p>Revisar historial de alertas y eventos</p>
                </button>
            </div>
        </section>

        <!-- Dispositivos -->
        <section class="devices">
            <div class="section-header">
                <h2>Dispositivos</h2>
                <button
                    class="btn btn-primary"
                    on:click={openAddDeviceForm}
                    disabled={deviceFormLoading}
                    title="Agregar un nuevo dispositivo"
                >
                    <Plus class="icon-small" /> Agregar Dispositivo
                </button>
            </div>
            {#if deviceFormLoading}
                <div class="loading">Cargando dispositivos...</div>
            {:else if devices.length === 0}
                <div class="empty-state">
                    <h3>No hay dispositivos registrados</h3>
                    <p>
                        Agrega el primer dispositivo para comenzar el monitoreo
                    </p>
                </div>
            {:else}
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {#each devices as device}
                        <div class="card device-card">
                            <div class="device-header">
                                <h3>{device.name}</h3>
                                <span class="device-id"
                                    >ID: {device.device_id}</span
                                >
                            </div>
                            <div class="device-details">
                                <p>
                                    <strong>Ubicación:</strong>
                                    {device.location || "N/A"}
                                </p>
                                <p>
                                    <strong>Adulto Mayor:</strong>
                                    {#if device.elderly_person_id}{elderlyPersons.find(
                                            (p) =>
                                                p.id ===
                                                device.elderly_person_id,
                                        )?.first_name || ""}
                                        {elderlyPersons.find(
                                            (p) =>
                                                p.id ===
                                                device.elderly_person_id,
                                        )?.last_name || ""}{:else}N/A{/if}
                                </p>
                                <p>
                                    <strong>Estado:</strong>
                                    {device.is_active ? "Activo" : "Inactivo"}
                                </p>
                            </div>
                            <div class="device-actions">
                                <button
                                    class="btn btn-primary"
                                    on:click={() => openEditDeviceForm(device)}
                                    title="Editar dispositivo"
                                >
                                    <Edit class="icon-small" /> Editar
                                </button>
                                <button
                                    class="btn btn-danger"
                                    on:click={() => handleDeleteDevice(device)}
                                    title="Eliminar dispositivo"
                                >
                                    <Trash2 class="icon-small" /> Eliminar
                                </button>
                            </div>
                        </div>
                    {/each}
                </div>
            {/if}
        </section>
    </div>
</div>

<ElderlyPersonForm
    visible={showForm}
    initialData={editingPerson}
    loading={formLoading}
    error={formError}
    title={formTitle}
    key={formKey}
    on:submit={handleFormSubmit}
    on:close={handleFormClose}
/>

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

<!-- En el modal ElderlyPersonForm, muestro formSuccess si existe -->
{#if formSuccess}
    <div class="form-success">{formSuccess}</div>
{/if}

<!-- Nuevo banner/modal visual para la sesión -->
{#if sessionExpiring && !sessionExpired}
    <div class="session-warning">
        <strong>¡Atención!</strong> Tu sesión está por expirar.
        <button on:click={handleRenewSession}>Renovar sesión</button>
    </div>
{/if}
{#if sessionExpired}
    <div class="session-expired">
        <strong>Sesión expirada.</strong> Por favor, vuelve a iniciar sesión.
        <button on:click={handleRenewSession}>Ir a login</button>
    </div>
{/if}

<style>
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 3rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e5e7eb;
    }
    .header-content h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    .header-content p {
        font-size: 1.1rem;
        color: var(--text-secondary);
    }
    .logout-button {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: #ef4444;
        color: white;
        border: none;
        border-radius: 0.375rem;
        cursor: pointer;
        font-size: 0.875rem;
        transition: background-color 0.15s ease-in-out;
    }
    .logout-button:hover {
        background: #dc2626;
    }
    .error-banner {
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #dc2626;
        padding: 1rem;
        border-radius: 0.375rem;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .error-banner button {
        background: #dc2626;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        cursor: pointer;
    }
    .error-detail {
        font-size: 0.9rem;
        color: #b91c1c;
        margin-top: 0.5rem;
        word-break: break-all;
    }
    .dashboard section {
        margin-bottom: 3rem;
    }
    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }
    .dashboard h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    .loading {
        text-align: center;
        padding: 2rem;
        color: var(--text-secondary);
        font-size: 1.1rem;
    }
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: var(--text-secondary);
    }
    .empty-state .icon-large {
        width: 4rem;
        height: 4rem;
        margin: 0 auto 1rem;
        color: var(--text-secondary);
    }
    .grid {
        display: grid;
    }
    .grid-cols-1 {
        grid-template-columns: repeat(1, minmax(0, 1fr));
    }
    .md\:grid-cols-2 {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .md\:grid-cols-3 {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
    .md\:grid-cols-4 {
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }
    .gap-4 {
        gap: 1rem;
    }
    .card {
        background: white;
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow:
            0 1px 3px 0 rgba(0, 0, 0, 0.1),
            0 1px 2px 0 rgba(0, 0, 0, 0.06);
        border: 1px solid #e5e7eb;
    }
    .stat {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .stat h3 {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }
    .stat p {
        color: var(--text-secondary);
        font-size: 0.875rem;
        margin: 0;
    }
    .icon {
        width: 2rem;
        height: 2rem;
        color: var(--primary-color);
    }
    .icon-small {
        width: 1rem;
        height: 1rem;
    }
    .icon-large {
        width: 4rem;
        height: 4rem;
    }
    .warning {
        color: #f59e0b;
    }
    .success {
        color: #10b981;
    }
    .person-card {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    .person-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .person-header h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    .age {
        background: var(--primary-color);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 500;
    }
    .person-status {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.875rem;
        font-weight: 500;
    }
    .status-indicator.active {
        color: #10b981;
    }
    .status-indicator.inactive {
        color: #6b7280;
    }
    .person-details {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    .person-details p {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin: 0;
    }
    .person-details .alert {
        color: #dc2626;
        font-weight: 500;
    }
    .person-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: auto;
    }
    .action-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 1rem;
        cursor: pointer;
        transition: transform 0.15s ease-in-out;
    }
    .action-card:hover {
        transform: translateY(-2px);
    }
    .action-card h3 {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    .action-card p {
        color: var(--text-secondary);
        font-size: 0.875rem;
        margin: 0;
    }
    .btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.15s ease-in-out;
        text-decoration: none;
    }
    .btn-primary {
        background: var(--primary-color);
        color: white;
    }
    .btn-primary:hover {
        background: var(--primary-dark);
    }
    .btn-secondary {
        background: #f3f4f6;
        color: var(--text-primary);
    }
    .btn-secondary:hover {
        background: #e5e7eb;
    }
    .btn-danger {
        background: #ef4444;
        color: white;
    }
    .btn-danger:hover {
        background: #dc2626;
    }
    @media (max-width: 768px) {
        .header {
            flex-direction: column;
            gap: 1rem;
            text-align: center;
        }
        .section-header {
            flex-direction: column;
            gap: 1rem;
            align-items: stretch;
        }
        .person-actions {
            flex-direction: column;
        }
    }
    .form-success {
        background: #d1fae5;
        color: #065f46;
        border: 1px solid #6ee7b7;
        border-radius: 0.375rem;
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }
    .session-warning {
        background: #fef9c3;
        color: #92400e;
        border: 1px solid #fde68a;
        border-radius: 0.375rem;
        padding: 1rem;
        margin-bottom: 1rem;
        text-align: center;
        font-size: 1rem;
        z-index: 1200;
    }
    .session-warning button {
        background: #2563eb;
        color: #fff;
        border: none;
        border-radius: 0.375rem;
        padding: 0.3rem 1rem;
        margin-left: 1rem;
        cursor: pointer;
    }
    .session-warning button:hover {
        background: #1d4ed8;
    }
    .session-expired {
        background: #fee2e2;
        color: #b91c1c;
        border: 1px solid #fecaca;
        border-radius: 0.375rem;
        padding: 1rem;
        margin-bottom: 1rem;
        text-align: center;
        font-size: 1rem;
        z-index: 1200;
    }
    .session-expired button {
        background: #2563eb;
        color: #fff;
        border: none;
        border-radius: 0.375rem;
        padding: 0.3rem 1rem;
        margin-left: 1rem;
        cursor: pointer;
    }
    .session-expired button:hover {
        background: #1d4ed8;
    }
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
    .devices {
        margin-top: 3rem;
        margin-bottom: 3rem;
        padding-top: 2rem;
        border-top: 3px solid #2563eb;
        border-radius: 0.5rem;
        background: #f8fafc;
    }
    .elderly-persons {
        margin-bottom: 3rem;
        padding-bottom: 2rem;
        border-bottom: 3px solid #2563eb;
        border-radius: 0.5rem;
        background: #f8fafc;
    }
</style>
