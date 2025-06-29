<script>
    import { caredPersonService } from '$lib/api.js';
    import { Clock, Heart, Mail, Phone, Plus, User } from 'lucide-svelte';
    import { onMount } from 'svelte';

    let caredPersons = [];
    let caregivers = [];
    let assignments = [];
    let loading = true;
    let error = null;

    onMount(async () => {
        try {
            await loadData();
        } catch (err) {
            error = err.message;
        } finally {
            loading = false;
        }
    });

    async function loadData() {
        try {
            // Cargar personas cuidadas
            const caredResponse = await caredPersonService.getAll();
            caredPersons = caredResponse.data || caredResponse || [];

            // Cargar cuidadores (usuarios con rol de cuidador)
            // Por ahora usamos un array vacío ya que no tenemos un servicio específico para usuarios
            caregivers = [];

            // Cargar asignaciones
            // Por ahora usamos un array vacío ya que no tenemos un servicio específico para asignaciones
            assignments = [];
        } catch (err) {
            console.error('Error loading care data:', err);
            throw new Error('Error al cargar datos de cuidado');
        }
    }

    function getCaredPersonById(id) {
        return caredPersons.find(person => person.id === id);
    }

    function getCaregiverById(id) {
        return caregivers.find(caregiver => caregiver.id === id);
    }

    function getAssignmentStatus(assignment) {
        if (assignment.is_active) {
            return { text: 'Activa', class: 'status-active' };
        }
        return { text: 'Inactiva', class: 'status-inactive' };
    }
</script>

<div class="care-management">
    <div class="page-header">
        <div class="header-content">
            <h1>Gestión de Cuidado</h1>
            <p>Administra personas cuidadas, cuidadores y asignaciones</p>
        </div>
        <div class="header-actions">
            <button class="btn btn-primary">
                <Plus class="w-4 h-4" />
                Nueva Asignación
            </button>
        </div>
    </div>

    {#if loading}
        <div class="loading">
            <div class="spinner"></div>
            <p>Cargando datos de cuidado...</p>
        </div>
    {:else if error}
        <div class="error">
            <p>{error}</p>
            <button class="btn btn-secondary" on:click={loadData}>Reintentar</button>
        </div>
    {:else}
        <div class="care-content">
            <!-- Resumen -->
            <div class="summary-cards">
                <div class="summary-card">
                    <div class="card-icon">
                        <Heart class="w-6 h-6" />
                    </div>
                    <div class="card-content">
                        <h3>{caredPersons.length}</h3>
                        <p>Personas Cuidadas</p>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="card-icon">
                        <User class="w-6 h-6" />
                    </div>
                    <div class="card-content">
                        <h3>{caregivers.length}</h3>
                        <p>Cuidadores</p>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="card-icon">
                        <Clock class="w-6 h-6" />
                    </div>
                    <div class="card-content">
                        <h3>{assignments.filter(a => a.is_active).length}</h3>
                        <p>Asignaciones Activas</p>
                    </div>
                </div>
            </div>

            <!-- Personas Cuidadas -->
            <div class="section">
                <h2>Personas Cuidadas</h2>
                {#if caredPersons.length === 0}
                    <div class="empty-state">
                        <Heart class="w-12 h-12" />
                        <h3>No hay personas cuidadas</h3>
                        <p>Agrega la primera persona bajo cuidado</p>
                    </div>
                {:else}
                    <div class="cards-grid">
                        {#each caredPersons as person}
                            <div class="person-card">
                                <div class="person-header">
                                    <div class="person-avatar">
                                        <User class="w-8 h-8" />
                                    </div>
                                    <div class="person-info">
                                        <h3>{person.first_name} {person.last_name}</h3>
                                        <p class="person-age">
                                            {person.age ? `${person.age} años` : 'Edad no especificada'}
                                        </p>
                                    </div>
                                </div>
                                <div class="person-details">
                                    {#if person.care_level}
                                        <span class="care-level {person.care_level}">
                                            {person.care_level}
                                        </span>
                                    {/if}
                                    {#if person.phone}
                                        <div class="contact-info">
                                            <Phone class="w-4 h-4" />
                                            <span>{person.phone}</span>
                                        </div>
                                    {/if}
                                    {#if person.email}
                                        <div class="contact-info">
                                            <Mail class="w-4 h-4" />
                                            <span>{person.email}</span>
                                        </div>
                                    {/if}
                                </div>
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>

            <!-- Asignaciones -->
            <div class="section">
                <h2>Asignaciones de Cuidadores</h2>
                {#if assignments.length === 0}
                    <div class="empty-state">
                        <Clock class="w-12 h-12" />
                        <h3>No hay asignaciones</h3>
                        <p>Crea la primera asignación de cuidador</p>
                    </div>
                {:else}
                    <div class="assignments-table">
                        <table>
                            <thead>
                                <tr>
                                    <th>Cuidador</th>
                                    <th>Persona Cuidada</th>
                                    <th>Estado</th>
                                    <th>Fecha Inicio</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                {#each assignments as assignment}
                                    {@const caredPerson = getCaredPersonById(assignment.cared_person_id)}
                                    {@const caregiver = getCaregiverById(assignment.caregiver_id)}
                                    {@const status = getAssignmentStatus(assignment)}
                                    <tr>
                                        <td>
                                            {#if caregiver}
                                                <div class="caregiver-info">
                                                    <User class="w-4 h-4" />
                                                    <span>{caregiver.first_name} {caregiver.last_name}</span>
                                                </div>
                                            {:else}
                                                <span class="text-muted">Cuidador no encontrado</span>
                                            {/if}
                                        </td>
                                        <td>
                                            {#if caredPerson}
                                                <div class="cared-person-info">
                                                    <Heart class="w-4 h-4" />
                                                    <span>{caredPerson.first_name} {caredPerson.last_name}</span>
                                                </div>
                                            {:else}
                                                <span class="text-muted">Persona no encontrada</span>
                                            {/if}
                                        </td>
                                        <td>
                                            <span class="status {status.class}">{status.text}</span>
                                        </td>
                                        <td>
                                            {assignment.start_date ? new Date(assignment.start_date).toLocaleDateString() : 'No especificada'}
                                        </td>
                                        <td>
                                            <button class="btn btn-sm btn-secondary">Editar</button>
                                        </td>
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                {/if}
            </div>
        </div>
    {/if}
</div>

<style>
    .care-management {
        padding: 2rem;
    }

    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .header-content h1 {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }

    .header-content p {
        color: #6b7280;
        margin: 0.5rem 0 0 0;
    }

    .btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 500;
        text-decoration: none;
        border: none;
        cursor: pointer;
        transition: all 0.2s;
    }

    .btn-primary {
        background: #3b82f6;
        color: white;
    }

    .btn-primary:hover {
        background: #2563eb;
    }

    .btn-secondary {
        background: #f3f4f6;
        color: #374151;
    }

    .btn-secondary:hover {
        background: #e5e7eb;
    }

    .btn-sm {
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
    }

    .loading, .error {
        text-align: center;
        padding: 4rem 2rem;
    }

    .spinner {
        border: 4px solid #f3f4f6;
        border-top: 4px solid #3b82f6;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .summary-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 3rem;
    }

    .summary-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .card-icon {
        width: 48px;
        height: 48px;
        background: #dbeafe;
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #3b82f6;
    }

    .card-content h3 {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }

    .card-content p {
        color: #6b7280;
        margin: 0;
    }

    .section {
        margin-bottom: 3rem;
    }

    .section h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1.5rem;
    }

    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        background: white;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        color: #6b7280;
    }

    .empty-state h3 {
        margin: 1rem 0 0.5rem 0;
        color: #374151;
    }

    .cards-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    .person-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .person-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .person-avatar {
        width: 48px;
        height: 48px;
        background: #f3f4f6;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #6b7280;
    }

    .person-info h3 {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0;
    }

    .person-age {
        color: #6b7280;
        margin: 0.25rem 0 0 0;
    }

    .person-details {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .care-level {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
    }

    .care-level.low {
        background: #dcfce7;
        color: #166534;
    }

    .care-level.medium {
        background: #fef3c7;
        color: #92400e;
    }

    .care-level.high {
        background: #fee2e2;
        color: #991b1b;
    }

    .contact-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #6b7280;
        font-size: 0.875rem;
    }

    .assignments-table {
        background: white;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    th, td {
        padding: 1rem;
        text-align: left;
        border-bottom: 1px solid #f3f4f6;
    }

    th {
        background: #f9fafb;
        font-weight: 600;
        color: #374151;
    }

    .caregiver-info, .cared-person-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .status {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .status-active {
        background: #dcfce7;
        color: #166534;
    }

    .status-inactive {
        background: #fee2e2;
        color: #991b1b;
    }

    .text-muted {
        color: #9ca3af;
    }
</style> 