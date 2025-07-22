<script lang="ts">
    import {
        createPackage,
        deletePackage,
        getPackages,
        updatePackage,
    } from "$lib/api/packages";
    import PackageIcon from "$lib/ui/icons/PackageIcon.svelte";
    import RefreshIcon from "$lib/ui/icons/RefreshIcon.svelte";
    import { onMount } from "svelte";
    import PackageFormModal from "./PackageFormModal.svelte";

    // Tipos explícitos para paquetes
    interface Package {
        id: string;
        package_type: string;
        name: string;
        description?: string;
        price_monthly: number;
        price_yearly?: number;
        currency: string;
        max_users?: number;
        max_devices?: number;
        max_storage_gb?: number;
        features?: any;
        limitations?: any;
        customizable_options?: any;
        add_ons_available?: any;
        base_configuration?: any;
        is_customizable: boolean;
        support_level?: string;
        response_time_hours?: number;
        is_active: boolean;
        is_featured: boolean;
        created_at: string;
        updated_at: string;
    }

    // Estados
    let packages: Package[] = [];
    let loading = false;
    let error = "";
    let showModal = false;
    let showDeleteModal = false;
    let selectedPackage: Package | null = null;
    let deleting = false;
    let showDeleteNotification = false;
    let deleteNotificationType: "success" | "error" = "success";
    let deleteNotificationMessage = "";
    let deleteNotificationSubtitle = "";

    // Filtros
    let searchTerm = "";
    let statusFilter = "";
    let typeFilter = "";
    let filterTimeout: number;

    // Paginación
    let currentPage = 1;
    let totalPages = 1;
    let totalItems = 0;
    let itemsPerPage = 10;

    function getFilterParams() {
        const params: any = {};

        // Search filter
        if (searchTerm && searchTerm.trim()) {
            params.search = searchTerm.trim();
        }

        // Status filter
        if (statusFilter) {
            params.is_active = statusFilter === "activo";
        }

        // Type filter
        if (typeFilter && typeFilter.trim()) {
            params.package_type = typeFilter.trim();
        }

        // Pagination
        params.page = currentPage;
        params.limit = itemsPerPage;

        return params;
    }

    $: if (
        searchTerm !== undefined ||
        statusFilter !== undefined ||
        typeFilter !== undefined
    ) {
        clearTimeout(filterTimeout);
        filterTimeout = setTimeout(() => {
            loadPackages();
        }, 300);
    }

    // Labels para tipos de paquetes
    const PACKAGE_TYPE_LABELS = {
        individual: "Individual",
        professional: "Profesional",
        institutional: "Institucional",
    };

    // Labels para niveles de soporte
    const SUPPORT_LEVEL_LABELS = {
        basic: "Básico",
        standard: "Estándar",
        premium: "Premium",
        enterprise: "Empresarial",
    };

    async function loadPackages() {
        loading = true;
        error = "";

        try {
            const response = await getPackages();

            if (response && Array.isArray(response)) {
                packages = response;
                totalItems = packages.length;
                totalPages = Math.ceil(totalItems / itemsPerPage);

                // Aplicar filtros localmente
                let filteredPackages = packages;

                if (searchTerm && searchTerm.trim()) {
                    const search = searchTerm.trim().toLowerCase();
                    filteredPackages = filteredPackages.filter(
                        (pkg) =>
                            pkg.name.toLowerCase().includes(search) ||
                            (pkg.description &&
                                pkg.description.toLowerCase().includes(search)),
                    );
                }

                if (statusFilter) {
                    const isActive = statusFilter === "activo";
                    filteredPackages = filteredPackages.filter(
                        (pkg) => pkg.is_active === isActive,
                    );
                }

                if (typeFilter && typeFilter.trim()) {
                    filteredPackages = filteredPackages.filter(
                        (pkg) => pkg.package_type === typeFilter,
                    );
                }

                packages = filteredPackages;
                totalItems = packages.length;
                totalPages = Math.ceil(totalItems / itemsPerPage);
            } else {
                error = "Error al cargar paquetes";
            }
        } catch (err) {
            console.error("Error loading packages:", err);
            error = "Error de conexión al cargar paquetes";
        } finally {
            loading = false;
        }
    }

    function openModal(pkg?: Package | null) {
        selectedPackage = pkg || null;
        showModal = true;
    }

    function closeModal() {
        showModal = false;
        selectedPackage = null;
    }

    async function handlePackageSubmit(event: CustomEvent) {
        const packageData = event.detail;

        try {
            if (selectedPackage) {
                // Actualizar paquete existente
                const response = await updatePackage(
                    selectedPackage.id,
                    packageData,
                );
                if (response.success) {
                    await loadPackages();
                    closeModal();
                } else {
                    console.error("Error updating package:", response.message);
                }
            } else {
                // Crear nuevo paquete
                const response = await createPackage(packageData);
                if (response.success) {
                    await loadPackages();
                    closeModal();
                } else {
                    console.error("Error creating package:", response.message);
                }
            }
        } catch (err) {
            console.error("Error handling package submit:", err);
        }
    }

    function openDeleteModal(pkg: Package) {
        selectedPackage = pkg;
        showDeleteModal = true;
    }

    function closeDeleteModal() {
        showDeleteModal = false;
        selectedPackage = null;
    }

    async function confirmDelete() {
        if (!selectedPackage) return;

        deleting = true;
        try {
            const response = await deletePackage(selectedPackage.id);
            if (response.success) {
                showDeleteNotification = true;
                deleteNotificationType = "success";
                deleteNotificationMessage = "Paquete eliminado exitosamente";
                deleteNotificationSubtitle = `"${selectedPackage.name}" ha sido eliminado`;

                setTimeout(() => {
                    showDeleteNotification = false;
                }, 5000);

                await loadPackages();
            } else {
                showDeleteNotification = true;
                deleteNotificationType = "error";
                deleteNotificationMessage = "Error al eliminar paquete";
                deleteNotificationSubtitle =
                    response.message || "No se pudo eliminar el paquete";

                setTimeout(() => {
                    showDeleteNotification = false;
                }, 5000);
            }
        } catch (err) {
            console.error("Error deleting package:", err);
            showDeleteNotification = true;
            deleteNotificationType = "error";
            deleteNotificationMessage = "Error de conexión";
            deleteNotificationSubtitle = "No se pudo eliminar el paquete";

            setTimeout(() => {
                showDeleteNotification = false;
            }, 5000);
        } finally {
            deleting = false;
            closeDeleteModal();
        }
    }

    function prevPage() {
        if (currentPage > 1) {
            currentPage--;
            loadPackages();
        }
    }

    function nextPage() {
        if (currentPage < totalPages) {
            currentPage++;
            loadPackages();
        }
    }

    function formatPrice(price: number): string {
        return new Intl.NumberFormat("es-AR", {
            style: "currency",
            currency: "ARS",
        }).format(price / 100); // Asumiendo que el precio está en centavos
    }

    function formatDate(dateString: string): string {
        return new Date(dateString).toLocaleDateString("es-AR");
    }

    onMount(() => {
        loadPackages();
    });
</script>

<div class="package-table-section">
    <div class="section-header">
        <div class="header-content">
            <h2>📦 Gestión de Paquetes</h2>
            <p>Administra paquetes de servicios y suscripciones</p>
        </div>
        <div class="header-actions">
            <button
                class="btn-secondary"
                on:click={loadPackages}
                disabled={loading}
            >
                <RefreshIcon size={16} />
                {loading ? "Cargando..." : "Actualizar"}
            </button>
            <button class="btn-primary" on:click={() => openModal()}>
                <span>+</span> Nuevo Paquete
            </button>
        </div>
    </div>

    <!-- Filtros -->
    <div class="filters-section">
        <div class="filters-grid">
            <div class="filter-group">
                <label>Buscar</label>
                <input
                    type="text"
                    placeholder="Buscar por nombre..."
                    bind:value={searchTerm}
                />
            </div>
            <div class="filter-group">
                <label>Estado</label>
                <select bind:value={statusFilter}>
                    <option value="">Todos</option>
                    <option value="activo">Activo</option>
                    <option value="inactivo">Inactivo</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Tipo</label>
                <select bind:value={typeFilter}>
                    <option value="">Todos</option>
                    <option value="individual">Individual</option>
                    <option value="professional">Profesional</option>
                    <option value="institutional">Institucional</option>
                </select>
            </div>
        </div>
    </div>

    <!-- Tabla de Paquetes -->
    <div class="table-container">
        {#if loading}
            <div class="loading">Cargando paquetes...</div>
        {:else if error}
            <div class="error">{error}</div>
        {:else if packages.length === 0}
            <div class="empty">
                <PackageIcon size={48} />
                <h3>No hay paquetes</h3>
                <p>No se encontraron paquetes con los filtros aplicados</p>
                <button class="btn-primary" on:click={() => openModal()}>
                    Crear primer paquete
                </button>
            </div>
        {:else}
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Tipo</th>
                        <th>Precio Mensual</th>
                        <th>Precio Anual</th>
                        <th>Límites</th>
                        <th>Soporte</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {#each packages as pkg (pkg.id)}
                        <tr>
                            <td>
                                <div class="package-info">
                                    <div class="package-name">
                                        {pkg.name}
                                        {#if pkg.is_featured}
                                            <span class="featured-badge"
                                                >Destacado</span
                                            >
                                        {/if}
                                    </div>
                                    {#if pkg.description}
                                        <div class="package-description">
                                            {pkg.description}
                                        </div>
                                    {/if}
                                </div>
                            </td>
                            <td>
                                <span class="package-type">
                                    {PACKAGE_TYPE_LABELS[
                                        pkg.package_type as keyof typeof PACKAGE_TYPE_LABELS
                                    ] || pkg.package_type}
                                </span>
                            </td>
                            <td>
                                <span class="price"
                                    >{formatPrice(pkg.price_monthly)}</span
                                >
                            </td>
                            <td>
                                {#if pkg.price_yearly}
                                    <span class="price"
                                        >{formatPrice(pkg.price_yearly)}</span
                                    >
                                {:else}
                                    <span class="no-price">-</span>
                                {/if}
                            </td>
                            <td>
                                <div class="limits">
                                    {#if pkg.max_users}
                                        <span class="limit-item"
                                            >👥 {pkg.max_users}</span
                                        >
                                    {/if}
                                    {#if pkg.max_devices}
                                        <span class="limit-item"
                                            >📱 {pkg.max_devices}</span
                                        >
                                    {/if}
                                    {#if pkg.max_storage_gb}
                                        <span class="limit-item"
                                            >💾 {pkg.max_storage_gb}GB</span
                                        >
                                    {/if}
                                    {#if !pkg.max_users && !pkg.max_devices && !pkg.max_storage_gb}
                                        <span class="unlimited">Ilimitado</span>
                                    {/if}
                                </div>
                            </td>
                            <td>
                                {#if pkg.support_level}
                                    <span class="support-level">
                                        {SUPPORT_LEVEL_LABELS[
                                            pkg.support_level as keyof typeof SUPPORT_LEVEL_LABELS
                                        ] || pkg.support_level}
                                    </span>
                                {:else}
                                    <span class="no-support">-</span>
                                {/if}
                            </td>
                            <td>
                                <span
                                    class="status-badge {pkg.is_active
                                        ? 'active'
                                        : 'inactive'}"
                                >
                                    {pkg.is_active ? "Activo" : "Inactivo"}
                                </span>
                            </td>
                            <td>
                                <div class="actions-grid">
                                    <button
                                        class="action-btn"
                                        title="Editar paquete"
                                        on:click={() => openModal(pkg)}
                                    >
                                        <svg
                                            width="20"
                                            height="20"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor"
                                            stroke-width="1.8"
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                        >
                                            <path d="M12 20h9" />
                                            <path
                                                d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19.5 3 21l1.5-4L16.5 3.5z"
                                            />
                                        </svg>
                                    </button>
                                    <button
                                        class="action-btn delete"
                                        title="Eliminar paquete"
                                        on:click={() => openDeleteModal(pkg)}
                                    >
                                        <svg
                                            width="20"
                                            height="20"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor"
                                            stroke-width="1.8"
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                        >
                                            <path d="M3 6h18" />
                                            <path
                                                d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                                            />
                                            <path
                                                d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0v12m4-12v12"
                                            />
                                        </svg>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>

            <!-- Paginación -->
            {#if totalPages > 1}
                <div class="pagination">
                    <button on:click={prevPage} disabled={currentPage === 1}>
                        Anterior
                    </button>
                    <span>Página {currentPage} de {totalPages}</span>
                    <button
                        on:click={nextPage}
                        disabled={currentPage === totalPages}
                    >
                        Siguiente
                    </button>
                </div>
            {/if}
        {/if}
    </div>
</div>

<!-- Modal de Formulario -->
<PackageFormModal
    open={showModal}
    editMode={!!selectedPackage}
    initialData={selectedPackage}
    on:submit={handlePackageSubmit}
    on:cancel={closeModal}
/>

<!-- Modal de Confirmación de Eliminación -->
{#if showDeleteModal && selectedPackage}
    <div class="modal-outer">
        <div class="modal-backdrop" on:click={closeDeleteModal}></div>
        <div class="modal delete-modal" role="dialog" aria-modal="true">
            <div class="modal-header">
                <h3>Confirmar Eliminación</h3>
                <button class="modal-close" on:click={closeDeleteModal}
                    >&times;</button
                >
            </div>
            <div class="modal-content">
                <div class="delete-warning">
                    <svg
                        width="48"
                        height="48"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.8"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <path d="M12 9v4" />
                        <path d="M12 17h.01" />
                        <path d="M21 19H3l9-16 9 16z" />
                    </svg>
                    <h4>¿Eliminar paquete?</h4>
                    <p>
                        Estás a punto de eliminar el paquete <strong
                            >"{selectedPackage.name}"</strong
                        >. Esta acción no se puede deshacer.
                    </p>
                    <p class="warning-text">
                        ⚠️ Los usuarios con este paquete asignado perderán su
                        suscripción.
                    </p>
                </div>
                <div class="modal-actions">
                    <button
                        type="button"
                        class="btn-danger"
                        on:click={confirmDelete}
                        disabled={deleting}
                    >
                        {deleting ? "Eliminando..." : "Sí, eliminar"}
                    </button>
                    <button
                        type="button"
                        class="btn-secondary"
                        on:click={closeDeleteModal}
                        disabled={deleting}
                    >
                        Cancelar
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if}

<!-- Notificación de Eliminación -->
{#if showDeleteNotification}
    <div class="notification {deleteNotificationType}">
        <div class="notification-content">
            <h4>{deleteNotificationMessage}</h4>
            <p>{deleteNotificationSubtitle}</p>
        </div>
        <button
            class="notification-close"
            on:click={() => (showDeleteNotification = false)}
        >
            &times;
        </button>
    </div>
{/if}

<style>
    .package-table-section {
        background: var(--color-bg-card);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-md);
        padding: 1.5rem;
        margin-bottom: 2rem;
    }

    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 2rem;
    }

    .header-content h2 {
        margin: 0 0 0.5rem 0;
        color: var(--color-text-primary);
        font-size: 1.5rem;
    }

    .header-content p {
        margin: 0;
        color: var(--color-text-secondary);
        font-size: 0.9rem;
    }

    .header-actions {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .btn-primary,
    .btn-secondary {
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: var(--border-radius);
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .btn-primary {
        background: var(--color-primary);
        color: white;
    }

    .btn-primary:hover {
        background: var(--color-primary-dark);
    }

    .btn-secondary {
        background: var(--color-bg-secondary);
        color: var(--color-text-primary);
        border: 1px solid var(--color-border);
    }

    .btn-secondary:hover {
        background: var(--color-bg-tertiary);
    }

    .filters-section {
        margin-bottom: 2rem;
        padding: 1rem;
        background: var(--color-bg-secondary);
        border-radius: var(--border-radius);
        border: 1px solid var(--color-border);
    }

    .filters-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }

    .filter-group {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .filter-group label {
        font-weight: 500;
        color: var(--color-text-primary);
        font-size: 0.9rem;
    }

    .filter-group input,
    .filter-group select {
        padding: 0.5rem;
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        background: var(--color-bg-primary);
        color: var(--color-text-primary);
    }

    .table-container {
        overflow-x: auto;
    }

    .data-table {
        width: 100%;
        border-collapse: collapse;
        background: var(--color-bg-primary);
        border-radius: var(--border-radius);
        overflow: hidden;
    }

    .data-table th,
    .data-table td {
        padding: 1rem;
        text-align: left;
        border-bottom: 1px solid var(--color-border);
    }

    .data-table th {
        background: var(--color-bg-secondary);
        font-weight: 600;
        color: var(--color-text-primary);
        font-size: 0.9rem;
    }

    .data-table tr:hover {
        background: var(--color-bg-secondary);
    }

    .package-info {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .package-name {
        font-weight: 500;
        color: var(--color-text-primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .featured-badge {
        background: var(--color-accent);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .package-description {
        font-size: 0.85rem;
        color: var(--color-text-secondary);
        line-height: 1.4;
    }

    .package-type {
        background: var(--color-bg-tertiary);
        color: var(--color-text-primary);
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .price {
        font-weight: 600;
        color: var(--color-success);
    }

    .no-price {
        color: var(--color-text-secondary);
        font-style: italic;
    }

    .limits {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .limit-item {
        background: var(--color-bg-tertiary);
        color: var(--color-text-primary);
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
    }

    .unlimited {
        color: var(--color-success);
        font-weight: 500;
        font-size: 0.85rem;
    }

    .support-level {
        background: var(--color-primary);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .no-support {
        color: var(--color-text-secondary);
        font-style: italic;
    }

    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .status-badge.active {
        background: var(--color-success);
        color: white;
    }

    .status-badge.inactive {
        background: var(--color-danger);
        color: white;
    }

    .actions-grid {
        display: flex;
        gap: 0.5rem;
    }

    .action-btn {
        background: none;
        border: none;
        padding: 0.5rem;
        border-radius: var(--border-radius);
        cursor: pointer;
        color: var(--color-text-secondary);
        transition: all 0.2s;
    }

    .action-btn:hover {
        background: var(--color-bg-secondary);
        color: var(--color-text-primary);
    }

    .action-btn.delete:hover {
        background: var(--color-danger);
        color: white;
    }

    .pagination {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin-top: 2rem;
        padding: 1rem;
    }

    .pagination button {
        padding: 0.5rem 1rem;
        border: 1px solid var(--color-border);
        background: var(--color-bg-primary);
        color: var(--color-text-primary);
        border-radius: var(--border-radius);
        cursor: pointer;
        transition: all 0.2s;
    }

    .pagination button:hover:not(:disabled) {
        background: var(--color-bg-secondary);
    }

    .pagination button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .loading,
    .error,
    .empty {
        text-align: center;
        padding: 3rem;
        color: var(--color-text-secondary);
    }

    .empty {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }

    .empty h3 {
        margin: 0;
        color: var(--color-text-primary);
    }

    .error {
        color: var(--color-danger);
    }

    /* Modal styles */
    .modal-outer {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .modal-backdrop {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
    }

    .modal {
        position: relative;
        background: var(--color-bg-primary);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        max-width: 500px;
        width: 90%;
        max-height: 90vh;
        overflow-y: auto;
    }

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem;
        border-bottom: 1px solid var(--color-border);
    }

    .modal-header h3 {
        margin: 0;
        color: var(--color-text-primary);
    }

    .modal-close {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: var(--color-text-secondary);
        padding: 0;
        width: 2rem;
        height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: var(--border-radius);
    }

    .modal-close:hover {
        background: var(--color-bg-secondary);
        color: var(--color-text-primary);
    }

    .modal-content {
        padding: 1.5rem;
    }

    .delete-warning {
        text-align: center;
        color: var(--color-text-primary);
    }

    .delete-warning svg {
        color: var(--color-warning);
        margin-bottom: 1rem;
    }

    .delete-warning h4 {
        margin: 0 0 1rem 0;
        color: var(--color-text-primary);
    }

    .delete-warning p {
        margin: 0 0 1rem 0;
        line-height: 1.5;
    }

    .warning-text {
        color: var(--color-warning) !important;
        font-weight: 500;
    }

    .modal-actions {
        display: flex;
        gap: 1rem;
        justify-content: flex-end;
        margin-top: 2rem;
    }

    .btn-danger {
        background: var(--color-danger);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: var(--border-radius);
        cursor: pointer;
        font-weight: 500;
        transition: background-color 0.2s;
    }

    .btn-danger:hover:not(:disabled) {
        background: var(--color-danger-dark);
    }

    /* Notification styles */
    .notification {
        position: fixed;
        top: 2rem;
        right: 2rem;
        background: var(--color-bg-primary);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        border-left: 4px solid;
        max-width: 400px;
        z-index: 1001;
        animation: slideIn 0.3s ease-out;
    }

    .notification.success {
        border-left-color: var(--color-success);
    }

    .notification.error {
        border-left-color: var(--color-danger);
    }

    .notification-content {
        padding: 1rem;
    }

    .notification-content h4 {
        margin: 0 0 0.5rem 0;
        color: var(--color-text-primary);
        font-size: 1rem;
    }

    .notification-content p {
        margin: 0;
        color: var(--color-text-secondary);
        font-size: 0.9rem;
    }

    .notification-close {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        background: none;
        border: none;
        font-size: 1.25rem;
        cursor: pointer;
        color: var(--color-text-secondary);
        padding: 0.25rem;
        border-radius: var(--border-radius);
    }

    .notification-close:hover {
        background: var(--color-bg-secondary);
        color: var(--color-text-primary);
    }

    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    /* Responsive */
    @media (max-width: 768px) {
        .section-header {
            flex-direction: column;
            gap: 1rem;
            align-items: stretch;
        }

        .header-actions {
            justify-content: stretch;
        }

        .filters-grid {
            grid-template-columns: 1fr;
        }

        .data-table {
            font-size: 0.9rem;
        }

        .data-table th,
        .data-table td {
            padding: 0.75rem 0.5rem;
        }

        .actions-grid {
            flex-direction: column;
            gap: 0.25rem;
        }

        .modal {
            width: 95%;
            margin: 1rem;
        }
    }
</style>
