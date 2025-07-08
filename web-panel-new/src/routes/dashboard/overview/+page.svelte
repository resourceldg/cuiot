<script>
    import MetricCard from "$lib/ui/MetricCard.svelte";
    import SectionHeader from "$lib/ui/SectionHeader.svelte";

    // Datos mock para las métricas
    const metrics = [
        {
            icon: "👥",
            label: "Usuarios",
            value: 1247,
            trend: "+12%",
            trendType: "up",
            color: "var(--color-accent)",
        },
        {
            icon: "💻",
            label: "Dispositivos",
            value: 892,
            trend: "+8%",
            trendType: "up",
            color: "var(--color-success)",
        },
        {
            icon: "🚨",
            label: "Alertas",
            value: 23,
            trend: "+5%",
            trendType: "up",
            color: "var(--color-danger)",
        },
        {
            icon: "🏢",
            label: "Instituciones",
            value: 45,
            trend: "+3%",
            trendType: "up",
            color: "var(--color-accent)",
        },
    ];

    // Datos mock para alertas recientes
    const recentAlerts = [
        {
            title: "Presión arterial alta",
            type: "Crítico",
            time: "2 min",
            user: "María González",
            device: "BP Monitor #123",
            color: "var(--color-danger)",
        },
        {
            title: "Dispositivo offline",
            type: "Advertencia",
            time: "15 min",
            user: "Juan Pérez",
            device: "IoT Sensor #456",
            color: "var(--color-warning)",
        },
        {
            title: "Medicación pendiente",
            type: "Info",
            time: "1 hora",
            user: "Ana López",
            device: "Medication Reminder",
            color: "var(--color-accent)",
        },
    ];
</script>

<SectionHeader title="Dashboard" icon="📊" />

<div class="metrics-grid">
    {#each metrics as m}
        <MetricCard
            icon={m.icon}
            label={m.label}
            value={m.value}
            trend={m.trend}
            trendType={m.trendType}
            color={m.color}
        />
    {/each}
</div>

<div class="alerts-card">
    <div class="alerts-header">Alertas recientes</div>
    <ul class="alerts-list">
        {#each recentAlerts as alert}
            <li class="alert-item">
                <div class="alert-title" style="color: {alert.color}">
                    {alert.title}
                </div>
                <div class="alert-details">
                    {alert.type} · {alert.time} · {alert.user} · {alert.device}
                </div>
            </li>
        {/each}
    </ul>
</div>

<style>
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 2.2rem;
        margin: 2.5rem 0 0 0;
    }
    .alerts-card {
        background: var(--color-bg-card);
        border-radius: 16px;
        box-shadow: 0 2px 16px rgba(0, 0, 0, 0.18);
        margin-top: 2.5rem;
        padding: 2rem 2.2rem 1.2rem 2.2rem;
        max-width: 900px;
        width: 100%;
        border: 1.5px solid var(--color-border);
    }
    .alerts-header {
        color: var(--color-accent);
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
    }
    .alerts-list {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 1.1rem;
    }
    .alert-item {
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        padding-bottom: 0.7rem;
    }
    .alert-item:last-child {
        border-bottom: none;
    }
    .alert-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    .alert-details {
        color: var(--color-text-secondary);
        font-size: 0.98rem;
    }
</style>
