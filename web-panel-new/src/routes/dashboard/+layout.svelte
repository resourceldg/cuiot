<script>
    import { goto } from "$app/navigation";
    let userName = "Usuario Demo";
    function logout() {
        localStorage.removeItem("authToken");
        goto("/login");
    }
    // Svelte action para renderizar SVG inline desde string
    export function svg(node, svgString) {
        node.innerHTML = svgString;
    }
    // Sidebar navigation items with SVG icons
    const nav = [
        {
            href: "/dashboard/overview",
            label: "Dashboard",
            icon: `<svg viewBox='0 0 24 24' width='26' height='26' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='3' width='7' height='7' rx='2'/><rect x='14' y='3' width='7' height='7' rx='2'/><rect x='14' y='14' width='7' height='7' rx='2'/><rect x='3' y='14' width='7' height='7' rx='2'/></svg>`,
        },
        {
            href: "/dashboard/admin",
            label: "Admin",
            icon: `<svg viewBox='0 0 24 24' width='26' height='26' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='3.5'/><path d='M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06A1.65 1.65 0 0 0 15 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 15a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9c.36.36.36.95 0 1.31z'/></svg>`,
        },
        {
            href: "/dashboard/alerts",
            label: "Alertas",
            icon: `<svg viewBox='0 0 24 24' width='26' height='26' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><path d='M12 9v4'/><path d='M12 17h.01'/><path d='M21 19H3l9-16 9 16z'/></svg>`,
        },
        {
            href: "/dashboard/devices",
            label: "Dispositivos",
            icon: `<svg viewBox='0 0 24 24' width='26' height='26' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><rect x='2' y='6' width='20' height='12' rx='2'/><path d='M6 20h12'/></svg>`,
        },
        {
            href: "/dashboard/care",
            label: "Cuidados",
            icon: `<svg viewBox='0 0 24 24' width='26' height='26' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><path d='M12 21C12 21 4 13.5 4 8.5C4 5.5 6.5 3 9.5 3C11.24 3 12 4.5 12 4.5C12 4.5 12.76 3 14.5 3C17.5 3 20 5.5 20 8.5C20 13.5 12 21 12 21Z'/></svg>`,
        },
        {
            href: "/dashboard/reports",
            label: "Reportes",
            icon: `<svg viewBox='0 0 24 24' width='26' height='26' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='4' width='18' height='18' rx='2'/><path d='M16 2v4'/><path d='M8 2v4'/><path d='M3 10h18'/></svg>`,
        },
        {
            href: "/dashboard/events",
            label: "Eventos",
            icon: `<svg viewBox='0 0 24 24' width='26' height='26' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='4' width='18' height='18' rx='2'/><path d='M16 2v4'/><path d='M8 2v4'/><path d='M3 10h18'/><rect x='8' y='14' width='2' height='2'/><rect x='14' y='14' width='2' height='2'/></svg>`,
        },
        {
            href: "/dashboard/calendar",
            label: "Calendario",
            icon: `<svg viewBox='0 0 24 24' width='26' height='26' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='4' width='18' height='18' rx='2'/><path d='M16 2v4'/><path d='M8 2v4'/><path d='M3 10h18'/></svg>`,
        },
        {
            href: "/dashboard/profile",
            label: "Perfil",
            icon: `<svg viewBox='0 0 24 24' width='26' height='26' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='8' r='4'/><path d='M4 20c0-4 4-7 8-7s8 3 8 7'/></svg>`,
        },
        {
            href: "/dashboard/settings",
            label: "Configuración",
            icon: `<svg viewBox='0 0 24 24' width='26' height='26' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='3'/><path d='M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06A1.65 1.65 0 0 0 15 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 15a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9c.36.36.36.95 0 1.31z'/></svg>`,
        },
    ];
    let current = "/dashboard/overview";
</script>

<div class="dashboard-layout">
    <aside class="sidebar">
        <div class="sidebar-logo">
            <svg width="36" height="36" viewBox="0 0 36 36"
                ><rect
                    x="4"
                    y="4"
                    width="28"
                    height="28"
                    rx="8"
                    fill="#23262f"
                /><text
                    x="18"
                    y="25"
                    text-anchor="middle"
                    font-size="18"
                    fill="#b0b8c9"
                    font-family="monospace">VS</text
                ></svg
            >
        </div>
        <nav class="sidebar-nav">
            {#each nav as item}
                <a
                    class="sidebar-link {item.href === current ? 'active' : ''}"
                    href={item.href}
                    title={item.label}
                    rel="prefetch"
                >
                    <span class="sidebar-icon" use:svg={item.icon} />
                    <span class="sidebar-label">{item.label}</span>
                </a>
            {/each}
        </nav>
    </aside>
    <div class="main-area">
        <header class="dashboard-header">
            <span class="header-title">Dashboard</span>
            <div class="header-user-area">
                <span class="header-user">{userName}</span>
                <button
                    class="logout-btn"
                    on:click={logout}
                    title="Cerrar sesión"
                >
                    <span class="logout-icon">
                        <svg
                            viewBox="0 0 24 24"
                            width="22"
                            height="22"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            ><path d="M16 17l5-5-5-5" /><path
                                d="M21 12H9"
                            /><path
                                d="M12 19v2a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v2"
                            /></svg
                        >
                    </span>
                </button>
            </div>
        </header>
        <main class="dashboard-main">
            <slot />
        </main>
    </div>
</div>

<style>
    :root {
        --color-bg: #23272e;
        --color-bg-card: #23272e;
        --color-bg-sidebar: #23272e;
        --color-bg-header: #23272e;
        --color-border: #2d3138;
        --color-accent: #00e676;
        --color-danger: #ff4d6d;
        --color-success: #00e676;
        --color-warning: #f1c40f;
        --color-text: #f3f6fa;
        --color-text-secondary: #b0b8c9;
        --color-bg-hover: #262a31;
    }
    .dashboard-layout {
        display: flex;
        min-height: 100vh;
        background: var(--color-bg);
    }
    .sidebar {
        width: 90px;
        background: var(--color-bg-sidebar);
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 1.2rem 0 0 0;
        gap: 2rem;
        border-right: 1.5px solid var(--color-border);
        box-shadow: none;
    }
    .sidebar-logo {
        margin-bottom: 2rem;
    }
    .sidebar-nav {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        width: 100%;
    }
    .sidebar-link {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.2rem;
        padding: 1.1rem 0 0.3rem 0;
        color: var(--color-text-secondary);
        text-decoration: none;
        font-size: 1.2rem;
        border-left: none;
        transition:
            background 0.15s,
            color 0.15s;
        border-radius: 8px;
        box-shadow: none;
    }
    .sidebar-link.active,
    .sidebar-link:hover,
    .sidebar-link:focus {
        background: var(--color-bg-hover);
        color: var(--color-accent);
        border-left: none;
        box-shadow: none;
    }
    .sidebar-icon svg {
        display: block;
        width: 26px;
        height: 26px;
        stroke: currentColor;
        color: inherit;
        transition: color 0.15s;
    }
    .sidebar-link.active .sidebar-icon svg,
    .sidebar-link:hover .sidebar-icon svg,
    .sidebar-link:focus .sidebar-icon svg {
        color: var(--color-accent);
    }
    .sidebar-label {
        font-size: 0.92rem;
        margin-top: 0.1rem;
        font-weight: 500;
    }
    .main-area {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-width: 0;
    }
    .dashboard-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: var(--color-bg-header);
        padding: 0.7rem 2.2rem;
        min-height: 58px;
        border-bottom: 1.5px solid var(--color-border);
        box-shadow: none;
    }
    .header-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--color-accent);
    }
    .header-user-area {
        display: flex;
        align-items: center;
        gap: 1.2rem;
    }
    .header-user {
        font-size: 1.08rem;
        color: var(--color-text-secondary);
    }
    .logout-btn {
        background: none;
        border: none;
        color: var(--color-danger);
        font-size: 1.3rem;
        cursor: pointer;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        transition: background 0.15s;
        display: flex;
        align-items: center;
    }
    .logout-btn:hover,
    .logout-btn:focus {
        background: rgba(255, 77, 109, 0.08);
    }
    .logout-icon svg {
        display: block;
        width: 22px;
        height: 22px;
        stroke: currentColor;
    }
    .dashboard-main {
        flex: 1;
        padding: 2.5rem 2.5rem 2.5rem 2rem;
        background: var(--color-bg);
        min-height: 0;
        overflow-x: auto;
    }
    @media (max-width: 700px) {
        .sidebar {
            width: 56px;
        }
        .dashboard-main {
            padding: 1.2rem 0.5rem 1.2rem 0.5rem;
        }
    }
</style>
