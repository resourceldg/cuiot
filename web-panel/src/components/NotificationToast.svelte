<script>
    import { notifications, removeNotification } from '$lib/stores.js';
    import { CheckCircle, XCircle, AlertTriangle, Info, X } from 'lucide-svelte';
    import { fade, fly } from 'svelte/transition';

    function getIcon(type) {
        switch (type) {
            case 'success':
                return CheckCircle;
            case 'error':
                return XCircle;
            case 'warning':
                return AlertTriangle;
            default:
                return Info;
        }
    }

    function getIconColor(type) {
        switch (type) {
            case 'success':
                return 'text-green-500';
            case 'error':
                return 'text-red-500';
            case 'warning':
                return 'text-yellow-500';
            default:
                return 'text-blue-500';
        }
    }

    function getBgColor(type) {
        switch (type) {
            case 'success':
                return 'bg-green-50 border-green-200';
            case 'error':
                return 'bg-red-50 border-red-200';
            case 'warning':
                return 'bg-yellow-50 border-yellow-200';
            default:
                return 'bg-blue-50 border-blue-200';
        }
    }
</script>

<div class="fixed top-4 right-4 z-50 space-y-2">
    {#each $notifications as notification (notification.id)}
        <div
            class="notification-toast {getBgColor(notification.type)} border rounded-lg shadow-lg p-4 max-w-sm"
            transition:fly={{ y: -50, duration: 300 }}
        >
            <div class="flex items-start gap-3">
                <div class="flex-shrink-0">
                    <svelte:component 
                        this={getIcon(notification.type)} 
                        class="w-5 h-5 {getIconColor(notification.type)}" 
                    />
                </div>
                <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">
                        {notification.message}
                    </p>
                </div>
                <button
                    class="flex-shrink-0 ml-2 text-gray-400 hover:text-gray-600"
                    on:click={() => removeNotification(notification.id)}
                >
                    <X class="w-4 h-4" />
                </button>
            </div>
        </div>
    {/each}
</div>

<style>
    .notification-toast {
        backdrop-filter: blur(10px);
    }
</style> 