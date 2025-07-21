<script lang="ts">
    import { goto } from "$app/navigation";
    import ArrowLeftIcon from "$lib/ui/icons/ArrowLeftIcon.svelte";
    import UserIcon from "$lib/ui/icons/UserIcon.svelte";
    import UserForm from "../../../../components/dashboard/admin/UserForm.svelte";
    import UserHierarchyGuide from "../../../../components/dashboard/admin/UserHierarchyGuide.svelte";
    import SectionHeader from "../../../../components/shared/ui/SectionHeader.svelte";

    // Estados
    let showGuide = false;
    let loading = false;
    let error = "";
    let success = "";
    let isTransitioning = false; // Nuevo estado para controlar la transición

    function goBack() {
        if (isTransitioning) return; // Prevenir navegación durante transición
        goto("/dashboard/users");
    }

    async function handleFormSubmit(event: any) {
        const formData = event.detail;
        console.log("📝 Página create: Usuario creado exitosamente", formData);

        // Activar estado de transición
        isTransitioning = true;
        loading = true;

        // El UserForm ya maneja toda la lógica de creación y asignación de roles
        // Solo necesitamos manejar el éxito y redirección
        success = "Usuario creado exitosamente";

        // Pasar el ID del usuario recién creado a la página de usuarios
        const userId = formData.debugResult?.createResult?.data?.id;
        if (userId) {
            // Guardar el ID en sessionStorage para que UserTable lo detecte
            sessionStorage.setItem("newlyCreatedUserId", userId);
            console.log("🎉 Página create: Usuario recién creado ID:", userId);
        }

        // Redirigir después de un breve delay
        setTimeout(() => {
            goto("/dashboard/users");
        }, 1500);
    }

    function toggleGuide() {
        if (isTransitioning) return; // Prevenir apertura durante transición
        showGuide = !showGuide;
    }
</script>

<svelte:head>
    <title>Crear Usuario - Sistema de Cuidado</title>
</svelte:head>

<div class="create-user-page">
    <div class="page-header">
        <button class="back-btn" on:click={goBack} disabled={isTransitioning}>
            <ArrowLeftIcon size={20} />
            <span>Volver a Usuarios</span>
        </button>

        <SectionHeader
            title="Crear Nuevo Usuario"
            subtitle="Registro completo de usuario en el sistema"
        >
            <span slot="icon">
                <UserIcon size={32} />
            </span>
        </SectionHeader>

        <button
            class="guide-btn"
            on:click={toggleGuide}
            disabled={isTransitioning}
        >
            📋 Ver Guía
        </button>
    </div>

    {#if error}
        <div class="error-banner">
            <span>{error}</span>
        </div>
    {/if}

    {#if success}
        <div class="success-banner">
            <span>{success}</span>
        </div>
    {/if}

    <div class="page-content">
        <UserForm on:submit={handleFormSubmit} disabled={isTransitioning} />

        <!-- Overlay de loading durante transición -->
        {#if isTransitioning}
            <div class="loading-overlay">
                <div class="loading-spinner"></div>
                <p>Redirigiendo a la lista de usuarios...</p>
            </div>
        {/if}
    </div>
</div>

<!-- Modal de Guía -->
{#if showGuide}
    <div class="modal-overlay" on:click={toggleGuide}>
        <div class="modal-content" on:click|stopPropagation>
            <UserHierarchyGuide on:close={toggleGuide} />
        </div>
    </div>
{/if}

<style>
    .create-user-page {
        max-width: 1200px;
        margin: 0 auto;
        padding: var(--spacing-lg);
    }

    .page-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: var(--spacing-xl);
        gap: var(--spacing-lg);
    }

    .back-btn {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        background: var(--color-bg-card);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        padding: var(--spacing-sm) var(--spacing-md);
        color: var(--color-text);
        cursor: pointer;
        transition: all 0.2s;
        font-size: 0.9rem;
    }

    .back-btn:hover:not(:disabled) {
        background: var(--color-bg-hover);
        border-color: var(--color-accent);
    }

    .back-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        background: var(--color-bg-disabled);
    }

    .guide-btn {
        background: var(--color-accent);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: var(--spacing-sm) var(--spacing-md);
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s;
    }

    .guide-btn:hover:not(:disabled) {
        background: var(--color-accent-dark);
    }

    .guide-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        background: var(--color-accent-disabled);
    }

    .error-banner,
    .success-banner {
        padding: var(--spacing-md);
        border-radius: var(--border-radius);
        margin-bottom: var(--spacing-lg);
        font-weight: 500;
    }

    .error-banner {
        background: var(--color-danger-bg);
        color: var(--color-danger);
        border: 1px solid var(--color-danger);
    }

    .success-banner {
        background: var(--color-success-bg);
        color: var(--color-success);
        border: 1px solid var(--color-success);
    }

    .page-content {
        background: var(--color-bg-card);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-md);
        overflow: hidden;
        position: relative;
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

    .loading-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(var(--color-bg-card-rgb, 255, 255, 255), 0.9);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 1001;
        border-radius: var(--border-radius);
        backdrop-filter: blur(2px);
    }

    .loading-spinner {
        border: 4px solid var(--color-border);
        border-top: 4px solid var(--color-accent);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin-bottom: var(--spacing-sm);
    }

    .loading-overlay p {
        color: var(--color-text);
        font-weight: 500;
        margin: 0;
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    @media (max-width: 768px) {
        .page-header {
            flex-direction: column;
            align-items: stretch;
            gap: var(--spacing-md);
        }

        .create-user-page {
            padding: var(--spacing-md);
        }
    }
</style>
