<script>
    export let message = "";
    export let type = "success"; // 'success' | 'error'
    export let visible = false;
    export let duration = 2500;
    let timeout;

    $: if (visible && message) {
        clearTimeout(timeout);
        timeout = setTimeout(() => (visible = false), duration);
    }
</script>

{#if visible}
    <div class="toast {type}">
        {message}
    </div>
{/if}

<style>
    .toast {
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        min-width: 220px;
        max-width: 90vw;
        padding: 1rem 2rem;
        border-radius: 0.5rem;
        color: #fff;
        font-weight: 500;
        font-size: 1rem;
        box-shadow: 0 4px 24px 0 rgba(37, 99, 235, 0.12);
        z-index: 3000;
        opacity: 0.98;
        animation: fadeIn 0.2s;
        text-align: center;
    }
    .toast.success {
        background: #10b981;
    }
    .toast.error {
        background: #ef4444;
    }
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateX(-50%) translateY(20px);
        }
        to {
            opacity: 0.98;
            transform: translateX(-50%) translateY(0);
        }
    }
</style>
