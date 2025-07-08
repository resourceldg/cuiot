<script>
    import Card from "$lib/ui/Card.svelte";
    import MetricCard from "$lib/ui/MetricCard.svelte";
    import ChartIcon from "$lib/ui/icons/ChartIcon.svelte";
    import CpuIcon from "$lib/ui/icons/CpuIcon.svelte";
    import DatabaseIcon from "$lib/ui/icons/DatabaseIcon.svelte";
    import NetworkIcon from "$lib/ui/icons/NetworkIcon.svelte";

    // Datos simulados de métricas del sistema
    let systemMetrics = {
        cpu: 45,
        ram: 67,
        disk: 23,
        connections: 1234,
        queriesPerSecond: 1567,
        uptime: 99.98,
        lastDowntime: "2 días",
        ltv: 2450,
        churn: 3.2,
    };

    function getCpuColor(cpu) {
        if (cpu < 50) return "var(--color-success)";
        if (cpu < 80) return "var(--color-warning)";
        return "var(--color-error)";
    }

    function getRamColor(ram) {
        if (ram < 60) return "var(--color-success)";
        if (ram < 85) return "var(--color-warning)";
        return "var(--color-error)";
    }
</script>

<Card style="flex:1; min-width:300px;">
    <h3 style="margin-bottom:var(--spacing-md);">Métricas del Sistema</h3>

    <div class="metrics-grid">
        <div class="metric-group">
            <h4 class="group-title">Rendimiento</h4>
            <div class="metric-row">
                <MetricCard
                    title="CPU"
                    value="{systemMetrics.cpu}%"
                    icon={CpuIcon}
                    color={getCpuColor(systemMetrics.cpu)}
                    size="small"
                />
                <MetricCard
                    title="RAM"
                    value="{systemMetrics.ram}%"
                    icon={CpuIcon}
                    color={getRamColor(systemMetrics.ram)}
                    size="small"
                />
                <MetricCard
                    title="Disco"
                    value="{systemMetrics.disk}%"
                    icon={CpuIcon}
                    color="var(--color-accent)"
                    size="small"
                />
            </div>
        </div>

        <div class="metric-group">
            <h4 class="group-title">Base de Datos</h4>
            <div class="metric-row">
                <MetricCard
                    title="Conexiones"
                    value={systemMetrics.connections}
                    icon={DatabaseIcon}
                    color="var(--color-accent)"
                    size="small"
                />
                <MetricCard
                    title="Queries/s"
                    value={systemMetrics.queriesPerSecond}
                    icon={DatabaseIcon}
                    color="var(--color-success)"
                    size="small"
                />
            </div>
        </div>

        <div class="metric-group">
            <h4 class="group-title">Disponibilidad</h4>
            <div class="metric-row">
                <MetricCard
                    title="Uptime"
                    value="{systemMetrics.uptime}%"
                    icon={NetworkIcon}
                    color="var(--color-success)"
                    size="small"
                />
                <MetricCard
                    title="Último down"
                    value={systemMetrics.lastDowntime}
                    icon={NetworkIcon}
                    color="var(--color-warning)"
                    size="small"
                />
            </div>
        </div>

        <div class="metric-group">
            <h4 class="group-title">Negocio</h4>
            <div class="metric-row">
                <MetricCard
                    title="LTV"
                    value="${systemMetrics.ltv}"
                    icon={ChartIcon}
                    color="var(--color-success)"
                    size="small"
                />
                <MetricCard
                    title="Churn"
                    value="{systemMetrics.churn}%"
                    icon={ChartIcon}
                    color="var(--color-warning)"
                    size="small"
                />
            </div>
        </div>
    </div>

    <div class="system-status">
        <div class="status-indicator status-operational">
            <span class="status-dot"></span>
            <span class="status-text">Sistema Operativo</span>
        </div>
    </div>
</Card>

<style>
    .metrics-grid {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-lg);
    }

    .metric-group {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-sm);
    }

    .group-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--color-text-secondary);
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: var(--spacing-sm);
    }

    .system-status {
        margin-top: var(--spacing-lg);
        padding-top: var(--spacing-md);
        border-top: 1px solid var(--color-border);
    }

    .status-indicator {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--color-success);
        animation: pulse 2s infinite;
    }

    .status-operational .status-dot {
        background: var(--color-success);
    }

    .status-text {
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--color-text);
    }

    @keyframes pulse {
        0% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
        100% {
            opacity: 1;
        }
    }

    @media (max-width: 768px) {
        .metric-row {
            grid-template-columns: 1fr 1fr;
        }
    }
</style>
