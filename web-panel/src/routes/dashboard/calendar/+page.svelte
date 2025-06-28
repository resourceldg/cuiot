<script>
    import { onMount } from "svelte";
    // Importa FullCalendar y estilos (asume que ya está instalado)
    import { Calendar } from "@fullcalendar/core";
    import dayGridPlugin from "@fullcalendar/daygrid";
    import interactionPlugin from "@fullcalendar/interaction";
    import timeGridPlugin from "@fullcalendar/timegrid";
    // Dummy o real

    let calendar;
    let calendarEl;
    let eventTypes = [];
    let filterType = "";
    let filterPerson = "";
    let elderlyPersons = [
        { id: "1", name: "Juan Pérez" },
        { id: "2", name: "Ana Gómez" },
    ];
    let events = [
        {
            id: "1",
            title: "Turno médico",
            start: "2024-07-01T10:00:00",
            end: "2024-07-01T11:00:00",
            event_type: "medical",
            elderly_person_id: "1",
            color: "#2563eb",
        },
        {
            id: "2",
            title: "Visita familiar",
            start: "2024-07-02T17:00:00",
            end: "2024-07-02T18:00:00",
            event_type: "family",
            elderly_person_id: "2",
            color: "#10b981",
        },
        {
            id: "3",
            title: "Medicación",
            start: "2024-07-03T08:00:00",
            end: "2024-07-03T08:15:00",
            event_type: "medication",
            elderly_person_id: "1",
            color: "#f59e42",
        },
    ];

    onMount(() => {
        eventTypes = [
            { key: "medical", label: "Turno médico", color: "#2563eb" },
            { key: "family", label: "Visita familiar", color: "#10b981" },
            { key: "medication", label: "Medicación", color: "#f59e42" },
            { key: "kinesiologia", label: "Kinesiología", color: "#a855f7" },
            { key: "nutrition", label: "Nutrición", color: "#f43f5e" },
            { key: "sensor", label: "Evento de sensor", color: "#64748b" },
            { key: "other", label: "Otro", color: "#6b7280" },
        ];
        calendar = new Calendar(calendarEl, {
            plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
            initialView: "dayGridMonth",
            events: () => {
                let filtered = events;
                if (filterType)
                    filtered = filtered.filter(
                        (e) => e.event_type === filterType,
                    );
                if (filterPerson)
                    filtered = filtered.filter(
                        (e) => e.elderly_person_id === filterPerson,
                    );
                return filtered;
            },
            eventClick: function (info) {
                alert(
                    "Evento: " +
                        info.event.title +
                        "\nTipo: " +
                        info.event.extendedProps.event_type,
                );
            },
            dateClick: function (info) {
                alert("Crear nuevo evento en: " + info.dateStr);
            },
            height: 650,
            headerToolbar: {
                left: "prev,next today",
                center: "title",
                right: "dayGridMonth,timeGridWeek,timeGridDay",
            },
        });
        calendar.render();
    });

    function handleTypeFilter(e) {
        filterType = e.target.value;
        calendar.refetchEvents();
    }
    function handlePersonFilter(e) {
        filterPerson = e.target.value;
        calendar.refetchEvents();
    }
</script>

<div class="calendar-filters">
    <label
        >Filtrar por adulto mayor:
        <select on:change={handlePersonFilter}>
            <option value="">Todos</option>
            {#each elderlyPersons as p}
                <option value={p.id}>{p.name}</option>
            {/each}
        </select>
    </label>
    <label
        >Filtrar por tipo de evento:
        <select on:change={handleTypeFilter}>
            <option value="">Todos</option>
            {#each eventTypes as t}
                <option value={t.key}>{t.label}</option>
            {/each}
        </select>
    </label>
</div>
<div bind:this={calendarEl} class="calendar-container"></div>

<style>
    .calendar-filters {
        display: flex;
        gap: 2rem;
        margin-bottom: 1.5rem;
        align-items: center;
    }
    .calendar-filters label {
        font-weight: 500;
        color: #2563eb;
    }
    .calendar-container {
        background: #fff;
        border-radius: 0.75rem;
        box-shadow: 0 2px 8px 0 rgba(37, 99, 235, 0.08);
        padding: 1.5rem;
    }
</style>
