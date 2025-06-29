<script>
    import { caredPersonService, eventService } from "$lib/api.js";
    import {
        Calendar,
        CalendarDays,
        Clock,
        Filter,
        MapPin,
        Search,
        User,
    } from "lucide-svelte";
    import { onMount } from "svelte";

    let events = [];
    let caredPersons = [];
    let loading = true;
    let error = "";
    let selectedEventType = "all";
    let selectedPerson = "all";
    let searchTerm = "";

    const eventTypeOptions = [
        { value: "all", label: "Todos los tipos" },
        { value: "medical", label: "Turno médico" },
        { value: "family", label: "Visita familiar" },
        { value: "medication", label: "Medicación" },
        { value: "kinesiologia", label: "Kinesiología" },
        { value: "nutrition", label: "Nutrición" },
        { value: "sensor", label: "Evento de sensor" },
        { value: "other", label: "Otro" },
    ];

    onMount(async () => {
        await loadData();
    });

    async function loadData() {
        try {
            loading = true;
            error = "";

            const [eventsData, caredPersonsData] = await Promise.all([
                eventService.getAll(),
                caredPersonService.getAll(),
            ]);

            events = eventsData.map((event) => {
                const caredPerson = caredPersonsData.find(
                    (cp) => cp.id === event.cared_person_id,
                );
                return {
                    ...event,
                    caredPersonName: caredPerson
                        ? `${caredPerson.first_name} ${caredPerson.last_name}`
                        : "Persona no encontrada",
                };
            });

            caredPersons = caredPersonsData;
        } catch (err) {
            error = `Error al cargar eventos: ${err.message}`;
            console.error("Error loading events:", err);
        } finally {
            loading = false;
        }
    }

    function getFilteredEvents() {
        return events
            .filter((event) => {
                const typeMatch =
                    selectedEventType === "all" ||
                    event.event_type === selectedEventType;
                const personMatch =
                    selectedPerson === "all" ||
                    event.cared_person_id === parseInt(selectedPerson);
                const searchMatch =
                    !searchTerm ||
                    event.title
                        ?.toLowerCase()
                        .includes(searchTerm.toLowerCase()) ||
                    event.description
                        ?.toLowerCase()
                        .includes(searchTerm.toLowerCase()) ||
                    event.caredPersonName
                        ?.toLowerCase()
                        .includes(searchTerm.toLowerCase());

                return typeMatch && personMatch && searchMatch;
            })
            .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    }

    function getEventTypeColor(eventType) {
        switch (eventType) {
            case "medical":
                return "text-blue-600 bg-blue-100 border-blue-200";
            case "family":
                return "text-green-600 bg-green-100 border-green-200";
            case "medication":
                return "text-orange-600 bg-orange-100 border-orange-200";
            case "kinesiologia":
                return "text-purple-600 bg-purple-100 border-purple-200";
            case "nutrition":
                return "text-pink-600 bg-pink-100 border-pink-200";
            case "sensor":
                return "text-gray-600 bg-gray-100 border-gray-200";
            default:
                return "text-gray-600 bg-gray-100 border-gray-200";
        }
    }

    function getEventTypeIcon(eventType) {
        switch (eventType) {
            case "medical":
                return "🏥";
            case "family":
                return "👨‍👩‍👧‍👦";
            case "medication":
                return "💊";
            case "kinesiologia":
                return "🏃‍♂️";
            case "nutrition":
                return "🍎";
            case "sensor":
                return "📡";
            default:
                return "📅";
        }
    }

    function formatDateTime(date) {
        return new Date(date).toLocaleString("es-ES", {
            year: "numeric",
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        });
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
</script>

<svelte:head>
    <title>Eventos - CUIOT</title>
</svelte:head>

<div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
        <div>
            <h1 class="text-2xl font-bold text-gray-900">
                📅 Eventos del Sistema
            </h1>
            <p class="text-gray-600">
                Historial y gestión de eventos de cuidado
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

    <!-- Filtros y búsqueda -->
    <div class="bg-white rounded-lg shadow-sm border p-4">
        <div class="flex items-center space-x-4 mb-4">
            <Filter class="w-5 h-5 text-gray-500" />
            <h3 class="font-medium text-gray-900">Filtros y búsqueda</h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1"
                    >Tipo de evento</label
                >
                <select
                    bind:value={selectedEventType}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                >
                    {#each eventTypeOptions as option}
                        <option value={option.value}>{option.label}</option>
                    {/each}
                </select>
            </div>

            <div>
                <label class="block text-sm font-medium text-gray-700 mb-1"
                    >Persona</label
                >
                <select
                    bind:value={selectedPerson}
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                >
                    <option value="all">Todas las personas</option>
                    {#each caredPersons as person}
                        <option value={person.id}
                            >{person.first_name} {person.last_name}</option
                        >
                    {/each}
                </select>
            </div>

            <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1"
                    >Buscar</label
                >
                <div class="relative">
                    <Search
                        class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400"
                    />
                    <input
                        type="text"
                        bind:value={searchTerm}
                        placeholder="Buscar por título, descripción o persona..."
                        class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    />
                </div>
            </div>
        </div>
    </div>

    <!-- Estadísticas rápidas -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="bg-white rounded-lg shadow-sm border p-4">
            <div class="flex items-center">
                <CalendarDays class="w-8 h-8 text-blue-600" />
                <div class="ml-3">
                    <p class="text-sm font-medium text-gray-600">
                        Total eventos
                    </p>
                    <p class="text-2xl font-bold text-gray-900">
                        {events.length}
                    </p>
                </div>
            </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm border p-4">
            <div class="flex items-center">
                <div
                    class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center"
                >
                    <span class="text-green-600 text-lg">👨‍👩‍👧‍👦</span>
                </div>
                <div class="ml-3">
                    <p class="text-sm font-medium text-gray-600">
                        Visitas familiares
                    </p>
                    <p class="text-2xl font-bold text-gray-900">
                        {events.filter((e) => e.event_type === "family").length}
                    </p>
                </div>
            </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm border p-4">
            <div class="flex items-center">
                <div
                    class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center"
                >
                    <span class="text-blue-600 text-lg">🏥</span>
                </div>
                <div class="ml-3">
                    <p class="text-sm font-medium text-gray-600">
                        Turnos médicos
                    </p>
                    <p class="text-2xl font-bold text-gray-900">
                        {events.filter((e) => e.event_type === "medical")
                            .length}
                    </p>
                </div>
            </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm border p-4">
            <div class="flex items-center">
                <div
                    class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center"
                >
                    <span class="text-orange-600 text-lg">💊</span>
                </div>
                <div class="ml-3">
                    <p class="text-sm font-medium text-gray-600">
                        Medicaciones
                    </p>
                    <p class="text-2xl font-bold text-gray-900">
                        {events.filter((e) => e.event_type === "medication")
                            .length}
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- Lista de Eventos -->
    {#if loading}
        <div class="flex justify-center items-center h-64">
            <div
                class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"
            ></div>
        </div>
    {:else}
        <div class="space-y-4">
            {#each getFilteredEvents() as event}
                <div
                    class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                >
                    <div class="flex items-start justify-between">
                        <div class="flex-1">
                            <div class="flex items-center space-x-3 mb-2">
                                <div
                                    class="p-2 rounded-lg {getEventTypeColor(
                                        event.event_type,
                                    )}"
                                >
                                    <span class="text-lg"
                                        >{getEventTypeIcon(
                                            event.event_type,
                                        )}</span
                                    >
                                </div>
                                <div>
                                    <h3 class="font-semibold text-gray-900">
                                        {event.title}
                                    </h3>
                                    <p class="text-sm text-gray-600">
                                        {event.description}
                                    </p>
                                </div>
                            </div>

                            <div
                                class="flex items-center space-x-4 text-sm text-gray-500 mb-3"
                            >
                                <div class="flex items-center">
                                    <User class="w-4 h-4 mr-1" />
                                    {event.caredPersonName}
                                </div>
                                <div class="flex items-center">
                                    <Calendar class="w-4 h-4 mr-1" />
                                    {formatDateTime(
                                        event.start_datetime ||
                                            event.created_at,
                                    )}
                                </div>
                                <div class="flex items-center">
                                    <Clock class="w-4 h-4 mr-1" />
                                    {formatTimeAgo(event.created_at)}
                                </div>
                                {#if event.location}
                                    <div class="flex items-center">
                                        <MapPin class="w-4 h-4 mr-1" />
                                        {event.location}
                                    </div>
                                {/if}
                            </div>

                            <div class="flex items-center space-x-2">
                                <span
                                    class="px-2 py-1 text-xs font-medium rounded-full {getEventTypeColor(
                                        event.event_type,
                                    )}"
                                >
                                    {event.event_type.toUpperCase()}
                                </span>
                                {#if event.is_recurring}
                                    <span
                                        class="px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-700"
                                    >
                                        RECURRENTE
                                    </span>
                                {/if}
                            </div>
                        </div>
                    </div>
                </div>
            {/each}

            {#if getFilteredEvents().length === 0}
                <div class="text-center py-12">
                    <Calendar class="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 class="text-lg font-medium text-gray-900 mb-2">
                        No hay eventos
                    </h3>
                    <p class="text-gray-600">
                        No se encontraron eventos con los filtros seleccionados.
                    </p>
                </div>
            {/if}
        </div>
    {/if}
</div>
