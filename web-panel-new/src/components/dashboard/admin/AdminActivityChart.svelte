<script>
    import Card from "$lib/ui/Card.svelte";
    import ChartIcon from "$lib/ui/icons/ChartIcon.svelte";

    // Datos simulados para el gráfico de actividad
    let activityData = [
        { date: "2024-01-01", users: 1200, devices: 850, alerts: 15 },
        { date: "2024-01-02", users: 1250, devices: 870, alerts: 12 },
        { date: "2024-01-03", users: 1180, devices: 820, alerts: 18 },
        { date: "2024-01-04", users: 1320, devices: 920, alerts: 8 },
        { date: "2024-01-05", users: 1280, devices: 890, alerts: 14 },
        { date: "2024-01-06", users: 1350, devices: 950, alerts: 6 },
        { date: "2024-01-07", users: 1400, devices: 980, alerts: 10 },
    ];

    function formatDate(dateString) {
        return new Date(dateString).toLocaleDateString("es-ES", {
            day: "2-digit",
            month: "2-digit",
        });
    }

    function getMaxValue() {
        return Math.max(
            ...activityData.map((d) =>
                Math.max(d.users, d.devices, d.alerts * 50),
            ),
        );
    }

    function getBarHeight(value, maxValue) {
        return (value / maxValue) * 100;
    }
</script>

<Card style="width:100%;">
    <h3
        style="margin-bottom:var(--spacing-md); display:flex; align-items:center;"
    >
        <ChartIcon size={20} style="margin-right:var(--spacing-sm);" />
        Actividad del Sistema (Últimos 7 días)
    </h3>

    <div class="chart-container">
        <div class="chart-legend">
            <div class="legend-item">
                <span class="legend-color legend-users"></span>
                <span class="legend-label">Usuarios Activos</span>
            </div>
            <div class="legend-item">
                <span class="legend-color legend-devices"></span>
                <span class="legend-label">Dispositivos Conectados</span>
            </div>
            <div class="legend-item">
                <span class="legend-color legend-alerts"></span>
                <span class="legend-label">Alertas (x50)</span>
            </div>
        </div>

        <div class="chart-bars">
            {#each activityData as dataPoint, index}
                <div class="chart-bar-group">
                    <div class="bar-container">
                        <div
                            class="bar bar-users"
                            style="height: {getBarHeight(
                                dataPoint.users,
                                getMaxValue(),
                            )}%"
                            title="Usuarios: {dataPoint.users}"
                        ></div>
                        <div
                            class="bar bar-devices"
                            style="height: {getBarHeight(
                                dataPoint.devices,
                                getMaxValue(),
                            )}%"
                            title="Dispositivos: {dataPoint.devices}"
                        ></div>
                        <div
                            class="bar bar-alerts"
                            style="height: {getBarHeight(
                                dataPoint.alerts * 50,
                                getMaxValue(),
                            )}%"
                            title="Alertas: {dataPoint.alerts}"
                        ></div>
                    </div>
                    <span class="bar-label">{formatDate(dataPoint.date)}</span>
                </div>
            {/each}
        </div>
    </div>

    <div class="chart-stats">
        <div class="stat-card">
            <span class="stat-title">Promedio Usuarios</span>
            <span class="stat-value"
                >{Math.round(
                    activityData.reduce((sum, d) => sum + d.users, 0) /
                        activityData.length,
                )}</span
            >
        </div>
        <div class="stat-card">
            <span class="stat-title">Promedio Dispositivos</span>
            <span class="stat-value"
                >{Math.round(
                    activityData.reduce((sum, d) => sum + d.devices, 0) /
                        activityData.length,
                )}</span
            >
        </div>
        <div class="stat-card">
            <span class="stat-title">Total Alertas</span>
            <span class="stat-value"
                >{activityData.reduce((sum, d) => sum + d.alerts, 0)}</span
            >
        </div>
        <div class="stat-card">
            <span class="stat-title">Tendencia</span>
            <span class="stat-value stat-trend">↗️ +12.5%</span>
        </div>
    </div>
</Card>

<style>
    .chart-container {
        margin-bottom: var(--spacing-lg);
    }

    .chart-legend {
        display: flex;
        justify-content: center;
        gap: var(--spacing-lg);
        margin-bottom: var(--spacing-md);
        flex-wrap: wrap;
    }

    .legend-item {
        display: flex;
        align-items: center;
        gap: var(--spacing-xs);
    }

    .legend-color {
        width: 12px;
        height: 12px;
        border-radius: 2px;
    }

    .legend-users {
        background: var(--color-accent);
    }

    .legend-devices {
        background: var(--color-success);
    }

    .legend-alerts {
        background: var(--color-warning);
    }

    .legend-label {
        font-size: 0.85rem;
        color: var(--color-text-secondary);
    }

    .chart-bars {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        height: 200px;
        padding: 0 var(--spacing-sm);
        gap: var(--spacing-xs);
    }

    .chart-bar-group {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--spacing-xs);
        flex: 1;
    }

    .bar-container {
        display: flex;
        align-items: flex-end;
        gap: 2px;
        width: 100%;
        height: 100%;
    }

    .bar {
        flex: 1;
        min-height: 4px;
        border-radius: 2px;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .bar:hover {
        opacity: 0.8;
        transform: scaleY(1.05);
    }

    .bar-users {
        background: var(--color-accent);
    }

    .bar-devices {
        background: var(--color-success);
    }

    .bar-alerts {
        background: var(--color-warning);
    }

    .bar-label {
        font-size: 0.75rem;
        color: var(--color-text-secondary);
        text-align: center;
    }

    .chart-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: var(--spacing-md);
        padding-top: var(--spacing-md);
        border-top: 1px solid var(--color-border);
    }

    .stat-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--spacing-xs);
        padding: var(--spacing-md);
        background: var(--color-bg-hover);
        border-radius: var(--border-radius);
        text-align: center;
    }

    .stat-title {
        font-size: 0.8rem;
        color: var(--color-text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--color-text);
    }

    .stat-trend {
        color: var(--color-success);
    }

    @media (max-width: 768px) {
        .chart-legend {
            flex-direction: column;
            align-items: center;
            gap: var(--spacing-sm);
        }

        .chart-bars {
            height: 150px;
        }

        .chart-stats {
            grid-template-columns: 1fr 1fr;
        }

        .bar-label {
            font-size: 0.7rem;
        }
    }
</style>
