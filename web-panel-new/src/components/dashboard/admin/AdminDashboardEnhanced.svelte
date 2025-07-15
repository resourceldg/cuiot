<script lang="ts">
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
    // Importar APIs para cargar métricas
    import {
        getAlerts,
        getAlertTypes,
        getCaredPersons,
        getDevices,
        getDeviceTypes,
        getInstitutions,
        getPackages,
        getStatusTypes,
        getUsers,
    } from "$lib/api/index.js";

    // Estados de carga
    let dashboardLoading = true;
    let dashboardError = null;
    let showUserGuide = false;

    // Métricas por módulo
    let coreMetrics = {
        statusTypesCount: 0,
        deviceTypesCount: 0,
        alertTypesCount: 0,
    };

    let careMetrics = {
        caredPersonsCount: 0,
        assignmentsCount: 0,
        observationsToday: 0,
    };

    let iotMetrics = {
        activeDevicesCount: 0,
        eventsToday: 0,
        criticalAlertsCount: 0,
    };

    let businessMetrics = {
        institutionsCount: 0,
        activePackagesCount: 0,
        activeUsersCount: 0,
        monthlyBilling: 0,
    };

    let scoringMetrics = {
        avgScore: 0,
        pendingReviews: 0,
    };

    let monitoringMetrics = {
        reportsGenerated: 0,
    };

    onMount(async () => {
        try {
            await loadAllMetrics();
            dashboardLoading = false;
        } catch (error) {
            dashboardError = error.message;
            dashboardLoading = false;
        }
    });

    async function loadAllMetrics() {
        try {
            // Cargar métricas del módulo Core
            const [statusTypes, deviceTypes, alertTypes] = await Promise.all([
                getStatusTypes({ is_active: true }),
                getDeviceTypes({ is_active: true }),
                getAlertTypes({ is_active: true }),
            ]);

            coreMetrics = {
                statusTypesCount: statusTypes.data?.length || 0,
                deviceTypesCount: deviceTypes.data?.length || 0,
                alertTypesCount: alertTypes.data?.length || 0,
            };

            // Cargar métricas del módulo Care
            const caredPersons = await getCaredPersons({ is_active: true });
            careMetrics = {
                caredPersonsCount: caredPersons.data?.length || 0,
                assignmentsCount: 0, // TODO: Implementar cuando esté la API
                observationsToday: 0, // TODO: Implementar cuando esté la API
            };

            // Cargar métricas del módulo IoT
            const [devices, alerts] = await Promise.all([
                getDevices({ is_active: true }),
                getAlerts(),
            ]);

            const criticalAlerts = alerts.filter(
                (a: any) => a.severity === "critical",
            );
            iotMetrics = {
                activeDevicesCount: devices.data?.length || 0,
                eventsToday: 0, // TODO: Implementar cuando esté la API
                criticalAlertsCount: criticalAlerts.length,
            };

            // Cargar métricas del módulo Business
            const [users, institutions, packages] = await Promise.all([
                getUsers({ is_active: true }),
                getInstitutions(),
                getPackages(),
            ]);

            businessMetrics = {
                institutionsCount: institutions.length || 0,
                activePackagesCount: packages.length || 0,
                activeUsersCount: users.data?.length || 0,
                monthlyBilling: 0, // TODO: Implementar cuando esté la API
            };

            // Métricas de Scoring y Monitoring (placeholder)
            scoringMetrics = {
                avgScore: 4.2, // TODO: Implementar cuando esté la API
                pendingReviews: 0, // TODO: Implementar cuando esté la API
            };

            monitoringMetrics = {
                reportsGenerated: 0, // TODO: Implementar cuando esté la API
            };
        } catch (error) {
            console.error("Error loading metrics:", error);
            throw error;
        }
    }

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
            case "manageCore":
                goto("/dashboard/core");
                break;
            case "manageCare":
                goto("/dashboard/care");
                break;
            case "manageIoT":
                goto("/dashboard/iot");
                break;
            case "manageBusiness":
                goto("/dashboard/business");
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
        <!-- Header y KPIs principales -->
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

        <!-- Alertas críticas -->
        <div class="dashboard-section dashboard-alerts">
            <AdminCriticalAlerts />
        </div>

        <!-- Acciones rápidas -->
        <div class="dashboard-section dashboard-quickactions">
            <AdminQuickActions
                on:showUserGuide={handleQuickAction}
                on:createUser={handleQuickAction}
                on:manageUsers={handleQuickAction}
                on:systemSettings={handleQuickAction}
                on:manageCore={handleQuickAction}
                on:manageCare={handleQuickAction}
                on:manageIoT={handleQuickAction}
                on:manageBusiness={handleQuickAction}
            />
        </div>

        <!-- Métricas por módulo -->
        <div class="dashboard-section dashboard-metrics">
            <div class="metrics-grid">
                <!-- Módulo Core -->
                <div class="metric-module">
                    <h3>📋 Catálogos</h3>
                    <div class="metric-cards">
                        <div class="metric-card" on:click={() => goTo("core")}>
                            <span class="metric-value"
                                >{coreMetrics.statusTypesCount}</span
                            >
                            <span class="metric-label">Tipos de Estado</span>
                        </div>
                        <div class="metric-card" on:click={() => goTo("core")}>
                            <span class="metric-value"
                                >{coreMetrics.deviceTypesCount}</span
                            >
                            <span class="metric-label"
                                >Tipos de Dispositivos</span
                            >
                        </div>
                        <div class="metric-card" on:click={() => goTo("core")}>
                            <span class="metric-value"
                                >{coreMetrics.alertTypesCount}</span
                            >
                            <span class="metric-label">Tipos de Alertas</span>
                        </div>
                    </div>
                </div>

                <!-- Módulo Care -->
                <div class="metric-module">
                    <h3>🏥 Cuidados</h3>
                    <div class="metric-cards">
                        <div class="metric-card" on:click={() => goTo("care")}>
                            <span class="metric-value"
                                >{careMetrics.caredPersonsCount}</span
                            >
                            <span class="metric-label">Personas Cuidadas</span>
                        </div>
                        <div class="metric-card" on:click={() => goTo("care")}>
                            <span class="metric-value"
                                >{careMetrics.assignmentsCount}</span
                            >
                            <span class="metric-label"
                                >Asignaciones Activas</span
                            >
                        </div>
                        <div class="metric-card" on:click={() => goTo("care")}>
                            <span class="metric-value"
                                >{careMetrics.observationsToday}</span
                            >
                            <span class="metric-label">Observaciones Hoy</span>
                        </div>
                    </div>
                </div>

                <!-- Módulo IoT -->
                <div class="metric-module">
                    <h3>📱 IoT</h3>
                    <div class="metric-cards">
                        <div
                            class="metric-card"
                            on:click={() => goTo("devices")}
                        >
                            <span class="metric-value"
                                >{iotMetrics.activeDevicesCount}</span
                            >
                            <span class="metric-label"
                                >Dispositivos Activos</span
                            >
                        </div>
                        <div
                            class="metric-card"
                            on:click={() => goTo("events")}
                        >
                            <span class="metric-value"
                                >{iotMetrics.eventsToday}</span
                            >
                            <span class="metric-label">Eventos Hoy</span>
                        </div>
                        <div
                            class="metric-card critical"
                            on:click={() => goTo("alerts")}
                        >
                            <span class="metric-value"
                                >{iotMetrics.criticalAlertsCount}</span
                            >
                            <span class="metric-label">Alertas Críticas</span>
                        </div>
                    </div>
                </div>

                <!-- Módulo Business -->
                <div class="metric-module">
                    <h3>💼 Negocio</h3>
                    <div class="metric-cards">
                        <div
                            class="metric-card"
                            on:click={() => goTo("institutions")}
                        >
                            <span class="metric-value"
                                >{businessMetrics.institutionsCount}</span
                            >
                            <span class="metric-label">Instituciones</span>
                        </div>
                        <div
                            class="metric-card"
                            on:click={() => goTo("packages")}
                        >
                            <span class="metric-value"
                                >{businessMetrics.activePackagesCount}</span
                            >
                            <span class="metric-label">Paquetes Activos</span>
                        </div>
                        <div class="metric-card" on:click={() => goTo("users")}>
                            <span class="metric-value"
                                >{businessMetrics.activeUsersCount}</span
                            >
                            <span class="metric-label">Usuarios Activos</span>
                        </div>
                    </div>
                </div>

                <!-- Módulo Scoring -->
                <div class="metric-module">
                    <h3>⭐ Calificaciones</h3>
                    <div class="metric-cards">
                        <div
                            class="metric-card"
                            on:click={() => goTo("scoring")}
                        >
                            <span class="metric-value"
                                >{scoringMetrics.avgScore}</span
                            >
                            <span class="metric-label"
                                >Calificación Promedio</span
                            >
                        </div>
                        <div
                            class="metric-card"
                            on:click={() => goTo("scoring")}
                        >
                            <span class="metric-value"
                                >{scoringMetrics.pendingReviews}</span
                            >
                            <span class="metric-label">Reseñas Pendientes</span>
                        </div>
                    </div>
                </div>

                <!-- Módulo Monitoring -->
                <div class="metric-module">
                    <h3>📊 Monitoreo</h3>
                    <div class="metric-cards">
                        <div
                            class="metric-card"
                            on:click={() => goTo("reports")}
                        >
                            <span class="metric-value"
                                >{monitoringMetrics.reportsGenerated}</span
                            >
                            <span class="metric-label">Reportes Generados</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Notificaciones -->
        <div class="dashboard-section dashboard-notifications">
            <AdminNotificationsPanel />
        </div>

        <!-- Actividad del sistema -->
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
            "header header"
            "alerts quickactions"
            "metrics metrics"
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

    .dashboard-metrics {
        grid-area: metrics;
        background: var(--color-bg-card);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-md);
        padding: var(--spacing-xl);
    }

    .dashboard-notifications {
        grid-area: notifications;
    }

    .dashboard-activity {
        grid-area: activity;
        width: 100%;
        background: var(--color-bg-card);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-md);
        padding: var(--spacing-xl) var(--spacing-lg);
    }

    .dashboard-section {
        min-width: 0;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: var(--spacing-lg);
    }

    .metric-module {
        background: var(--color-bg-hover);
        border-radius: var(--border-radius);
        padding: var(--spacing-lg);
        border: 1px solid var(--color-border);
    }

    .metric-module h3 {
        margin: 0 0 var(--spacing-md) 0;
        color: var(--color-accent);
        font-size: 1.1rem;
        font-weight: 600;
    }

    .metric-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: var(--spacing-md);
    }

    .metric-card {
        background: var(--color-bg-card);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        padding: var(--spacing-md);
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
    }

    .metric-card:hover {
        border-color: var(--color-accent);
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }

    .metric-card.critical {
        border-color: var(--color-danger);
        background: rgba(255, 77, 109, 0.1);
    }

    .metric-card.critical:hover {
        border-color: var(--color-danger);
        background: rgba(255, 77, 109, 0.2);
    }

    .metric-value {
        display: block;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--color-accent);
        margin-bottom: var(--spacing-xs);
    }

    .metric-card.critical .metric-value {
        color: var(--color-danger);
    }

    .metric-label {
        display: block;
        font-size: 0.9rem;
        color: var(--color-text-secondary);
        font-weight: 500;
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

    @media (max-width: 1024px) {
        .admin-dashboard-grid {
            grid-template-columns: 1fr;
            grid-template-areas:
                "header"
                "alerts"
                "quickactions"
                "metrics"
                "notifications"
                "activity";
            padding: var(--spacing-md);
        }

        .metrics-grid {
            grid-template-columns: 1fr;
        }

        .metric-cards {
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        }

        .dashboard-activity {
            width: 100%;
            padding: var(--spacing-lg) var(--spacing-md);
        }
    }

    @media (max-width: 768px) {
        .metric-cards {
            grid-template-columns: 1fr;
        }

        .metric-module {
            padding: var(--spacing-md);
        }
    }
</style>
