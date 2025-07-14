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
        if (
            debugResult &&
            debugResult.updateResult &&
            !debugResult.updateResult.error
        ) {
            success = true;
            notificationType = "success";
            notificationMessage = "¡Usuario actualizado correctamente!";
            notificationSubtitle =
                "Los cambios han sido guardados exitosamente.";
            showNotification = true;
            dispatch("save"); // Notifica éxito al padre
        } else {
            success = false;
            error = "Error al actualizar el usuario";
            notificationType = "error";
            notificationMessage = "Error al actualizar el usuario";
            notificationSubtitle = "No se pudieron guardar los cambios.";
            showNotification = true;
            submitting = false;
        }
    }

    function handleCancel() {
        if (!submitting) {
            dispatch("cancel");
        }
    }

    function handleNotificationClose() {
        showNotification = false;
        if (success) {
            handleCancel(); // Cierra el modal solo si fue exitoso
        }
        submitting = false;
    }
</script>

{#if open}
    <Portal>
        <div class="modal-backdrop" on:click={handleCancel}></div>
        <div class="modal" role="dialog" aria-modal="true">
            <button
                class="modal-close"
                on:click={handleCancel}
                title="Cerrar"
                disabled={submitting}>&times;</button
            >
            <h3>Editar usuario</h3>
            <UserForm
                initialData={formData}
                on:submit={handleSubmit}
                editMode={true}
                {sessionUserRole}
            />
            {#if error && !showNotification}
                <div class="form-error">{error}</div>
            {/if}
            {#if debugResult && !success && !showNotification}
                <details>
                    <summary>DEBUG: Respuesta de la API</summary>
                    <pre
                        style="background: #f0f0f0; padding: 10px; border-radius: 4px; font-size: 12px; overflow: auto; max-height: 200px;">{JSON.stringify(
                            debugResult,
                            null,
                            2,
                        )}</pre>
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
            <!-- Componente de notificación -->
            <ModalNotification
                type={notificationType}
                message={notificationMessage}
                subtitle={notificationSubtitle}
                show={showNotification}
                duration={2000}
                on:close={handleNotificationClose}
            />
        </div>
    </Portal>
{/if}

<style>
    .modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: var(--color-bg-card);
        border-radius: 16px;
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.18),
            0 1.5px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5rem 1.5rem 1.2rem 1.5rem;
        min-width: 320px;
        max-width: 420px;
        width: 100%;
        max-height: 90vh;
        overflow-y: auto;
        z-index: 2100;
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        margin: 0;
        box-sizing: border-box;
        align-items: stretch;
        animation: modal-fade-in 0.22s cubic-bezier(0.4, 1.3, 0.6, 1) both;
    }
    .modal.popover {
        position: absolute;
        top: unset;
        left: unset;
        transform: none;
        min-width: 320px;
        max-width: 420px;
        width: 100%;
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.18),
            0 1.5px 6px rgba(0, 0, 0, 0.1);
        border-radius: 16px;
        padding: 1.2rem 1.2rem 1.1rem 1.2rem;
        gap: 1.1rem;
        animation: modal-slide-fade-in 0.22s cubic-bezier(0.4, 1.3, 0.6, 1) both;
    }
    .modal-arrow {
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%);
        width: 24px;
        height: 12px;
        overflow: visible;
        z-index: 2200;
    }
    .modal-arrow::after {
        content: "";
        display: block;
        width: 24px;
        height: 12px;
        background: transparent;
        border-left: 12px solid transparent;
        border-right: 12px solid transparent;
        border-bottom: 12px solid var(--color-bg-card);
        margin: 0 auto;
    }
    @keyframes modal-fade-in {
        from {
            opacity: 0;
            transform: translate(-50%, -60%) scale(0.98);
        }
        to {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }
    }
    @keyframes modal-slide-fade-in {
        from {
            opacity: 0;
            transform: translateY(24px) scale(0.98);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.6);
        z-index: 2000;
    }
    .modal-close {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: none;
        border: none;
        font-size: 2rem;
        color: var(--color-text-muted);
        cursor: pointer;
        transition: color 0.2s;
        z-index: 2200;
    }
    .modal-close:hover:not(:disabled) {
        color: var(--color-accent);
    }
    .modal-close:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    .modal-actions {
        display: flex;
        justify-content: flex-end;
        gap: 0.8rem;
        margin-top: 1.2rem;
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
        background: var(--color-bg-secondary);
        color: var(--color-text);
        border: 1px solid var(--color-border);
    }
    .modal-actions button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
    .form-error {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.7rem 0 0.5rem 0;
        font-size: 0.98rem;
    }
    /* Asegura que el modal nunca se salga del viewport */
    .modal,
    .modal.popover {
        max-width: 98vw;
        max-height: 95vh;
        overflow-y: auto;
    }

    body {
        overflow: hidden !important;
    }

    @media (max-width: 600px) {
        .modal,
        .modal.popover {
            padding: 0.5rem 0.25rem;
            min-width: 0;
            max-width: 98vw;
            width: 98vw;
        }
        .modal h3 {
            font-size: 1.1rem;
        }
    }
</style>
