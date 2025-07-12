<script lang="ts">
    import { goto } from "$app/navigation";
    import { createUser } from "$lib/api/users";
    import ArrowLeftIcon from "$lib/ui/icons/ArrowLeftIcon.svelte";
    import UserIcon from "$lib/ui/icons/UserIcon.svelte";
    import UserForm from "../../../../components/dashboard/admin/UserForm.svelte";
    import UserHierarchyGuide from "../../../../components/dashboard/admin/UserHierarchyGuide.svelte";
    import SectionHeader from "../../../../components/shared/ui/SectionHeader.svelte";

    // Estados
    let showGuide = false;
    let formData: any = {};
    let loading = false;
    let error = "";
    let success = "";

    function goBack() {
        goto("/dashboard/users");
    }

    async function handleFormSubmit(event: any) {
        formData = event.detail;
        loading = true;
        error = "";
        success = "";

        try {
            // Preparar datos para la API
            const userData = {
                email: formData.email,
                first_name: formData.first_name,
                last_name: formData.last_name,
                phone: formData.phone,
                password: formData.password,
                username: formData.username || null,
                date_of_birth: formData.date_of_birth || null,
                gender: formData.gender || null,
                professional_license: formData.professional_license || null,
                specialization: formData.specialization || null,
                experience_years: formData.experience_years || null,
                is_freelance: formData.is_freelance || false,
                hourly_rate: formData.hourly_rate || null,
                availability: formData.availability || null,
                is_verified: formData.is_verified || false,
                institution_id: formData.institution_id || null,
                is_active:
                    formData.is_active !== undefined
                        ? formData.is_active
                        : true,
            };

            console.log("Enviando datos a la API:", userData);

            const { data, error: apiError } = await createUser(userData);

            if (apiError) {
                error = apiError;
                console.error("Error al crear usuario:", apiError);
            } else {
                success = "Usuario creado exitosamente";
                console.log("Usuario creado:", data);

                // Redirigir a la lista de usuarios después de 2 segundos
                setTimeout(() => {
                    goto("/dashboard/users");
                }, 2000);
            }
        } catch (err) {
            error =
                err instanceof Error
                    ? err.message
                    : "Error desconocido al crear usuario";
            console.error("Error inesperado:", err);
        } finally {
            loading = false;
        }
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
        <UserForm on:submit={handleFormSubmit} disabled={loading} />

        {#if loading}
            <div class="loading-overlay">
                <div class="loading-spinner"></div>
                <p>Creando usuario...</p>
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
        background: rgba(255, 255, 255, 0.9);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 1001;
        border-radius: var(--border-radius);
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
