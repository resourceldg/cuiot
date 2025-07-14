<script lang="ts">
    export let title = "";
    export let value: string | number = "";
    export let subtitle = "";
    export let icon = "";
    export let trend: {
        value: string;
        type: "positive" | "negative" | "neutral";
    } | null = null;
    export let color: "blue" | "green" | "red" | "orange" | "purple" | "gray" =
        "blue";
    export let size: "small" | "medium" | "large" = "medium";
    export let loading = false;

    const colorClasses = {
        blue: "metric-card--blue",
        green: "metric-card--green",
        red: "metric-card--red",
        orange: "metric-card--orange",
        purple: "metric-card--purple",
        gray: "metric-card--gray",
    };

    const sizeClasses = {
        small: "metric-card--small",
        medium: "metric-card--medium",
        large: "metric-card--large",
    };
</script>

<div class="metric-card {colorClasses[color]} {sizeClasses[size]}">
    <div class="metric-header">
        {#if icon}
            <div class="metric-icon">
                {icon}
            </div>
        {/if}
        <div class="metric-title">{title}</div>
    </div>

    <div class="metric-content">
        {#if loading}
            <div class="metric-loading">
                <div class="loading-skeleton"></div>
            </div>
        {:else}
            <div class="metric-value">{value}</div>
            {#if subtitle}
                <div class="metric-subtitle">{subtitle}</div>
            {/if}
            {#if trend}
                <div class="metric-trend metric-trend--{trend.type}">
                    {trend.value}
                </div>
            {/if}
        {/if}
    </div>
</div>

<style>
    .metric-card {
        background: var(--color-bg-card);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        padding: var(--spacing-lg);
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }

    .metric-header {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        margin-bottom: var(--spacing-md);
    }

    .metric-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: var(--border-radius);
        font-size: 1.2rem;
    }

    .metric-title {
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--color-text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-content {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-xs);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--color-text);
        line-height: 1.2;
    }

    .metric-subtitle {
        font-size: 0.85rem;
        color: var(--color-text-secondary);
    }

    .metric-trend {
        font-size: 0.8rem;
        font-weight: 600;
        padding: var(--spacing-xs) var(--spacing-sm);
        border-radius: var(--border-radius-sm);
        display: inline-flex;
        align-items: center;
        gap: var(--spacing-xs);
        width: fit-content;
    }

    .metric-trend::before {
        content: "";
        width: 0;
        height: 0;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
    }

    .metric-trend--positive {
        background: rgba(0, 230, 118, 0.1);
        color: var(--color-success);
    }

    .metric-trend--positive::before {
        border-bottom: 6px solid var(--color-success);
    }

    .metric-trend--negative {
        background: rgba(255, 77, 109, 0.1);
        color: var(--color-danger);
    }

    .metric-trend--negative::before {
        border-top: 6px solid var(--color-danger);
    }

    .metric-trend--neutral {
        background: rgba(176, 184, 201, 0.1);
        color: var(--color-text-secondary);
    }

    /* Color variants */
    .metric-card--blue .metric-icon {
        background: rgba(0, 123, 255, 0.1);
        color: #007bff;
    }

    .metric-card--green .metric-icon {
        background: rgba(0, 230, 118, 0.1);
        color: var(--color-success);
    }

    .metric-card--red .metric-icon {
        background: rgba(255, 77, 109, 0.1);
        color: var(--color-danger);
    }

    .metric-card--orange .metric-icon {
        background: rgba(241, 196, 15, 0.1);
        color: var(--color-warning);
    }

    .metric-card--purple .metric-icon {
        background: rgba(138, 43, 226, 0.1);
        color: #8a2be2;
    }

    .metric-card--gray .metric-icon {
        background: rgba(176, 184, 201, 0.1);
        color: var(--color-text-secondary);
    }

    /* Size variants */
    .metric-card--small {
        padding: var(--spacing-md);
    }

    .metric-card--small .metric-value {
        font-size: 1.5rem;
    }

    .metric-card--large {
        padding: var(--spacing-xl);
    }

    .metric-card--large .metric-value {
        font-size: 2.5rem;
    }

    /* Loading state */
    .metric-loading {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-sm);
    }

    .loading-skeleton {
        height: 2rem;
        background: linear-gradient(
            90deg,
            var(--color-border) 25%,
            var(--color-bg-hover) 50%,
            var(--color-border) 75%
        );
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
        border-radius: var(--border-radius-sm);
    }

    @keyframes loading {
        0% {
            background-position: 200% 0;
        }
        100% {
            background-position: -200% 0;
        }
    }

    @media (max-width: 768px) {
        .metric-card {
            padding: var(--spacing-md);
        }

        .metric-value {
            font-size: 1.5rem;
        }

        .metric-card--large .metric-value {
            font-size: 2rem;
        }
    }
</style>
