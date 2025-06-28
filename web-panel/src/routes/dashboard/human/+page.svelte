<script>
    import { goto } from "$app/navigation";
    import {
        alertService,
        authService,
        deviceService,
        elderlyPersonService,
        eventService,
    } from "$lib/api.js";
    import { getUserIdFromToken } from "$lib/auth.js";
    import { Calendar } from "@fullcalendar/core";
    import dayGridPlugin from "@fullcalendar/daygrid";
    import interactionPlugin from "@fullcalendar/interaction";
    import timeGridPlugin from "@fullcalendar/timegrid";
    import { onDestroy, onMount } from "svelte";
    import ElderlyPersonForm from "../../../components/ElderlyPersonForm.svelte";
    import EventForm from "../../../components/EventForm.svelte";
    import Toast from "../../../components/Toast.svelte";

    let elderlyPersons = [];
    let loading = true;
    let error = "";
    let errorDetail = "";
    let debugData = {};
    let showForm = false;
    let formLoading = false;
    let formError = "";
    let editingPerson = null;
    let formTitle = "Agregar Adulto Mayor";
    let formSuccess = "";
    let formKey = Date.now();
    let selectedPerson = null;
    let showDrawer = false;
    let drawerCalendar;
    let drawerCalendarEl;
    let drawerEvents = [];
    let drawerEventsLoading = false;
    let showEventForm = false;
    let editingEvent = null;
    let eventFormLoading = false;
    let eventFormError = "";
    let eventFormSuccess = "";
    let eventTypes = [
        { key: "medical", label: "Turno médico", color: "#2563eb" },
        { key: "family", label: "Visita familiar", color: "#10b981" },
        { key: "medication", label: "Medicación", color: "#f59e42" },
        { key: "kinesiologia", label: "Kinesiología", color: "#a855f7" },
        { key: "nutrition", label: "Nutrición", color: "#f43f5e" },
        { key: "sensor", label: "Evento de sensor", color: "#64748b" },
        { key: "other", label: "Otro", color: "#6b7280" },
    ];
    let lastLoadedPersonId = null;
    let toastMessage = "";
    let toastType = "success";
    let toastVisible = false;
    let alertPollingInterval = null;
    let audioContext;
    let alertSound;
    let unreadAlerts = new Set();
    let lastAlertCount = 0;
    let isPollingActive = false;

    onMount(async () => {
        if (!authService.isAuthenticated()) {
            goto("/login");
            return;
        }
        await loadDashboardData();

        // Inicializar audio para alertas
        try {
            audioContext = new (window.AudioContext ||
                window.webkitAudioContext)();
            alertSound = new Audio("/alert-sound.mp3"); // Sonido de alerta
        } catch (e) {
            console.log("Audio no disponible");
        }

        // Solicitar permisos de notificación
        if ("Notification" in window) {
            Notification.requestPermission();
        }
    });

    async function loadDashboardData() {
        try {
            loading = true;
            error = "";
            errorDetail = "";
            debugData = {};
            console.log("🔄 Cargando datos del dashboard...");
            console.log(
                "🔑 Token de autenticación:",
                localStorage.getItem("authToken") ? "Presente" : "Ausente",
            );

            const [elderlyData, alertsDataRaw, devicesDataRaw] =
                await Promise.all([
                    elderlyPersonService.getAll(),
                    alertService.getAll(),
                    deviceService.getAll(),
                ]);

            console.log("📊 Datos recibidos:", {
                elderlyData: elderlyData,
                alertsDataRaw: alertsDataRaw,
                devicesDataRaw: devicesDataRaw,
            });

            debugData.elderlyPersons = elderlyData;
            debugData.alerts = alertsDataRaw;
            debugData.devices = devicesDataRaw;
            const safeAlertsData = Array.isArray(alertsDataRaw)
                ? alertsDataRaw
                : [];

            console.log("🔍 Procesando elderlyData:", elderlyData);
            console.log("🔍 Es Array?", Array.isArray(elderlyData));

            elderlyPersons = Array.isArray(elderlyData)
                ? elderlyData
                      .filter((person) => {
                          console.log(
                              "🔍 Filtrando persona:",
                              person.first_name,
                              "is_deleted:",
                              person.is_deleted,
                          );
                          return person.is_deleted === false;
                      })
                      .map((person) => {
                          console.log(
                              "🔍 Mapeando persona:",
                              person.first_name,
                          );
                          const personAlerts = safeAlertsData.filter(
                              (alert) =>
                                  String(alert.elderly_person_id) ===
                                  String(person.id),
                          );
                          return {
                              ...person,
                              name: `${person.first_name} ${person.last_name}`,
                              age: person.age || "N/A",
                              lastActivity: "15 minutos",
                              location: "Sala de estar",
                              alerts: personAlerts.length,
                              criticalAlerts: personAlerts.filter(
                                  (a) =>
                                      a.severity === "critical" &&
                                      !a.is_resolved,
                              ),
                              warningAlerts: personAlerts.filter(
                                  (a) =>
                                      a.severity === "warning" &&
                                      !a.is_resolved,
                              ),
                          };
                      })
                      .sort((a, b) => {
                          const dateA = new Date(
                              a.updated_at || a.created_at,
                          ).getTime();
                          const dateB = new Date(
                              b.updated_at || b.created_at,
                          ).getTime();
                          return dateB - dateA;
                      })
                : [];

            console.log("✅ elderlyPersons final:", elderlyPersons);
            console.log("✅ Cantidad de personas:", elderlyPersons.length);
        } catch (err) {
            console.error("❌ Error en loadDashboardData:", err);
            console.error("❌ Error completo:", JSON.stringify(err, null, 2));
            error = "Error al cargar los datos";
            errorDetail = err?.message || JSON.stringify(err);
        } finally {
            loading = false;
        }
    }

    function openAddForm() {
        editingPerson = null;
        formTitle = "Agregar Adulto Mayor";
        formError = "";
        showForm = true;
        formKey = Date.now();
    }

    function openEditForm(person) {
        editingPerson = person;
        formTitle = "Editar Adulto Mayor";
        formError = "";
        showForm = true;
        formKey = Date.now();
    }

    async function handleFormSubmit(e) {
        formLoading = true;
        formError = "";
        try {
            const data = e.detail;
            if (!data.first_name || !data.last_name) {
                formError = "Nombre y apellido son obligatorios";
                return;
            }
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
        } catch (err) {
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

    async function handleDelete(person) {
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
            } catch (err) {
                alert(err?.message || "Error al eliminar");
            }
        }
    }

    function openDrawer(person) {
        selectedPerson = person;
        showDrawer = true;
    }

    function closeDrawer() {
        showDrawer = false;
        selectedPerson = null;
    }

    async function loadEventsForPerson(personId) {
        try {
            drawerEventsLoading = true;
            const events = await eventService.getAll();
            // Filtrar eventos por persona
            const personEvents = events.filter(
                (event) => String(event.elderly_person_id) === String(personId),
            );
            drawerEvents = personEvents.map((event) => ({
                id: event.id,
                title: event.title || event.event_type,
                start: event.start_datetime,
                end: event.end_datetime,
                event_type: event.event_type,
                color: getEventTypeColor(event.event_type),
                extendedProps: {
                    description: event.description,
                    location: event.location,
                    event_type: event.event_type,
                },
            }));
        } catch (err) {
            console.error("Error loading events:", err);
            drawerEvents = [];
        } finally {
            drawerEventsLoading = false;
        }
    }

    function getEventTypeColor(eventType) {
        const colorMap = {
            medical: "#2563eb",
            family: "#10b981",
            medication: "#f59e42",
            kinesiologia: "#a855f7",
            nutrition: "#f43f5e",
            sensor: "#64748b",
            other: "#6b7280",
        };
        return colorMap[eventType] || "#6b7280";
    }

    // Dummy data para analítica
    function getDummyAnalytics(person) {
        return {
            recentEvents: [
                { time: "08:15", type: "Movimiento", value: "Detectado" },
                { time: "07:50", type: "Temperatura", value: "22.1°C" },
                { time: "07:30", type: "Puerta", value: "Abierta" },
                { time: "07:00", type: "Movimiento", value: "No detectado" },
                { time: "06:45", type: "Temperatura", value: "21.8°C" },
            ],
            sensorActivity: [
                { label: "00-06h", value: 2 },
                { label: "06-12h", value: 5 },
                { label: "12-18h", value: 3 },
                { label: "18-24h", value: 4 },
            ],
        };
    }

    function openEventForm(event = null) {
        if (event) {
            // Normalizar fechas a string ISO si son Date
            const normalize = (dt) => {
                if (!dt) return "";
                if (typeof dt === "string") return new Date(dt).toISOString();
                if (dt instanceof Date) return dt.toISOString();
                return "";
            };
            editingEvent = {
                ...event,
                start_datetime: normalize(event.start_datetime || event.start),
                end_datetime: normalize(event.end_datetime || event.end),
            };
        } else {
            editingEvent = null;
        }
        showEventForm = true;
        eventFormError = "";
        eventFormSuccess = "";
    }

    function showToast(msg, type = "success") {
        toastMessage = msg;
        toastType = type;
        toastVisible = true;
    }

    function isValidUUID(uuid) {
        return /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/.test(
            uuid,
        );
    }

    /**
     * Maneja el submit del formulario de eventos.
     * Campos obligatorios: event_type, title, start_datetime, end_datetime, elderly_person_id, created_by_id
     */
    async function handleEventFormSubmit(e) {
        const eventData = e.detail;
        try {
            eventFormLoading = true;
            eventFormError = "";
            if (
                !selectedPerson ||
                !selectedPerson.id ||
                !isValidUUID(selectedPerson.id)
            ) {
                eventFormError =
                    "Debes seleccionar un adulto mayor válido antes de crear un evento.";
                showToast(eventFormError, "error");
                return;
            }
            if (!eventData.event_type) {
                eventFormError = "El tipo de evento es obligatorio";
                showToast(eventFormError, "error");
                return;
            }
            // Obtener el user_id del token JWT de forma robusta
            const created_by_id = getUserIdFromToken();
            if (!created_by_id) {
                eventFormError = "No se pudo obtener el usuario logueado.";
                showToast(eventFormError, "error");
                return;
            }
            // Normalizar y validar payload
            const payload = {
                ...eventData,
                elderly_person_id: selectedPerson.id,
                created_by_id,
                start_datetime: new Date(
                    eventData.start_datetime,
                ).toISOString(),
                end_datetime: new Date(eventData.end_datetime).toISOString(),
                device_id: eventData.device_id
                    ? String(eventData.device_id)
                    : undefined,
            };
            if (editingEvent) {
                await eventService.update(editingEvent.id, payload);
                eventFormSuccess = "Evento actualizado con éxito";
                showToast(eventFormSuccess, "success");
            } else {
                await eventService.create(payload);
                eventFormSuccess = "Evento creado con éxito";
                showToast(eventFormSuccess, "success");
            }
            showEventForm = false;
            await loadEventsForPerson(selectedPerson.id);
            setTimeout(() => {
                eventFormSuccess = "";
            }, 3000);
        } catch (err) {
            eventFormError = err?.message || "Error al guardar el evento";
            showToast(eventFormError, "error");
            console.error("Error creando evento:", err);
        } finally {
            eventFormLoading = false;
        }
    }

    async function handleEventDelete(eventId) {
        if (confirm("¿Seguro que deseas eliminar este evento?")) {
            try {
                await eventService.delete(eventId);
                await loadEventsForPerson(selectedPerson.id);
                eventFormSuccess = "Evento eliminado con éxito";
                setTimeout(() => {
                    eventFormSuccess = "";
                }, 3000);
            } catch (err) {
                alert(err?.message || "Error al eliminar el evento");
            }
        }
    }

    $: if (
        showDrawer &&
        selectedPerson &&
        selectedPerson.id !== lastLoadedPersonId
    ) {
        lastLoadedPersonId = selectedPerson.id;
        loadEventsForPerson(selectedPerson.id);
        setTimeout(() => {
            if (drawerCalendar) drawerCalendar.destroy();
            drawerCalendar = new Calendar(drawerCalendarEl, {
                plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
                initialView: "dayGridMonth",
                events: drawerEvents || [],
                height: 400,
                aspectRatio: 1.2,
                headerToolbar: {
                    left: "prev,next",
                    center: "title",
                    right: "dayGridMonth,timeGridWeek",
                },
                eventClick: function (info) {
                    openEventForm({
                        id: info.event.id,
                        title: info.event.title,
                        start_datetime: info.event.start,
                        end_datetime: info.event.end,
                        event_type: info.event.extendedProps.event_type,
                        description: info.event.extendedProps.description,
                        location: info.event.extendedProps.location,
                    });
                },
                dayMaxEvents: 3,
                moreLinkClick: "popover",
                eventDisplay: "block",
                eventTimeFormat: {
                    hour: "2-digit",
                    minute: "2-digit",
                    meridiem: false,
                },
            });
            drawerCalendar.render();
        }, 100);
    }

    // Reset lastLoadedPersonId when drawer closes
    $: if (!showDrawer) {
        lastLoadedPersonId = null;
    }

    function eventPriority(type) {
        // Prioridad: medical > medication > family > other
        if (type === "medical") return 4;
        if (type === "medication") return 3;
        if (type === "family") return 2;
        return 1;
    }

    function getEventTypeLabel(type) {
        const found = eventTypes.find((e) => e.key === type);
        return found ? found.label : type;
    }

    function formatEventDate(dt) {
        if (!dt) return "";
        const d = new Date(dt);
        return `${d.getDate().toString().padStart(2, "0")}/${(d.getMonth() + 1).toString().padStart(2, "0")} ${d.getHours().toString().padStart(2, "0")}:${d.getMinutes().toString().padStart(2, "0")}`;
    }

    $: if (showDrawer && selectedPerson && !isPollingActive) {
        // Cargar alertas críticas reales
        loadCriticalAlerts();

        // Iniciar polling cada 30 segundos (solo si no está activo)
        if (!alertPollingInterval) {
            isPollingActive = true;
            alertPollingInterval = setInterval(() => {
                if (showDrawer && selectedPerson) {
                    loadCriticalAlerts();
                } else {
                    stopAlertPolling();
                }
            }, 30000);
        }
    } else if (!showDrawer && isPollingActive) {
        // Limpiar polling cuando se cierra el drawer
        stopAlertPolling();
    }

    function stopAlertPolling() {
        if (alertPollingInterval) {
            clearInterval(alertPollingInterval);
            alertPollingInterval = null;
            isPollingActive = false;
        }
    }

    function loadCriticalAlerts() {
        if (!selectedPerson) return;

        alertService
            .getCriticalAlertsByElderlyPerson(selectedPerson.id)
            .then((alerts) => {
                const currentAlerts = (alerts.alerts || alerts).map((a) => ({
                    id: a.id,
                    message:
                        a.message ||
                        a.title ||
                        a.alert_type ||
                        "Alerta crítica",
                    type: a.alert_type || "general",
                    timestamp: a.created_at || new Date().toISOString(),
                    isRead: false,
                }));

                // Detectar nuevas alertas
                if (
                    currentAlerts.length > lastAlertCount &&
                    lastAlertCount > 0
                ) {
                    const newAlerts = currentAlerts.slice(lastAlertCount);
                    triggerAlertNotification(newAlerts);
                }

                lastAlertCount = currentAlerts.length;
                selectedPerson.criticalAlerts = currentAlerts;
            })
            .catch(() => {
                selectedPerson.criticalAlerts = [];
            });
    }

    function triggerAlertNotification(newAlerts) {
        // Sonido de alerta
        if (alertSound) {
            alertSound.play().catch(() => {});
        }

        // Notificación push
        if ("Notification" in window && Notification.permission === "granted") {
            const alert = newAlerts[0]; // Primera alerta nueva
            new Notification("Alerta Crítica", {
                body: `${selectedPerson.name}: ${alert.message}`,
                icon: "/favicon.ico",
                tag: "critical-alert",
                requireInteraction: true,
            });
        }

        // Marcar como no leídas
        newAlerts.forEach((alert) => unreadAlerts.add(alert.id));
    }

    function markAlertAsRead(alertId) {
        unreadAlerts.delete(alertId);
        selectedPerson.criticalAlerts = selectedPerson.criticalAlerts.map(
            (alert) =>
                alert.id === alertId ? { ...alert, isRead: true } : alert,
        );
    }

    function getAlertIcon(type) {
        switch (type) {
            case "medical":
                return "🏥";
            case "medication":
                return "💊";
            case "fall":
                return "⚠️";
            case "emergency":
                return "🚨";
            default:
                return "⚠️";
        }
    }

    function getAlertColor(type) {
        switch (type) {
            case "medical":
                return "text-red-600";
            case "medication":
                return "text-orange-600";
            case "fall":
                return "text-red-700";
            case "emergency":
                return "text-red-800";
            default:
                return "text-red-600";
        }
    }

    function getPersonLedColor(person) {
        if (!person.is_active) return "bg-gray-400";
        if (person.criticalAlerts && person.criticalAlerts.length > 0)
            return "bg-red-500";
        if (person.warningAlerts && person.warningAlerts.length > 0)
            return "bg-yellow-400";
        return "bg-green-500";
    }

    async function toggleActive(person) {
        try {
            await elderlyPersonService.update(person.id, {
                is_active: !person.is_active,
            });
            await loadDashboardData();
            // Si el drawer está abierto y el adulto es el seleccionado, refrescar selectedPerson
            if (
                showDrawer &&
                selectedPerson &&
                selectedPerson.id === person.id
            ) {
                const updated = await elderlyPersonService.getById(person.id);
                selectedPerson.is_active = updated.is_active;
                // Si hay otros campos que pueden cambiar, actualízalos aquí también
            }
            showToast(
                `Estado actualizado: ${!person.is_active ? "Activo" : "Inactivo"}`,
                "success",
            );
        } catch (err) {
            showToast("Error al actualizar estado", "error");
        }
    }

    onDestroy(() => {
        stopAlertPolling();
    });
</script>

<section class="py-8 px-4">
    <h2 class="text-2xl font-bold mb-6 text-blue-900">Gestión Humana</h2>
    <div class="flex items-center mb-4">
        <span class="text-lg font-semibold text-gray-700 mr-2"
            >Adultos Mayores</span
        >
        <button
            class="ml-2 bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors flex items-center"
            on:click={() => {
                showForm = true;
                editingPerson = null;
                formTitle = "Agregar Adulto Mayor";
            }}
        >
            <span class="text-xl mr-1">+</span> Agregar
        </button>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each elderlyPersons as person}
            <div
                class="bg-white rounded-xl shadow-md border border-gray-200 p-5 flex flex-col hover:shadow-lg transition-shadow cursor-pointer"
                on:click={() => openDrawer(person)}
            >
                <div class="flex items-center mb-3">
                    <div
                        class="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center text-2xl font-bold mr-4"
                    >
                        {person.name[0]}
                    </div>
                    <div class="flex-1">
                        <h3
                            class="text-lg font-semibold text-blue-900 mb-1 flex items-center gap-2"
                        >
                            <span>{person.name}</span>
                            <span
                                class="inline-block w-3 h-3 rounded-full {getPersonLedColor(
                                    person,
                                )} border border-gray-300"
                                title={person.is_active
                                    ? person.criticalAlerts &&
                                      person.criticalAlerts.length > 0
                                        ? "Alerta crítica"
                                        : person.warningAlerts &&
                                            person.warningAlerts.length > 0
                                          ? "Advertencia"
                                          : "Activo"
                                    : "Inactivo"}
                            ></span>
                        </h3>
                        <div
                            class="flex items-center gap-2 text-sm text-gray-600"
                        >
                            <span>{person.age} años</span>
                            <span
                                class="px-2 py-0.5 rounded-full text-xs font-semibold {person.is_active
                                    ? 'bg-green-100 text-green-700'
                                    : 'bg-gray-200 text-gray-500'}"
                            >
                                {person.is_active ? "Activo" : "Inactivo"}
                            </span>
                        </div>
                        <div class="text-xs text-gray-400 mt-1">
                            Última actividad: {person.lastActivity}
                        </div>
                    </div>
                    {#if person.alerts > 0}
                        <span
                            class="ml-2 bg-red-500 text-white text-xs font-bold rounded-full px-2 py-1 animate-pulse"
                            >{person.alerts}</span
                        >
                    {/if}
                </div>
            </div>
        {/each}
    </div>
</section>

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

<EventForm
    visible={showEventForm}
    initialData={editingEvent}
    loading={eventFormLoading}
    error={eventFormError}
    title={editingEvent ? "Editar Evento" : "Nuevo Evento"}
    on:submit={handleEventFormSubmit}
    on:close={() => (showEventForm = false)}
/>

{#if formSuccess}
    <div class="form-success">{formSuccess}</div>
{/if}

<Toast
    message={toastMessage}
    type={toastType}
    visible={toastVisible}
    style="position: fixed; top: 2rem; right: 2rem; z-index: 9999;"
/>

{#if showDrawer && selectedPerson}
    <div
        class="fixed inset-0 bg-black bg-opacity-50 z-40"
        on:click={closeDrawer}
    ></div>
    <div
        class="fixed right-0 top-0 h-full w-96 bg-white shadow-xl z-50 overflow-y-auto"
    >
        <div class="p-6">
            <div class="flex justify-between items-center mb-6">
                <h2
                    class="text-xl font-bold text-gray-800 flex items-center gap-2"
                >
                    {selectedPerson.name}
                    <span
                        class="inline-block w-3 h-3 rounded-full {getPersonLedColor(
                            selectedPerson,
                        )} border border-gray-300"
                        title={selectedPerson.is_active
                            ? selectedPerson.criticalAlerts &&
                              selectedPerson.criticalAlerts.length > 0
                                ? "Alerta crítica"
                                : selectedPerson.warningAlerts &&
                                    selectedPerson.warningAlerts.length > 0
                                  ? "Advertencia"
                                  : "Activo"
                            : "Inactivo"}
                    ></span>
                    <span
                        class="px-2 py-0.5 rounded-full text-xs font-semibold {selectedPerson.is_active
                            ? 'bg-green-100 text-green-700'
                            : 'bg-gray-200 text-gray-500'}"
                    >
                        {selectedPerson.is_active ? "Activo" : "Inactivo"}
                    </span>
                    <label
                        class="switch ml-2"
                        title={selectedPerson.is_active
                            ? "Desactivar adulto mayor"
                            : "Activar adulto mayor"}
                    >
                        <input
                            type="checkbox"
                            checked={selectedPerson.is_active}
                            on:change={() => toggleActive(selectedPerson)}
                        />
                        <span class="slider"></span>
                    </label>
                </h2>
                <button
                    on:click={closeDrawer}
                    class="text-gray-500 hover:text-gray-700"
                >
                    <svg
                        class="w-6 h-6"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M6 18L18 6M6 6l12 12"
                        ></path>
                    </svg>
                </button>
            </div>

            <!-- ALERTAS CRÍTICAS -->
            {#if selectedPerson.criticalAlerts && selectedPerson.criticalAlerts.length > 0}
                <div class="space-y-2 mb-6">
                    <h3
                        class="text-lg font-semibold text-red-700 mb-3 flex items-center"
                    >
                        <span class="text-xl mr-2">🚨</span> Alertas Críticas
                    </h3>
                    {#each selectedPerson.criticalAlerts as alert}
                        <div
                            class="flex items-center space-x-2 p-3 bg-red-50 border-l-4 border-red-500 rounded-r transition-all duration-200 hover:bg-red-100 cursor-pointer {!alert.isRead
                                ? 'ring-2 ring-red-300 animate-pulse'
                                : ''}"
                            on:click={() => markAlertAsRead(alert.id)}
                        >
                            <span class="text-lg"
                                >{getAlertIcon(alert.type)}</span
                            >
                            <span
                                class="text-sm font-medium {getAlertColor(
                                    alert.type,
                                )} flex-1">{alert.message}</span
                            >
                            {#if !alert.isRead}
                                <span
                                    class="w-2 h-2 bg-red-500 rounded-full animate-ping"
                                ></span>
                            {/if}
                            <span class="text-xs text-gray-500">
                                {formatEventDate(alert.timestamp)}
                            </span>
                        </div>
                    {/each}
                </div>
            {:else}
                <div class="mb-6">
                    <h3
                        class="text-lg font-semibold text-gray-700 mb-3 flex items-center"
                    >
                        <span class="text-xl mr-2">🚨</span> Alertas Críticas
                    </h3>
                    <p class="text-gray-500 text-sm">
                        No hay alertas críticas activas
                    </p>
                </div>
            {/if}

            <!-- EVENTOS PROGRAMADOS -->
            <div class="mb-6">
                <div class="flex justify-between items-center mb-3">
                    <h3 class="text-lg font-semibold text-gray-800">
                        Eventos Programados
                    </h3>
                    <button
                        on:click={() => openEventForm()}
                        class="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors"
                        disabled={!selectedPerson ||
                            !selectedPerson.id ||
                            !isValidUUID(selectedPerson.id)}
                    >
                        + Nuevo
                    </button>
                </div>

                {#if drawerEventsLoading}
                    <div class="text-center py-4">
                        <div
                            class="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"
                        ></div>
                    </div>
                {:else if drawerEvents && drawerEvents.length > 0}
                    <div class="space-y-2 max-h-64 overflow-y-auto">
                        {#each drawerEvents.sort((a, b) => new Date(a.start) - new Date(b.start)) as event}
                            <div
                                class="bg-white border border-gray-200 rounded-lg p-3 hover:shadow-md transition-shadow"
                            >
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center space-x-2">
                                        <span
                                            class="w-3 h-3 rounded-full"
                                            style="background-color: {event.color}"
                                        ></span>
                                        <span class="font-medium text-gray-800"
                                            >{event.title}</span
                                        >
                                    </div>
                                    <div class="flex items-center space-x-2">
                                        <span class="text-xs text-gray-500"
                                            >{formatEventDate(
                                                event.start,
                                            )}</span
                                        >
                                        <button
                                            on:click={() =>
                                                openEventForm(event)}
                                            class="text-blue-600 hover:text-blue-800 text-xs"
                                        >
                                            Editar
                                        </button>
                                        <button
                                            on:click={() =>
                                                handleEventDelete(event.id)}
                                            class="text-red-600 hover:text-red-800 text-xs"
                                        >
                                            Eliminar
                                        </button>
                                    </div>
                                </div>
                            </div>
                        {/each}
                    </div>
                {:else}
                    <p class="text-gray-500 text-sm">
                        No hay eventos programados
                    </p>
                {/if}
            </div>

            <!-- ANALÍTICA -->
            <div class="bg-gray-50 rounded-lg p-4">
                <h3 class="text-lg font-semibold text-gray-800 mb-3">
                    Analítica de Sensores
                </h3>

                <!-- Actividad por hora -->
                <div class="mb-4">
                    <h4 class="text-sm font-medium text-gray-700 mb-2">
                        Actividad por Hora
                    </h4>
                    <div class="space-y-1">
                        {#each getDummyAnalytics(selectedPerson).sensorActivity as bar}
                            <div class="flex items-center space-x-2">
                                <span class="text-xs text-gray-600 w-12"
                                    >{bar.label}</span
                                >
                                <div
                                    class="flex-1 bg-gray-200 rounded-full h-2"
                                >
                                    <div
                                        class="bg-blue-600 h-2 rounded-full"
                                        style="width: {bar.value * 20}%"
                                    ></div>
                                </div>
                                <span class="text-xs text-gray-600 w-4"
                                    >{bar.value}</span
                                >
                            </div>
                        {/each}
                    </div>
                </div>

                <!-- Eventos Recientes -->
                <div>
                    <h4 class="text-sm font-medium text-gray-700 mb-2">
                        Eventos Recientes
                    </h4>
                    <div class="space-y-1">
                        {#each getDummyAnalytics(selectedPerson).recentEvents as ev}
                            <div class="flex justify-between text-xs">
                                <span class="text-gray-600">{ev.time}</span>
                                <span class="text-gray-800">{ev.type}</span>
                                <span class="text-gray-600">{ev.value}</span>
                            </div>
                        {/each}
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}

<style>
    .switch {
        position: relative;
        display: inline-block;
        width: 38px;
        height: 22px;
        vertical-align: middle;
    }
    .switch input {
        opacity: 0;
        width: 0;
        height: 0;
    }
    .slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #d1d5db;
        transition: 0.4s;
        border-radius: 22px;
    }
    .slider:before {
        position: absolute;
        content: "";
        height: 16px;
        width: 16px;
        left: 3px;
        bottom: 3px;
        background-color: white;
        transition: 0.4s;
        border-radius: 50%;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
    }
    input:checked + .slider {
        background-color: #22c55e;
    }
    input:focus + .slider {
        box-shadow: 0 0 1px #22c55e;
    }
    input:checked + .slider:before {
        transform: translateX(16px);
    }
</style>
