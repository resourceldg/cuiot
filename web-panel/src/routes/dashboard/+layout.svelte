<script>
    import { goto } from "$app/navigation";
    import { authService } from "$lib/api.js";
    import { getCurrentUser, getNavigationForRole, getRoleDisplayName, requireAuth } from "$lib/roles.js";
    import { currentUser, userRole, initializeStores, clearStores, refreshCurrentUserFromBackend } from "$lib/stores.js";
    import { LogOut, Settings, Shield, User } from "lucide-svelte";
    import { onMount } from "svelte";
    import ProfileDropdown from "../../components/ProfileDropdown.svelte";

    let sections = [];
    let activeSection = "";

    onMount(async () => {
        // Verificar autenticación
        if (!requireAuth()) return;
        
        // Inicializar stores
        initializeStores();
        
        // Refrescar usuario desde backend para nombre real
        await refreshCurrentUserFromBackend();
        
        // Determinar sección activa basada en la URL actual
        setActiveSection();
        
        // Suscribirse a cambios en el rol del usuario
        const unsubscribe = userRole.subscribe(role => {
            if (role) {
                sections = getNavigationForRole(role);
                setActiveSection();
            }
        });
        
        return unsubscribe;
    });

    function setActiveSection() {
        const currentPath = window.location.pathname;
        const currentSection = sections.find(section => section.path === currentPath);
        activeSection = currentSection ? currentSection.label : sections[0]?.label || "";
    }

    function navigate(path, label) {
        activeSection = label;
        goto(path);
    }

    function logout() {
        clearStores();
        authService.logout();
        goto("/");
    }

    function goToProfile() {
        goto("/dashboard/profile");
    }

    function goToSettings() {
        goto("/dashboard/settings");
    }
</script>

<div class="dashboard-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
        <div class="sidebar-header">
            <div class="logo">
                <div class="logo-icon">
                    <Shield class="w-6 h-6" />
                </div>
                <div class="logo-text">
                    <span class="logo-title">CUIOT</span>
                    <span class="logo-subtitle">Cuidado</span>
                </div>
            </div>
        </div>

        <nav class="sidebar-nav">
            {#each sections as section}
                <button
                    class="nav-btn {activeSection === section.label
                        ? 'active'
                        : ''}"
                    on:click={() => navigate(section.path, section.label)}
                >
                    <span class="icon">{section.icon}</span>
                    <span class="label">{section.label}</span>
                </button>
            {/each}
        </nav>

        <div class="sidebar-footer">
            <div class="user-info">
                <div class="user-avatar">
                    <User class="w-5 h-5" />
                </div>
                <div class="user-details">
                    <span class="user-name">{$currentUser?.name || 'Usuario'}</span>
                    <span class="user-role">{$currentUser ? getRoleDisplayName($currentUser.role) : 'Usuario'}</span>
                </div>
            </div>

            <div class="user-actions">
                <button
                    class="action-btn"
                    on:click={goToProfile}
                    title="Perfil"
                >
                    <User class="w-4 h-4" />
                </button>
                <button
                    class="action-btn"
                    on:click={goToSettings}
                    title="Configuración"
                >
                    <Settings class="w-4 h-4" />
                </button>
                <button
                    class="action-btn logout"
                    on:click={logout}
                    title="Cerrar sesión"
                >
                    <LogOut class="w-4 h-4" />
                </button>
            </div>
        </div>
    </aside>

    <!-- Main Content -->
    <div class="main-content">
        <header class="topbar">
            <div class="topbar-left">
                <h1 class="page-title">{activeSection}</h1>
                <p class="page-subtitle">CUIOT - Tecnologías para el Cuidado</p>
            </div>

            <div class="topbar-right">
                <div class="system-status">
                    <div class="status-indicator online"></div>
                    <span>Sistema Online</span>
                </div>
                {#if $currentUser}
                    <ProfileDropdown user={$currentUser} onLogout={logout} />
                {/if}
            </div>
        </header>

        <main class="main-area">
            <slot />
        </main>
    </div>
</div>

<style>
    .dashboard-layout {
        display: flex;
        min-height: 100vh;
        background: #f8fafc;
    }

    /* Sidebar */
    .sidebar {
        width: 280px;
        background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        display: flex;
        flex-direction: column;
        position: fixed;
        height: 100vh;
        z-index: 50;
    }

    .sidebar-header {
        padding: 2rem 1.5rem 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .logo-icon {
        width: 40px;
        height: 40px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .logo-text {
        display: flex;
        flex-direction: column;
    }

    .logo-title {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.025em;
    }

    .logo-subtitle {
        font-size: 0.75rem;
        opacity: 0.8;
        font-weight: 500;
    }

    .sidebar-nav {
        flex: 1;
        padding: 1rem 0;
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .nav-btn {
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.875rem;
        padding: 0.75rem 1.5rem;
        text-align: left;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        transition: all 0.2s ease;
        border-radius: 0;
        position: relative;
    }

    .nav-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: white;
    }

    .nav-btn.active {
        background: rgba(255, 255, 255, 0.15);
        color: white;
        font-weight: 600;
    }

    .nav-btn.active::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: white;
        border-radius: 0 2px 2px 0;
    }

    .nav-btn .icon {
        font-size: 1.25rem;
        width: 1.25rem;
        text-align: center;
    }

    .nav-btn .label {
        font-weight: 500;
    }

    .sidebar-footer {
        padding: 1rem 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(0, 0, 0, 0.1);
    }

    .user-info {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }

    .user-avatar {
        width: 32px;
        height: 32px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .user-details {
        display: flex;
        flex-direction: column;
        flex: 1;
    }

    .user-name {
        font-size: 0.875rem;
        font-weight: 600;
    }

    .user-role {
        font-size: 0.75rem;
        opacity: 0.8;
    }

    .user-actions {
        display: flex;
        gap: 0.5rem;
    }

    .action-btn {
        width: 32px;
        height: 32px;
        background: rgba(255, 255, 255, 0.1);
        border: none;
        border-radius: 6px;
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }

    .action-btn:hover {
        background: rgba(255, 255, 255, 0.2);
    }

    .action-btn.logout:hover {
        background: #ef4444;
    }

    /* Main Content */
    .main-content {
        flex: 1;
        margin-left: 280px;
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    .topbar {
        background: white;
        border-bottom: 1px solid #e5e7eb;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }

    .topbar-left h1 {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }

    .page-subtitle {
        font-size: 0.875rem;
        color: #6b7280;
        margin: 0.25rem 0 0 0;
    }

    .topbar-right {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .system-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.875rem;
        color: #6b7280;
    }

    .status-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
    }

    .status-indicator.online {
        background: #10b981;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
    }

    .main-area {
        flex: 1;
        padding: 2rem;
        overflow-y: auto;
    }

    /* Responsive */
    @media (max-width: 1024px) {
        .sidebar {
            width: 240px;
        }

        .main-content {
            margin-left: 240px;
        }
    }

    @media (max-width: 768px) {
        .sidebar {
            transform: translateX(-100%);
            transition: transform 0.3s ease;
        }

        .sidebar.open {
            transform: translateX(0);
        }

        .main-content {
            margin-left: 0;
        }

        .topbar {
            padding: 1rem;
        }

        .main-area {
            padding: 1rem;
        }
    }
</style>
