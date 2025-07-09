<script>
    import { goto } from "$app/navigation";
    import BookIcon from "$lib/ui/icons/BookIcon.svelte";
    import BuildingIcon from "$lib/ui/icons/BuildingIcon.svelte";
    import EventToastIcon from "$lib/ui/icons/EventToastIcon.svelte";
    import PackageIcon from "$lib/ui/icons/PackageIcon.svelte";
    import SettingsIcon from "$lib/ui/icons/SettingsIcon.svelte";
    import ShieldIcon from "$lib/ui/icons/ShieldIcon.svelte";
    import UsersIcon from "$lib/ui/icons/UsersIcon.svelte";
    import { createEventDispatcher } from "svelte";
    import SectionHeader from "../../shared/ui/SectionHeader.svelte";

    const dispatch = createEventDispatcher();

    function showUserGuide() {
        dispatch("showUserGuide");
    }

    function goToUsers() {
        goto("/dashboard/users");
    }
    function goToPackages() {
        goto("/dashboard/packages");
    }
    function goToInstitutions() {
        goto("/dashboard/institutions");
    }
    function goToEvents() {
        goto("/dashboard/events");
    }
    function goToSettings() {
        goto("/dashboard/settings");
    }
</script>

<div class="quick-actions">
    <SectionHeader
        title="Acciones Rápidas"
        subtitle="Accesos directos a las principales secciones"
    >
        <span slot="icon">
            <SettingsIcon size={24} />
        </span>
    </SectionHeader>

    <div class="actions-grid">
        <button class="action-card" on:click={goToUsers}>
            <div class="action-icon">
                <UsersIcon size={24} />
            </div>
            <div class="action-content">
                <h3>Usuarios</h3>
                <p>Ver, editar y administrar usuarios</p>
            </div>
        </button>

        <button class="action-card" on:click={goToPackages}>
            <div class="action-icon">
                <PackageIcon size={24} />
            </div>
            <div class="action-content">
                <h3>Paquetes</h3>
                <p>Gestionar paquetes y servicios</p>
            </div>
        </button>

        <button class="action-card" on:click={goToInstitutions}>
            <div class="action-icon">
                <BuildingIcon size={24} />
            </div>
            <div class="action-content">
                <h3>Instituciones</h3>
                <p>Administrar instituciones y relaciones</p>
            </div>
        </button>

        <button class="action-card" on:click={goToEvents}>
            <div class="action-icon">
                <EventToastIcon size={24} />
            </div>
            <div class="action-content">
                <h3>Eventos</h3>
                <p>Ver y gestionar eventos del sistema</p>
            </div>
        </button>

        <button class="action-card" on:click={showUserGuide}>
            <div class="action-icon">
                <ShieldIcon size={24} />
            </div>
            <div class="action-content">
                <h3>Guía de Jerarquía</h3>
                <p>Ver reglas de negocio y permisos</p>
            </div>
        </button>

        <button class="action-card" on:click={goToSettings}>
            <div class="action-icon">
                <BookIcon size={24} />
            </div>
            <div class="action-content">
                <h3>Configuración</h3>
                <p>Ajustes del sistema y parámetros</p>
            </div>
        </button>
    </div>
</div>

<style>
    .quick-actions {
        background: var(--color-bg-card);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-md);
        padding: var(--spacing-lg);
    }

    .actions-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: var(--spacing-md);
        margin-top: var(--spacing-lg);
    }

    .action-card {
        display: flex;
        align-items: center;
        gap: var(--spacing-md);
        padding: var(--spacing-md);
        background: var(--color-bg);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        cursor: pointer;
        transition: all 0.2s;
        text-align: left;
    }

    .action-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        border-color: var(--color-accent);
    }

    .action-icon {
        flex-shrink: 0;
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: var(--color-bg-hover);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--color-accent);
    }

    .action-content h3 {
        margin: 0 0 4px 0;
        font-size: 1rem;
        font-weight: 600;
        color: var(--color-text);
    }

    .action-content p {
        margin: 0;
        font-size: 0.85rem;
        color: var(--color-text-muted);
        line-height: 1.4;
    }

    @media (max-width: 768px) {
        .actions-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
