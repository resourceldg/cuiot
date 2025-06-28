<script>
    import { goto } from "$app/navigation";
    let sections = [
        { path: "/dashboard/human", label: "Gestión Humana", icon: "👵" },
        { path: "/dashboard/devices", label: "Dispositivos", icon: "📟" },
        { path: "/dashboard/admin", label: "Administración", icon: "⚙️" },
        { path: "/debug", label: "Debug & Testing", icon: "🧪" },
    ];
    let activeSection = sections[0].label;
    function navigate(path, label) {
        activeSection = label;
        goto(path);
    }
    function logout() {
        goto("/login");
    }
</script>

<div class="dashboard-layout">
    <aside class="sidebar">
        <div class="logo">👴<span>VSLT</span></div>
        <nav>
            {#each sections as section}
                <button
                    class="nav-btn {activeSection === section.label
                        ? 'active'
                        : ''}"
                    on:click={() => navigate(section.path, section.label)}
                >
                    <span class="icon">{section.icon}</span>
                    {section.label}
                </button>
            {/each}
        </nav>
    </aside>
    <div class="main-content">
        <header class="topbar">
            <h1>{activeSection}</h1>
            <button class="logout-btn" on:click={logout}>Cerrar sesión</button>
        </header>
        <main>
            <slot />
        </main>
    </div>
</div>

<style>
    .dashboard-layout {
        display: flex;
        min-height: 100vh;
        background: #f3f4f6;
    }
    .sidebar {
        width: 220px;
        background: #2563eb;
        color: #fff;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem 1rem 1rem 1rem;
        min-height: 100vh;
    }
    .logo {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 2rem;
        letter-spacing: 2px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .logo span {
        font-size: 1.3rem;
        font-weight: 600;
    }
    nav {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    .nav-btn {
        background: none;
        border: none;
        color: #fff;
        font-size: 1.05rem;
        padding: 0.8rem 1rem;
        border-radius: 0.5rem;
        text-align: left;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.7rem;
        transition: background 0.15s;
    }
    .nav-btn.active,
    .nav-btn:hover {
        background: #1d4ed8;
    }
    .icon {
        font-size: 1.3rem;
    }
    .main-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-width: 0;
    }
    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #fff;
        padding: 1.2rem 2rem 1.2rem 2rem;
        border-bottom: 1px solid #e5e7eb;
        box-shadow: 0 1px 4px 0 rgba(37, 99, 235, 0.04);
    }
    .topbar h1 {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2563eb;
        margin: 0;
    }
    .logout-btn {
        background: #ef4444;
        color: #fff;
        border: none;
        border-radius: 0.375rem;
        padding: 0.5rem 1.2rem;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        transition: background 0.15s;
    }
    .logout-btn:hover {
        background: #dc2626;
    }
    main {
        padding: 2.5rem 2.5rem 2.5rem 2.5rem;
        min-height: 80vh;
    }
    @media (max-width: 900px) {
        .sidebar {
            width: 60px;
            padding: 1rem 0.2rem;
        }
        .logo span {
            display: none;
        }
        .nav-btn {
            font-size: 0.9rem;
            padding: 0.7rem 0.5rem;
        }
        .main-content {
            padding-left: 0;
        }
        main {
            padding: 1rem;
        }
    }
</style>
