<script>
    import ProtectedRoute from '../../../components/ProtectedRoute.svelte';
    import { userService } from '$lib/api.js';
    import { showError, showSuccess } from '$lib/stores.js';
    import { onMount } from 'svelte';
    import { Plus, Users, Settings, Shield } from 'lucide-svelte';

    let users = [];
    let loading = true;
    let error = null;

    onMount(async () => {
        await loadUsers();
    });

    async function loadUsers() {
        try {
            loading = true;
            // Por ahora usamos datos mock, cuando tengamos el endpoint real lo conectamos
            users = [
                {
                    id: 1,
                    first_name: 'Admin',
                    last_name: 'Sistema',
                    email: 'admin@cuiot.com',
                    role: 'admin',
                    is_active: true
                },
                {
                    id: 2,
                    first_name: 'María',
                    last_name: 'González',
                    email: 'maria@cuiot.com',
                    role: 'caregiver',
                    is_active: true
                }
            ];
        } catch (err) {
            error = err.message;
            showError('Error al cargar usuarios');
        } finally {
            loading = false;
        }
    }

    function getRoleDisplayName(role) {
        const roleNames = {
            'admin': 'Administrador',
            'caregiver': 'Cuidador',
            'family': 'Familiar',
            'patient': 'Paciente',
            'institution_admin': 'Admin de Institución'
        };
        return roleNames[role] || role;
    }
</script>

<ProtectedRoute permission="users.read">
    <div class="admin-dashboard">
        <div class="page-header">
            <div class="header-content">
                <h1>Administración del Sistema</h1>
                <p>Gestiona usuarios, roles y configuración del sistema</p>
            </div>
            <div class="header-actions">
                <button class="btn btn-primary">
                    <Plus class="w-4 h-4" />
                    Nuevo Usuario
                </button>
            </div>
        </div>

        {#if error}
            <div class="error-banner">
                <p>{error}</p>
            </div>
        {/if}

        <div class="admin-content">
            <!-- Resumen -->
            <div class="summary-cards">
                <div class="summary-card">
                    <div class="card-icon">
                        <Users class="w-6 h-6" />
                    </div>
                    <div class="card-content">
                        <h3>{users.length}</h3>
                        <p>Usuarios Activos</p>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="card-icon">
                        <Shield class="w-6 h-6" />
                    </div>
                    <div class="card-content">
                        <h3>5</h3>
                        <p>Roles del Sistema</p>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="card-icon">
                        <Settings class="w-6 h-6" />
                    </div>
                    <div class="card-content">
                        <h3>12</h3>
                        <p>Configuraciones</p>
                    </div>
                </div>
            </div>

            <!-- Gestión de Usuarios -->
            <div class="section">
                <h2>Gestión de Usuarios</h2>
                {#if loading}
                    <div class="loading">
                        <div class="spinner"></div>
                        <p>Cargando usuarios...</p>
                    </div>
                {:else if users.length === 0}
                    <div class="empty-state">
                        <Users class="w-12 h-12" />
                        <h3>No hay usuarios registrados</h3>
                        <p>Agrega el primer usuario del sistema</p>
                    </div>
                {:else}
                    <div class="users-table">
                        <table>
                            <thead>
                                <tr>
                                    <th>Nombre</th>
                                    <th>Email</th>
                                    <th>Rol</th>
                                    <th>Estado</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                {#each users as user}
                                    <tr>
                                        <td>
                                            <div class="user-info">
                                                <div class="user-avatar">
                                                    <Users class="w-4 h-4" />
                                                </div>
                                                <span>{user.first_name} {user.last_name}</span>
                                            </div>
                                        </td>
                                        <td>{user.email}</td>
                                        <td>
                                            <span class="role-badge">
                                                {getRoleDisplayName(user.role)}
                                            </span>
                                        </td>
                                        <td>
                                            <span class="status {user.is_active ? 'active' : 'inactive'}">
                                                {user.is_active ? 'Activo' : 'Inactivo'}
                                            </span>
                                        </td>
                                        <td>
                                            <button class="btn btn-sm btn-secondary">Editar</button>
                                            <button class="btn btn-sm btn-danger">Eliminar</button>
                                        </td>
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                {/if}
            </div>

            <!-- Configuración del Sistema -->
            <div class="section">
                <h2>Configuración del Sistema</h2>
                <div class="config-grid">
                    <div class="config-card">
                        <h3>Configuración General</h3>
                        <p>Configuración básica del sistema</p>
                        <button class="btn btn-secondary">Configurar</button>
                    </div>
                    <div class="config-card">
                        <h3>Roles y Permisos</h3>
                        <p>Gestiona roles y permisos de usuarios</p>
                        <button class="btn btn-secondary">Gestionar</button>
                    </div>
                    <div class="config-card">
                        <h3>Backup y Restauración</h3>
                        <p>Configuración de respaldos automáticos</p>
                        <button class="btn btn-secondary">Configurar</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</ProtectedRoute>

<style>
    .admin-dashboard {
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

    .btn-danger {
        background: #ef4444;
        color: white;
    }

    .btn-danger:hover {
        background: #dc2626;
    }

    .btn-sm {
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
    }

    .error-banner {
        background: #fee2e2;
        border: 1px solid #fecaca;
        color: #991b1b;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
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

    .loading, .empty-state {
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

    .empty-state h3 {
        margin: 1rem 0 0.5rem 0;
        color: #374151;
    }

    .users-table {
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

    .user-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .user-avatar {
        width: 32px;
        height: 32px;
        background: #f3f4f6;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #6b7280;
    }

    .role-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 500;
        background: #dbeafe;
        color: #1e40af;
    }

    .status {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .status.active {
        background: #dcfce7;
        color: #166534;
    }

    .status.inactive {
        background: #fee2e2;
        color: #991b1b;
    }

    .config-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    .config-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .config-card h3 {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0 0 0.5rem 0;
    }

    .config-card p {
        color: #6b7280;
        margin: 0 0 1rem 0;
    }
</style>
