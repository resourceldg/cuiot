<script>
    import { goto } from "$app/navigation";
    import {
        getAlerts,
        getInstitutions,
        getPackages,
        getUsers,
    } from "$lib/api/index.js";
    import Button from "$lib/ui/Button.svelte";
    import MetricCard from "$lib/ui/MetricCard.svelte";
    import AdminIcon from "$lib/ui/icons/AdminIcon.svelte";
    import AlertIcon from "$lib/ui/icons/AlertIcon.svelte";
    import PackageIcon from "$lib/ui/icons/PackageIcon.svelte";
    import UserIcon from "$lib/ui/icons/UserIcon.svelte";
    import { onMount } from "svelte";

    let users = [];
    let institutions = [];
    let packages = [];
    let alerts = [];
    let loading = true;
    let error = null;

    onMount(async () => {
        await loadKPIData();
    });

    async function loadKPIData() {
        loading = true;
        try {
            const [usersData, institutionsData, packagesData, alertsData] =
                await Promise.all([
                    getUsers(),
                    getInstitutions(),
                    getPackages(),
                    getAlerts(),
                ]);

            users = usersData;
            institutions = institutionsData;
            packages = packagesData;
            alerts = alertsData;
        } catch (err) {
            error = err.message;
            console.error("Error loading KPI data:", err);
        } finally {
            loading = false;
        }
    }

    function goTo(section) {
        goto(`/dashboard/${section}`);
    }

    const criticalAlerts = alerts.filter((a) => a.severity === "critical");
</script>

<div class="kpi-row">
    <Button
        variant="plain"
        aria-label="Ver paquetes activos"
        on:click={() => goTo("packages")}
        class="kpi-action-btn"
        disabled={loading}
    >
        <MetricCard
            title="Paquetes activos"
            value={loading ? "..." : packages.length}
            icon={PackageIcon}
            color="var(--color-accent)"
            {loading}
        />
    </Button>

    <Button
        variant="plain"
        aria-label="Ver usuarios activos"
        on:click={() => goTo("users")}
        class="kpi-action-btn"
        disabled={loading}
    >
        <MetricCard
            title="Usuarios activos"
            value={loading ? "..." : users.length}
            icon={UserIcon}
            {loading}
        />
    </Button>

    <Button
        variant="plain"
        aria-label="Ver instituciones"
        on:click={() => goTo("institutions")}
        class="kpi-action-btn"
        disabled={loading}
    >
        <MetricCard
            title="Instituciones"
            value={loading ? "..." : (institutions?.length ?? 0)}
            icon={AdminIcon}
            {loading}
        />
    </Button>

    <Button
        variant="plain"
        aria-label="Ver alertas críticas"
        on:click={() => goTo("alerts")}
        class="kpi-action-btn"
        disabled={loading}
        style="position:relative;"
    >
        <MetricCard
            title="Alertas críticas"
            value={loading ? "..." : criticalAlerts.length}
            icon={AlertIcon}
            color="var(--color-error)"
            {loading}
        />
        {#if !loading && criticalAlerts.length > 0}
            <span class="kpi-badge" aria-label="Alertas críticas activas"
            ></span>
        {/if}
    </Button>
</div>

{#if error}
    <div class="kpi-error">
        <p>Error al cargar métricas: {error}</p>
        <button on:click={loadKPIData}>Reintentar</button>
    </div>
{/if}

<style>
    .kpi-row {
        display: flex;
        flex-direction: row;
        gap: var(--spacing-lg);
        margin-bottom: var(--spacing-xl);
        flex-wrap: nowrap;
    }
    .kpi-row > * {
        flex: 1 1 0;
        min-width: 200px;
        max-width: 100%;
    }
    .kpi-action-btn {
        display: block;
        width: 100%;
        background: none;
        border: none;
        padding: 0;
        border-radius: var(--border-radius);
        box-shadow: none;
        cursor: pointer;
        transition: transform 0.1s;
        position: relative;
        color: var(--color-accent);
    }
    .kpi-action-btn:focus {
        outline: 2px solid var(--color-accent);
    }
    .kpi-action-btn:hover:not(:disabled) {
        transform: translateY(-2px) scale(1.02);
    }
    .kpi-action-btn:disabled {
        cursor: not-allowed;
        opacity: 0.6;
    }
    .kpi-badge {
        position: absolute;
        top: 18px;
        right: 32px;
        width: 16px;
        height: 16px;
        background: var(--color-error);
        border-radius: 50%;
        border: 2px solid var(--color-bg-card);
        box-shadow: 0 0 8px var(--color-error);
        animation: badge-pulse 1.2s infinite cubic-bezier(0.4, 0, 0.6, 1);
        z-index: 2;
    }
    @keyframes badge-pulse {
        0% {
            box-shadow: 0 0 0 0 var(--color-error);
        }
        70% {
            box-shadow: 0 0 0 8px rgba(255, 77, 109, 0.2);
        }
        100% {
            box-shadow: 0 0 0 0 var(--color-error);
        }
    }
    .kpi-error {
        display: flex;
        align-items: center;
        gap: var(--spacing-md);
        padding: var(--spacing-md);
        background: rgba(255, 77, 109, 0.1);
        border: 1px solid var(--color-error);
        border-radius: var(--border-radius);
        margin-bottom: var(--spacing-lg);
    }
    .kpi-error button {
        background: var(--color-error);
        color: white;
        border: none;
        padding: var(--spacing-xs) var(--spacing-sm);
        border-radius: var(--border-radius-sm);
        cursor: pointer;
        font-size: 0.9rem;
    }
    .kpi-error button:hover {
        opacity: 0.9;
    }
    @media (max-width: 768px) {
        .kpi-row {
            flex-direction: column;
            gap: var(--spacing-md);
        }
        .kpi-row > * {
            min-width: 0;
        }
    }
</style>
