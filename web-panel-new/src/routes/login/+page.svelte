<script>
    import { goto } from "$app/navigation";
    import { login } from "$lib/auth.js";
    import LoginForm from "$lib/ui/LoginForm.svelte";

    let error = "";
    let loading = false;

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

<LoginForm {error} {loading} onSubmit={handleLogin} />
