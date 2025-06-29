<script lang="ts">
    import { caredPersonService, reportService } from "$lib/api.js";
    import { onMount } from "svelte";
    let reports = [];
    let caredPersons = [];
    let loading = true;
    let error = "";
    let selectedPerson = "";
    let showForm = false;
    let formData = {
        title: "",
        description: "",
        cared_person_id: "",
        report_type: "general",
    };
    let files: File[] = [];
    let formError = "";
    let formSuccess = "";
    let editingReport = null;
    let showEditForm = false;

    onMount(async () => {
        await loadData();
    });

    async function loadData() {
        loading = true;
        try {
            caredPersons = await caredPersonService.getAll();
            reports = await reportService.getAll();
        } catch (e) {
            error = e.message || "Error al cargar reportes";
        } finally {
            loading = false;
        }
    }

    async function handleFilter() {
        loading = true;
        try {
            if (selectedPerson) {
                reports =
                    await reportService.getByCaredPersonId(selectedPerson);
            } else {
                reports = await reportService.getAll();
            }
        } catch (e) {
            error = e.message || "Error al filtrar reportes";
        } finally {
            loading = false;
        }
    }

    function openForm() {
        showForm = true;
        formData = {
            title: "",
            description: "",
            cared_person_id: selectedPerson || "",
            report_type: "general",
        };
        files = [];
        formError = "";
        formSuccess = "";
    }

    function closeForm() {
        showForm = false;
    }

    async function handleFileChange(event) {
        files = Array.from(event.target.files);
    }

    async function handleSubmit() {
        formError = "";
        formSuccess = "";
        if (!formData.title || !formData.cared_person_id) {
            formError = "Título y persona bajo cuidado son obligatorios";
            return;
        }
        try {
            await reportService.create(formData, files);
            formSuccess = "Reporte creado correctamente";
            showForm = false;
            await loadData();
        } catch (e) {
            formError = e.message || "Error al crear reporte";
        }
    }

    function downloadFile(file) {
        window.open(file.url, "_blank");
    }

    function openEditForm(report) {
        editingReport = { ...report };
        showEditForm = true;
        formError = "";
        formSuccess = "";
    }

    function closeEditForm() {
        showEditForm = false;
        editingReport = null;
    }

    async function handleEditSubmit() {
        formError = "";
        formSuccess = "";
        if (!editingReport.title || !editingReport.cared_person_id) {
            formError = "Título y persona bajo cuidado son obligatorios";
            return;
        }
        try {
            await reportService.update(editingReport.id, editingReport);
            formSuccess = "Reporte actualizado correctamente";
            showEditForm = false;
            await loadData();
        } catch (e) {
            formError = e.message || "Error al actualizar reporte";
        }
    }

    async function handleDelete(report) {
        if (!confirm(`¿Eliminar el reporte "${report.title}"?`)) return;
        try {
            await reportService.delete(report.id);
            await loadData();
        } catch (e) {
            error = e.message || "Error al eliminar reporte";
        }
    }
</script>

<svelte:head>
    <title>Reportes - CUIOT</title>
</svelte:head>

<div class="max-w-5xl mx-auto py-8 px-4">
    <div class="flex justify-between items-center mb-6">
        <div>
            <h1
                class="text-2xl font-bold text-gray-900 flex items-center gap-2"
            >
                📈 Reportes
            </h1>
            <p class="text-gray-600">
                Historial y gestión de reportes de cuidado
            </p>
        </div>
        <button
            class="px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-700"
            on:click={openForm}>Nuevo Reporte</button
        >
    </div>

    <div
        class="bg-white rounded-lg shadow-sm border p-4 mb-6 flex flex-col md:flex-row md:items-center gap-4"
    >
        <label class="font-medium text-gray-700">Filtrar por persona:</label>
        <select
            class="border rounded px-3 py-2"
            bind:value={selectedPerson}
            on:change={handleFilter}
        >
            <option value="">Todas</option>
            {#each caredPersons as person}
                <option value={person.id}
                    >{person.first_name} {person.last_name}</option
                >
            {/each}
        </select>
    </div>

    {#if loading}
        <div class="flex justify-center items-center h-64">
            <div
                class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"
            ></div>
        </div>
    {:else if error}
        <div class="bg-red-50 border-l-4 border-red-400 p-4 mb-6 text-red-700">
            {error}
        </div>
    {:else}
        <div class="bg-white rounded-lg shadow-sm border p-4">
            <h2 class="text-lg font-semibold text-gray-800 mb-4">
                Lista de Reportes
            </h2>
            {#if reports.length === 0}
                <p class="text-gray-500">No hay reportes registrados.</p>
            {:else}
                <table class="min-w-full divide-y divide-gray-200">
                    <thead>
                        <tr>
                            <th
                                class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
                                >Título</th
                            >
                            <th
                                class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
                                >Persona</th
                            >
                            <th
                                class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
                                >Tipo</th
                            >
                            <th
                                class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
                                >Fecha</th
                            >
                            <th
                                class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
                                >Archivos</th
                            >
                            <th
                                class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
                                >Acciones</th
                            >
                        </tr>
                    </thead>
                    <tbody>
                        {#each reports as report}
                            <tr class="hover:bg-gray-50">
                                <td class="px-4 py-2">{report.title}</td>
                                <td class="px-4 py-2"
                                    >{#if report.cared_person}{report
                                            .cared_person.first_name}
                                        {report.cared_person.last_name}{/if}</td
                                >
                                <td class="px-4 py-2">{report.report_type}</td>
                                <td class="px-4 py-2"
                                    >{new Date(
                                        report.created_at,
                                    ).toLocaleString("es-ES")}</td
                                >
                                <td class="px-4 py-2">
                                    {#if report.attached_files && report.attached_files.length > 0}
                                        <ul class="space-y-1">
                                            {#each report.attached_files as file}
                                                <li>
                                                    <button
                                                        class="text-blue-600 hover:underline text-xs"
                                                        on:click={() =>
                                                            downloadFile(file)}
                                                        >{file.filename}</button
                                                    >
                                                </li>
                                            {/each}
                                        </ul>
                                    {:else}
                                        <span class="text-gray-400 text-xs"
                                            >Sin archivos</span
                                        >
                                    {/if}
                                </td>
                                <td class="px-4 py-2">
                                    <button
                                        class="text-blue-600 hover:underline text-xs mr-2"
                                        on:click={() => openEditForm(report)}
                                        >Editar</button
                                    >
                                    <button
                                        class="text-red-600 hover:underline text-xs"
                                        on:click={() => handleDelete(report)}
                                        >Eliminar</button
                                    >
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            {/if}
        </div>
    {/if}

    {#if showForm}
        <div
            class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
        >
            <div
                class="bg-white rounded-lg shadow-lg p-8 w-full max-w-lg relative"
            >
                <button
                    class="absolute top-2 right-2 text-gray-400 hover:text-gray-700"
                    on:click={closeForm}>&times;</button
                >
                <h2 class="text-xl font-bold mb-4">Nuevo Reporte</h2>
                {#if formError}
                    <div class="bg-red-100 text-red-700 p-2 rounded mb-2">
                        {formError}
                    </div>
                {/if}
                {#if formSuccess}
                    <div class="bg-green-100 text-green-700 p-2 rounded mb-2">
                        {formSuccess}
                    </div>
                {/if}
                <form on:submit|preventDefault={handleSubmit}>
                    <div class="mb-4">
                        <label class="block text-gray-700 font-medium mb-1"
                            >Título</label
                        >
                        <input
                            class="w-full border rounded px-3 py-2"
                            bind:value={formData.title}
                            required
                        />
                    </div>
                    <div class="mb-4">
                        <label class="block text-gray-700 font-medium mb-1"
                            >Descripción</label
                        >
                        <textarea
                            class="w-full border rounded px-3 py-2"
                            bind:value={formData.description}
                        ></textarea>
                    </div>
                    <div class="mb-4">
                        <label class="block text-gray-700 font-medium mb-1"
                            >Persona Bajo Cuidado</label
                        >
                        <select
                            class="w-full border rounded px-3 py-2"
                            bind:value={formData.cared_person_id}
                            required
                        >
                            <option value="">Selecciona una persona</option>
                            {#each caredPersons as person}
                                <option value={person.id}
                                    >{person.first_name}
                                    {person.last_name}</option
                                >
                            {/each}
                        </select>
                    </div>
                    <div class="mb-4">
                        <label class="block text-gray-700 font-medium mb-1"
                            >Tipo de Reporte</label
                        >
                        <select
                            class="w-full border rounded px-3 py-2"
                            bind:value={formData.report_type}
                        >
                            <option value="general">General</option>
                            <option value="medical">Médico</option>
                            <option value="incident">Incidente</option>
                            <option value="family">Familiar</option>
                        </select>
                    </div>
                    <div class="mb-4">
                        <label class="block text-gray-700 font-medium mb-1"
                            >Archivos Adjuntos</label
                        >
                        <input
                            type="file"
                            multiple
                            on:change={handleFileChange}
                        />
                    </div>
                    <div class="flex justify-end gap-2">
                        <button
                            type="button"
                            class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                            on:click={closeForm}>Cancelar</button
                        >
                        <button
                            type="submit"
                            class="px-4 py-2 bg-primary text-white rounded hover:bg-blue-700"
                            >Crear</button
                        >
                    </div>
                </form>
            </div>
        </div>
    {/if}

    {#if showEditForm}
        <div
            class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
        >
            <div
                class="bg-white rounded-lg shadow-lg p-8 w-full max-w-lg relative"
            >
                <button
                    class="absolute top-2 right-2 text-gray-400 hover:text-gray-700"
                    on:click={closeEditForm}>&times;</button
                >
                <h2 class="text-xl font-bold mb-4">Editar Reporte</h2>
                {#if formError}
                    <div class="bg-red-100 text-red-700 p-2 rounded mb-2">
                        {formError}
                    </div>
                {/if}
                {#if formSuccess}
                    <div class="bg-green-100 text-green-700 p-2 rounded mb-2">
                        {formSuccess}
                    </div>
                {/if}
                <form on:submit|preventDefault={handleEditSubmit}>
                    <div class="mb-4">
                        <label class="block text-gray-700 font-medium mb-1"
                            >Título</label
                        >
                        <input
                            class="w-full border rounded px-3 py-2"
                            bind:value={editingReport.title}
                            required
                        />
                    </div>
                    <div class="mb-4">
                        <label class="block text-gray-700 font-medium mb-1"
                            >Descripción</label
                        >
                        <textarea
                            class="w-full border rounded px-3 py-2"
                            bind:value={editingReport.description}
                        ></textarea>
                    </div>
                    <div class="mb-4">
                        <label class="block text-gray-700 font-medium mb-1"
                            >Persona Bajo Cuidado</label
                        >
                        <select
                            class="w-full border rounded px-3 py-2"
                            bind:value={editingReport.cared_person_id}
                            required
                        >
                            <option value="">Selecciona una persona</option>
                            {#each caredPersons as person}
                                <option value={person.id}
                                    >{person.first_name}
                                    {person.last_name}</option
                                >
                            {/each}
                        </select>
                    </div>
                    <div class="mb-4">
                        <label class="block text-gray-700 font-medium mb-1"
                            >Tipo de Reporte</label
                        >
                        <select
                            class="w-full border rounded px-3 py-2"
                            bind:value={editingReport.report_type}
                        >
                            <option value="general">General</option>
                            <option value="medical">Médico</option>
                            <option value="incident">Incidente</option>
                            <option value="family">Familiar</option>
                        </select>
                    </div>
                    <div class="flex justify-end gap-2">
                        <button
                            type="button"
                            class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                            on:click={closeEditForm}>Cancelar</button
                        >
                        <button
                            type="submit"
                            class="px-4 py-2 bg-primary text-white rounded hover:bg-blue-700"
                            >Guardar</button
                        >
                    </div>
                </form>
            </div>
        </div>
    {/if}
</div>
