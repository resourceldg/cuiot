import { authService } from '$lib/api.js';

export function load({ url }) {
    // Verificar si el usuario está autenticado
    const isAuthenticated = authService.isAuthenticated();
    const isAuthPage = url.pathname === '/login' || url.pathname === '/register';

    // Si no está autenticado y no está en una página de auth, redirigir a login
    if (!isAuthenticated && !isAuthPage && url.pathname !== '/') {
        return {
            redirect: '/login'
        };
    }

    // Si está autenticado y está en una página de auth, redirigir al dashboard
    if (isAuthenticated && isAuthPage) {
        return {
            redirect: '/'
        };
    }

    return {
        isAuthenticated,
        isAuthPage
    };
}

export const prerender = true;
export const ssr = false; 