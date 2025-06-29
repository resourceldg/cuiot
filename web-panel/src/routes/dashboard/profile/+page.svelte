<script lang="ts">
    import { goto } from "$app/navigation";
    import { userService } from "$lib/api.js";
    import { onMount } from "svelte";
    import AvailabilitySection from "../../../components/AvailabilitySection.svelte";
    import ChangePasswordSection from "../../../components/ChangePasswordSection.svelte";
    import PreferencesSection from "../../../components/PreferencesSection.svelte";
    import ProfileCard from "../../../components/ProfileCard.svelte";
    import ProfileEditModal from "../../../components/ProfileEditModal.svelte";

    let user = null;
    let userId = null;
    let feedback = { success: null, error: null };
    let showEdit = false;
    let loading = true;

    function parseJwt(token) {
        try {
            return JSON.parse(atob(token.split(".")[1]));
        } catch {
            return {};
        }
    }

    // Cargar datos completos del usuario desde el backend
    async function loadUser() {
        loading = true;
        feedback = { success: null, error: null };
        const token = localStorage.getItem("authToken");
        if (token) {
            try {
                const payload = parseJwt(token);
                userId = payload.sub ? parseInt(payload.sub) : null;
                if (!userId)
                    throw new Error("No se pudo obtener el ID de usuario");
                user = await userService.getById(userId);
            } catch (e) {
                feedback.error = e.message || "Error al cargar usuario.";
                user = null;
            }
        } else {
            goto("/login");
        }
        loading = false;
    }

    onMount(loadUser);

    // Maneja el guardado de datos personales
    async function handleSave(e) {
        feedback = { success: null, error: null };
        try {
            if (!userId) throw new Error("No se pudo obtener el ID de usuario");
            await userService.update(userId, e.detail);
            feedback.success = "Datos actualizados correctamente.";
            await loadUser(); // Refresca los datos
        } catch (err) {
            feedback.error = err.message || "Error al actualizar los datos.";
        }
    }
</script>

<svelte:head>
    <title>Mi Cuenta - CUIOT</title>
</svelte:head>

<div class="py-8 flex flex-col items-center min-h-screen bg-gray-50">
    {#if loading}
        <div class="flex flex-col items-center justify-center h-64">
            <div
                class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"
            ></div>
            <span class="text-gray-500">Cargando perfil...</span>
        </div>
    {:else if user}
        <!-- Card de perfil con botón de editar -->
        <ProfileCard {user} editable={true} on:edit={() => (showEdit = true)} />
        <!-- Modal de edición de perfil -->
        <ProfileEditModal
            {user}
            show={showEdit}
            on:close={() => (showEdit = false)}
            on:save={handleSave}
            on:delete={() => {
                alert(
                    "¿Seguro que quieres eliminar la cuenta? (Aquí va la lógica real)",
                );
            }}
        />
        <!-- Feedback visual -->
        {#if feedback.success}
            <div class="mt-4 text-green-600">{feedback.success}</div>
        {/if}
        {#if feedback.error}
            <div class="mt-4 text-red-600">{feedback.error}</div>
        {/if}
        <!-- Sección de cambio de contraseña -->
        <ChangePasswordSection />
        <!-- Sección de preferencias -->
        <PreferencesSection />
        <!-- Sección de disponibilidad -->
        <AvailabilitySection />
    {:else}
        <div class="text-red-600 mt-8">
            No se pudo cargar el perfil del usuario.
        </div>
    {/if}
</div>

<style>
    .min-h-screen {
        min-height: 100vh;
    }
    .bg-gray-50 {
        background-color: #f9fafb;
    }
</style>
