<script lang="ts">
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let filters: Array<{
        key: string;
        label: string;
        type: "select" | "date" | "checkbox" | "text";
        options?: Array<{ value: string; label: string }>;
        placeholder?: string;
    }> = [];

    export let searchPlaceholder = "Buscar...";
    export let showSearch = true;
    export let showExport = false;
    export let showClear = true;
    export let loading = false;

    // Estados de filtros
    let filterValues: Record<string, any> = {};
    let searchValue = "";

    // Inicializar valores de filtros
    $: {
        filters.forEach((filter) => {
            if (!(filter.key in filterValues)) {
                filterValues[filter.key] =
                    filter.type === "checkbox" ? false : "";
            }
        });
    }

    // Funciones
    function handleFilterChange(key: string, value: any) {
        filterValues[key] = value;
        dispatch("filterChange", { key, value });
    }

    function handleSearch(event: Event) {
        const target = event.target as HTMLInputElement;
        searchValue = target.value;
        dispatch("search", { value: searchValue });
    }

    function handleExport() {
        dispatch("export");
    }

    function handleClear() {
        // Limpiar todos los filtros
        Object.keys(filterValues).forEach((key) => {
            filterValues[key] =
                filters.find((f) => f.key === key)?.type === "checkbox"
                    ? false
                    : "";
        });
        searchValue = "";
        dispatch("clear");
    }
</script>

<div class="filter-bar">
    <div class="filter-controls">
        <!-- Filtros -->
        {#each filters as filter}
            <div class="filter-item">
                {#if filter.type !== "checkbox"}
                    <label class="filter-label">{filter.label}</label>
                {/if}
                <div class="filter-input-wrapper">
                    {#if filter.type === "select"}
                        <select
                            bind:value={filterValues[filter.key]}
                            on:change={(e) =>
                                handleFilterChange(filter.key, e.target.value)}
                            class="filter-select"
                        >
                            <option value=""
                                >{filter.placeholder ||
                                    `Seleccionar ${filter.label}`}</option
                            >
                            {#each filter.options || [] as option}
                                <option value={option.value}
                                    >{option.label}</option
                                >
                            {/each}
                        </select>
                    {:else if filter.type === "date"}
                        <input
                            type="date"
                            bind:value={filterValues[filter.key]}
                            on:change={(e) =>
                                handleFilterChange(filter.key, e.target.value)}
                            class="filter-input"
                            placeholder={filter.placeholder}
                        />
                    {:else if filter.type === "checkbox"}
                        <label class="filter-checkbox">
                            <input
                                type="checkbox"
                                bind:checked={filterValues[filter.key]}
                                on:change={(e) =>
                                    handleFilterChange(
                                        filter.key,
                                        e.target.checked,
                                    )}
                            />
                            <span>{filter.label}</span>
                        </label>
                    {:else if filter.type === "text"}
                        <input
                            type="text"
                            bind:value={filterValues[filter.key]}
                            on:input={(e) =>
                                handleFilterChange(filter.key, e.target.value)}
                            class="filter-input"
                            placeholder={filter.placeholder || filter.label}
                        />
                    {/if}
                </div>
            </div>
        {/each}

        <!-- Búsqueda -->
        {#if showSearch}
            <div class="filter-item search-item">
                <div class="search-wrapper">
                    <input
                        type="text"
                        bind:value={searchValue}
                        on:input={handleSearch}
                        placeholder={searchPlaceholder}
                        class="search-input"
                    />
                    <span class="search-icon">🔍</span>
                </div>
            </div>
        {/if}
    </div>

    <!-- Acciones -->
    <div class="filter-actions">
        {#if showClear}
            <button
                class="action-btn action-btn--clear"
                on:click={handleClear}
                disabled={loading}
            >
                Limpiar
            </button>
        {/if}

        {#if showExport}
            <button
                class="action-btn action-btn--export"
                on:click={handleExport}
                disabled={loading}
            >
                Exportar
            </button>
        {/if}
    </div>
</div>

<style>
    .filter-bar {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        gap: var(--spacing-lg);
        padding: var(--spacing-lg);
        background: var(--color-bg-card);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        margin-bottom: var(--spacing-lg);
    }

    .filter-controls {
        display: flex;
        gap: var(--spacing-md);
        flex-wrap: wrap;
        flex: 1;
    }

    .filter-item {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-xs);
        min-width: 150px;
    }

    .filter-label {
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--color-text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .filter-input-wrapper {
        position: relative;
    }

    .filter-input,
    .filter-select {
        width: 100%;
        padding: var(--spacing-sm) var(--spacing-md);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        background: var(--color-bg);
        color: var(--color-text);
        font-size: 0.9rem;
        transition: border-color 0.2s ease;
    }

    .filter-input:focus,
    .filter-select:focus {
        outline: none;
        border-color: var(--color-accent);
    }

    .filter-checkbox {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        cursor: pointer;
        font-size: 0.9rem;
        color: var(--color-text);
    }

    .filter-checkbox input[type="checkbox"] {
        width: 16px;
        height: 16px;
        accent-color: var(--color-accent);
    }

    .search-item {
        min-width: 200px;
    }

    .search-wrapper {
        position: relative;
    }

    .search-input {
        width: 100%;
        padding: var(--spacing-sm) var(--spacing-md);
        padding-right: 40px;
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

    .search-icon {
        position: absolute;
        right: var(--spacing-sm);
        top: 50%;
        transform: translateY(-50%);
        color: var(--color-text-secondary);
        font-size: 0.9rem;
    }

    .filter-actions {
        display: flex;
        gap: var(--spacing-sm);
        align-items: flex-end;
    }

    .action-btn {
        padding: var(--spacing-sm) var(--spacing-md);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        background: var(--color-bg);
        color: var(--color-text);
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        white-space: nowrap;
    }

    .action-btn:hover:not(:disabled) {
        background: var(--color-bg-hover);
        transform: translateY(-1px);
    }

    .action-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .action-btn--clear {
        border-color: var(--color-text-secondary);
        color: var(--color-text-secondary);
    }

    .action-btn--clear:hover:not(:disabled) {
        background: var(--color-text-secondary);
        color: var(--color-bg);
    }

    .action-btn--export {
        background: var(--color-accent);
        color: var(--color-bg);
        border-color: var(--color-accent);
    }

    .action-btn--export:hover:not(:disabled) {
        opacity: 0.9;
    }

    @media (max-width: 768px) {
        .filter-bar {
            flex-direction: column;
            align-items: stretch;
            gap: var(--spacing-md);
        }

        .filter-controls {
            flex-direction: column;
        }

        .filter-item {
            min-width: auto;
        }

        .search-item {
            min-width: auto;
        }

        .filter-actions {
            justify-content: flex-end;
        }
    }

    @media (max-width: 480px) {
        .filter-actions {
            flex-direction: column;
        }

        .action-btn {
            width: 100%;
        }
    }
</style>
