<script>
    import {
        deleteAlert as deleteAlertApi,
        getAlerts,
        getInstitutions,
        getPackages,
        getUsers,
        markAlertAsRead as markAlertAsReadApi,
    } from "$lib/api/index.js";
    import Card from "$lib/ui/Card.svelte";
    import DataTable from "$lib/ui/DataTable.svelte";
    import AdminIcon from "$lib/ui/icons/AdminIcon.svelte";
    import AlertIcon from "$lib/ui/icons/AlertIcon.svelte";
    import EditIcon from "$lib/ui/icons/EditIcon.svelte";
    import EyeIcon from "$lib/ui/icons/EyeIcon.svelte";
    import NotificationIcon from "$lib/ui/icons/NotificationIcon.svelte";
    import PackageIcon from "$lib/ui/icons/PackageIcon.svelte";
    import TrashIcon from "$lib/ui/icons/TrashIcon.svelte";
    import UserIcon from "$lib/ui/icons/UserIcon.svelte";
    import MetricCard from "$lib/ui/MetricCard.svelte";
    import SectionHeader from "$lib/ui/SectionHeader.svelte";
    import { onMount } from "svelte";

    let users = [];
    let institutions = [];
    let packageRows = [];
    let alerts = [];
    let usersLoading = false;
    let institutionsLoading = false;
    let packagesLoading = false;
    let alertsLoading = false;
    let usersError = null;
    let institutionsError = null;
    let packagesError = null;
    let alertsError = null;

    const alertColumns = [
        { key: "title", label: "Título", sortable: true },
        { key: "severity", label: "Severidad", sortable: true },
        { key: "created_at", label: "Fecha", sortable: true },
    ];

    onMount(async () => {
        await loadDashboardData();
    });

    async function loadDashboardData() {
        // Load users
        usersLoading = true;
        try {
            users = await getUsers();
        } catch (error) {
            usersError = error.message;
            console.error("Error loading users:", error);
        } finally {
            usersLoading = false;
        }

        // Load institutions
        institutionsLoading = true;
        try {
            institutions = await getInstitutions();
        } catch (error) {
            institutionsError = error.message;
            console.error("Error loading institutions:", error);
        } finally {
            institutionsLoading = false;
        }

        // Load packages
        packagesLoading = true;
        try {
            packageRows = await getPackages();
        } catch (error) {
            packagesError = error.message;
            console.error("Error loading packages:", error);
        } finally {
            packagesLoading = false;
        }

        // Load alerts
        alertsLoading = true;
        try {
            alerts = await getAlerts();
        } catch (error) {
            alertsError = error.message;
            console.error("Error loading alerts:", error);
        } finally {
            alertsLoading = false;
        }
    }

    async function deleteAlert(id) {
        try {
            await deleteAlertApi(id);
            alerts = alerts.filter((alert) => alert.id !== id);
        } catch (error) {
            console.error("Error deleting alert:", error);
        }
    }

    async function markAlertAsRead(id) {
        try {
            await markAlertAsReadApi(id);
            alerts = alerts.map((alert) =>
                alert.id === id ? { ...alert, read: true } : alert,
            );
        } catch (error) {
            console.error("Error marking alert as read:", error);
        }
    }
</script>

<svelte:head>
    <title>Panel de Administración - Sistema de Cuidado</title>
</svelte:head>

<div class="admin-dashboard">
    <SectionHeader
        title="Panel de Administración"
        subtitle="Gestión integral del sistema"
    >
        <span slot="icon">
            <AdminIcon size={32} />
        </span>
    </SectionHeader>

    <div class="dashboard-kpi-row">
        <MetricCard
            title="Paquetes activos"
            value={packageRows.length}
            icon={PackageIcon}
            color="var(--color-accent)"
        />
        <MetricCard
            title="Usuarios activos"
            value={users.length}
            icon={UserIcon}
        />
        <MetricCard
            title="Instituciones"
            value={institutions?.length ?? 0}
            icon={AdminIcon}
        />
        <MetricCard
            title="Alertas críticas"
            value={alerts.filter((a) => a.severity === "critical").length}
            icon={AlertIcon}
            color="var(--color-error)"
        />
    </div>

    <div class="dashboard-section-row">
        <Card style="flex:2; min-width:320px;">
            <h3
                style="margin-bottom:var(--spacing-md); display:flex; align-items:center;"
            >
                <NotificationIcon
                    size={20}
                    style="margin-right:var(--spacing-sm);"
                /> Notificaciones recientes
            </h3>
            <DataTable
                columns={alertColumns}
                rows={alerts.slice(0, 5)}
                loading={alertsLoading}
                error={alertsError}
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
                        ><EyeIcon size={18} /></button
                    >
                    <button
                        class="action-btn"
                        title="Marcar como leída"
                        aria-label="Marcar como leída"
                        on:click={() => markAlertAsRead(row.id)}
                        style="color:var(--color-success)"
                        ><EditIcon size={18} /></button
                    >
                    <button
                        class="action-btn"
                        title="Eliminar"
                        aria-label="Eliminar notificación"
                        on:click={() => deleteAlert(row.id)}
                        style="color:var(--color-error)"
                        ><TrashIcon size={18} /></button
                    >
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
        <Card style="flex:1; min-width:260px; margin-left:var(--spacing-lg);">
            <h3 style="margin-bottom:var(--spacing-md);">Gestión rápida</h3>
            <div class="quick-actions">
                <button
                    class="quick-action-btn"
                    on:click={() => {
                        /* ir a paquetes */
                    }}><PackageIcon size={20} /> Paquetes</button
                >
                <button
                    class="quick-action-btn"
                    on:click={() => {
                        /* ir a usuarios */
                    }}><UserIcon size={20} /> Usuarios</button
                >
                <button
                    class="quick-action-btn"
                    on:click={() => {
                        /* ir a instituciones */
                    }}><AdminIcon size={20} /> Instituciones</button
                >
            </div>
        </Card>
    </div>
</div>

<style>
    .admin-dashboard {
        padding: var(--spacing-lg);
        max-width: 1400px;
        margin: 0 auto;
    }

    .dashboard-kpi-row {
        display: flex;
        gap: var(--spacing-lg);
        margin-bottom: var(--spacing-xl);
    }

    .dashboard-section-row {
        display: flex;
        gap: var(--spacing-xl);
        align-items: flex-start;
    }

    .quick-actions {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-md);
    }

    .quick-action-btn {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        background: var(--color-bg-card);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        padding: var(--spacing-sm) var(--spacing-md);
        font-size: 1rem;
        color: var(--color-accent);
        cursor: pointer;
        transition: background 0.2s;
    }

    .quick-action-btn:hover {
        background: var(--color-bg-hover);
    }

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

    @media (max-width: 768px) {
        .dashboard-kpi-row {
            flex-direction: column;
            gap: var(--spacing-md);
        }

        .dashboard-section-row {
            flex-direction: column;
            gap: var(--spacing-lg);
        }

        .quick-action-btn {
            justify-content: center;
        }
    }
</style>
