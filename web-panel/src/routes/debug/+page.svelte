<script lang="ts">
    import { debugService } from "$lib/api.js";
    import {
        Activity,
        AlertTriangle,
        CheckCircle,
        Info,
        MapPin,
        Play,
        RefreshCw,
        Trash2,
        XCircle,
    } from "lucide-svelte";
    import { onMount } from "svelte";

    // Estado de la aplicación
    let loading = false;
    let error = "";
    let success = "";

    // Datos de debug
    let debugSummary: any = null;
    let debugEvents: any[] = [];
    let debugLocations: any[] = [];
    let debugGeofences: any[] = [];
    let testDataGenerated = false;
    let currentCaredPersonId: string | null = null;

    // Estados de carga
    let eventsLoading = false;
    let locationsLoading = false;
    let geofencesLoading = false;

    onMount(async () => {
        await checkExistingTestData();
    });

    async function checkExistingTestData() {
        try {
            // Por ahora usamos un ID de prueba - en producción vendría del usuario autenticado
            const testUserId = "550e8400-e29b-41d4-a716-446655440000";
            await loadDebugSummary(testUserId);
        } catch (err) {
            console.log("No hay datos de prueba existentes");
        }
    }

    async function generateTestData() {
        try {
            loading = true;
            error = "";
            success = "";

            // ID de usuario de prueba - en producción vendría del usuario autenticado
            const testUserId = "550e8400-e29b-41d4-a716-446655440000";

            const result = await debugService.generateTestData(testUserId);
            currentCaredPersonId = result.cared_person_id;
            testDataGenerated = true;

            success = `✅ Datos de prueba generados exitosamente:
                - Persona bajo cuidado: ${result.cared_person_id}
                - Geofences: ${result.geofences.length}
                - Eventos: ${result.events.length}
                - Ubicaciones: ${result.locations.length}
                - Protocolo: ${result.protocol_id}`;

            await loadDebugSummary(currentCaredPersonId);
        } catch (err: any) {
            error = `❌ Error al generar datos de prueba: ${err.message}`;
            console.error("Error generating test data:", err);
        } finally {
            loading = false;
        }
    }

    async function cleanupTestData() {
        if (!currentCaredPersonId) {
            error = "No hay datos de prueba para limpiar";
            return;
        }

        try {
            loading = true;
            error = "";
            success = "";

            await debugService.cleanupTestData(currentCaredPersonId);

            success = "✅ Datos de prueba eliminados exitosamente";
            testDataGenerated = false;
            currentCaredPersonId = null;
            debugSummary = null;
            debugEvents = [];
            debugLocations = [];
            debugGeofences = [];
        } catch (err: any) {
            error = `❌ Error al limpiar datos de prueba: ${err.message}`;
            console.error("Error cleaning test data:", err);
        } finally {
            loading = false;
        }
    }

    async function loadDebugSummary(caredPersonId: string) {
        try {
            const summary = await debugService.getDebugSummary(caredPersonId);
            debugSummary = summary;
        } catch (err: any) {
            console.error("Error loading debug summary:", err);
        }
    }

    async function loadDebugEvents() {
        if (!currentCaredPersonId) return;

        try {
            eventsLoading = true;
            const events = await debugService.getDebugEvents({
                cared_person_id: currentCaredPersonId,
                limit: 50,
            });
            debugEvents = events;
        } catch (err: any) {
            console.error("Error loading debug events:", err);
        } finally {
            eventsLoading = false;
        }
    }

    async function loadDebugLocations() {
        if (!currentCaredPersonId) return;

        try {
            locationsLoading = true;
            const locations = await debugService.getDebugLocations(
                currentCaredPersonId,
                50,
            );
            debugLocations = locations;
        } catch (err: any) {
            console.error("Error loading debug locations:", err);
        } finally {
            locationsLoading = false;
        }
    }

    async function loadDebugGeofences() {
        try {
            geofencesLoading = true;
            const geofences =
                await debugService.getDebugGeofences(currentCaredPersonId);
            debugGeofences = geofences;
        } catch (err: any) {
            console.error("Error loading debug geofences:", err);
        } finally {
            geofencesLoading = false;
        }
    }

    function getSeverityColor(severity: string) {
        switch (severity) {
            case "critical":
                return "text-red-600 bg-red-100";
            case "high":
                return "text-orange-600 bg-orange-100";
            case "medium":
                return "text-yellow-600 bg-yellow-100";
            case "low":
                return "text-green-600 bg-green-100";
            default:
                return "text-gray-600 bg-gray-100";
        }
    }

    function formatDate(dateString: string) {
        return new Date(dateString).toLocaleString("es-ES");
    }
</script>

<svelte:head>
    <title>Debug - Sistema de Cuidado</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">
                🧪 Panel de Debug y Testing
            </h1>
            <p class="text-gray-600">
                Prueba todas las funcionalidades del sistema sin dispositivos
                IoT
            </p>
        </div>

        <!-- Alertas -->
        {#if error}
            <div class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <div class="flex items-center">
                    <XCircle class="h-5 w-5 text-red-400 mr-2" />
                    <span class="text-red-800 whitespace-pre-line">{error}</span
                    >
                </div>
            </div>
        {/if}

        {#if success}
            <div
                class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg"
            >
                <div class="flex items-center">
                    <CheckCircle class="h-5 w-5 text-green-400 mr-2" />
                    <span class="text-green-800 whitespace-pre-line"
                        >{success}</span
                    >
                </div>
            </div>
        {/if}

        <!-- Controles principales -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <!-- Generar datos de prueba -->
            <div class="bg-white p-6 rounded-lg shadow-sm border">
                <div class="flex items-center mb-4">
                    <Play class="h-6 w-6 text-blue-600 mr-2" />
                    <h2 class="text-xl font-semibold text-gray-900">
                        Generar Datos de Prueba
                    </h2>
                </div>
                <p class="text-gray-600 mb-4">
                    Crea un conjunto completo de datos simulados para probar el
                    sistema
                </p>
                <button
                    on:click={generateTestData}
                    disabled={loading || testDataGenerated}
                    class="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                >
                    {#if loading}
                        <RefreshCw class="h-4 w-4 mr-2 animate-spin" />
                        Generando...
                    {:else}
                        <Play class="h-4 w-4 mr-2" />
                        Generar Datos
                    {/if}
                </button>
            </div>

            <!-- Limpiar datos de prueba -->
            <div class="bg-white p-6 rounded-lg shadow-sm border">
                <div class="flex items-center mb-4">
                    <Trash2 class="h-6 w-6 text-red-600 mr-2" />
                    <h2 class="text-xl font-semibold text-gray-900">
                        Limpiar Datos
                    </h2>
                </div>
                <p class="text-gray-600 mb-4">
                    Elimina todos los datos de prueba generados
                </p>
                <button
                    on:click={cleanupTestData}
                    disabled={loading || !testDataGenerated}
                    class="w-full bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                >
                    {#if loading}
                        <RefreshCw class="h-4 w-4 mr-2 animate-spin" />
                        Limpiando...
                    {:else}
                        <Trash2 class="h-4 w-4 mr-2" />
                        Limpiar Datos
                    {/if}
                </button>
            </div>
        </div>

        <!-- Resumen de datos -->
        {#if debugSummary}
            <div class="bg-white p-6 rounded-lg shadow-sm border mb-8">
                <div class="flex items-center mb-4">
                    <Info class="h-6 w-6 text-green-600 mr-2" />
                    <h2 class="text-xl font-semibold text-gray-900">
                        Resumen de Datos
                    </h2>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div class="text-center p-4 bg-blue-50 rounded-lg">
                        <div class="text-2xl font-bold text-blue-600">
                            {debugSummary.total_locations}
                        </div>
                        <div class="text-sm text-gray-600">Ubicaciones</div>
                    </div>
                    <div class="text-center p-4 bg-green-50 rounded-lg">
                        <div class="text-2xl font-bold text-green-600">
                            {debugSummary.total_events}
                        </div>
                        <div class="text-sm text-gray-600">Eventos</div>
                    </div>
                    <div class="text-center p-4 bg-purple-50 rounded-lg">
                        <div class="text-2xl font-bold text-purple-600">
                            {debugSummary.total_geofences}
                        </div>
                        <div class="text-sm text-gray-600">Geofences</div>
                    </div>
                    <div class="text-center p-4 bg-orange-50 rounded-lg">
                        <div class="text-lg font-bold text-orange-600">
                            {debugSummary.cared_person_name}
                        </div>
                        <div class="text-sm text-gray-600">Persona</div>
                    </div>
                </div>

                {#if debugSummary.last_location}
                    <div class="mt-4 p-4 bg-gray-50 rounded-lg">
                        <h3 class="font-semibold text-gray-900 mb-2">
                            Última Ubicación
                        </h3>
                        <div class="text-sm text-gray-600">
                            Lat: {debugSummary.last_location.latitude}, Lng: {debugSummary
                                .last_location.longitude}
                            <br />
                            Fecha: {formatDate(
                                debugSummary.last_location.created_at,
                            )}
                        </div>
                    </div>
                {/if}

                {#if debugSummary.last_event}
                    <div class="mt-4 p-4 bg-gray-50 rounded-lg">
                        <h3 class="font-semibold text-gray-900 mb-2">
                            Último Evento
                        </h3>
                        <div class="text-sm text-gray-600">
                            Tipo: {debugSummary.last_event.event_type}
                            <br />
                            Severidad:
                            <span
                                class="px-2 py-1 rounded text-xs {getSeverityColor(
                                    debugSummary.last_event.severity_level,
                                )}"
                            >
                                {debugSummary.last_event.severity_level}
                            </span>
                            <br />
                            Fecha: {formatDate(
                                debugSummary.last_event.created_at,
                            )}
                        </div>
                    </div>
                {/if}
            </div>
        {/if}

        <!-- Datos detallados -->
        {#if testDataGenerated}
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Eventos de Debug -->
                <div class="bg-white p-6 rounded-lg shadow-sm border">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center">
                            <AlertTriangle
                                class="h-6 w-6 text-orange-600 mr-2"
                            />
                            <h2 class="text-xl font-semibold text-gray-900">
                                Eventos
                            </h2>
                        </div>
                        <button
                            on:click={loadDebugEvents}
                            disabled={eventsLoading}
                            class="text-blue-600 hover:text-blue-700"
                        >
                            <RefreshCw
                                class="h-4 w-4 {eventsLoading
                                    ? 'animate-spin'
                                    : ''}"
                            />
                        </button>
                    </div>

                    {#if debugEvents.length > 0}
                        <div class="space-y-3 max-h-96 overflow-y-auto">
                            {#each debugEvents as event}
                                <div class="p-3 bg-gray-50 rounded-lg">
                                    <div
                                        class="flex justify-between items-start"
                                    >
                                        <div>
                                            <div
                                                class="font-medium text-gray-900"
                                            >
                                                {event.event_type}
                                            </div>
                                            <div class="text-sm text-gray-600">
                                                {event.description}
                                            </div>
                                        </div>
                                        <span
                                            class="px-2 py-1 rounded text-xs {getSeverityColor(
                                                event.severity_level,
                                            )}"
                                        >
                                            {event.severity_level}
                                        </span>
                                    </div>
                                    <div class="text-xs text-gray-500 mt-1">
                                        {formatDate(event.created_at)}
                                    </div>
                                </div>
                            {/each}
                        </div>
                    {:else}
                        <p class="text-gray-500 text-center py-4">
                            No hay eventos para mostrar
                        </p>
                    {/if}
                </div>

                <!-- Ubicaciones -->
                <div class="bg-white p-6 rounded-lg shadow-sm border">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center">
                            <MapPin class="h-6 w-6 text-blue-600 mr-2" />
                            <h2 class="text-xl font-semibold text-gray-900">
                                Ubicaciones
                            </h2>
                        </div>
                        <button
                            on:click={loadDebugLocations}
                            disabled={locationsLoading}
                            class="text-blue-600 hover:text-blue-700"
                        >
                            <RefreshCw
                                class="h-4 w-4 {locationsLoading
                                    ? 'animate-spin'
                                    : ''}"
                            />
                        </button>
                    </div>

                    {#if debugLocations.length > 0}
                        <div class="space-y-3 max-h-96 overflow-y-auto">
                            {#each debugLocations as location}
                                <div class="p-3 bg-gray-50 rounded-lg">
                                    <div class="font-medium text-gray-900">
                                        {location.latitude.toFixed(6)}, {location.longitude.toFixed(
                                            6,
                                        )}
                                    </div>
                                    <div class="text-sm text-gray-600">
                                        Fuente: {location.source_type}
                                    </div>
                                    <div class="text-xs text-gray-500">
                                        {formatDate(location.created_at)}
                                    </div>
                                </div>
                            {/each}
                        </div>
                    {:else}
                        <p class="text-gray-500 text-center py-4">
                            No hay ubicaciones para mostrar
                        </p>
                    {/if}
                </div>

                <!-- Geofences -->
                <div class="bg-white p-6 rounded-lg shadow-sm border">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center">
                            <Activity class="h-6 w-6 text-green-600 mr-2" />
                            <h2 class="text-xl font-semibold text-gray-900">
                                Geofences
                            </h2>
                        </div>
                        <button
                            on:click={loadDebugGeofences}
                            disabled={geofencesLoading}
                            class="text-blue-600 hover:text-blue-700"
                        >
                            <RefreshCw
                                class="h-4 w-4 {geofencesLoading
                                    ? 'animate-spin'
                                    : ''}"
                            />
                        </button>
                    </div>

                    {#if debugGeofences.length > 0}
                        <div class="space-y-3 max-h-96 overflow-y-auto">
                            {#each debugGeofences as geofence}
                                <div class="p-3 bg-gray-50 rounded-lg">
                                    <div class="font-medium text-gray-900">
                                        {geofence.name}
                                    </div>
                                    <div class="text-sm text-gray-600">
                                        Tipo: {geofence.type}
                                    </div>
                                    <div class="text-sm text-gray-600">
                                        Radio: {geofence.radius}m
                                    </div>
                                    <div class="text-xs text-gray-500">
                                        {geofence.latitude.toFixed(6)}, {geofence.longitude.toFixed(
                                            6,
                                        )}
                                    </div>
                                </div>
                            {/each}
                        </div>
                    {:else}
                        <p class="text-gray-500 text-center py-4">
                            No hay geofences para mostrar
                        </p>
                    {/if}
                </div>
            </div>
        {/if}

        <!-- Instrucciones -->
        {#if !testDataGenerated}
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-6 mt-8">
                <div class="flex items-center mb-4">
                    <Info class="h-6 w-6 text-blue-600 mr-2" />
                    <h3 class="text-lg font-semibold text-blue-900">
                        ¿Cómo usar este panel?
                    </h3>
                </div>
                <div class="text-blue-800 space-y-2">
                    <p>
                        1. <strong>Genera datos de prueba</strong> para crear una
                        persona simulada con eventos, ubicaciones y geofences
                    </p>
                    <p>
                        2. <strong>Explora los datos</strong> generados para ver
                        cómo funciona el sistema
                    </p>
                    <p>
                        3. <strong>Prueba las funcionalidades</strong> del frontend
                        con datos realistas
                    </p>
                    <p>
                        4. <strong>Limpia los datos</strong> cuando termines de probar
                    </p>
                </div>
            </div>
        {/if}
    </div>
</div>
