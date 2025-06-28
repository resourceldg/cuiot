<script>
    import { onMount } from "svelte";

    let loginResult = "";
    let elderlyResult = "";
    let currentToken = "";
    let loading = false;

    const API_BASE_URL = "http://localhost:8000/api/v1";

    async function apiRequest(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const defaultHeaders = {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        };

        const token = localStorage.getItem("authToken");
        if (token) {
            defaultHeaders.Authorization = `Bearer ${token}`;
        }

        const config = {
            ...options,
            headers: defaultHeaders,
        };

        try {
            const response = await fetch(url, config);
            console.log("Response status:", response.status);
            console.log("Response headers:", response.headers);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("API Error:", error);
            throw error;
        }
    }

    async function testLogin() {
        try {
            loading = true;
            const formData = new FormData();
            formData.append("username", "lucia.garcia@email.com");
            formData.append("password", "password123");

            const response = await apiRequest("/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams(formData),
            });

            localStorage.setItem("authToken", response.access_token);
            loginResult = JSON.stringify(response, null, 2);
            updateTokenDisplay();
        } catch (error) {
            loginResult = `Error: ${error.message}`;
        } finally {
            loading = false;
        }
    }

    async function testGetElderlyPersons() {
        try {
            loading = true;
            const response = await apiRequest("/elderly-persons/");
            elderlyResult = JSON.stringify(response, null, 2);
        } catch (error) {
            elderlyResult = `Error: ${error.message}`;
        } finally {
            loading = false;
        }
    }

    function updateTokenDisplay() {
        const token = localStorage.getItem("authToken");
        currentToken = token
            ? `Token: ${token.substring(0, 50)}...`
            : "No token";
    }

    onMount(() => {
        updateTokenDisplay();
    });
</script>

<svelte:head>
    <title>Test API - Viejos Son Los Trapos</title>
</svelte:head>

<div class="container mx-auto p-8 max-w-4xl">
    <h1 class="text-3xl font-bold mb-8 text-blue-900">Test API Frontend</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-white p-6 rounded-lg shadow-md">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">Login</h2>
            <button
                on:click={testLogin}
                disabled={loading}
                class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 mb-4"
            >
                {loading ? "Testing..." : "Test Login"}
            </button>
            <div
                class="bg-gray-100 p-4 rounded text-sm font-mono overflow-auto max-h-64"
            >
                <pre>{loginResult || "No result yet"}</pre>
            </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-md">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">
                Get Elderly Persons
            </h2>
            <button
                on:click={testGetElderlyPersons}
                disabled={loading}
                class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50 mb-4"
            >
                {loading ? "Testing..." : "Get Elderly Persons"}
            </button>
            <div
                class="bg-gray-100 p-4 rounded text-sm font-mono overflow-auto max-h-64"
            >
                <pre>{elderlyResult || "No result yet"}</pre>
            </div>
        </div>
    </div>

    <div class="mt-8 bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-xl font-semibold mb-4 text-gray-800">Current Token</h2>
        <div class="bg-gray-100 p-4 rounded text-sm font-mono">
            {currentToken}
        </div>
    </div>

    <div class="mt-8 bg-blue-50 p-6 rounded-lg">
        <h2 class="text-xl font-semibold mb-4 text-blue-900">Instrucciones</h2>
        <ol class="list-decimal list-inside space-y-2 text-blue-800">
            <li>Haz clic en "Test Login" para autenticarte</li>
            <li>Verifica que el token se muestre en "Current Token"</li>
            <li>Haz clic en "Get Elderly Persons" para obtener los datos</li>
            <li>
                Si todo funciona, los adultos mayores deberían aparecer en la
                página de Human
            </li>
        </ol>
    </div>
</div>
