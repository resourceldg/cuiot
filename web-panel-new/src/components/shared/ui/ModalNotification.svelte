<script lang="ts">
    import { createEventDispatcher, onMount } from "svelte";

    export let type: "success" | "error" = "success";
    export let message: string = "";
    export let subtitle: string = "";
    export let duration: number = 2000;
    export let show: boolean = false;

    const dispatch = createEventDispatcher();
    let animationComplete = false;

    // Iconos para cada tipo
    const icons = {
        success: "✓",
        error: "✕",
    };

    // Colores para cada tipo
    const colors = {
        success: {
            bg: "#d4edda",
            border: "#c3e6cb",
            text: "#155724",
            icon: "#28a745",
        },
        error: {
            bg: "#f8d7da",
            border: "#f5c6cb",
            text: "#721c24",
            icon: "#dc3545",
        },
    };

    // Mensajes por defecto
    const defaultMessages = {
        success: {
            title: "¡Operación exitosa!",
            subtitle: "La acción se completó correctamente.",
        },
        error: {
            title: "Error",
            subtitle: "Ocurrió un problema al procesar la acción.",
        },
    };

    // Usar mensaje personalizado o por defecto
    $: displayMessage = message || defaultMessages[type].title;
    $: displaySubtitle = subtitle || defaultMessages[type].subtitle;
    $: currentColors = colors[type];

    onMount(() => {
        if (show && duration > 0) {
            setTimeout(() => {
                animationComplete = true;
                setTimeout(() => {
                    dispatch("close");
                }, 300); // Tiempo para la animación de salida
            }, duration);
        }
    });

    // Reiniciar animación cuando show cambia
    $: if (show) {
        animationComplete = false;
    }
</script>

{#if show}
    <div
        class="modal-notification"
        class:success={type === "success"}
        class:error={type === "error"}
    >
        <!-- Círculo animado de fondo -->
        <div
            class="notification-circle"
            class:complete={animationComplete}
        ></div>

        <!-- Contenido de la notificación -->
        <div class="notification-content" class:complete={animationComplete}>
            <div class="notification-icon" style="color: {currentColors.icon}">
                {icons[type]}
            </div>
            <div class="notification-text">
                <h4 style="color: {currentColors.text}">{displayMessage}</h4>
                <p style="color: {currentColors.text}">{displaySubtitle}</p>
            </div>
        </div>
    </div>
{/if}

<style>
    .modal-notification {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1002;
        overflow: hidden;
        border-radius: inherit;
    }

    .notification-circle {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        opacity: 0.9;
    }

    .notification-circle.complete {
        width: 200%;
        height: 200%;
        opacity: 0.95;
    }

    .success .notification-circle {
        background: radial-gradient(
            circle,
            rgba(40, 167, 69, 0.1) 0%,
            rgba(40, 167, 69, 0.05) 100%
        );
    }

    .error .notification-circle {
        background: radial-gradient(
            circle,
            rgba(220, 53, 69, 0.1) 0%,
            rgba(220, 53, 69, 0.05) 100%
        );
    }

    .notification-content {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        transform: scale(0.8);
        opacity: 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .notification-content.complete {
        transform: scale(1);
        opacity: 1;
    }

    .notification-icon {
        font-size: 2.5rem;
        font-weight: bold;
        line-height: 1;
        min-width: 2.5rem;
        text-align: center;
    }

    .notification-text h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
        font-weight: 600;
    }

    .notification-text p {
        margin: 0;
        opacity: 0.8;
        font-size: 0.95rem;
    }

    /* Animaciones adicionales para el contenido */
    @keyframes slideIn {
        from {
            transform: translateY(20px) scale(0.9);
            opacity: 0;
        }
        to {
            transform: translateY(0) scale(1);
            opacity: 1;
        }
    }

    .notification-content {
        animation: slideIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Responsive */
    @media (max-width: 600px) {
        .notification-content {
            padding: 1rem;
            margin: 1rem;
        }

        .notification-icon {
            font-size: 2rem;
            min-width: 2rem;
        }

        .notification-text h4 {
            font-size: 1.1rem;
        }

        .notification-text p {
            font-size: 0.9rem;
        }
    }
</style>
