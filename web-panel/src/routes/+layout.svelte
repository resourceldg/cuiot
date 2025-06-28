<script>
    import { goto } from "$app/navigation";
    import { authService, onSessionToast } from "$lib/api.js";
    import { onMount } from "svelte";
    import "../app.css";
    import Toast from "../components/Toast.svelte";

    let sessionToastVisible = false;
    let sessionToastMessage = "";
    let sessionToastType = "info";
    let sessionToastTimeout;

    function showSessionToast(type, timeLeft) {
        clearTimeout(sessionToastTimeout);
        if (type === "expiring") {
            sessionToastMessage = `Tu sesión expira en ${Math.max(1, Math.floor(timeLeft / 10) * 10)} segundos`;
            sessionToastType = "warning";
            sessionToastVisible = true;
            sessionToastTimeout = setTimeout(() => {
                sessionToastVisible = false;
            }, 5000);
        } else if (type === "expired") {
            sessionToastMessage =
                "Sesión expirada. Por favor, vuelve a iniciar sesión.";
            sessionToastType = "error";
            sessionToastVisible = true;
            sessionToastTimeout = setTimeout(() => {
                sessionToastVisible = false;
                goto("/login");
            }, 2500);
        }
    }

    onMount(() => {
        onSessionToast(showSessionToast);
        if (window.location.pathname === "/") {
            if (authService.isAuthenticated()) {
                goto("/dashboard");
            } else {
                goto("/login");
            }
        }
    });
</script>

<main>
    <slot />
    {#if sessionToastVisible}
        <div class="fixed top-6 right-6 z-[9999]">
            <Toast
                message={sessionToastMessage}
                type={sessionToastType}
                visible={sessionToastVisible}
            />
        </div>
    {/if}
</main>
