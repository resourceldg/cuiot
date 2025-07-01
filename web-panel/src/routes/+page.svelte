<script lang="ts">
    import { goto } from "$app/navigation";
    import {
        alertService,
        authService,
        authStore,
        deviceService,
        elderlyPersonService,
    } from "$lib/api.js";
    import type { ElderlyPerson, SystemStatus } from "$lib/types";
    import {
        Activity,
        ArrowRight,
        Heart,
        MapPin,
        Shield,
        Smartphone,
        Users,
    } from "lucide-svelte";
    import { onMount } from "svelte";

    // Datos reales del backend
    let elderlyPersons: ElderlyPerson[] = [];
    let systemStatus: SystemStatus = {
        devices: 0,
        activeAlerts: 0,
        totalEvents: 0,
        uptime: "99.8%",
    };
    let loading = true;
    let error = "";
    let errorDetail = "";
    let debugData: any = {};

    // Modal y estado de formulario
    let showForm = false;
    let formLoading = false;
    let formError = "";
    let editingPerson: ElderlyPerson | null = null;
    let formTitle = "Agregar Adulto Mayor";
    let formSuccess = "";
    let formKey = Date.now();

    // Nuevo estado para la sesión
    let sessionExpiring = false;
    let sessionExpired = false;

    // Estado para dispositivos
    let devices: any[] = [];
    let deviceFormVisible = false;
    let deviceFormLoading = false;
    let deviceFormError = "";
    let editingDevice: any = null;
    let deviceFormTitle = "Agregar Dispositivo";
    let deviceFormKey = Date.now();

    let isAuthenticated = false;

    onMount(() => {
        isAuthenticated = authService.isAuthenticated();
    });

    onMount(async () => {
        // Verificar autenticación
        if (!authService.isAuthenticated()) {
            goto("/login");
            return;
        }
        await loadDashboardData();
        await loadDevicesAndElderly();
    });

    async function loadDashboardData() {
        try {
            loading = true;
            error = "";
            errorDetail = "";
            debugData = {};
            // Cargar datos en paralelo
            const [elderlyData, alertsDataRaw, devicesDataRaw] =
                await Promise.all([
                    elderlyPersonService.getAll(),
                    alertService.getAll(),
                    deviceService.getAll(),
                ]);
            // Debug monitor
            debugData.elderlyPersons = elderlyData;
            debugData.alerts = alertsDataRaw;
            debugData.devices = devicesDataRaw;
            // Asegurar arrays
            const safeAlertsData = Array.isArray(alertsDataRaw)
                ? alertsDataRaw
                : [];
            const safeDevicesData = Array.isArray(devicesDataRaw)
                ? devicesDataRaw
                : [];
            // Procesar personas bajo cuidado y ordenar por updated_at/created_at descendente
            elderlyPersons = Array.isArray(elderlyData)
                ? elderlyData
                      .map((person: any) => ({
                          ...person,
                          name: `${person.first_name} ${person.last_name}`,
                          age: person.age || "N/A",
                          status: "active", // TODO: Determinar estado real
                          lastActivity: "15 minutos", // TODO: Obtener de eventos
                          location: "Sala de estar", // TODO: Obtener de dispositivos
                          alerts: safeAlertsData.filter(
                              (alert: any) =>
                                  alert.elderly_person_id === person.id
                          ).length,
                      }))
                      .sort((a: any, b: any) => {
                          const dateA = new Date(
                              a.updated_at || a.created_at
                          ).getTime();
                          const dateB = new Date(
                              b.updated_at || b.created_at
                          ).getTime();
                          return dateB - dateA;
                      })
                : [];
            // Actualizar estado del sistema
            systemStatus = {
                devices: safeDevicesData.length,
                activeAlerts: safeAlertsData.filter(
                    (alert: any) => !alert.resolved
                ).length,
                totalEvents: 156, // TODO: Obtener de eventos
                uptime: "99.8%",
            };
            formSuccess = editingPerson
                ? "Adulto mayor editado con éxito"
                : "Adulto mayor creado con éxito";
            setTimeout(() => {
                formSuccess = "";
            }, 2000);
        } catch (err: any) {
            error = "Error al cargar los datos del dashboard";
            errorDetail = err?.message || JSON.stringify(err);
            console.error("Error loading dashboard data:", err);
        } finally {
            loading = false;
        }
    }

    function handleLogout() {
        authService.logout();
        authStore.update((state: any) => ({
            ...state,
            isAuthenticated: false,
        }));
        goto("/login");
    }

    function openAddForm() {
        editingPerson = null;
        formTitle = "Agregar Adulto Mayor";
        formError = "";
        showForm = true;
        formKey = Date.now();
    }

    function openEditForm(person: ElderlyPerson) {
        editingPerson = person;
        formTitle = "Editar Adulto Mayor";
        formError = "";
        showForm = true;
        formKey = Date.now();
    }

    async function handleFormSubmit(e: any) {
        formLoading = true;
        formError = "";
        try {
            // Validar datos antes de enviar
            const data = e.detail;
            if (!data.first_name || !data.last_name) {
                formError = "Nombre y apellido son obligatorios";
                return;
            }
            // Limpiar campos vacíos
            const payload = {
                first_name: data.first_name.trim(),
                last_name: data.last_name.trim(),
                age: data.age ? Number(data.age) : null,
                address: data.address ? data.address.trim() : "",
                emergency_contacts: Array.isArray(data.emergency_contacts)
                    ? data.emergency_contacts
                    : [],
            };
            if (editingPerson) {
                await elderlyPersonService.update(editingPerson.id, payload);
            } else {
                await elderlyPersonService.create(payload);
            }
            showForm = false;
            await loadDashboardData();
        } catch (err: any) {
            formError =
                err?.message || (err && err.toString()) || "Error al guardar";
        } finally {
            formLoading = false;
        }
    }

    function handleFormClose() {
        showForm = false;
        editingPerson = null;
        formError = "";
        formKey = Date.now();
    }

    async function handleDelete(person: ElderlyPerson) {
        if (
            confirm(
                `¿Seguro que deseas eliminar a ${person.first_name} ${person.last_name}?`
            )
        ) {
            try {
                await elderlyPersonService.delete(person.id);
                await loadDashboardData();
                formSuccess = "Adulto mayor eliminado con éxito";
                setTimeout(() => {
                    formSuccess = "";
                }, 2000);
            } catch (err: any) {
                alert(err?.message || "Error al eliminar");
            }
        }
    }

    function handleConfigureDevice() {
        alert("Funcionalidad próximamente: configurar dispositivo");
    }

    function handleViewAlerts() {
        alert("Funcionalidad próximamente: ver alertas");
    }

    function handleRenewSession() {
        // Redirige a login para renovar sesión
        goto("/login");
    }

    // Cargar dispositivos y personas bajo cuidado
    async function loadDevicesAndElderly() {
        try {
            deviceFormLoading = true;
            // elderlyPersons ya se carga en loadDashboardData, pero lo recargamos por si acaso
            const [devicesData, elderlyData] = await Promise.all([
                deviceService.getAll(),
                elderlyPersonService.getAll(),
            ]);
            devices = Array.isArray(devicesData)
                ? devicesData.sort((a: any, b: any) => {
                      const dateA = new Date(
                          a.updated_at || a.created_at
                      ).getTime();
                      const dateB = new Date(
                          b.updated_at || b.created_at
                      ).getTime();
                      return dateB - dateA;
                  })
                : [];
            elderlyPersons = Array.isArray(elderlyData) ? elderlyData : [];
        } catch (err: any) {
            deviceFormError = err?.message || "Error al cargar dispositivos";
        } finally {
            deviceFormLoading = false;
        }
    }

    function openAddDeviceForm() {
        editingDevice = null;
        deviceFormTitle = "Agregar Dispositivo";
        deviceFormError = "";
        deviceFormVisible = true;
        deviceFormKey = Date.now();
    }

    function openEditDeviceForm(device: any) {
        editingDevice = device;
        deviceFormTitle = "Editar Dispositivo";
        deviceFormError = "";
        deviceFormVisible = true;
        deviceFormKey = Date.now();
    }

    function closeDeviceForm() {
        deviceFormVisible = false;
        editingDevice = null;
        deviceFormError = "";
        deviceFormKey = Date.now();
    }

    async function handleDeviceFormSubmit(e: any) {
        deviceFormLoading = true;
        deviceFormError = "";
        try {
            const data = e.detail;
            if (!data.name || !data.device_id || !data.elderly_person_id) {
                deviceFormError =
                    "Nombre, ID de dispositivo y adulto mayor son obligatorios";
                return;
            }
            if (editingDevice) {
                await deviceService.update(editingDevice.id, data);
            } else {
                await deviceService.create(data);
            }
            deviceFormVisible = false;
            await loadDevicesAndElderly();
        } catch (err: any) {
            deviceFormError =
                err?.message || (err && err.toString()) || "Error al guardar";
        } finally {
            deviceFormLoading = false;
        }
    }

    async function handleDeleteDevice(device: any) {
        if (
            confirm(
                `¿Seguro que deseas eliminar el dispositivo '${device.name}'?`
            )
        ) {
            try {
                await deviceService.delete(device.id);
                await loadDevicesAndElderly();
            } catch (err: any) {
                alert(err?.message || "Error al eliminar dispositivo");
            }
        }
    }

    function handleGetStarted() {
        if (isAuthenticated) {
            goto("/dashboard");
        } else {
            goto("/login");
        }
    }

    function handleLearnMore() {
        // Scroll to features section
        document
            .getElementById("features")
            ?.scrollIntoView({ behavior: "smooth" });
    }
</script>

<svelte:head>
    <title>CUIOT - Tecnologías para el Cuidado</title>
    <meta
        name="description"
        content="Plataforma integral de monitoreo y cuidado para personas que requieren atención especializada"
    />
</svelte:head>

<!-- Hero Section -->
<section class="hero-section">
    <div class="hero-background">
        <div class="hero-overlay" />
    </div>

    <div class="container mx-auto px-6 py-20">
        <div class="text-center max-w-4xl mx-auto">
            <div class="mb-8">
                <h1 class="text-5xl md:text-7xl font-bold text-white mb-6">
                    CUIOT
                </h1>
                <p class="text-xl md:text-2xl text-blue-100 mb-8">
                    Tecnologías para el Cuidado
                </p>
                <p
                    class="text-lg md:text-xl text-blue-50 mb-12 max-w-3xl mx-auto"
                >
                    Plataforma integral de monitoreo inteligente que conecta
                    cuidadores, instituciones y familias para brindar el mejor
                    cuidado posible a quienes más lo necesitan.
                </p>
            </div>

            <div
                class="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
                <button
                    on:click={handleGetStarted}
                    class="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-blue-50 transition-all duration-300 flex items-center gap-2 shadow-lg hover:shadow-xl"
                >
                    {isAuthenticated ? "Ir al Dashboard" : "Comenzar"}
                    <ArrowRight class="w-5 h-5" />
                </button>
                <button
                    on:click={handleLearnMore}
                    class="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition-all duration-300"
                >
                    Conocer Más
                </button>
            </div>
        </div>
    </div>
</section>

<!-- Features Section -->
<section id="features" class="py-20 bg-gray-50">
    <div class="container mx-auto px-6">
        <div class="text-center mb-16">
            <h2 class="text-4xl font-bold text-gray-900 mb-4">
                Solución Integral de Cuidado
            </h2>
            <p class="text-xl text-gray-600 max-w-3xl mx-auto">
                Nuestra plataforma combina tecnología IoT avanzada con
                inteligencia artificial para crear un ecosistema completo de
                cuidado y monitoreo.
            </p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <!-- Monitoreo Inteligente -->
            <div
                class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
            >
                <div
                    class="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mb-6"
                >
                    <Activity class="w-8 h-8 text-blue-600" />
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-4">
                    Monitoreo Inteligente
                </h3>
                <p class="text-gray-600">
                    Sensores avanzados y algoritmos de IA para detectar patrones
                    de comportamiento y alertar sobre situaciones que requieren
                    atención inmediata.
                </p>
            </div>

            <!-- Seguridad 24/7 -->
            <div
                class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
            >
                <div
                    class="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mb-6"
                >
                    <Shield class="w-8 h-8 text-green-600" />
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-4">
                    Seguridad 24/7
                </h3>
                <p class="text-gray-600">
                    Sistema de alertas en tiempo real con protocolos de
                    emergencia automatizados y comunicación directa con
                    servicios de emergencia.
                </p>
            </div>

            <!-- Gestión de Cuidadores -->
            <div
                class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
            >
                <div
                    class="w-16 h-16 bg-purple-100 rounded-lg flex items-center justify-center mb-6"
                >
                    <Users class="w-8 h-8 text-purple-600" />
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-4">
                    Gestión de Cuidadores
                </h3>
                <p class="text-gray-600">
                    Coordinación eficiente entre cuidadores, asignación
                    inteligente de tareas y seguimiento del bienestar de cada
                    persona bajo cuidado.
                </p>
            </div>

            <!-- Ubicación y Geofencing -->
            <div
                class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
            >
                <div
                    class="w-16 h-16 bg-orange-100 rounded-lg flex items-center justify-center mb-6"
                >
                    <MapPin class="w-8 h-8 text-orange-600" />
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-4">
                    Ubicación y Geofencing
                </h3>
                <p class="text-gray-600">
                    Seguimiento de ubicación en tiempo real con zonas de
                    seguridad personalizables y alertas automáticas cuando se
                    cruzan límites.
                </p>
            </div>

            <!-- Dispositivos IoT -->
            <div
                class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
            >
                <div
                    class="w-16 h-16 bg-red-100 rounded-lg flex items-center justify-center mb-6"
                >
                    <Smartphone class="w-8 h-8 text-red-600" />
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-4">
                    Dispositivos IoT
                </h3>
                <p class="text-gray-600">
                    Red de sensores inteligentes que monitorean signos vitales,
                    actividad física y condiciones ambientales de manera no
                    invasiva.
                </p>
            </div>

            <!-- Cuidado Personalizado -->
            <div
                class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
            >
                <div
                    class="w-16 h-16 bg-pink-100 rounded-lg flex items-center justify-center mb-6"
                >
                    <Heart class="w-8 h-8 text-pink-600" />
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-4">
                    Cuidado Personalizado
                </h3>
                <p class="text-gray-600">
                    Protocolos de cuidado adaptados a las necesidades
                    específicas de cada persona, con seguimiento personalizado y
                    reportes detallados.
                </p>
            </div>
        </div>
    </div>
</section>

<!-- How It Works Section -->
<section class="py-20 bg-white">
    <div class="container mx-auto px-6">
        <div class="text-center mb-16">
            <h2 class="text-4xl font-bold text-gray-900 mb-4">
                ¿Cómo Funciona?
            </h2>
            <p class="text-xl text-gray-600 max-w-3xl mx-auto">
                Un proceso simple y efectivo para implementar el cuidado
                inteligente
            </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div class="text-center">
                <div
                    class="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6"
                >
                    <span class="text-white text-2xl font-bold">1</span>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-4">
                    Configuración
                </h3>
                <p class="text-gray-600">
                    Instalamos y configuramos los dispositivos IoT en el entorno
                    de cuidado, adaptándolos a las necesidades específicas.
                </p>
            </div>

            <div class="text-center">
                <div
                    class="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6"
                >
                    <span class="text-white text-2xl font-bold">2</span>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-4">
                    Monitoreo
                </h3>
                <p class="text-gray-600">
                    El sistema comienza a recopilar datos en tiempo real,
                    analizando patrones y detectando situaciones que requieren
                    atención.
                </p>
            </div>

            <div class="text-center">
                <div
                    class="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6"
                >
                    <span class="text-white text-2xl font-bold">3</span>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-4">
                    Cuidado
                </h3>
                <p class="text-gray-600">
                    Los cuidadores reciben alertas inteligentes y pueden
                    coordinar la atención de manera eficiente y personalizada.
                </p>
            </div>
        </div>
    </div>
</section>

<!-- CTA Section -->
<section class="py-20 bg-blue-600">
    <div class="container mx-auto px-6 text-center">
        <h2 class="text-4xl font-bold text-white mb-6">
            ¿Listo para Transformar el Cuidado?
        </h2>
        <p class="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Únete a la revolución del cuidado inteligente y brinda la mejor
            atención posible a quienes más lo necesitan.
        </p>
        <button
            on:click={handleGetStarted}
            class="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-blue-50 transition-all duration-300 flex items-center gap-2 mx-auto"
        >
            {isAuthenticated ? "Acceder al Sistema" : "Comenzar Ahora"}
            <ArrowRight class="w-5 h-5" />
        </button>
    </div>
</section>

<!-- Footer -->
<footer class="bg-gray-900 text-white py-12">
    <div class="container mx-auto px-6">
        <div class="grid md:grid-cols-4 gap-8">
            <div>
                <h3 class="text-2xl font-bold mb-4">CUIOT</h3>
                <p class="text-gray-400">Tecnologías para el Cuidado</p>
            </div>
            <div>
                <h4 class="font-semibold mb-4">Plataforma</h4>
                <ul class="space-y-2 text-gray-400">
                    <li>
                        <a href="#" class="hover:text-white transition-colors"
                            >Características</a
                        >
                    </li>
                    <li>
                        <a href="#" class="hover:text-white transition-colors"
                            >Precios</a
                        >
                    </li>
                    <li>
                        <a href="#" class="hover:text-white transition-colors"
                            >API</a
                        >
                    </li>
                </ul>
            </div>
            <div>
                <h4 class="font-semibold mb-4">Soporte</h4>
                <ul class="space-y-2 text-gray-400">
                    <li>
                        <a href="#" class="hover:text-white transition-colors"
                            >Documentación</a
                        >
                    </li>
                    <li>
                        <a href="#" class="hover:text-white transition-colors"
                            >Contacto</a
                        >
                    </li>
                    <li>
                        <a href="#" class="hover:text-white transition-colors"
                            >Estado del Sistema</a
                        >
                    </li>
                </ul>
            </div>
            <div>
                <h4 class="font-semibold mb-4">Legal</h4>
                <ul class="space-y-2 text-gray-400">
                    <li>
                        <a href="#" class="hover:text-white transition-colors"
                            >Privacidad</a
                        >
                    </li>
                    <li>
                        <a href="#" class="hover:text-white transition-colors"
                            >Términos</a
                        >
                    </li>
                    <li>
                        <a href="#" class="hover:text-white transition-colors"
                            >Cookies</a
                        >
                    </li>
                </ul>
            </div>
        </div>
        <div
            class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400"
        >
            <p>
                &copy; 2024 CUIOT - Tecnologías para el Cuidado. Todos los
                derechos reservados.
            </p>
        </div>
    </div>
</footer>

<style>
    .hero-section {
        position: relative;
        min-height: 100vh;
        display: flex;
        align-items: center;
        background: linear-gradient(
            135deg,
            #1e3a8a 0%,
            #3b82f6 50%,
            #1e40af 100%
        );
    }

    .hero-background {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: radial-gradient(
                circle at 20% 80%,
                rgba(120, 119, 198, 0.3) 0%,
                transparent 50%
            ),
            radial-gradient(
                circle at 80% 20%,
                rgba(255, 119, 198, 0.3) 0%,
                transparent 50%
            ),
            radial-gradient(
                circle at 40% 40%,
                rgba(120, 219, 255, 0.3) 0%,
                transparent 50%
            );
    }

    .hero-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.1);
    }

    .container {
        position: relative;
        z-index: 10;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .hero-section {
            min-height: 80vh;
            padding: 2rem 0;
        }
    }
</style>
