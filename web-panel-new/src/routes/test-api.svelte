<script>
    import { authFetch } from "$lib/api/authFetch";
    import { getToken, login } from "$lib/auth.js";
    import { onMount } from "svelte";

    let email = "";
    let password = "";
    let token = "";
    let loginResult = "";
    let usersResult = "";
    let rolesResult = "";
    let loading = false;
    let error = "";

    function updateToken() {
        token = getToken() || "";
    }

    async function handleLogin() {
        loading = true;
        error = "";
        loginResult = "";
        try {
            await login(email, password);
            updateToken();
            loginResult = "Login OK";
        } catch (e) {
            if (e instanceof Error) {
                error = e.message;
            } else {
                error = "Error de autenticación";
            }
        } finally {
            loading = false;
        }
    }

    async function testUsers() {
        usersResult = "";
        try {
            const res = await authFetch("/users");
            usersResult =
                `${res.status} ${res.statusText}\n` +
                JSON.stringify(await res.json(), null, 2);
        } catch (e) {
            if (e instanceof Error) {
                usersResult = "Error: " + e.message;
            } else {
                usersResult = "Error: " + e;
            }
        }
    }

    async function testRoles() {
        rolesResult = "";
        try {
            const res = await authFetch("/users/roles");
            rolesResult =
                `${res.status} ${res.statusText}\n` +
                JSON.stringify(await res.json(), null, 2);
        } catch (e) {
            if (e instanceof Error) {
                rolesResult = "Error: " + e.message;
            } else {
                rolesResult = "Error: " + e;
            }
        }
    }

    onMount(updateToken);
</script>

<h1>Test API Usuarios/Roles</h1>

<div style="margin-bottom:2rem;">
    <label>Email: <input bind:value={email} type="email" /></label>
    <label style="margin-left:1rem;"
        >Password: <input bind:value={password} type="password" /></label
    >
    <button on:click={handleLogin} disabled={loading} style="margin-left:1rem;"
        >Login</button
    >
    {#if error}<span style="color:red; margin-left:1rem;">{error}</span>{/if}
    {#if loginResult}<span style="color:green; margin-left:1rem;"
            >{loginResult}</span
        >{/if}
</div>

<div style="margin-bottom:1rem;">
    <strong>Token actual:</strong>
    <div
        style="word-break:break-all; background:#222; color:#fff; padding:0.5rem;"
    >
        {token || "No token"}
    </div>
</div>

<div style="margin-bottom:1rem;">
    <button on:click={testUsers} disabled={!token}>Probar /users</button>
    <pre style="background:#eee; padding:0.5rem;">{usersResult}</pre>
</div>

<div style="margin-bottom:1rem;">
    <button on:click={testRoles} disabled={!token}>Probar /users/roles</button>
    <pre style="background:#eee; padding:0.5rem;">{rolesResult}</pre>
</div>
