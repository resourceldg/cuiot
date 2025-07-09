<script>
    import { goto } from "$app/navigation";
    import { login } from "$lib/auth.js";
    import LoginForm from "$lib/ui/LoginForm.svelte";

    let error = "";
    let loading = false;
    let sessionMessage = "";

    // Mostrar mensaje de sesión expirada si existe
    if (typeof window !== "undefined") {
        sessionMessage = sessionStorage.getItem("sessionMessage") || "";
        if (sessionMessage) sessionStorage.removeItem("sessionMessage");
    }

    async function handleLogin({ email, password }) {
        error = "";
        loading = true;
        try {
            await login(email, password);
            loading = false;
            goto("/dashboard");
        } catch (e) {
            error = e.message || "Error de autenticación";
            loading = false;
        }
    }
</script>

{#if sessionMessage}
    <div class="session-expired-banner">{sessionMessage}</div>
{/if}

<LoginForm {error} {loading} onSubmit={handleLogin} />

<style>
    .session-expired-banner {
        background: rgba(255, 77, 109, 0.12);
        color: var(--color-danger);
        border: 1.5px solid var(--color-danger);
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-size: 1.05rem;
        text-align: center;
        margin: 1.5rem auto 1.2rem auto;
        max-width: 400px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
</style>
