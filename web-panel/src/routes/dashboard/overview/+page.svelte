<script lang="ts">
    import {
        Activity,
        AlertTriangle,
        CheckCircle,
        Clock,
        Heart,
        MapPin,
        Shield,
        TrendingUp,
        Users,
        XCircle,
    } from "lucide-svelte";
    import { onMount } from "svelte";

    // Estado de la aplicación
    let loading = true;
    let error = "";

    // Datos del sistema
    let systemStats = {
        totalCaredPersons: 0,
        activeDevices: 0,
        activeAlerts: 0,
        totalEvents: 0,
        systemUptime: "99.8%",
        lastUpdate: new Date(),
    };

    let recentActivity = [];
    let quickActions = [
        {
            title: "Agregar Persona",
            description: "Registrar nueva persona bajo cuidado",
            icon: Users,
            action: () => console.log("Agregar persona"),
            color: "blue",
        },
        {
            title: "Configurar Dispositivo",
            description: "Instalar nuevo dispositivo IoT",
            icon: Activity,
            action: () => console.log("Configurar dispositivo"),
            color: "green",
        },
        {
            title: "Ver Alertas",
            description: "Revisar alertas activas",
            icon: AlertTriangle,
            action: () => console.log("Ver alertas"),
            color: "red",
        },
        {
            title: "Generar Reporte",
            description: "Crear reporte de actividad",
            icon: TrendingUp,
            action: () => console.log("Generar reporte"),
            color: "purple",
        },
    ];

    onMount(async () => {
        await loadSystemData();
    });

    async function loadSystemData() {
        try {
            loading = true;
            error = "";

            // Simular carga de datos del sistema
            // En producción, esto vendría de endpoints reales
            await new Promise((resolve) => setTimeout(resolve, 1000));

            systemStats = {
                totalCaredPersons: 12,
                activeDevices: 8,
                activeAlerts: 3,
                totalEvents: 156,
                systemUptime: "99.8%",
                lastUpdate: new Date(),
            };

            recentActivity = [
                {
                    id: 1,
                    type: "alert",
                    message: "Alerta de caída detectada - María González",
                    time: "2 minutos",
                    severity: "high",
                },
                {
                    id: 2,
                    type: "device",
                    message: "Dispositivo IoT reconectado - Sensor 001",
                    time: "5 minutos",
                    severity: "low",
                },
                {
                    id: 3,
                    type: "care",
                    message: "Medicamento administrado - Juan Pérez",
                    time: "15 minutos",
                    severity: "medium",
                },
                {
                    id: 4,
                    type: "location",
                    message: "Persona fuera de zona segura - Ana López",
                    time: "1 hora",
                    severity: "high",
                },
            ];
        } catch (err: any) {
            error = `Error al cargar datos: ${err.message}`;
            console.error("Error loading system data:", err);
        } finally {
            loading = false;
        }
    }

    function getSeverityColor(severity: string) {
        switch (severity) {
            case "high":
                return "text-red-600 bg-red-100";
            case "medium":
                return "text-yellow-600 bg-yellow-100";
            case "low":
                return "text-green-600 bg-green-100";
            default:
                return "text-gray-600 bg-gray-100";
        }
    }

    function getActivityIcon(type: string) {
        switch (type) {
            case "alert":
                return AlertTriangle;
            case "device":
                return Activity;
            case "care":
                return Heart;
            case "location":
                return MapPin;
            default:
                return Activity;
        }
    }

    function formatTime(date: Date) {
        return date.toLocaleTimeString("es-ES", {
            hour: "2-digit",
            minute: "2-digit",
        });
    }
</script>

<svelte:head>
    <title>Vista General - CUIOT</title>
</svelte:head>

<div class="overview-container">
    {#if error}
        <div class="error-banner">
            <XCircle class="w-5 h-5" />
            <span>{error}</span>
        </div>
    {/if}

    <!-- Header con estadísticas principales -->
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon blue">
                <Users class="w-6 h-6" />
            </div>
            <div class="stat-content">
                <h3 class="stat-number">{systemStats.totalCaredPersons}</h3>
                <p class="stat-label">Personas Bajo Cuidado</p>
                <p class="stat-change positive">+2 este mes</p>
            </div>
        </div>

        <div class="stat-card">
            <div class="stat-icon green">
                <Activity class="w-6 h-6" />
            </div>
            <div class="stat-content">
                <h3 class="stat-number">{systemStats.activeDevices}</h3>
                <p class="stat-label">Dispositivos Activos</p>
                <p class="stat-change positive">100% operativos</p>
            </div>
        </div>

        <div class="stat-card">
            <div class="stat-icon red">
                <AlertTriangle class="w-6 h-6" />
            </div>
            <div class="stat-content">
                <h3 class="stat-number">{systemStats.activeAlerts}</h3>
                <p class="stat-label">Alertas Activas</p>
                <p class="stat-change neutral">Requieren atención</p>
            </div>
        </div>

        <div class="stat-card">
            <div class="stat-icon purple">
                <TrendingUp class="w-6 h-6" />
            </div>
            <div class="stat-content">
                <h3 class="stat-number">{systemStats.totalEvents}</h3>
                <p class="stat-label">Eventos Totales</p>
                <p class="stat-change positive">+24 hoy</p>
            </div>
        </div>
    </div>

    <!-- Sistema de estado -->
    <div class="system-status-card">
        <div class="status-header">
            <h2>Estado del Sistema</h2>
            <div class="status-indicator online">
                <div class="status-dot"></div>
                <span>Sistema Online</span>
            </div>
        </div>

        <div class="status-grid">
            <div class="status-item">
                <Shield class="w-5 h-5 text-green-600" />
                <div>
                    <p class="status-label">Seguridad</p>
                    <p class="status-value">Activa</p>
                </div>
            </div>

            <div class="status-item">
                <Clock class="w-5 h-5 text-blue-600" />
                <div>
                    <p class="status-label">Uptime</p>
                    <p class="status-value">{systemStats.systemUptime}</p>
                </div>
            </div>

            <div class="status-item">
                <CheckCircle class="w-5 h-5 text-green-600" />
                <div>
                    <p class="status-label">Última Actualización</p>
                    <p class="status-value">
                        {formatTime(systemStats.lastUpdate)}
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- Contenido principal -->
    <div class="main-content-grid">
        <!-- Actividad Reciente -->
        <div class="content-card">
            <div class="card-header">
                <h2>Actividad Reciente</h2>
                <button
                    class="refresh-btn"
                    on:click={loadSystemData}
                    disabled={loading}
                >
                    {#if loading}
                        <div class="loading-spinner"></div>
                    {:else}
                        <Activity class="w-4 h-4" />
                    {/if}
                </button>
            </div>

            <div class="activity-list">
                {#if recentActivity.length > 0}
                    {#each recentActivity as activity}
                        <div class="activity-item">
                            <div class="activity-icon">
                                <svelte:component
                                    this={getActivityIcon(activity.type)}
                                    class="w-4 h-4"
                                />
                            </div>
                            <div class="activity-content">
                                <p class="activity-message">
                                    {activity.message}
                                </p>
                                <p class="activity-time">{activity.time}</p>
                            </div>
                            <span
                                class="severity-badge {getSeverityColor(
                                    activity.severity,
                                )}"
                            >
                                {activity.severity}
                            </span>
                        </div>
                    {/each}
                {:else}
                    <div class="empty-state">
                        <Activity class="w-8 h-8 text-gray-400" />
                        <p>No hay actividad reciente</p>
                    </div>
                {/if}
            </div>
        </div>

        <!-- Acciones Rápidas -->
        <div class="content-card">
            <div class="card-header">
                <h2>Acciones Rápidas</h2>
            </div>

            <div class="quick-actions-grid">
                {#each quickActions as action}
                    <button
                        class="quick-action-btn {action.color}"
                        on:click={action.action}
                    >
                        <div class="action-icon">
                            <svelte:component
                                this={action.icon}
                                class="w-5 h-5"
                            />
                        </div>
                        <div class="action-content">
                            <h3>{action.title}</h3>
                            <p>{action.description}</p>
                        </div>
                    </button>
                {/each}
            </div>
        </div>
    </div>
</div>

<style>
    .overview-container {
        max-width: 1200px;
        margin: 0 auto;
    }

    .error-banner {
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #dc2626;
        padding: 1rem;
        border-radius: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 2rem;
    }

    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .stat-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .stat-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
    }

    .stat-icon.blue {
        background: linear-gradient(135deg, #3b82f6, #1e40af);
    }
    .stat-icon.green {
        background: linear-gradient(135deg, #10b981, #059669);
    }
    .stat-icon.red {
        background: linear-gradient(135deg, #ef4444, #dc2626);
    }
    .stat-icon.purple {
        background: linear-gradient(135deg, #8b5cf6, #7c3aed);
    }

    .stat-content {
        flex: 1;
    }

    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        color: #1f2937;
        margin: 0;
        line-height: 1;
    }

    .stat-label {
        color: #6b7280;
        font-size: 0.875rem;
        margin: 0.25rem 0;
    }

    .stat-change {
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0;
    }

    .stat-change.positive {
        color: #10b981;
    }
    .stat-change.negative {
        color: #ef4444;
    }
    .stat-change.neutral {
        color: #6b7280;
    }

    /* System Status */
    .system-status-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 2rem;
    }

    .status-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .status-header h2 {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }

    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.875rem;
        font-weight: 500;
    }

    .status-indicator.online {
        color: #10b981;
    }
    .status-indicator.offline {
        color: #ef4444;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: currentColor;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
    }

    .status-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }

    .status-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem;
        background: #f9fafb;
        border-radius: 0.75rem;
    }

    .status-label {
        font-size: 0.875rem;
        color: #6b7280;
        margin: 0;
    }

    .status-value {
        font-size: 0.875rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0;
    }

    /* Main Content Grid */
    .main-content-grid {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 2rem;
    }

    .content-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .card-header h2 {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }

    .refresh-btn {
        background: none;
        border: none;
        color: #6b7280;
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 0.5rem;
        transition: all 0.2s ease;
    }

    .refresh-btn:hover:not(:disabled) {
        background: #f3f4f6;
        color: #374151;
    }

    .loading-spinner {
        width: 16px;
        height: 16px;
        border: 2px solid rgba(107, 114, 128, 0.3);
        border-top: 2px solid #6b7280;
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

    /* Activity List */
    .activity-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .activity-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem;
        background: #f9fafb;
        border-radius: 0.75rem;
        transition: background 0.2s ease;
    }

    .activity-item:hover {
        background: #f3f4f6;
    }

    .activity-icon {
        width: 32px;
        height: 32px;
        background: white;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #6b7280;
    }

    .activity-content {
        flex: 1;
    }

    .activity-message {
        font-size: 0.875rem;
        color: #1f2937;
        margin: 0;
        font-weight: 500;
    }

    .activity-time {
        font-size: 0.75rem;
        color: #6b7280;
        margin: 0.25rem 0 0 0;
    }

    .severity-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 0.375rem;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: capitalize;
    }

    .empty-state {
        text-align: center;
        padding: 2rem;
        color: #6b7280;
    }

    .empty-state p {
        margin: 0.5rem 0 0 0;
        font-size: 0.875rem;
    }

    /* Quick Actions */
    .quick-actions-grid {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .quick-action-btn {
        background: none;
        border: 1px solid #e5e7eb;
        border-radius: 0.75rem;
        padding: 1rem;
        cursor: pointer;
        text-align: left;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .quick-action-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .quick-action-btn.blue:hover {
        border-color: #3b82f6;
    }
    .quick-action-btn.green:hover {
        border-color: #10b981;
    }
    .quick-action-btn.red:hover {
        border-color: #ef4444;
    }
    .quick-action-btn.purple:hover {
        border-color: #8b5cf6;
    }

    .action-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
    }

    .quick-action-btn.blue .action-icon {
        background: #3b82f6;
    }
    .quick-action-btn.green .action-icon {
        background: #10b981;
    }
    .quick-action-btn.red .action-icon {
        background: #ef4444;
    }
    .quick-action-btn.purple .action-icon {
        background: #8b5cf6;
    }

    .action-content h3 {
        font-size: 0.875rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0;
    }

    .action-content p {
        font-size: 0.75rem;
        color: #6b7280;
        margin: 0.25rem 0 0 0;
    }

    /* Responsive */
    @media (max-width: 1024px) {
        .main-content-grid {
            grid-template-columns: 1fr;
        }
    }

    @media (max-width: 768px) {
        .stats-grid {
            grid-template-columns: 1fr;
        }

        .status-grid {
            grid-template-columns: 1fr;
        }

        .overview-container {
            padding: 0 1rem;
        }
    }
</style>
