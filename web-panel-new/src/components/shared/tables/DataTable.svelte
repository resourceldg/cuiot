<script lang="ts">
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let columns: Array<{
        key: string;
        label: string;
        sortable?: boolean;
        width?: string;
        render?: (value: any, item: any) => string;
    }> = [];

    export let data: any[] = [];
    export let loading = false;
    export let selectable = false;
    export let sortable = true;
    export let pagination = true;
    export let itemsPerPage = 10;
    export let currentPage = 1;
    export let totalItems = 0;
    export let selectedItems: any[] = [];
    export let sortColumn = "";
    export let sortDirection: "asc" | "desc" = "asc";
    export let emptyMessage = "No hay datos disponibles";
    export let searchTerm = "";
    export let showSearch = true;
    export let searchPlaceholder = "Buscar...";

    // Estados internos
    let allSelected = false;
    let filteredData = data;

    // Reactividad para filtrado y paginación
    $: {
        filteredData = data.filter((item) => {
            if (!searchTerm) return true;
            return columns.some((col) => {
                const value = item[col.key];
                return (
                    value &&
                    value
                        .toString()
                        .toLowerCase()
                        .includes(searchTerm.toLowerCase())
                );
            });
        });
    }

    $: totalPages = Math.ceil(totalItems / itemsPerPage);
    $: startIndex = (currentPage - 1) * itemsPerPage;
    $: endIndex = Math.min(startIndex + itemsPerPage, totalItems);
    $: paginatedData = filteredData.slice(startIndex, endIndex);

    // Funciones
    function handleSort(columnKey: string) {
        if (
            !sortable ||
            !columns.find((col) => col.key === columnKey)?.sortable
        )
            return;

        if (sortColumn === columnKey) {
            sortDirection = sortDirection === "asc" ? "desc" : "asc";
        } else {
            sortColumn = columnKey;
            sortDirection = "asc";
        }

        dispatch("sort", { column: sortColumn, direction: sortDirection });
    }

    function handlePageChange(page: number) {
        if (page < 1 || page > totalPages) return;
        currentPage = page;
        dispatch("pageChange", { page });
    }

    function handleSelectionChange(item: any, checked: boolean) {
        if (checked) {
            selectedItems = [...selectedItems, item];
        } else {
            selectedItems = selectedItems.filter(
                (selected) => selected.id !== item.id,
            );
        }
        dispatch("selectionChange", { selectedItems });
    }

    function handleSelectAll(checked: boolean) {
        if (checked) {
            selectedItems = [...paginatedData];
        } else {
            selectedItems = [];
        }
        allSelected = checked;
        dispatch("selectionChange", { selectedItems });
    }

    function handleSearch(event: Event) {
        const target = event.target as HTMLInputElement;
        searchTerm = target.value;
        currentPage = 1; // Reset to first page when searching
        dispatch("search", { value: searchTerm });
    }

    function handleAction(action: string, item: any) {
        dispatch("action", { action, item });
    }

    function isSelected(item: any) {
        return selectedItems.some((selected) => selected.id === item.id);
    }

    function renderCell(column: any, item: any) {
        const value = item[column.key];

        if (column.render) {
            return column.render(value, item);
        }

        return value || "-";
    }
</script>

<div class="data-table-container">
    <!-- Search Bar -->
    {#if showSearch}
        <div class="table-search">
            <input
                type="text"
                placeholder={searchPlaceholder}
                bind:value={searchTerm}
                on:input={handleSearch}
                class="search-input"
            />
        </div>
    {/if}

    <!-- Table -->
    <div class="table-wrapper">
        <table class="data-table">
            <thead>
                <tr>
                    {#if selectable}
                        <th class="select-column">
                            <input
                                type="checkbox"
                                checked={allSelected}
                                on:change={(e) =>
                                    handleSelectAll(e.target.checked)}
                            />
                        </th>
                    {/if}
                    {#each columns as column}
                        <th
                            class="table-header {column.sortable && sortable
                                ? 'sortable'
                                : ''}"
                            style="width: {column.width || 'auto'}"
                            on:click={() => handleSort(column.key)}
                        >
                            <div class="header-content">
                                <span>{column.label}</span>
                                {#if column.sortable && sortable}
                                    <span class="sort-icon">
                                        {#if sortColumn === column.key}
                                            {sortDirection === "asc"
                                                ? "↑"
                                                : "↓"}
                                        {:else}
                                            ↕
                                        {/if}
                                    </span>
                                {/if}
                            </div>
                        </th>
                    {/each}
                    <th class="actions-column">Acciones</th>
                </tr>
            </thead>
            <tbody>
                {#if loading}
                    <tr>
                        <td
                            colspan={columns.length + (selectable ? 2 : 1)}
                            class="loading-row"
                        >
                            <div class="loading-spinner"></div>
                            <span>Cargando datos...</span>
                        </td>
                    </tr>
                {:else if paginatedData.length === 0}
                    <tr>
                        <td
                            colspan={columns.length + (selectable ? 2 : 1)}
                            class="empty-row"
                        >
                            <div class="empty-state">
                                <span class="empty-icon">📋</span>
                                <span>{emptyMessage}</span>
                            </div>
                        </td>
                    </tr>
                {:else}
                    {#each paginatedData as item (item.id || item)}
                        <tr class="table-row">
                            {#if selectable}
                                <td class="select-cell">
                                    <input
                                        type="checkbox"
                                        checked={isSelected(item)}
                                        on:change={(e) =>
                                            handleSelectionChange(
                                                item,
                                                e.target.checked,
                                            )}
                                    />
                                </td>
                            {/if}
                            {#each columns as column}
                                <td class="table-cell">
                                    {@html renderCell(column, item)}
                                </td>
                            {/each}
                            <td class="actions-cell">
                                <div class="action-buttons">
                                    <button
                                        class="action-btn action-btn--edit"
                                        on:click={() =>
                                            handleAction("edit", item)}
                                        title="Editar"
                                    >
                                        ✏️
                                    </button>
                                    <button
                                        class="action-btn action-btn--delete"
                                        on:click={() =>
                                            handleAction("delete", item)}
                                        title="Eliminar"
                                    >
                                        🗑️
                                    </button>
                                </div>
                            </td>
                        </tr>
                    {/each}
                {/if}
            </tbody>
        </table>
    </div>

    <!-- Pagination -->
    {#if pagination && totalPages > 1}
        <div class="table-pagination">
            <div class="pagination-info">
                Mostrando {startIndex + 1}-{endIndex} de {totalItems} resultados
            </div>
            <div class="pagination-controls">
                <button
                    class="pagination-btn"
                    disabled={currentPage === 1}
                    on:click={() => handlePageChange(currentPage - 1)}
                >
                    ← Anterior
                </button>

                {#each Array.from( { length: Math.min(5, totalPages) }, (_, i) => {
                        const page = i + 1;
                        return page;
                    }, ) as page}
                    <button
                        class="pagination-btn {currentPage === page
                            ? 'active'
                            : ''}"
                        on:click={() => handlePageChange(page)}
                    >
                        {page}
                    </button>
                {/each}

                <button
                    class="pagination-btn"
                    disabled={currentPage === totalPages}
                    on:click={() => handlePageChange(currentPage + 1)}
                >
                    Siguiente →
                </button>
            </div>
        </div>
    {/if}
</div>

<style>
    .data-table-container {
        background: var(--color-bg-card);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        overflow: hidden;
    }

    .table-search {
        padding: var(--spacing-md);
        border-bottom: 1px solid var(--color-border);
    }

    .search-input {
        width: 100%;
        max-width: 300px;
        padding: var(--spacing-sm) var(--spacing-md);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        background: var(--color-bg);
        color: var(--color-text);
        font-size: 0.9rem;
    }

    .search-input:focus {
        outline: none;
        border-color: var(--color-accent);
    }

    .table-wrapper {
        overflow-x: auto;
    }

    .data-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }

    .table-header {
        background: var(--color-bg-hover);
        padding: var(--spacing-md);
        text-align: left;
        font-weight: 600;
        color: var(--color-text);
        border-bottom: 1px solid var(--color-border);
        white-space: nowrap;
    }

    .table-header.sortable {
        cursor: pointer;
        user-select: none;
    }

    .table-header.sortable:hover {
        background: var(--color-border);
    }

    .header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: var(--spacing-sm);
    }

    .sort-icon {
        font-size: 0.8rem;
        color: var(--color-text-secondary);
    }

    .table-row {
        border-bottom: 1px solid var(--color-border);
        transition: background-color 0.2s ease;
    }

    .table-row:hover {
        background: var(--color-bg-hover);
    }

    .table-cell {
        padding: var(--spacing-md);
        color: var(--color-text);
        border-bottom: 1px solid var(--color-border);
    }

    .select-column,
    .select-cell {
        width: 50px;
        text-align: center;
    }

    .actions-column,
    .actions-cell {
        width: 120px;
        text-align: center;
    }

    .action-buttons {
        display: flex;
        gap: var(--spacing-xs);
        justify-content: center;
    }

    .action-btn {
        background: none;
        border: none;
        padding: var(--spacing-xs);
        border-radius: var(--border-radius-sm);
        cursor: pointer;
        font-size: 1rem;
        transition: all 0.2s ease;
    }

    .action-btn--edit:hover {
        background: rgba(0, 230, 118, 0.1);
    }

    .action-btn--delete:hover {
        background: rgba(255, 77, 109, 0.1);
    }

    .loading-row,
    .empty-row {
        text-align: center;
        padding: var(--spacing-xl);
    }

    .loading-spinner {
        width: 20px;
        height: 20px;
        border: 2px solid var(--color-border);
        border-top: 2px solid var(--color-accent);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto var(--spacing-sm);
    }

    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--spacing-sm);
        color: var(--color-text-secondary);
    }

    .empty-icon {
        font-size: 2rem;
    }

    .table-pagination {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--spacing-md);
        border-top: 1px solid var(--color-border);
        background: var(--color-bg-hover);
    }

    .pagination-info {
        color: var(--color-text-secondary);
        font-size: 0.9rem;
    }

    .pagination-controls {
        display: flex;
        gap: var(--spacing-xs);
    }

    .pagination-btn {
        padding: var(--spacing-sm) var(--spacing-md);
        border: 1px solid var(--color-border);
        background: var(--color-bg);
        color: var(--color-text);
        border-radius: var(--border-radius-sm);
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }

    .pagination-btn:hover:not(:disabled) {
        background: var(--color-bg-hover);
    }

    .pagination-btn.active {
        background: var(--color-accent);
        color: var(--color-bg);
        border-color: var(--color-accent);
    }

    .pagination-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    @media (max-width: 768px) {
        .table-pagination {
            flex-direction: column;
            gap: var(--spacing-md);
        }

        .pagination-controls {
            flex-wrap: wrap;
            justify-content: center;
        }

        .action-buttons {
            flex-direction: column;
        }
    }
</style>
