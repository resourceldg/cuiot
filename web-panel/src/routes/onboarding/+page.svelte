<script>
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";

    let userRole = "";
    let currentStep = 0;
    let loading = false;

    const onboardingSteps = {
        familiar: [
            {
                title: "¡Bienvenido a CUIOT! 👨‍👩‍👧‍👦",
                description:
                    "Como familiar, podrás monitorear el estado de tus seres queridos y recibir alertas en tiempo real.",
                icon: "👨‍👩‍👧‍👦",
            },
            {
                title: "Monitoreo en Tiempo Real",
                description:
                    "Recibe notificaciones instantáneas sobre el estado y actividad de las personas bajo tu cuidado.",
                icon: "📱",
            },
            {
                title: "Protocolos de Emergencia",
                description:
                    "Configura protocolos personalizados para diferentes situaciones de emergencia.",
                icon: "🚨",
            },
        ],
        cuidador: [
            {
                title: "¡Bienvenido Cuidador! 🧑‍⚕️",
                description:
                    "Como cuidador profesional, tendrás acceso a herramientas avanzadas para el cuidado de tus pacientes.",
                icon: "🧑‍⚕️",
            },
            {
                title: "Gestión de Pacientes",
                description:
                    "Administra múltiples pacientes, sus dispositivos y configuraciones de cuidado.",
                icon: "👥",
            },
            {
                title: "Reportes y Analytics",
                description:
                    "Genera reportes detallados y analiza patrones de comportamiento y salud.",
                icon: "📊",
            },
        ],
        admin: [
            {
                title: "¡Bienvenido Administrador! 🏢",
                description:
                    "Como administrador de institución, tendrás control total sobre usuarios, dispositivos y configuraciones.",
                icon: "🏢",
            },
            {
                title: "Gestión Institucional",
                description:
                    "Administra usuarios, roles, dispositivos y configuraciones a nivel institucional.",
                icon: "⚙️",
            },
            {
                title: "Métricas y Reportes",
                description:
                    "Accede a métricas globales, reportes institucionales y analytics avanzados.",
                icon: "📈",
            },
        ],
        paciente: [
            {
                title: "¡Bienvenido! 🧓",
                description:
                    "Como persona bajo cuidado, podrás gestionar tu propio estado y solicitar ayuda cuando la necesites.",
                icon: "🧓",
            },
            {
                title: "Autogestión",
                description:
                    "Configura tus preferencias, revisa tu estado y solicita ayuda con un solo clic.",
                icon: "👤",
            },
            {
                title: "Comunicación Directa",
                description:
                    "Mantén comunicación directa con tus cuidadores y familiares.",
                icon: "💬",
            },
        ],
    };

    onMount(() => {
        // Obtener el rol del usuario desde localStorage o del token
        const token = localStorage.getItem("authToken");
        if (token) {
            try {
                const payload = JSON.parse(atob(token.split(".")[1]));
                userRole = payload.role || "familiar";
            } catch (e) {
                userRole = "familiar";
            }
        } else {
            goto("/login");
        }
    });

    function nextStep() {
        if (currentStep < onboardingSteps[userRole].length - 1) {
            currentStep++;
        } else {
            completeOnboarding();
        }
    }

    function skipOnboarding() {
        completeOnboarding();
    }

    function completeOnboarding() {
        loading = true;
        localStorage.setItem("onboardingCompleted", "true");

        // Redirigir según el rol
        setTimeout(() => {
            switch (userRole) {
                case "familiar":
                    goto("/dashboard/overview");
                    break;
                case "cuidador":
                    goto("/dashboard/human");
                    break;
                case "admin":
                    goto("/dashboard/admin");
                    break;
                case "paciente":
                    goto("/dashboard/overview");
                    break;
                default:
                    goto("/dashboard/overview");
            }
        }, 500);
    }
</script>

<svelte:head>
    <title>Bienvenido - CUIOT</title>
</svelte:head>

<div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-health to-primary p-4"
>
    <div
        class="bg-white rounded-2xl shadow-2xl p-12 w-full max-w-lg text-center"
    >
        {#if onboardingSteps[userRole] && onboardingSteps[userRole][currentStep]}
            <div class="mb-8">
                <div class="text-6xl mb-6">
                    {onboardingSteps[userRole][currentStep].icon}
                </div>
                <h1 class="text-2xl font-bold text-gray-800 mb-4">
                    {onboardingSteps[userRole][currentStep].title}
                </h1>
                <p class="text-lg text-gray-600 leading-relaxed">
                    {onboardingSteps[userRole][currentStep].description}
                </p>

                <div class="flex justify-center gap-2 mt-8">
                    {#each onboardingSteps[userRole] as _, index}
                        <div
                            class="w-3 h-3 rounded-full transition-colors duration-300 {index ===
                            currentStep
                                ? 'bg-primary'
                                : 'bg-gray-300'}"
                        ></div>
                    {/each}
                </div>
            </div>
        {/if}

        <div class="flex justify-between gap-4">
            <button
                class="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-600 font-medium rounded-lg hover:border-gray-400 hover:text-gray-700 transition-colors duration-200 disabled:opacity-50"
                on:click={skipOnboarding}
                disabled={loading}
            >
                Saltar
            </button>
            <button
                class="flex-1 px-6 py-3 bg-gradient-to-r from-primary to-health text-white font-semibold rounded-lg hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                on:click={nextStep}
                disabled={loading}
            >
                {#if currentStep === onboardingSteps[userRole]?.length - 1}
                    {#if loading}
                        <div class="flex items-center justify-center">
                            <div
                                class="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"
                            ></div>
                            Cargando...
                        </div>
                    {:else}
                        Comenzar
                    {/if}
                {:else}
                    Siguiente
                {/if}
            </button>
        </div>
    </div>
</div>
