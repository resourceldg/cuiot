<script lang="ts">
    import { createEventDispatcher } from "svelte";
    export let user = {
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        role: "Cuidador",
        is_verified: false,
        username: "",
        date_of_birth: "",
    };
    export let editable = false;
    export let loading = false;
    const dispatch = createEventDispatcher();

    let editMode = false;
    let form = { ...user };

    // Definición de campos para fácil extensión
    const fields = [
        { key: "first_name", label: "Nombre", type: "text", required: true },
        { key: "last_name", label: "Apellido", type: "text", required: false },
        { key: "username", label: "Usuario", type: "text", required: false },
        { key: "email", label: "Email", type: "email", required: true },
        { key: "phone", label: "Teléfono", type: "tel", required: false },
        {
            key: "date_of_birth",
            label: "Fecha de nacimiento",
            type: "date",
            required: false,
        },
        // Agregar más campos aquí si se desea
    ];

    function startEdit() {
        editMode = true;
        form = { ...user };
    }
    function cancelEdit() {
        editMode = false;
        form = { ...user };
    }
    function save() {
        dispatch("save", { ...form });
        editMode = false;
    }

    function handleEdit() {
        dispatch("edit");
    }
</script>

<div
    class="w-full max-w-2xl bg-white rounded-xl shadow-md border border-gray-100 p-8 mb-8"
>
    <div
        class="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-2"
    >
        <div>
            <h2 class="text-2xl font-bold text-gray-900">Perfil de Cuidador</h2>
            <p class="text-gray-500 text-sm">
                Información personal y profesional
            </p>
        </div>
        <button
            on:click={handleEdit}
            class="btn-primary flex items-center gap-2"
            disabled={loading}
        >
            <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                ></path>
            </svg>
            Editar Perfil
        </button>
    </div>
    {#if loading}
        <div class="flex justify-center items-center py-8">
            <div
                class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"
            ></div>
        </div>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div>
                <div class="text-xs text-gray-500 mb-1">Nombre Completo</div>
                <div
                    class="font-semibold text-gray-900 bg-gray-50 rounded px-3 py-2"
                >
                    {user.first_name}
                    {user.last_name}
                </div>
            </div>
            <div>
                <div class="text-xs text-gray-500 mb-1">Email</div>
                <div
                    class="font-semibold text-gray-900 bg-gray-50 rounded px-3 py-2"
                >
                    {user.email}
                </div>
            </div>
            <div>
                <div class="text-xs text-gray-500 mb-1">Teléfono</div>
                <div class="text-gray-900 bg-gray-50 rounded px-3 py-2">
                    {user.phone}
                </div>
            </div>
            <div>
                <div class="text-xs text-gray-500 mb-1">
                    Fecha de Nacimiento
                </div>
                <div class="text-gray-900 bg-gray-50 rounded px-3 py-2">
                    {user.date_of_birth
                        ? new Date(user.date_of_birth).toLocaleDateString(
                              "es-ES",
                          )
                        : "No especificado"}
                </div>
            </div>
        </div>
        <div class="border-t pt-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">
                Información Profesional
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <div class="text-xs text-gray-500 mb-1">Especialidad</div>
                    <div class="text-gray-900 bg-gray-50 rounded px-3 py-2">
                        {user.role}
                    </div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 mb-1">
                        Años de Experiencia
                    </div>
                    <div class="text-gray-900 bg-gray-50 rounded px-3 py-2">
                        {user.is_verified ? "✔ Verificado" : "No verificado"}
                    </div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 mb-1">
                        Certificaciones
                    </div>
                    <div class="text-gray-900 bg-gray-50 rounded px-3 py-2">
                        {user.certifications || "-"}
                    </div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 mb-1">Estado</div>
                    <div class="text-gray-900 bg-gray-50 rounded px-3 py-2">
                        <span
                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {user.is_verified
                                ? 'bg-green-100 text-green-800'
                                : 'bg-red-100 text-red-800'}"
                        >
                            {user.is_verified ? "Activo" : "Inactivo"}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    .bg-green-100 {
        background-color: #d1fae5;
    }
    .text-green-700 {
        color: #047857;
    }
    .bg-yellow-100 {
        background-color: #fef9c3;
    }
    .text-yellow-700 {
        color: #b45309;
    }
</style>
