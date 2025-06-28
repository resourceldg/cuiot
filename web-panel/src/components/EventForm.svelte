<script>
    import { Calendar, Clock, FileText, MapPin, Tag, X } from "lucide-svelte";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let visible = false;
    export let initialData = null;
    export let loading = false;
    export let error = "";
    export let title = "Nuevo Evento";

    let formData = {
        title: "",
        description: "",
        event_type: "medical",
        start_datetime: "",
        end_datetime: "",
        location: "",
    };

    const eventTypes = [
        { key: "medical", label: "Turno médico", color: "#2563eb" },
        { key: "family", label: "Visita familiar", color: "#10b981" },
        { key: "medication", label: "Medicación", color: "#f59e42" },
        { key: "kinesiologia", label: "Kinesiología", color: "#a855f7" },
        { key: "nutrition", label: "Nutrición", color: "#f43f5e" },
        { key: "sensor", label: "Evento de sensor", color: "#64748b" },
        { key: "other", label: "Otro", color: "#6b7280" },
    ];

    // Utilidades para formato argentino
    function toArgDateTimeLocal(dt) {
        if (!dt) return "";
        const d = new Date(dt);
        const yyyy = d.getFullYear();
        const mm = String(d.getMonth() + 1).padStart(2, "0");
        const dd = String(d.getDate()).padStart(2, "0");
        const hh = String(d.getHours()).padStart(2, "0");
        const min = String(d.getMinutes()).padStart(2, "0");
        return `${yyyy}-${mm}-${dd}T${hh}:${min}`;
    }
    function fromArgDateTimeLocal(str) {
        return str ? new Date(str) : null;
    }
    function toArgDisplayParts(dt) {
        if (!dt) return { fecha: "", hora: "" };
        const d = new Date(dt);
        return {
            fecha: `${d.getDate().toString().padStart(2, "0")}/${(d.getMonth() + 1).toString().padStart(2, "0")}/${d.getFullYear()}`,
            hora: `${d.getHours().toString().padStart(2, "0")}:${d.getMinutes().toString().padStart(2, "0")}`,
        };
    }

    $: if (visible && initialData) {
        formData = {
            title: initialData.title || "",
            description: initialData.description || "",
            event_type: initialData.event_type || "medical",
            start_datetime: toArgDateTimeLocal(initialData.start_datetime),
            end_datetime: toArgDateTimeLocal(initialData.end_datetime),
            location: initialData.location || "",
        };
    } else if (visible && !initialData) {
        // Por defecto: inicio ahora, fin +1h
        const now = new Date();
        const plus1h = new Date(now.getTime() + 60 * 60 * 1000);
        formData = {
            title: "",
            description: "",
            event_type: "medical",
            start_datetime: toArgDateTimeLocal(now),
            end_datetime: toArgDateTimeLocal(plus1h),
            location: "",
        };
    }

    // Validación en tiempo real
    $: dateError = "";
    $: {
        if (formData.start_datetime && formData.end_datetime) {
            const start = fromArgDateTimeLocal(formData.start_datetime);
            const end = fromArgDateTimeLocal(formData.end_datetime);
            if (end < start) {
                dateError =
                    "La fecha/hora de fin no puede ser anterior al inicio";
            }
        }
    }

    function handleStartChange(e) {
        formData.start_datetime = e.target.value;
        // Si el fin es anterior, lo ajusto a +1h
        const start = fromArgDateTimeLocal(formData.start_datetime);
        const end = fromArgDateTimeLocal(formData.end_datetime);
        if (!end || end < start) {
            const plus1h = new Date(start.getTime() + 60 * 60 * 1000);
            formData.end_datetime = toArgDateTimeLocal(plus1h);
        }
    }

    $: if (!formData.event_type) {
        formData.event_type = eventTypes[0].key;
    }

    function handleSubmit() {
        if (!formData.title.trim()) {
            error = "El título es obligatorio";
            return;
        }
        if (!formData.event_type || formData.event_type.trim() === "") {
            error = "El tipo de evento es obligatorio";
            return;
        }
        if (!formData.start_datetime) {
            error = "La fecha y hora de inicio es obligatoria";
            return;
        }
        if (!formData.end_datetime) {
            error = "La fecha y hora de fin es obligatoria";
            return;
        }
        if (dateError) {
            error = dateError;
            return;
        }
        const submitData = {
            ...formData,
            title: formData.title.trim(),
            description: formData.description.trim(),
            location: formData.location.trim(),
            event_type: formData.event_type,
            start_datetime: fromArgDateTimeLocal(
                formData.start_datetime,
            ).toISOString(),
            end_datetime: fromArgDateTimeLocal(
                formData.end_datetime,
            ).toISOString(),
        };
        console.log("Evento a enviar:", submitData);
        dispatch("submit", submitData);
    }

    function handleClose() {
        dispatch("close");
    }

    function getEventTypeColor(type) {
        const eventType = eventTypes.find((et) => et.key === type);
        return eventType ? eventType.color : "#6b7280";
    }
</script>

{#if visible}
    <div class="modal-overlay" on:click={handleClose}>
        <div class="modal" on:click|stopPropagation>
            <div class="modal-header">
                <h2>{title}</h2>
                <button class="close-btn" on:click={handleClose}>
                    <X class="icon-small" />
                </button>
            </div>

            <form class="modal-body" on:submit|preventDefault={handleSubmit}>
                {#if error}
                    <div class="error-message">
                        {error}
                    </div>
                {/if}
                {#if dateError}
                    <div class="error-message">{dateError}</div>
                {/if}

                <div class="form-group">
                    <label for="title">
                        <FileText class="icon-small" />
                        Título del evento *
                    </label>
                    <input
                        id="title"
                        type="text"
                        bind:value={formData.title}
                        placeholder="Ej: Turno médico con Dr. García"
                        required
                    />
                </div>

                <div class="form-group">
                    <label for="event_type">
                        <Tag class="icon-small" />
                        Tipo de evento
                    </label>
                    <select id="event_type" bind:value={formData.event_type}>
                        {#each eventTypes as type}
                            <option
                                value={type.key}
                                style="color: {type.color}"
                            >
                                {type.label}
                            </option>
                        {/each}
                    </select>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label for="start_datetime">
                            <Calendar class="icon-small" />
                            Inicio *
                        </label>
                        <input
                            id="start_datetime"
                            type="datetime-local"
                            bind:value={formData.start_datetime}
                            on:change={handleStartChange}
                            required
                        />
                        <div class="input-hint">
                            <span class="fecha-hint"
                                >{toArgDisplayParts(formData.start_datetime)
                                    .fecha}</span
                            >
                            <span class="hora-hint"
                                >{toArgDisplayParts(formData.start_datetime)
                                    .hora}</span
                            >
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="end_datetime">
                            <Clock class="icon-small" />
                            Fin *
                        </label>
                        <input
                            id="end_datetime"
                            type="datetime-local"
                            bind:value={formData.end_datetime}
                            min={formData.start_datetime}
                            required
                        />
                        <div class="input-hint">
                            <span class="fecha-hint"
                                >{toArgDisplayParts(formData.end_datetime)
                                    .fecha}</span
                            >
                            <span class="hora-hint"
                                >{toArgDisplayParts(formData.end_datetime)
                                    .hora}</span
                            >
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label for="location">
                        <MapPin class="icon-small" />
                        Ubicación
                    </label>
                    <input
                        id="location"
                        type="text"
                        bind:value={formData.location}
                        placeholder="Ej: Consultorio 5, Hospital Central"
                    />
                </div>

                <div class="form-group">
                    <label for="description">
                        <FileText class="icon-small" />
                        Descripción
                    </label>
                    <textarea
                        id="description"
                        bind:value={formData.description}
                        placeholder="Detalles adicionales del evento..."
                        rows="3"
                    ></textarea>
                </div>

                <div class="form-actions">
                    <button
                        type="button"
                        class="btn btn-secondary"
                        on:click={handleClose}
                    >
                        Cancelar
                    </button>
                    <button
                        type="submit"
                        class="btn btn-primary"
                        disabled={loading}
                    >
                        {#if loading}
                            Guardando...
                        {:else}
                            {initialData ? "Actualizar" : "Crear"} evento
                        {/if}
                    </button>
                </div>
            </form>
        </div>
    </div>
{/if}

<style>
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 2000;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 1rem;
    }

    .modal {
        background: white;
        border-radius: 0.75rem;
        box-shadow:
            0 20px 25px -5px rgba(0, 0, 0, 0.1),
            0 10px 10px -5px rgba(0, 0, 0, 0.04);
        width: 100%;
        max-width: 600px;
        max-height: 90vh;
        overflow-y: auto;
    }

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 1.5rem 0 1.5rem;
        border-bottom: 1px solid #e5e7eb;
        margin-bottom: 1.5rem;
    }

    .modal-header h2 {
        margin: 0;
        color: #1f2937;
        font-size: 1.25rem;
        font-weight: 600;
    }

    .close-btn {
        background: none;
        border: none;
        color: #6b7280;
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 0.375rem;
        transition: background-color 0.15s;
    }

    .close-btn:hover {
        background-color: #f3f4f6;
    }

    .modal-body {
        padding: 0 1.5rem 1.5rem 1.5rem;
    }

    .error-message {
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #dc2626;
        padding: 0.75rem;
        border-radius: 0.375rem;
        margin-bottom: 1rem;
        font-size: 0.875rem;
    }

    .form-group {
        margin-bottom: 1.25rem;
    }

    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }

    .form-group label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        color: #374151;
        font-weight: 500;
        font-size: 0.875rem;
    }

    .form-group input,
    .form-group select,
    .form-group textarea {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #d1d5db;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        transition:
            border-color 0.15s,
            box-shadow 0.15s;
    }

    .form-group input:focus,
    .form-group select:focus,
    .form-group textarea:focus {
        outline: none;
        border-color: #2563eb;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }

    .form-group textarea {
        resize: vertical;
        min-height: 80px;
    }

    .input-hint {
        font-size: 0.8rem;
        margin-top: 0.2rem;
    }
    .input-hint .fecha-hint {
        font-weight: bold;
        color: #222;
    }
    .input-hint .hora-hint {
        color: #2563eb;
        font-weight: 500;
        margin-left: 0.3em;
    }

    .form-actions {
        display: flex;
        justify-content: flex-end;
        gap: 1rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
    }

    .btn {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 0.375rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.15s;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }

    .btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .btn-primary {
        background: #2563eb;
        color: white;
    }

    .btn-primary:hover:not(:disabled) {
        background: #1d4ed8;
    }

    .btn-secondary {
        background: #6b7280;
        color: white;
    }

    .btn-secondary:hover:not(:disabled) {
        background: #4b5563;
    }

    .icon-small {
        width: 16px;
        height: 16px;
    }

    @media (max-width: 640px) {
        .form-row {
            grid-template-columns: 1fr;
        }

        .form-actions {
            flex-direction: column;
        }

        .modal {
            margin: 0.5rem;
        }
    }
</style>
