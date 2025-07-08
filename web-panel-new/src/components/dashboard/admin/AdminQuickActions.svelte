<script>
    import { goto } from "$app/navigation";
    import Card from "$lib/ui/Card.svelte";
    import AdminIcon from "$lib/ui/icons/AdminIcon.svelte";
    import DeviceIcon from "$lib/ui/icons/DeviceIcon.svelte";
    import PackageIcon from "$lib/ui/icons/PackageIcon.svelte";
    import ReportIcon from "$lib/ui/icons/ReportIcon.svelte";
    import SettingsIcon from "$lib/ui/icons/SettingsIcon.svelte";
    import UserIcon from "$lib/ui/icons/UserIcon.svelte";

    const quickActions = [
        {
            label: "Paquetes",
            icon: PackageIcon,
            action: () => goto("/dashboard/packages"),
            description: "Gestionar paquetes de servicios",
        },
        {
            label: "Usuarios",
            icon: UserIcon,
            action: () => goto("/dashboard/users"),
            description: "Administrar usuarios del sistema",
        },
        {
            label: "Instituciones",
            icon: AdminIcon,
            action: () => goto("/dashboard/institutions"),
            description: "Gestionar instituciones",
        },
        {
            label: "Dispositivos",
            icon: DeviceIcon,
            action: () => goto("/dashboard/devices"),
            description: "Monitorear dispositivos IoT",
        },
        {
            label: "Reportes",
            icon: ReportIcon,
            action: () => goto("/dashboard/reports"),
            description: "Ver reportes y analytics",
        },
        {
            label: "Configuración",
            icon: SettingsIcon,
            action: () => goto("/dashboard/settings"),
            description: "Configuración del sistema",
        },
    ];
</script>

<Card style="flex:1; min-width:260px; margin-left:var(--spacing-lg);">
    <h3 style="margin-bottom:var(--spacing-md);">Gestión rápida</h3>

    <div class="quick-actions">
        {#each quickActions as action}
            <button
                class="quick-action-btn"
                on:click={action.action}
                title={action.description}
            >
                <div class="action-icon">
                    <svelte:component this={action.icon} size={20} />
                </div>
                <div class="action-content">
                    <span class="action-label">{action.label}</span>
                    <span class="action-description">{action.description}</span>
                </div>
            </button>
        {/each}
    </div>

    <div class="quick-stats">
        <div class="stat-item">
            <span class="stat-label">Sistema</span>
            <span class="stat-value">Operativo</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Última actualización</span>
            <span class="stat-value">Hace 2 min</span>
        </div>
    </div>
</Card>

<style>
    .quick-actions {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-sm);
        margin-bottom: var(--spacing-lg);
    }

    .quick-action-btn {
        display: flex;
        align-items: center;
        gap: var(--spacing-md);
        background: var(--color-bg-card);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        padding: var(--spacing-md);
        font-size: 1rem;
        color: var(--color-text);
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
        width: 100%;
    }

    .quick-action-btn:hover {
        background: var(--color-bg-hover);
        border-color: var(--color-accent);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 230, 118, 0.1);
    }

    .action-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        background: var(--color-bg-hover);
        border-radius: var(--border-radius-sm);
        color: var(--color-accent);
        flex-shrink: 0;
    }

    .action-content {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-xs);
        flex: 1;
    }

    .action-label {
        font-weight: 600;
        color: var(--color-text);
    }

    .action-description {
        font-size: 0.85rem;
        color: var(--color-text-secondary);
        line-height: 1.3;
    }

    .quick-stats {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-sm);
        padding-top: var(--spacing-md);
        border-top: 1px solid var(--color-border);
    }

    .stat-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--spacing-xs) 0;
    }

    .stat-label {
        font-size: 0.9rem;
        color: var(--color-text-secondary);
    }

    .stat-value {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--color-success);
    }

    @media (max-width: 768px) {
        .quick-action-btn {
            justify-content: flex-start;
        }

        .action-content {
            min-width: 0;
        }

        .action-description {
            display: none;
        }
    }
</style>
