<script lang="ts">
    import PackageIcon from "$lib/ui/icons/PackageIcon.svelte";
    import { createEventDispatcher } from "svelte";

    export let open = false;
    export let editMode = false;
    export let initialData = null;
    export let loading = false;

    const dispatch = createEventDispatcher();

    let form = {
        name: "",
        package_type: "individual",
        description: "",
        price_monthly: 0,
        price_yearly: 0,
        max_users: null,
        max_devices: null,
        is_active: true,
        is_featured: false,
    };
    let error = "";
    let submitting = false;

    $: if (editMode && initialData && typeof initialData === "object") {
        form = { ...form, ...initialData };
    }

    function closeModal() {
        if (!submitting) {
            dispatch("cancel");
        }
    }

    function handleSubmit() {
        error = "";
        submitting = true;
        // Validaciones mínimas
        if (!form.name.trim()) {
            error = "El nombre es obligatorio";
            submitting = false;
            return;
        }
        if (!form.package_type) {
            error = "El tipo de paquete es obligatorio";
            submitting = false;
            return;
        }
        if (form.price_monthly < 0) {
            error = "El precio mensual debe ser mayor o igual a 0";
            submitting = false;
            return;
        }
        // Emitir evento con los datos
        dispatch("submit", { ...form });
        submitting = false;
    }
</script>

{#if open}
    <div class="modal-outer">
        <div class="modal-backdrop" on:click={closeModal}></div>
        <div class="modal" role="dialog" aria-modal="true">
            <div class="modal-header">
                <h3>{editMode ? "Editar paquete" : "Nuevo paquete"}</h3>
                <button
                    class="modal-close"
                    on:click={closeModal}
                    disabled={submitting}>&times;</button
                >
            </div>
            <div class="modal-content">
                <form on:submit|preventDefault={handleSubmit} class="user-form">
                    <div class="form-section required">
                        <div class="section-header">
                            <h3>
                                <PackageIcon
                                    size={20}
                                    class="package-icon-inline"
                                />Datos del Paquete
                            </h3>
                            <span class="required-badge">Obligatorio</span>
                        </div>
                        <div class="form-grid">
                            <div class="form-group">
                                <label>Nombre *</label>
                                <input
                                    type="text"
                                    bind:value={form.name}
                                    required
                                />
                            </div>
                            <div class="form-group">
                                <label>Tipo *</label>
                                <select bind:value={form.package_type} required>
                                    <option value="individual"
                                        >Individual</option
                                    >
                                    <option value="professional"
                                        >Profesional</option
                                    >
                                    <option value="institutional"
                                        >Institucional</option
                                    >
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Precio mensual (ARS) *</label>
                                <input
                                    type="number"
                                    min="0"
                                    bind:value={form.price_monthly}
                                    required
                                />
                            </div>
                            <div class="form-group">
                                <label>Precio anual (ARS)</label>
                                <input
                                    type="number"
                                    min="0"
                                    bind:value={form.price_yearly}
                                />
                            </div>
                            <div class="form-group">
                                <label>Máx. usuarios</label>
                                <input
                                    type="number"
                                    min="1"
                                    bind:value={form.max_users}
                                />
                            </div>
                            <div class="form-group">
                                <label>Máx. dispositivos</label>
                                <input
                                    type="number"
                                    min="1"
                                    bind:value={form.max_devices}
                                />
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Descripción</label>
                            <textarea bind:value={form.description}></textarea>
                        </div>
                        <div class="form-group">
                            <label>
                                <input
                                    type="checkbox"
                                    bind:checked={form.is_active}
                                /> Activo
                            </label>
                            <label>
                                <input
                                    type="checkbox"
                                    bind:checked={form.is_featured}
                                /> Destacado
                            </label>
                        </div>
                    </div>
                    {#if error}
                        <div class="error-banner">{error}</div>
                    {/if}
                    <div class="modal-actions">
                        <button
                            type="submit"
                            class="btn-primary"
                            disabled={submitting}
                        >
                            {submitting
                                ? "Guardando..."
                                : editMode
                                  ? "Guardar cambios"
                                  : "Crear paquete"}
                        </button>
                        <button
                            type="button"
                            class="btn-secondary"
                            on:click={closeModal}
                            disabled={submitting}>Cancelar</button
                        >
                    </div>
                </form>
            </div>
        </div>
    </div>
{/if}

<style>
    @import "../shared/form-modal-layout.css";
    .package-icon-inline {
        vertical-align: middle;
        margin-right: 0.4em;
    }
</style>
