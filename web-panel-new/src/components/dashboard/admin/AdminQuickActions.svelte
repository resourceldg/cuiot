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

    function goToCore() {
        dispatch("manageCore");
    }

    function goToCare() {
        dispatch("manageCare");
    }

    function goToIoT() {
        dispatch("manageIoT");
    }

    function goToBusiness() {
        dispatch("manageBusiness");
    }

    function goToScoring() {
        goto("/dashboard/scoring");
    }

    function goToMonitoring() {
        goto("/dashboard/monitoring");
    }
</script>

<div class="quick-actions">
    <SectionHeader
        title="Acciones Rápidas"
        subtitle="Accesos directos organizados por módulos"
    >
        <span slot="icon">
            <SettingsIcon size={24} />
        </span>
    </SectionHeader>

    <div class="actions-grid">
        <!-- Módulo Core -->
        <button class="action-card core-module" on:click={goToCore}>
            <div class="action-icon">
                <ShieldIcon size={24} />
            </div>
            <div class="action-content">
                <h3>📋 Catálogos</h3>
                <p>Tipos de estado, dispositivos, alertas</p>
            </div>
        </button>

        <!-- Módulo Care -->
        <button class="action-card care-module" on:click={goToCare}>
            <div class="action-icon">
                <ShieldIcon size={24} />
            </div>
            <div class="action-content">
                <h3>🏥 Cuidados</h3>
                <p>Personas cuidadas, asignaciones, observaciones</p>
            </div>
        </button>

        <!-- Módulo IoT -->
        <button class="action-card iot-module" on:click={goToIoT}>
            <div class="action-icon">
                <EventToastIcon size={24} />
            </div>
            <div class="action-content">
                <h3>📱 IoT</h3>
                <p>Dispositivos, eventos, alertas, geocercas</p>
            </div>
        </button>

        <!-- Módulo Business -->
        <button class="action-card business-module" on:click={goToBusiness}>
            <div class="action-icon">
                <BuildingIcon size={24} />
            </div>
            <div class="action-content">
                <h3>💼 Negocio</h3>
                <p>Instituciones, paquetes, facturación</p>
            </div>
        </button>

        <!-- Usuarios -->
        <button class="action-card" on:click={goToUsers}>
            <div class="action-icon">
                <UsersIcon size={24} />
            </div>
            <div class="action-content">
                <h3>👥 Usuarios</h3>
                <p>Ver, editar y administrar usuarios</p>
            </div>
        </button>

        <!-- Paquetes -->
        <button class="action-card" on:click={goToPackages}>
            <div class="action-icon">
                <PackageIcon size={24} />
            </div>
            <div class="action-content">
                <h3>📦 Paquetes</h3>
                <p>Gestionar paquetes y servicios</p>
            </div>
        </button>

        <!-- Instituciones -->
        <button class="action-card" on:click={goToInstitutions}>
            <div class="action-icon">
                <BuildingIcon size={24} />
            </div>
            <div class="action-content">
                <h3>🏢 Instituciones</h3>
                <p>Administrar instituciones y relaciones</p>
            </div>
        </button>

        <!-- Eventos -->
        <button class="action-card" on:click={goToEvents}>
            <div class="action-icon">
                <EventToastIcon size={24} />
            </div>
            <div class="action-content">
                <h3>📅 Eventos</h3>
                <p>Ver y gestionar eventos del sistema</p>
            </div>
        </button>

        <!-- Scoring -->
        <button class="action-card scoring-module" on:click={goToScoring}>
            <div class="action-icon">
                <ShieldIcon size={24} />
            </div>
            <div class="action-content">
                <h3>⭐ Calificaciones</h3>
                <p>Puntuaciones y reseñas</p>
            </div>
        </button>

        <!-- Monitoring -->
        <button class="action-card monitoring-module" on:click={goToMonitoring}>
            <div class="action-icon">
                <BookIcon size={24} />
            </div>
            <div class="action-content">
                <h3>📊 Monitoreo</h3>
                <p>Reportes y métricas del sistema</p>
            </div>
        </button>

        <!-- Guía de Jerarquía -->
        <button class="action-card" on:click={showUserGuide}>
            <div class="action-icon">
                <ShieldIcon size={24} />
            </div>
            <div class="action-content">
                <h3>📖 Guía de Jerarquía</h3>
                <p>Ver reglas de negocio y permisos</p>
            </div>
        </button>

        <!-- Configuración -->
        <button class="action-card" on:click={goToSettings}>
            <div class="action-icon">
                <BookIcon size={24} />
            </div>
            <div class="action-content">
                <h3>⚙️ Configuración</h3>
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
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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

    /* Estilos específicos por módulo */
    .action-card.core-module:hover {
        border-color: #00e676;
        background: rgba(0, 230, 118, 0.05);
    }

    .action-card.care-module:hover {
        border-color: #ff6b6b;
        background: rgba(255, 107, 107, 0.05);
    }

    .action-card.iot-module:hover {
        border-color: #4ecdc4;
        background: rgba(78, 205, 196, 0.05);
    }

    .action-card.business-module:hover {
        border-color: #45b7d1;
        background: rgba(69, 183, 209, 0.05);
    }

    .action-card.scoring-module:hover {
        border-color: #f9ca24;
        background: rgba(249, 202, 36, 0.05);
    }

    .action-card.monitoring-module:hover {
        border-color: #6c5ce7;
        background: rgba(108, 92, 231, 0.05);
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
        color: var(--color-text-secondary);
        line-height: 1.4;
    }

    @media (max-width: 768px) {
        .actions-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
