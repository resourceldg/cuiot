<script>
    import Card from "$lib/ui/Card.svelte";
    import AlertIcon from "$lib/ui/icons/AlertIcon.svelte";
    import InfoIcon from "$lib/ui/icons/InfoIcon.svelte";
    import WarningIcon from "$lib/ui/icons/WarningIcon.svelte";

    // Datos simulados de alertas críticas
    let criticalAlerts = [
        {
            id: 1,
            type: "critical",
            title: "Dispositivo IoT offline",
            description: "ID: DEV-001 - Sin respuesta desde hace 15 minutos",
            time: "Hace 5 min",
        },
        {
            id: 2,
            type: "warning",
            title: "Base de datos lenta",
            description: "2.3s avg response time - Límite: 1.5s",
            time: "Hace 12 min",
        },
        {
            id: 3,
            type: "info",
            title: "Backup completado",
            description: "Backup automático completado exitosamente",
            time: "Hace 30 min",
        },
        {
            id: 4,
            type: "critical",
            title: "Intento de acceso no autorizado",
            description: "IP: 192.168.1.100 - Bloqueado automáticamente",
            time: "Hace 45 min",
        },
    ];

    function getAlertIcon(type) {
        switch (type) {
            case "critical":
                return AlertIcon;
            case "warning":
                return WarningIcon;
            case "info":
                return InfoIcon;
            default:
                return InfoIcon;
        }
    }

    function getAlertColor(type) {
        switch (type) {
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

    function getAlertBgColor(type) {
        switch (type) {
            case "critical":
                return "rgba(255, 77, 109, 0.1)";
            case "warning":
                return "rgba(241, 196, 15, 0.1)";
            case "info":
                return "rgba(0, 230, 118, 0.1)";
            default:
                return "rgba(176, 184, 201, 0.1)";
        }
    }
</script>

<Card style="flex:1; min-width:300px;">
    <h3
        style="margin-bottom:var(--spacing-md); display:flex; align-items:center;"
    >
        <AlertIcon size={20} style="margin-right:var(--spacing-sm);" />
        Alertas Críticas
    </h3>

    <div class="alerts-container">
        {#each criticalAlerts as alert}
            <div
                class="alert-item alert-{alert.type}"
                style="border-left-color: {getAlertColor(
                    alert.type,
                )}; background: {getAlertBgColor(alert.type)};"
            >
                <div class="alert-icon">
                    <svelte:component
                        this={getAlertIcon(alert.type)}
                        size={16}
                    />
                </div>
                <div class="alert-content">
                    <div class="alert-header">
                        <span class="alert-title">{alert.title}</span>
                        <span class="alert-time">{alert.time}</span>
                    </div>
                    <p class="alert-description">{alert.description}</p>
                </div>
                <div class="alert-actions">
                    <button class="alert-action-btn" title="Ver detalles">
                        Ver
                    </button>
                    <button class="alert-action-btn" title="Resolver">
                        Resolver
                    </button>
                </div>
            </div>
        {/each}
    </div>

    <div class="alerts-summary">
        <div class="summary-item">
            <span class="summary-label">Críticas:</span>
            <span class="summary-value summary-critical">
                {criticalAlerts.filter((a) => a.type === "critical").length}
            </span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Advertencias:</span>
            <span class="summary-value summary-warning">
                {criticalAlerts.filter((a) => a.type === "warning").length}
            </span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Info:</span>
            <span class="summary-value summary-info">
                {criticalAlerts.filter((a) => a.type === "info").length}
            </span>
        </div>
    </div>
</Card>

<style>
    .alerts-container {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-sm);
        margin-bottom: var(--spacing-lg);
    }

    .alert-item {
        display: flex;
        align-items: flex-start;
        gap: var(--spacing-md);
        padding: var(--spacing-md);
        border-radius: var(--border-radius);
        border-left: 4px solid;
        transition: all 0.2s ease;
    }

    .alert-item:hover {
        transform: translateX(2px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .alert-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: var(--border-radius-sm);
        flex-shrink: 0;
    }

    .alert-content {
        flex: 1;
        min-width: 0;
    }

    .alert-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: var(--spacing-xs);
    }

    .alert-title {
        font-weight: 600;
        color: var(--color-text);
        font-size: 0.95rem;
    }

    .alert-time {
        font-size: 0.8rem;
        color: var(--color-text-secondary);
        white-space: nowrap;
    }

    .alert-description {
        font-size: 0.85rem;
        color: var(--color-text-secondary);
        margin: 0;
        line-height: 1.4;
    }

    .alert-actions {
        display: flex;
        gap: var(--spacing-xs);
        flex-shrink: 0;
    }

    .alert-action-btn {
        background: none;
        border: 1px solid var(--color-border);
        color: var(--color-text);
        padding: var(--spacing-xs) var(--spacing-sm);
        border-radius: var(--border-radius-sm);
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .alert-action-btn:hover {
        background: var(--color-bg-hover);
        border-color: var(--color-accent);
    }

    .alerts-summary {
        display: flex;
        justify-content: space-around;
        padding-top: var(--spacing-md);
        border-top: 1px solid var(--color-border);
    }

    .summary-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--spacing-xs);
    }

    .summary-label {
        font-size: 0.8rem;
        color: var(--color-text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .summary-value {
        font-size: 1.2rem;
        font-weight: 700;
    }

    .summary-critical {
        color: var(--color-error);
    }

    .summary-warning {
        color: var(--color-warning);
    }

    .summary-info {
        color: var(--color-accent);
    }

    @media (max-width: 768px) {
        .alert-header {
            flex-direction: column;
            gap: var(--spacing-xs);
        }

        .alert-actions {
            flex-direction: column;
        }

        .alerts-summary {
            flex-direction: column;
            gap: var(--spacing-sm);
        }
    }
</style>
