<script lang="ts">
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import {
        refreshAlerts,
        refreshCaredPersons,
        refreshEvents,
        systemData,
    } from "$lib/stores.js";
    import { onMount } from "svelte";

    let personId = "";
    let person = null;
    let loading = true;
    let error = "";
    let alerts = [];
    let events = [];

    $: personId = $page.params.id;
    $: person = $systemData.caredPersons.find(
        (p) => String(p.id) === String(personId),
    );
    $: alerts = $systemData.alerts.filter(
        (a) => String(a.cared_person_id) === String(personId),
    );
    $: events = $systemData.events.filter(
        (e) => String(e.cared_person_id) === String(personId),
    );
    $: activeAlerts = alerts.filter(
        (a) => a.status === "active" || a.status === "critical",
    );
    $: upcomingEvents = events
        .filter((e) => new Date(e.start_datetime) > new Date())
        .sort(
            (a, b) => new Date(a.start_datetime) - new Date(b.start_datetime),
        );
    $: recentEvents = events
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 5);

    onMount(async () => {
        loading = true;
        await Promise.all([
            refreshCaredPersons(),
            refreshAlerts(),
            refreshEvents(),
        ]);
        loading = false;
    });

    function goBack() {
        goto("/dashboard/human");
    }

    function formatDate(date) {
        return new Date(date).toLocaleString("es-ES", {
            year: "numeric",
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        });
    }
</script>

<svelte:head>
    <title>Detalle de Persona Bajo Cuidado</title>
</svelte:head>

{#if loading}
    <div class="flex justify-center items-center h-64">
        <div
            class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"
        ></div>
    </div>
{:else if !person}
    <div class="text-center py-12">
        <h2 class="text-2xl font-bold text-gray-800 mb-2">
            Persona no encontrada
        </h2>
        <button
            on:click={goBack}
            class="mt-4 px-4 py-2 bg-primary text-white rounded-lg"
            >Volver</button
        >
    </div>
{:else}
    <div class="max-w-4xl mx-auto py-8 px-4">
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
            <div class="flex items-center space-x-4">
                <div
                    class="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center text-3xl"
                >
                    👤
                </div>
                <div>
                    <h1 class="text-2xl font-bold text-gray-900">
                        {person.first_name}
                        {person.last_name}
                    </h1>
                    <p class="text-gray-600">
                        {person.age
                            ? person.age + " años"
                            : "Edad no registrada"}
                    </p>
                    <p class="text-sm text-green-700">
                        {person.is_active ? "Activo" : "Inactivo"}
                    </p>
                </div>
            </div>
            <div class="flex space-x-2">
                <button
                    class="px-3 py-2 bg-yellow-100 text-yellow-800 rounded-lg"
                    >Editar</button
                >
                <button class="px-3 py-2 bg-red-100 text-red-800 rounded-lg"
                    >Eliminar</button
                >
            </div>
        </div>

        <!-- Alertas activas -->
        <div class="mb-8">
            <h2
                class="text-lg font-semibold text-red-700 mb-2 flex items-center"
            >
                🚨 Alertas Activas
            </h2>
            {#if activeAlerts.length > 0}
                <ul class="space-y-2">
                    {#each activeAlerts as alert}
                        <li
                            class="bg-red-50 border-l-4 border-red-400 p-4 rounded flex items-center justify-between"
                        >
                            <div>
                                <p class="font-bold text-red-700">
                                    {alert.title}
                                </p>
                                <p class="text-sm text-gray-700">
                                    {alert.description}
                                </p>
                                <p class="text-xs text-gray-500">
                                    {formatDate(alert.created_at)}
                                </p>
                            </div>
                            <button
                                class="px-3 py-1 bg-green-100 text-green-700 rounded-lg"
                                >Resolver</button
                            >
                        </li>
                    {/each}
                </ul>
            {:else}
                <p class="text-gray-500">No hay alertas activas.</p>
            {/if}
        </div>

        <!-- Próximos eventos -->
        <div class="mb-8">
            <h2
                class="text-lg font-semibold text-blue-700 mb-2 flex items-center"
            >
                📅 Próximos Eventos
            </h2>
            {#if upcomingEvents.length > 0}
                <ul class="space-y-2">
                    {#each upcomingEvents as event}
                        <li
                            class="bg-blue-50 border-l-4 border-blue-400 p-4 rounded"
                        >
                            <p class="font-bold text-blue-800">
                                {event.title || event.event_type}
                            </p>
                            <p class="text-sm text-gray-700">
                                {event.description}
                            </p>
                            <p class="text-xs text-gray-500">
                                {formatDate(event.start_datetime)}
                            </p>
                        </li>
                    {/each}
                </ul>
            {:else}
                <p class="text-gray-500">No hay eventos próximos.</p>
            {/if}
        </div>

        <!-- Historial de actividad -->
        <div class="mb-8">
            <h2
                class="text-lg font-semibold text-gray-800 mb-2 flex items-center"
            >
                🕒 Historial Reciente
            </h2>
            {#if recentEvents.length > 0}
                <ul class="space-y-2">
                    {#each recentEvents as event}
                        <li
                            class="bg-gray-50 border-l-4 border-gray-300 p-4 rounded"
                        >
                            <p class="font-bold text-gray-800">
                                {event.title || event.event_type}
                            </p>
                            <p class="text-sm text-gray-700">
                                {event.description}
                            </p>
                            <p class="text-xs text-gray-500">
                                {formatDate(event.created_at)}
                            </p>
                        </li>
                    {/each}
                </ul>
            {:else}
                <p class="text-gray-500">No hay actividad reciente.</p>
            {/if}
        </div>

        <!-- Contactos de emergencia -->
        <div class="mb-8">
            <h2
                class="text-lg font-semibold text-green-700 mb-2 flex items-center"
            >
                📞 Contactos de Emergencia
            </h2>
            {#if person.emergency_contacts && person.emergency_contacts.length > 0}
                <ul class="space-y-2">
                    {#each person.emergency_contacts as contact}
                        <li
                            class="bg-green-50 border-l-4 border-green-400 p-4 rounded"
                        >
                            <p class="font-bold text-green-800">
                                {contact.name}
                            </p>
                            <p class="text-sm text-gray-700">{contact.phone}</p>
                        </li>
                    {/each}
                </ul>
            {:else}
                <p class="text-gray-500">
                    No hay contactos de emergencia registrados.
                </p>
            {/if}
        </div>

        <!-- Acciones rápidas -->
        <div class="flex space-x-4">
            <button class="flex-1 px-4 py-2 bg-primary text-white rounded-lg"
                >Agregar Evento</button
            >
            <button
                class="flex-1 px-4 py-2 bg-blue-100 text-blue-700 rounded-lg"
                >Nueva Alerta</button
            >
            <button
                class="flex-1 px-4 py-2 bg-green-100 text-green-700 rounded-lg"
                >Contactar Familiar</button
            >
        </div>
    </div>
{/if}
