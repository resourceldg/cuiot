<script lang="ts">
    import type { User } from "$lib/api/users";
    import { createEventDispatcher } from "svelte";
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
{/if}

<style>
    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.6);
        z-index: 1000;
    }
    .modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: var(--color-bg-card);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        padding: 2rem;
        min-width: 340px;
        max-width: 95vw;
        max-height: 90vh;
        overflow-y: auto;
        z-index: 1001;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        position: relative; /* Importante para el posicionamiento del ModalNotification */
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
        z-index: 1003; /* Por encima de la notificación */
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
        gap: 1rem;
    }
    .modal-actions button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .form-error {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
        border-radius: var(--border-radius);
        padding: 1rem;
        margin: 1rem 0;
    }

    @media (max-width: 600px) {
        .modal {
            padding: 1rem;
            min-width: 90vw;
        }
    }
</style>
