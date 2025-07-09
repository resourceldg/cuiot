<script lang="ts">
    import { goto } from "$app/navigation";
    import ArrowLeftIcon from "$lib/ui/icons/ArrowLeftIcon.svelte";
    import UserIcon from "$lib/ui/icons/UserIcon.svelte";
    import UserForm from "../../../../components/dashboard/admin/UserForm.svelte";
    import UserHierarchyGuide from "../../../../components/dashboard/admin/UserHierarchyGuide.svelte";
    import SectionHeader from "../../../../components/shared/ui/SectionHeader.svelte";

    // Estados
    let showGuide = false;
    let formData = {};
    let loading = false;
    let error = "";
    let success = "";

    function goBack() {
        goto("/dashboard/users");
    }

    function handleFormSubmit(event) {
        formData = event.detail;
        // Aquí se procesaría la creación del usuario
        console.log("Datos del formulario:", formData);
    }

    function toggleGuide() {
        showGuide = !showGuide;
    }
</script>

<svelte:head>
    <title>Crear Usuario - Sistema de Cuidado</title>
</svelte:head>

<div class="create-user-page">
    <div class="page-header">
        <button class="back-btn" on:click={goBack}>
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

        <button class="guide-btn" on:click={toggleGuide}> 📋 Ver Guía </button>
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
        <UserForm on:submit={handleFormSubmit} />
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

    .back-btn:hover {
        background: var(--color-bg-hover);
        border-color: var(--color-accent);
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

    .guide-btn:hover {
        background: var(--color-accent-dark);
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
