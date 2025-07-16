<script>
    import BuildingIcon from "$lib/ui/icons/BuildingIcon.svelte";
    import FamilyIcon from "$lib/ui/icons/FamilyIcon.svelte";
    import HeartIcon from "$lib/ui/icons/HeartIcon.svelte";
    import ShieldIcon from "$lib/ui/icons/ShieldIcon.svelte";
    import UserIcon from "$lib/ui/icons/UserIcon.svelte";
    import { createEventDispatcher } from "svelte";
    import SectionHeader from "../../shared/ui/SectionHeader.svelte";

    const dispatch = createEventDispatcher();

    // Jerarquía de roles y permisos
    const roleHierarchy = [
        {
            role: "sysadmin",
            name: "Administrador del Sistema",
            icon: ShieldIcon,
            color: "var(--color-danger)",
            canCreate: [
                "institution_admin",
                "caregiver",
                "family",
                "cared_person_self",
                "cared_person_delegated",
            ],
            restrictions: "Ninguna - control total del sistema",
            description:
                "Acceso completo a todas las funcionalidades del sistema",
        },
        {
            role: "institution_admin",
            name: "Administrador de Institución",
            icon: BuildingIcon,
            color: "var(--color-warning)",
            canCreate: [
                "caregiver",
                "family",
                "cared_person_self",
                "cared_person_delegated",
            ],
            restrictions:
                "Solo usuarios dentro de su institución, no puede crear otros admins",
            description:
                "Gestiona usuarios y operaciones dentro de su institución",
        },
        {
            role: "caregiver",
            name: "Cuidador Freelancer",
            icon: HeartIcon,
            color: "var(--color-success)",
            canCreate: [
                "family",
                "cared_person_self",
                "cared_person_delegated",
            ],
            restrictions:
                "Solo como parte de referidos, no puede crear admins ni cuidadores",
            description: "Puede referir familias y personas bajo cuidado",
        },
        {
            role: "family",
            name: "Familiar/Representante",
            icon: FamilyIcon,
            color: "var(--color-info)",
            canCreate: ["cared_person_delegated"],
            restrictions:
                "Solo personas bajo cuidado delegado como representante legal",
            description:
                "Representa legalmente a personas bajo cuidado delegado",
        },
        {
            role: "cared_person_self",
            name: "Persona en Autocuidado",
            icon: UserIcon,
            color: "var(--color-text-muted)",
            canCreate: [],
            restrictions: "No puede crear usuarios",
            description: "Persona independiente que gestiona su propio cuidado",
        },
        {
            role: "cared_person_delegated",
            name: "Persona con Cuidado Delegado",
            icon: UserIcon,
            color: "var(--color-text-muted)",
            canCreate: [],
            restrictions:
                "No puede crear usuarios, requiere representante legal",
            description: "Persona dependiente que necesita representación",
        },
    ];

    // Reglas de validación
    const validationRules = [
        {
            title: "Capacidad Legal",
            description:
                "Personas bajo cuidado delegado DEBEN tener un representante legal vinculado",
            critical: true,
        },
        {
            title: "Relaciones de Institución",
            description:
                "Usuarios se asocian a instituciones mediante relaciones muchos a muchos, no campo directo",
            critical: true,
        },
        {
            title: "Asignación de Paquetes",
            description:
                "Solo paquetes disponibles para el tipo de usuario y institución (si aplica)",
            critical: false,
        },
        {
            title: "Jerarquía de Roles",
            description:
                "No se puede crear usuarios con rol igual o superior al creador",
            critical: true,
        },
        {
            title: "Validaciones Obligatorias",
            description:
                "Email y teléfono únicos, validación de edad y capacidad legal",
            critical: true,
        },
    ];

    function closeGuide() {
        dispatch("close");
    }
</script>

<div class="hierarchy-guide">
    <div class="guide-header">
        <SectionHeader
            title="Guía de Jerarquía de Usuarios"
            subtitle="Reglas de negocio para creación y gestión de usuarios"
        >
            <span slot="icon">
                <ShieldIcon size={24} />
            </span>
        </SectionHeader>
        <button class="close-btn" on:click={closeGuide}>
            <span>×</span>
        </button>
    </div>

    <div class="guide-content">
        <!-- Jerarquía de Roles -->
        <div class="section">
            <h3>📊 Jerarquía de Roles y Permisos</h3>
            <div class="role-hierarchy">
                {#each roleHierarchy as role, index}
                    <div class="role-card" style="--role-color: {role.color}">
                        <div class="role-header">
                            <div class="role-icon">
                                <svelte:component this={role.icon} size={20} />
                            </div>
                            <div class="role-info">
                                <h4>{role.name}</h4>
                                <span class="role-tag">{role.role}</span>
                            </div>
                            <div class="role-level">Nivel {index + 1}</div>
                        </div>
                        <div class="role-details">
                            <p class="role-description">{role.description}</p>
                            <div class="role-permissions">
                                <strong>Puede crear:</strong>
                                <div class="permission-tags">
                                    {#each role.canCreate as permission}
                                        <span class="permission-tag"
                                            >{permission}</span
                                        >
                                    {/each}
                                    {#if role.canCreate.length === 0}
                                        <span class="permission-tag none"
                                            >Ninguno</span
                                        >
                                    {/if}
                                </div>
                            </div>
                            <div class="role-restrictions">
                                <strong>Restricciones:</strong>
                                <p>{role.restrictions}</p>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>

        <!-- Reglas de Validación -->
        <div class="section">
            <h3>⚖️ Reglas de Validación Críticas</h3>
            <div class="validation-rules">
                {#each validationRules as rule}
                    <div class="rule-card" class:critical={rule.critical}>
                        <div class="rule-header">
                            <h4>{rule.title}</h4>
                            {#if rule.critical}
                                <span class="critical-badge">Crítico</span>
                            {/if}
                        </div>
                        <p>{rule.description}</p>
                    </div>
                {/each}
            </div>
        </div>

        <!-- Casos de Uso -->
        <div class="section">
            <h3>🎯 Casos de Uso por Rol</h3>
            <div class="use-cases">
                <div class="use-case">
                    <h4>Sysadmin</h4>
                    <ul>
                        <li>Crear administradores de instituciones</li>
                        <li>Asignar cualquier rol y paquete</li>
                        <li>Gestionar usuarios globalmente</li>
                        <li>Configurar instituciones y paquetes</li>
                    </ul>
                </div>
                <div class="use-case">
                    <h4>Admin Institución</h4>
                    <ul>
                        <li>Crear cuidadores para su institución</li>
                        <li>Registrar familias y pacientes</li>
                        <li>Asignar paquetes institucionales</li>
                        <li>Gestionar relaciones usuario-institución</li>
                    </ul>
                </div>
                <div class="use-case">
                    <h4>Caregiver</h4>
                    <ul>
                        <li>Referir familias y pacientes</li>
                        <li>Asociarse como representante temporal</li>
                        <li>Ganar comisiones por referidos</li>
                        <li>No puede crear admins ni otros cuidadores</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Notas de Implementación -->
        <div class="section">
            <h3>💡 Notas de Implementación</h3>
            <div class="implementation-notes">
                <div class="note">
                    <strong>Dropdowns Filtrados:</strong> Los campos de institución,
                    paquete y rol deben filtrarse según el rol del usuario autenticado.
                </div>
                <div class="note">
                    <strong>Validaciones en Tiempo Real:</strong> Verificar capacidad
                    legal, unicidad de email/teléfono, y restricciones de jerarquía.
                </div>
                <div class="note">
                    <strong>Relaciones Múltiples:</strong> Usar tablas de relación
                    para instituciones y paquetes, no campos directos.
                </div>
                <div class="note">
                    <strong>Auditoría:</strong> Registrar quién creó cada usuario
                    y con qué permisos.
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .hierarchy-guide {
        background: var(--color-bg-card);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        max-width: 1200px;
        margin: 0 auto;
        overflow: hidden;
    }

    .guide-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--spacing-lg);
        border-bottom: 1px solid var(--color-border);
        background: var(--color-bg);
    }

    .close-btn {
        background: none;
        border: none;
        font-size: 24px;
        cursor: pointer;
        color: var(--color-text-muted);
        padding: var(--spacing-sm);
        border-radius: var(--border-radius);
        transition: all 0.2s;
    }

    .close-btn:hover {
        background: var(--color-bg-hover);
        color: var(--color-text);
    }

    .guide-content {
        padding: var(--spacing-xl);
        max-height: 80vh;
        overflow-y: auto;
    }

    .section {
        margin-bottom: var(--spacing-xl);
    }

    .section h3 {
        color: var(--color-text);
        margin-bottom: var(--spacing-lg);
        font-size: 1.25rem;
        font-weight: 600;
    }

    /* Jerarquía de Roles */
    .role-hierarchy {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: var(--spacing-lg);
    }

    .role-card {
        border: 2px solid var(--role-color);
        border-radius: var(--border-radius);
        padding: var(--spacing-lg);
        background: var(--color-bg);
        transition: all 0.2s;
    }

    .role-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    .role-header {
        display: flex;
        align-items: center;
        gap: var(--spacing-md);
        margin-bottom: var(--spacing-md);
    }

    .role-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: var(--role-color);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
    }

    .role-info h4 {
        margin: 0;
        color: var(--color-text);
        font-size: 1.1rem;
    }

    .role-tag {
        background: var(--role-color);
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }

    .role-level {
        margin-left: auto;
        background: var(--color-accent);
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .role-description {
        color: var(--color-text-muted);
        margin-bottom: var(--spacing-md);
        font-size: 0.9rem;
    }

    .role-permissions,
    .role-restrictions {
        margin-bottom: var(--spacing-sm);
    }

    .role-permissions strong,
    .role-restrictions strong {
        color: var(--color-text);
        font-size: 0.9rem;
    }

    .permission-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
        margin-top: 4px;
    }

    .permission-tag {
        background: var(--color-success);
        color: white;
        padding: 2px 6px;
        border-radius: 8px;
        font-size: 0.7rem;
    }

    .permission-tag.none {
        background: var(--color-text-muted);
    }

    /* Reglas de Validación */
    .validation-rules {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: var(--spacing-md);
    }

    .rule-card {
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        padding: var(--spacing-md);
        background: var(--color-bg);
    }

    .rule-card.critical {
        border-color: var(--color-danger);
        background: linear-gradient(
            135deg,
            var(--color-bg),
            rgba(220, 53, 69, 0.05)
        );
    }

    .rule-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--spacing-sm);
    }

    .rule-header h4 {
        margin: 0;
        color: var(--color-text);
        font-size: 1rem;
    }

    .critical-badge {
        background: var(--color-danger);
        color: white;
        padding: 2px 6px;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 600;
    }

    /* Casos de Uso */
    .use-cases {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: var(--spacing-lg);
    }

    .use-case {
        background: var(--color-bg);
        border: 1px solid var(--color-border);
        border-radius: var(--border-radius);
        padding: var(--spacing-md);
    }

    .use-case h4 {
        color: var(--color-accent);
        margin-bottom: var(--spacing-sm);
        font-size: 1rem;
    }

    .use-case ul {
        margin: 0;
        padding-left: var(--spacing-md);
        color: var(--color-text-muted);
        font-size: 0.9rem;
    }

    .use-case li {
        margin-bottom: 4px;
    }

    /* Notas de Implementación */
    .implementation-notes {
        display: grid;
        gap: var(--spacing-md);
    }

    .note {
        background: var(--color-bg);
        border-left: 4px solid var(--color-accent);
        padding: var(--spacing-md);
        color: var(--color-text-muted);
        font-size: 0.9rem;
    }

    .note strong {
        color: var(--color-text);
    }

    @media (max-width: 768px) {
        .guide-content {
            padding: var(--spacing-md);
        }

        .role-hierarchy {
            grid-template-columns: 1fr;
        }

        .validation-rules {
            grid-template-columns: 1fr;
        }

        .use-cases {
            grid-template-columns: 1fr;
        }
    }
</style>
