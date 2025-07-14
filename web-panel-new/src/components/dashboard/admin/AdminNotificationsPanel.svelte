<script>
    import { deleteAlert, getAlerts, markAlertAsRead } from "$lib/api/index.js";
    import Card from "$lib/ui/Card.svelte";
    import DataTable from "$lib/ui/DataTable.svelte";
    import EditIcon from "$lib/ui/icons/EditIcon.svelte";
    import EyeIcon from "$lib/ui/icons/EyeIcon.svelte";
    import NotificationIcon from "$lib/ui/icons/NotificationIcon.svelte";
    import TrashIcon from "$lib/ui/icons/TrashIcon.svelte";
    import { onMount } from "svelte";

    let alerts = [];
    let loading = true;
    let error = null;

    const alertColumns = [
        { key: "title", label: "Título", sortable: true },
        { key: "severity", label: "Severidad", sortable: true },
        { key: "created_at", label: "Fecha", sortable: true },
    ];

    onMount(async () => {
        await loadAlerts();
    });

    async function loadAlerts() {
        loading = true;
        try {
            alerts = await getAlerts();
        } catch (err) {
            error = err instanceof Error ? err.message : "Error desconocido";
        } finally {
            loading = false;
        }
    }

    async function handleDeleteAlert(id) {
        try {
            await deleteAlert(id);
            alerts = alerts.filter((alert) => alert.id !== id);
        } catch (err) {
            // console.error("Error deleting alert:", err);
        }
    }

    async function handleMarkAsRead(id) {
        try {
            await markAlertAsRead(id);
            alerts = alerts.map((alert) =>
                alert.id === id ? { ...alert, read: true } : alert,
            );
        } catch (err) {
            // console.error("Error marking alert as read:", err);
        }
    }

    function getSeverityColor(severity) {
        switch (severity) {
            case "critical":
                return "var(--color-error)";
            case "warning":
                return "var(--color-warning)";
            case "info":
                return "var(--color-accent)";
            default:
                return "var(--color-text-secondary)";
        }
    }

    function formatDate(dateString) {
        return new Date(dateString).toLocaleDateString("es-ES", {
            year: "numeric",
            month: "short",
            day: "numeric",
        });
    }
</script>

<Card style="flex:2; min-width:320px;">
    <h3
        style="margin-bottom:var(--spacing-md); display:flex; align-items:center;"
    >
        <NotificationIcon size={20} style="margin-right:var(--spacing-sm);" />
        Notificaciones recientes
    </h3>

    <DataTable
        columns={alertColumns}
        rows={alerts.slice(0, 5)}
        {loading}
        {error}
        page={1}
        pageSize={5}
        total={alerts.length}
        search={""}
        onSearch={() => {}}
        onPageChange={() => {}}
    >
        <span slot="row-actions" let:row>
            <button
                class="action-btn"
                title="Ver"
                aria-label="Ver notificación"
                on:click={() => {}}
                style="color:var(--color-accent)"
            >
                <EyeIcon size={18} />
            </button>
            <button
                class="action-btn"
                title="Marcar como leída"
                aria-label="Marcar como leída"
                on:click={() => handleMarkAsRead(row.id)}
                style="color:var(--color-success)"
            >
                <EditIcon size={18} />
            </button>
            <button
                class="action-btn"
                title="Eliminar"
                aria-label="Eliminar notificación"
                on:click={() => handleDeleteAlert(row.id)}
                style="color:var(--color-error)"
            >
                <TrashIcon size={18} />
            </button>
        </span>

        <span slot="cell-severity" let:row>
            <span
                class="severity-badge"
                style="color: {getSeverityColor(row.severity)}"
            >
                {row.severity}
            </span>
        </span>

        <span slot="cell-created_at" let:row>
            {formatDate(row.created_at)}
        </span>
    </DataTable>

    <div style="text-align:right; margin-top:var(--spacing-sm);">
        <button
            class="action-btn"
            style="color:var(--color-accent)"
            on:click={() => {}}
        >
            Ver todas las notificaciones
        </button>
    </div>
</Card>

<style>
    .action-btn {
        background: none;
        border: none;
        cursor: pointer;
        padding: var(--spacing-xs);
        border-radius: var(--border-radius-sm);
        transition: background 0.2s;
    }

    .action-btn:hover {
        background: var(--color-bg-hover);
    }

    .severity-badge {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        padding: var(--spacing-xs) var(--spacing-sm);
        border-radius: var(--border-radius-sm);
        background: rgba(255, 255, 255, 0.1);
    }
</style>
