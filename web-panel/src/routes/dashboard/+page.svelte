<script>
    import { goto } from "$app/navigation";
    const sections = [
        {
            path: "/dashboard/human",
            label: "Gestión Humana",
            description:
                "Gestiona personas bajo cuidado, recordatorios y alertas.",
            icon: "👵",
        },
        {
            path: "/dashboard/devices",
            label: "Dispositivos",
            description: "Administra y monitorea los dispositivos IoT.",
            icon: "📟",
        },
        {
            path: "/dashboard/admin",
            label: "Administración",
            description: "Gestión de usuarios y configuración avanzada.",
            icon: "⚙️",
        },
    ];
    function navigate(path) {
        goto(path);
    }
</script>

<div class="dashboard-home">
    <h1>👥 Personas Bajo Cuidado</h1>
    <p class="subtitle">
        Bienvenido al panel principal. Selecciona una sección para comenzar:
    </p>
    <div class="sections-grid">
        {#each sections as section}
            <div
                class="section-card"
                on:click={() => navigate(section.path)}
                tabindex="0"
            >
                <div class="icon">{section.icon}</div>
                <h2>{section.label}</h2>
                <p>{section.description}</p>
            </div>
        {/each}
    </div>
</div>

<style>
    .dashboard-home {
        max-width: 700px;
        margin: 3rem auto;
        text-align: center;
    }
    .dashboard-home h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: var(--text-secondary);
        font-size: 1.2rem;
        margin-bottom: 2.5rem;
    }
    .sections-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 2rem;
    }
    .section-card {
        background: #fff;
        border-radius: 0.75rem;
        box-shadow: 0 2px 8px 0 rgba(37, 99, 235, 0.08);
        border: 1px solid #e5e7eb;
        padding: 2rem 1.5rem;
        cursor: pointer;
        transition: box-shadow 0.15s, transform 0.12s;
        outline: none;
    }
    .section-card:hover,
    .section-card:focus {
        box-shadow: 0 4px 16px 0 rgba(37, 99, 235, 0.16);
        transform: translateY(-2px) scale(1.03);
        border-color: #2563eb;
    }
    .section-card .icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .section-card h2 {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    .section-card p {
        color: var(--text-secondary);
        font-size: 1rem;
    }
</style>
