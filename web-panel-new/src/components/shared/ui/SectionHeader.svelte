<script>
    export let title = "";
    export let subtitle = "";
    export let icon = null;
    export let actions = [];
</script>

<div class="section-header">
    <div class="header-content">
        {#if icon}
            <div class="header-icon">
                <slot name="icon">
                    {icon}
                </slot>
            </div>
        {/if}
        <div class="header-text">
            <h1 class="header-title">{title}</h1>
            {#if subtitle}
                <p class="header-subtitle">{subtitle}</p>
            {/if}
        </div>
    </div>

    {#if actions.length > 0}
        <div class="header-actions">
            {#each actions as action}
                <button
                    class="action-btn action-btn--{action.variant || 'primary'}"
                    on:click={action.action}
                    title={action.label}
                >
                    {#if action.icon}
                        <span class="action-icon">{action.icon}</span>
                    {/if}
                    {action.label}
                </button>
            {/each}
        </div>
    {/if}
</div>

<style>
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: var(--spacing-xl);
        padding-bottom: var(--spacing-md);
        border-bottom: 1px solid var(--color-border);
    }

    .header-content {
        display: flex;
        align-items: center;
        gap: var(--spacing-md);
    }

    .header-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        background: var(--color-bg-hover);
        border-radius: var(--border-radius);
        color: var(--color-accent);
    }

    .header-text {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-xs);
    }

    .header-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--color-text);
        margin: 0;
        line-height: 1.2;
    }

    .header-subtitle {
        font-size: 1rem;
        color: var(--color-text-secondary);
        margin: 0;
        line-height: 1.4;
    }

    .header-actions {
        display: flex;
        gap: var(--spacing-sm);
        align-items: center;
    }

    .action-btn {
        display: flex;
        align-items: center;
        gap: var(--spacing-xs);
        padding: var(--spacing-sm) var(--spacing-md);
        border: none;
        border-radius: var(--border-radius);
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
    }

    .action-btn--primary {
        background: var(--color-accent);
        color: var(--color-bg);
    }

    .action-btn--primary:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }

    .action-btn--secondary {
        background: var(--color-bg-hover);
        color: var(--color-text);
        border: 1px solid var(--color-border);
    }

    .action-btn--secondary:hover {
        background: var(--color-border);
    }

    .action-btn--danger {
        background: var(--color-danger);
        color: white;
    }

    .action-btn--danger:hover {
        opacity: 0.9;
    }

    .action-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 16px;
        height: 16px;
    }

    @media (max-width: 768px) {
        .section-header {
            flex-direction: column;
            align-items: flex-start;
            gap: var(--spacing-md);
        }

        .header-content {
            width: 100%;
        }

        .header-actions {
            width: 100%;
            justify-content: flex-end;
        }

        .header-title {
            font-size: 1.5rem;
        }
    }
</style>
