<script>
    import { alertService, caredPersonService } from "$lib/api.js";
    import {
        AlertTriangle,
        CheckCircle,
        Clock,
        Eye,
        Filter,
        MapPin,
        User,
    } from "lucide-svelte";
    import { onMount } from "svelte";

    let alerts = [];
    let caredPersons = [];
    let loading = true;
    let error = "";
    let selectedSeverity = "all";
    let selectedStatus = "all";
    let showResolved = false;

    const severityOptions = [
        { value: "all", label: "Todas las severidades" },
        { value: "critical", label: "Críticas" },
        { value: "high", label: "Altas" },
        { value: "medium", label: "Medias" },
        { value: "low", label: "Bajas" },
    ];

    const statusOptions = [
        { value: "all", label: "Todos los estados" },
        { value: "active", label: "Activas" },
        { value: "resolved", label: "Resueltas" },
        { value: "acknowledged", label: "Reconocidas" },
    ];

    onMount(async () => {
        await loadData();
    });

    async function loadData() {
        try {
            loading = true;
            error = "";

            const [alertsData, caredPersonsData] = await Promise.all([
                alertService.getAll(),
                caredPersonService.getAll(),
            ]);

            alerts = alertsData.map((alert) => {
                const caredPerson = caredPersonsData.find(
                    (cp) => cp.id === alert.cared_person_id,
                );
                return {
                    ...alert,
                    caredPersonName: caredPerson
                        ? `${caredPerson.first_name} ${caredPerson.last_name}`
                        : "Persona no encontrada",
                };
            });

            caredPersons = caredPersonsData;
        } catch (err) {
            error = `Error al cargar alertas: ${err.message}`;
            console.error("Error loading alerts:", err);
        } finally {
            loading = false;
        }
    }

    function getFilteredAlerts() {
        return alerts.filter((alert) => {
            const severityMatch =
                selectedSeverity === "all" ||
                alert.severity === selectedSeverity;
            const statusMatch =
                selectedStatus === "all" || alert.status === selectedStatus;
            const resolvedMatch = showResolved
                ? true
                : alert.status !== "resolved";

            return severityMatch && statusMatch && resolvedMatch;
        });
    }

    function getSeverityColor(severity) {
        switch (severity) {
            case "critical":
                return "text-red-600 bg-red-100 border-red-200";
            case "high":
                return "text-orange-600 bg-orange-100 border-orange-200";
            case "medium":
                return "text-yellow-600 bg-yellow-100 border-yellow-200";
            case "low":
                return "text-green-600 bg-green-100 border-green-200";
            default:
                return "text-gray-600 bg-gray-100 border-gray-200";
        }
    }

    function getStatusColor(status) {
        switch (status) {
            case "active":
                return "text-red-600 bg-red-100";
            case "resolved":
                return "text-green-600 bg-green-100";
            case "acknowledged":
                return "text-blue-600 bg-blue-100";
            default:
                return "text-gray-600 bg-gray-100";
        }
    }

    function getStatusIcon(status) {
        switch (status) {
            case "active":
                return AlertTriangle;
            case "resolved":
                return CheckCircle;
            case "acknowledged":
                return Eye;
            default:
                return Clock;
        }
    }

    function formatTimeAgo(date) {
        const now = new Date();
        const diffInMinutes = Math.floor(
            (now.getTime() - new Date(date).getTime()) / (1000 * 60),
        );

        if (diffInMinutes < 1) return "Ahora";
        if (diffInMinutes < 60) return `${diffInMinutes} minutos`;

        const diffInHours = Math.floor(diffInMinutes / 60);
        if (diffInHours < 24) return `${diffInHours} horas`;

        const diffInDays = Math.floor(diffInHours / 24);
        return `${diffInDays} días`;
    }

    async function updateAlertStatus(alertId, newStatus) {
        try {
            await alertService.update(alertId, { status: newStatus });
            await loadData(); // Recargar datos
        } catch (err) {
            error = `Error al actualizar alerta: ${err.message}`;
        }
    }
</script>

<svelte:head>
    <title>Alertas - CUIOT</title>
</svelte:head>

<div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
        <div>
            <h1 class="text-2xl font-bold text-gray-900">
                🚨 Alertas del Sistema
            </h1>
            <p class="text-gray-600">
                Monitoreo y gestión de alertas en tiempo real
            </p>
        </div>
        <button
            on:click={loadData}
            class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
            Actualizar
        </button>
    </div>

    {#if error}
        <div
            class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg"
        >
            {error}
        </div>
    {/if}

    <!-- Filtros -->
    <div class="bg-white rounded-lg shadow-sm border p-4">
        <div class="flex items-center space-x-4 mb-4">
            <Filter class="w-5 h-5 text-gray-500" />
            <h3 class="font-medium text-gray-900">Filtros</h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1"
                    >Severidad</label
                >
                <select
                    bind:value={selectedSeverity}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                >
                    {#each severityOptions as option}
                        <option value={option.value}>{option.label}</option>
                    {/each}
                </select>
            </div>

            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1"
                    >Estado</label
                >
                <select
                    bind:value={selectedStatus}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                >
                    {#each statusOptions as option}
                        <option value={option.value}>{option.label}</option>
                    {/each}
                </select>
            </div>

            <div class="flex items-center">
                <label class="flex items-center">
                    <input
                        type="checkbox"
                        bind:checked={showResolved}
                        class="rounded border-gray-300 text-primary focus:ring-primary"
                    />
                    <span class="ml-2 text-sm text-gray-700"
                        >Mostrar resueltas</span
                    >
                </label>
            </div>
        </div>
    </div>

    <!-- Lista de Alertas -->
    {#if loading}
        <div class="flex justify-center items-center h-64">
            <div
                class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"
            ></div>
        </div>
    {:else}
        <div class="space-y-4">
            {#each getFilteredAlerts() as alert}
                <div
                    class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                >
                    <div class="flex items-start justify-between">
                        <div class="flex-1">
                            <div class="flex items-center space-x-3 mb-2">
                                <div
                                    class="p-2 rounded-lg {getSeverityColor(
                                        alert.severity,
                                    )}"
                                >
                                    <AlertTriangle class="w-5 h-5" />
                                </div>
                                <div>
                                    <h3 class="font-semibold text-gray-900">
                                        {alert.title}
                                    </h3>
                                    <p class="text-sm text-gray-600">
                                        {alert.description}
                                    </p>
                                </div>
                            </div>

                            <div
                                class="flex items-center space-x-4 text-sm text-gray-500 mb-3"
                            >
                                <div class="flex items-center">
                                    <User class="w-4 h-4 mr-1" />
                                    {alert.caredPersonName}
                                </div>
                                <div class="flex items-center">
                                    <Clock class="w-4 h-4 mr-1" />
                                    {formatTimeAgo(alert.created_at)}
                                </div>
                                {#if alert.location}
                                    <div class="flex items-center">
                                        <MapPin class="w-4 h-4 mr-1" />
                                        {alert.location}
                                    </div>
                                {/if}
                            </div>

                            <div class="flex items-center space-x-2">
                                <span
                                    class="px-2 py-1 text-xs font-medium rounded-full {getSeverityColor(
                                        alert.severity,
                                    )}"
                                >
                                    {alert.severity.toUpperCase()}
                                </span>
                                <span
                                    class="px-2 py-1 text-xs font-medium rounded-full {getStatusColor(
                                        alert.status,
                                    )}"
                                >
                                    {alert.status.toUpperCase()}
                                </span>
                            </div>
                        </div>

                        <div class="flex items-center space-x-2">
                            {#if alert.status === "active"}
                                <button
                                    on:click={() =>
                                        updateAlertStatus(
                                            alert.id,
                                            "acknowledged",
                                        )}
                                    class="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors"
                                    title="Marcar como reconocida"
                                >
                                    Reconocer
                                </button>
                                <button
                                    on:click={() =>
                                        updateAlertStatus(alert.id, "resolved")}
                                    class="px-3 py-1 text-sm bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors"
                                    title="Marcar como resuelta"
                                >
                                    Resolver
                                </button>
                            {:else if alert.status === "acknowledged"}
                                <button
                                    on:click={() =>
                                        updateAlertStatus(alert.id, "resolved")}
                                    class="px-3 py-1 text-sm bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors"
                                    title="Marcar como resuelta"
                                >
                                    Resolver
                                </button>
                            {/if}
                        </div>
                    </div>
                </div>
            {/each}

            {#if getFilteredAlerts().length === 0}
                <div class="text-center py-12">
                    <AlertTriangle
                        class="w-12 h-12 text-gray-400 mx-auto mb-4"
                    />
                    <h3 class="text-lg font-medium text-gray-900 mb-2">
                        No hay alertas
                    </h3>
                    <p class="text-gray-600">
                        No se encontraron alertas con los filtros seleccionados.
                    </p>
                </div>
            {/if}
        </div>
    {/if}
</div>
