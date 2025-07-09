<script>
    import { goto } from "$app/navigation";
    import AdminIcon from "$lib/ui/icons/AdminIcon.svelte";
    import { onMount } from "svelte";
    import SectionHeader from "../../shared/ui/SectionHeader.svelte";
    import AdminActivityChart from "./AdminActivityChart.svelte";
    import AdminCriticalAlerts from "./AdminCriticalAlerts.svelte";
    import AdminKPIRow from "./AdminKPIRow.svelte";
    import AdminNotificationsPanel from "./AdminNotificationsPanel.svelte";
    import AdminQuickActions from "./AdminQuickActions.svelte";
    import UserHierarchyGuide from "./UserHierarchyGuide.svelte";

    // Estados de carga
    let dashboardLoading = true;
    let dashboardError = null;
    let showUserGuide = false;

    onMount(async () => {
        try {
            // Aquí se cargarían todos los datos del dashboard
            await new Promise((resolve) => setTimeout(resolve, 1000)); // Simulación
            dashboardLoading = false;
        } catch (error) {
            dashboardError = error.message;
            dashboardLoading = false;
        }
    });

    function goTo(section) {
        goto(`/dashboard/${section}`);
    }

    function handleQuickAction(event) {
        switch (event.detail) {
            case "showUserGuide":
                showUserGuide = true;
                break;
            case "createUser":
                goto("/dashboard/users/create");
                break;
            case "manageUsers":
                goto("/dashboard/users");
                break;
            case "systemSettings":
                goto("/dashboard/settings");
                break;
        }
    }

    function closeUserGuide() {
        showUserGuide = false;
    }
</script>

<svelte:head>
    <title>Panel de Administración - Sistema de Cuidado</title>
</svelte:head>

{#if dashboardLoading}
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <p>Cargando dashboard...</p>
    </div>
{:else if dashboardError}
    <div class="error-container">
        <p>Error al cargar el dashboard: {dashboardError}</p>
        <button on:click={() => window.location.reload()}>Reintentar</button>
    </div>
{:else}
    <div class="admin-dashboard-grid">
        <div class="dashboard-section dashboard-alerts">
            <AdminCriticalAlerts />
        </div>
        <div class="dashboard-section dashboard-quickactions">
            <AdminQuickActions
                on:showUserGuide={handleQuickAction}
                on:createUser={handleQuickAction}
                on:manageUsers={handleQuickAction}
                on:systemSettings={handleQuickAction}
            />
        </div>
        <div class="admin-dashboard-header">
            <SectionHeader
                title="Panel de Administración"
                subtitle="Gestión integral del sistema"
            >
                <span slot="icon">
                    <AdminIcon size={32} />
                </span>
            </SectionHeader>
            <AdminKPIRow />
        </div>
        <div class="dashboard-section dashboard-notifications">
            <AdminNotificationsPanel />
        </div>
        <div class="dashboard-section dashboard-activity">
            <AdminActivityChart />
        </div>
    </div>
{/if}

<!-- Modal de Guía de Jerarquía -->
{#if showUserGuide}
    <div class="modal-overlay" on:click={closeUserGuide}>
        <div class="modal-content" on:click|stopPropagation>
            <UserHierarchyGuide on:close={closeUserGuide} />
        </div>
    </div>
{/if}

<style>
    .admin-dashboard-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-areas:
            "alerts quickactions"
            "header header"
            "notifications notifications"
            "activity activity";
        gap: var(--spacing-xl);
        max-width: 1400px;
        margin: 0 auto;
        padding: var(--spacing-lg);
    }
    .admin-dashboard-header {
        grid-area: header;
    }
    .dashboard-alerts {
        grid-area: alerts;
    }
    .dashboard-quickactions {
        grid-area: quickactions;
    }
    .dashboard-notifications {
        grid-area: notifications;
    }
    .dashboard-activity {
        grid-area: activity;
        /* Eliminar max-width y centrado */
        width: 100%;
        background: var(--color-bg-card);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-md);
        padding: var(--spacing-xl) var(--spacing-lg);
    }
    .dashboard-section {
        min-width: 0;
    }
    @media (max-width: 1024px) {
        .admin-dashboard-grid {
            grid-template-columns: 1fr;
            grid-template-areas:
                "alerts"
                "quickactions"
                "header"
                "notifications"
                "activity";
            padding: var(--spacing-md);
        }
        .dashboard-activity {
            width: 100%;
            padding: var(--spacing-lg) var(--spacing-md);
        }
    }

    .loading-container,
    .error-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 400px;
        gap: var(--spacing-md);
    }

    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid var(--color-border);
        border-top: 4px solid var(--color-accent);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    .error-container button {
        background: var(--color-accent);
        color: var(--color-bg);
        border: none;
        padding: var(--spacing-sm) var(--spacing-md);
        border-radius: var(--border-radius);
        cursor: pointer;
        font-weight: 500;
    }

    .error-container button:hover {
        opacity: 0.9;
    }

    /* Modal styles */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        padding: var(--spacing-md);
    }

    .modal-content {
        max-width: 90vw;
        max-height: 90vh;
        overflow: auto;
    }
</style>
