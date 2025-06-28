<script>
    import { createEventDispatcher } from "svelte";
    export let initialData = null; // Si se pasa, es edición
    export let loading = false;
    export let error = "";
    export let visible = false;
    export let title = "Agregar Adulto Mayor";

    const dispatch = createEventDispatcher();

    let form = {
        first_name: "",
        last_name: "",
        age: "",
        address: "",
        emergency_contacts: [],
    };

    // Reactividad profesional: actualiza el form solo cuando cambia initialData y el modal está visible
    $: if (visible && initialData) {
        form = {
            first_name: initialData.first_name || "",
            last_name: initialData.last_name || "",
            age: initialData.age || "",
            address: initialData.address || "",
            emergency_contacts: initialData.emergency_contacts || [],
        };
    }
    // Si abro para agregar, limpio el form
    $: if (visible && !initialData) {
        form = {
            first_name: "",
            last_name: "",
            age: "",
            address: "",
            emergency_contacts: [],
        };
    }

    function handleSubmit() {
        if (!form.first_name || !form.last_name) {
            dispatch("error", {
                message: "Nombre y apellido son obligatorios",
            });
            return;
        }
        dispatch("submit", {
            ...form,
            age: form.age ? Number(form.age) : null,
        });
    }

    function handleClose() {
        dispatch("close");
    }
</script>

{#if visible}
    <div class="modal-backdrop" on:click={handleClose}></div>
    <div class="modal">
        <div class="modal-header">
            <h2>{title}</h2>
            <button class="close-btn" on:click={handleClose}>&times;</button>
        </div>
        <form on:submit|preventDefault={handleSubmit} class="modal-form">
            {#if error}
                <div class="form-error">{error}</div>
            {/if}
            <div class="form-group">
                <label>Nombre *</label>
                <input
                    type="text"
                    bind:value={form.first_name}
                    required
                    disabled={loading}
                />
            </div>
            <div class="form-group">
                <label>Apellido *</label>
                <input
                    type="text"
                    bind:value={form.last_name}
                    required
                    disabled={loading}
                />
            </div>
            <div class="form-group">
                <label>Edad</label>
                <input
                    type="number"
                    min="0"
                    max="120"
                    bind:value={form.age}
                    disabled={loading}
                />
            </div>
            <div class="form-group">
                <label>Dirección</label>
                <input
                    type="text"
                    bind:value={form.address}
                    disabled={loading}
                />
            </div>
            <!-- Contactos de emergencia opcional -->
            <div class="form-actions">
                <button
                    type="submit"
                    class="btn btn-primary"
                    disabled={loading}
                    style="z-index: 1102;"
                >
                    {#if loading}Guardando...{:else}Guardar{/if}
                </button>
                <button
                    type="button"
                    class="btn btn-secondary"
                    on:click={handleClose}
                    disabled={loading}
                    style="z-index: 1102;">Cancelar</button
                >
            </div>
        </form>
    </div>
{/if}

<style>
    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.3);
        z-index: 1100;
    }
    .modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        border-radius: 10px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        z-index: 1101;
        min-width: 320px;
        max-width: 95vw;
        padding: 2rem 1.5rem 1.5rem 1.5rem;
    }
    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    .close-btn {
        background: none;
        border: none;
        font-size: 2rem;
        color: #888;
        cursor: pointer;
        line-height: 1;
        z-index: 1102;
    }
    .modal-form {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    .form-group {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }
    .form-group label {
        font-weight: 500;
        color: #374151;
        font-size: 0.95rem;
    }
    .form-group input {
        padding: 0.6rem;
        border: 1px solid #d1d5db;
        border-radius: 0.375rem;
        font-size: 1rem;
        background: #fff;
        color: #111827;
        z-index: 1102;
    }
    .form-error {
        background: #fee2e2;
        color: #b91c1c;
        border: 1px solid #fecaca;
        border-radius: 0.375rem;
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
        z-index: 1102;
    }
    .form-actions {
        display: flex;
        gap: 1rem;
        justify-content: flex-end;
        margin-top: 1rem;
        z-index: 1102;
    }
    .btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.15s ease-in-out;
        text-decoration: none;
        background: #2563eb;
        color: white;
        z-index: 1102;
    }
    .btn-primary {
        background: #2563eb;
        color: #fff !important;
    }
    .btn-primary:hover,
    .btn-primary:active,
    .btn-primary:focus {
        background: #1d4ed8;
        color: #fff !important;
    }
    .btn-secondary {
        background: #f3f4f6;
        color: #374151;
    }
    .btn-secondary:hover,
    .btn-secondary:active,
    .btn-secondary:focus {
        background: #e5e7eb;
        color: #111827;
    }
    .btn[disabled],
    .btn:disabled {
        background: #d1d5db !important;
        color: #9ca3af !important;
        cursor: not-allowed;
        opacity: 0.7;
    }
</style>
