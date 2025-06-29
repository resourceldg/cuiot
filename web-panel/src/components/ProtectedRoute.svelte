<script>
    import { requirePermission, requireAuth } from '$lib/roles.js';
    import { onMount } from 'svelte';

    export let permission = null;
    export let fallback = '/dashboard/overview';

    let authorized = false;
    let loading = true;

    onMount(() => {
        if (permission) {
            authorized = requirePermission(permission);
        } else {
            authorized = requireAuth();
        }
        loading = false;
    });
</script>

{#if loading}
    <div class="flex items-center justify-center h-64">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
{:else if authorized}
    <slot />
{:else}
    <div class="flex items-center justify-center h-64">
        <div class="text-center">
            <h2 class="text-xl font-semibold text-gray-900 mb-2">Acceso Denegado</h2>
            <p class="text-gray-600 mb-4">No tienes permisos para acceder a esta página.</p>
            <a href={fallback} class="text-blue-600 hover:text-blue-800">
                Volver al dashboard
            </a>
        </div>
    </div>
{/if} 