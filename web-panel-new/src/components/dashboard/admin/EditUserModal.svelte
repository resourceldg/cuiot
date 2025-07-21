<script lang="ts">
    import type { User } from "$lib/api/users";
    import { createEventDispatcher } from "svelte";
    import Portal from "svelte-portal";
    import ModalNotification from "../../shared/ui/ModalNotification.svelte";
    import UserForm from "./UserForm.svelte";

    export let user: User | null = null;
    export let open = false;
    export let loading = false;
    export let sessionUserRole: string = "";

    const dispatch = createEventDispatcher();
    let formData: any = null;
    let error = "";
    let debugResult: any = null;
    let success = false;
    let submitting = false;
    let showNotification = false;
    let notificationType: "success" | "error" = "success";
    let notificationMessage = "";
    let notificationSubtitle = "";

    // Precarga robusta SOLO al abrir el modal
    $: if (open && user) {
        formData = {
            id: user.id, // Asegura que el id esté presente
            first_name: user.first_name || "",
            last_name: user.last_name || "",
            email: user.email || "",
            phone: user.phone || "",
            password: "",
            confirm_password: "",
            // Mapear roles para compatibilidad
            role:
                Array.isArray(user.roles) && user.roles.length > 0
                    ? user.roles[0]
                    : "",
            is_active: user.is_active,
            date_of_birth: user.date_of_birth || "",
            gender: user.gender || "",
            institution_id: user.institution_id || null,
            professional_license: user.professional_license || "",
            specialization: user.specialization || "",
            experience_years: user.experience_years || 0,
            is_freelance: user.is_freelance || false,
            hourly_rate: user.hourly_rate || 0,
            availability: user.availability || "",
            legal_representative_id: null,
            legal_capacity_verified: false,
            terms_accepted: false,
            is_verified: user.is_verified || false,
        };
    }

    // Limpiar formData al cerrar
    $: if (!open) {
        formData = null;
        success = false;
        error = "";
        debugResult = null;
        submitting = false;
        showNotification = false;
    }

    // Efecto reactivo profesional para asegurar que el modal siempre sea visible y centrado
    $: if (open) {
        // Forzar scroll en todos los contenedores relevantes
        window.scrollTo({ top: 0 });
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
        // Intenta scrollear main y #app si existen
        const main = document.querySelector("main");
        if (main) main.scrollTop = 0;
        const app = document.getElementById("app");
        if (app) app.scrollTop = 0;
        // Si el modal sigue apareciendo fuera del viewport, migrar a portal (ver svelte-portal)
    }

    function handleSubmit(e: CustomEvent) {
        submitting = true;
        error = "";
        success = false;

        debugResult = e.detail.debugResult;
        console.log("🔧 EditUserModal handleSubmit: Recibido evento", {
            debugResult,
            hasUpdateResult: !!debugResult?.updateResult,
            hasAssignResult: !!debugResult?.assignResult,
            updateResult: debugResult?.updateResult,
            assignResult: debugResult?.assignResult,
        });

        // Verificar si hay errores en las respuestas de la API
        const updateError = debugResult?.updateResult?.error;
        const assignError = debugResult?.assignResult?.error;

        console.log("🔧 EditUserModal handleSubmit: Análisis de errores", {
            updateError,
            assignError,
            hasUpdateError: !!updateError,
            hasAssignError: !!assignError,
        });

        if (updateError || assignError) {
            success = false;
            const errorMessage =
                updateError || assignError || "Error desconocido";
            console.error("❌ EditUserModal handleSubmit: Error en operación", {
                updateError,
                assignError,
                errorMessage,
            });

            error = errorMessage;
            notificationType = "error";
            notificationMessage = "Error al actualizar el usuario";
            notificationSubtitle = errorMessage;
            showNotification = true;
            submitting = false;
        } else {
            success = true;
            console.log(
                "✅ EditUserModal handleSubmit: Usuario actualizado exitosamente",
                debugResult,
            );

            notificationType = "success";
            notificationMessage = "¡Usuario actualizado correctamente!";
            notificationSubtitle =
                "Los cambios han sido guardados exitosamente.";
            showNotification = true;
            console.log(
                "🔧 EditUserModal handleSubmit: Mostrando notificación de éxito",
                {
                    notificationType,
                    notificationMessage,
                    notificationSubtitle,
                    showNotification,
                },
            );
            dispatch("save"); // Notifica éxito al padre
        }
    }

    function handleCancel() {
        if (!submitting) {
            dispatch("cancel");
        }
    }

    function handleNotificationClose() {
        console.log(
            "🔧 EditUserModal handleNotificationClose: Cerrando notificación",
            {
                success,
                showNotification,
                submitting,
            },
        );
        showNotification = false;
        if (success) {
            console.log(
                "🔧 EditUserModal handleNotificationClose: Cerrando modal por éxito",
            );
            handleCancel(); // Cierra el modal solo si fue exitoso
        }
        submitting = false;
    }
</script>

{#if open}
    <Portal>
        <div class="modal-outer">
            <div class="modal-backdrop" on:click={handleCancel}></div>
            <div
                class="modal"
                role="dialog"
                aria-modal="true"
                on:click|stopPropagation
            >
                <div class="modal-header">
                    <h3>Editar usuario</h3>
                    <button
                        class="modal-close"
                        on:click={handleCancel}
                        title="Cerrar"
                        disabled={submitting}>&times;</button
                    >
                </div>
                <div class="modal-content">
                    <UserForm
                        initialData={formData}
                        on:submit={handleSubmit}
                        editMode={true}
                        {sessionUserRole}
                    />
                    {#if error && !showNotification}
                        <div class="error-banner">{error}</div>
                    {/if}
                    {#if debugResult && !success && !showNotification}
                        <details>
                            <summary>DEBUG: Respuesta de la API</summary>
                            <pre>{JSON.stringify(debugResult, null, 2)}</pre>
                        </details>
                    {/if}
                    <div class="modal-actions">
                        <button
                            class="btn-secondary"
                            on:click={handleCancel}
                            disabled={submitting}
                            >{submitting ? "Procesando..." : "Cancelar"}</button
                        >
                    </div>
                    <ModalNotification
                        type={notificationType}
                        message={notificationMessage}
                        subtitle={notificationSubtitle}
                        show={showNotification}
                        duration={2000}
                        on:close={handleNotificationClose}
                    />
                </div>
            </div>
        </div>
    </Portal>
{/if}

<style>
    .modal-outer {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 2100;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.6);
        z-index: 2100;
    }
    .modal {
        position: relative;
        background: var(--color-bg-card);
        border-radius: 16px;
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.18),
            0 1.5px 6px rgba(0, 0, 0, 0.1);
        min-width: 320px;
        max-width: 95vw;
        width: 100%;
        max-height: 95vh;
        overflow-y: auto;
        z-index: 2110;
        display: flex;
        flex-direction: column;
        margin: 0;
        box-sizing: border-box;
        align-items: stretch;
        animation: modal-fade-in 0.22s cubic-bezier(0.4, 1.3, 0.6, 1) both;
    }
    .modal-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid var(--color-border);
        padding: 1.2rem 1.2rem 0.5rem 1.2rem;
        margin-bottom: 0.5rem;
    }
    .modal-content {
        padding: 0 1.2rem 1.2rem 1.2rem;
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
    }
    .modal-close {
        background: none;
        border: none;
        font-size: 2rem;
        color: var(--color-text-secondary);
        cursor: pointer;
        transition: color 0.2s;
        z-index: 2200;
        padding: 0.2rem 0.5rem;
        border-radius: 8px;
    }
    .modal-close:hover:not(:disabled) {
        color: var(--color-accent);
        background: var(--color-bg-hover);
    }
    .modal-actions {
        display: flex;
        justify-content: flex-end;
        gap: 0.8rem;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid var(--color-border);
    }
    .modal-actions button {
        padding: 0.55rem 1.3rem;
        border-radius: 8px;
        border: none;
        font-size: 1rem;
        font-weight: 500;
        background: var(--color-accent);
        color: #fff;
        cursor: pointer;
        transition: background 0.18s;
        box-shadow: 0 1.5px 6px rgba(0, 0, 0, 0.08);
    }
    .modal-actions button.btn-secondary {
        background: var(--color-bg-card);
        color: var(--color-text);
        border: 1px solid var(--color-border);
    }
    .modal-actions button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
    .error-banner {
        background: rgba(255, 77, 109, 0.12);
        color: var(--color-danger);
        border: 1.5px solid var(--color-danger);
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-size: 1.05rem;
        text-align: center;
        margin: 0.7rem 0 0.5rem 0;
    }

    /* Media queries mejorados para responsividad */
    @media (max-width: 600px) {
        .modal-outer {
            align-items: flex-start;
        }
        .modal {
            padding: 0;
            min-width: 0;
            max-width: 98vw;
            width: 98vw;
            max-height: 98vh;
        }
        .modal-header {
            padding: 0.7rem 0.7rem 0.3rem 0.7rem;
        }
        .modal-content {
            padding: 0 0.7rem 0.7rem 0.7rem;
        }
        .modal-header h3 {
            font-size: 1.1rem;
        }
    }

    @media (min-width: 601px) and (max-width: 1200px) {
        .modal {
            max-width: 90vw;
            max-height: 90vh;
        }
    }

    @media (min-width: 1201px) {
        .modal {
            max-width: 1200px;
            max-height: 90vh;
        }
    }

    @media (max-width: 480px) {
        .modal {
            max-width: 100vw;
            width: 100vw;
            max-height: 100vh;
            border-radius: 0;
        }
        .modal-header {
            padding: 0.5rem 0.5rem 0.2rem 0.5rem;
        }
        .modal-content {
            padding: 0 0.5rem 0.5rem 0.5rem;
        }
    }
</style>
