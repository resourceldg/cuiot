<script lang="ts">
    import type { User } from "$lib/api/users";
    import { createEventDispatcher } from "svelte";
    import UserForm from "./UserForm.svelte";

    export let user: User | null = null;
    export let open = false;
    export let loading = false;
    export let sessionUserRole: string = "";

    const dispatch = createEventDispatcher();
    let formData: any = null;
    let error = "";
    let debugResult = null;
    let success = false;

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
    }

    function handleSubmit(e: CustomEvent) {
        debugResult = e.detail.debugResult;
        if (
            debugResult &&
            debugResult.updateResult &&
            !debugResult.updateResult.error
        ) {
            success = true;
            dispatch("save"); // Notifica éxito al padre
            setTimeout(() => {
                success = false;
                debugResult = null;
                handleCancel(); // Cierra el modal
            }, 1200);
        } else {
            success = false;
        }
    }

    function handleCancel() {
        dispatch("cancel");
    }
</script>

{#if open}
    <div class="modal-backdrop" on:click={handleCancel}></div>
    <div class="modal" role="dialog" aria-modal="true">
        <button class="modal-close" on:click={handleCancel} title="Cerrar"
            >&times;</button
        >
        <h3>Editar usuario</h3>

        <UserForm
            initialData={formData}
            on:submit={handleSubmit}
            editMode={true}
            {sessionUserRole}
        />
        {#if error}
            <div class="form-error">{error}</div>
        {/if}
        {#if debugResult}
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
        {#if success}
            <div
                class="form-success"
                style="background: #111; color: #fff; padding: 10px; border-radius: 4px; margin-top: 10px; text-align: center;"
            >
                Usuario actualizado correctamente.
            </div>
        {/if}
        <div class="modal-actions">
            <button class="btn-secondary" on:click={handleCancel}
                >Cancelar</button
            >
        </div>
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
    }
    .modal-actions {
        display: flex;
        justify-content: flex-end;
        gap: 1rem;
    }
    @media (max-width: 600px) {
        .modal {
            padding: 1rem;
            min-width: 90vw;
        }
    }
</style>
