# Modelo de Negocio y Arquitectura - Sistema de Monitoreo IoT para Adultos Mayores

## 1. Modelo de Negocio

### Usuarios Principales
- **Adultos mayores** (65+ años)
- **Personas con discapacidad** o movilidad reducida
- **Familiares y cuidadores** (hijos, nietos, personal de cuidado)
- **Centros de monitoreo** (privados, públicos, ONGs)
- **Proveedores de salud** (ambulancias, médicos, enfermeros)
- **Servicios de emergencia** locales

### Servicios Ofrecidos

#### Básicos
- Monitoreo remoto 24/7 (hogar, residencia, etc.)
- Alertas automáticas en tiempo real
- Botón/mando de emergencia con llamada directa
- Panel web para familiares y cuidadores
- Reportes de actividad y salud

#### Avanzados
- Videovigilancia bajo demanda
- Detección automática de caídas
- Monitoreo de signos vitales (presión arterial)
- Detección de gases tóxicos
- Integración con servicios de emergencia
- App móvil para familiares

### Modelo de Ingresos

#### Venta de Hardware
- Dispositivos IoT (sensores, cámaras, mandos)
- Instalación y configuración
- Mantenimiento técnico

#### Servicios de Suscripción
- **Básico**: Monitoreo básico + alertas (ARS 5,000/mes)
- **Premium**: + Videovigilancia + Reportes médicos (ARS 8,000/mes)
- **Profesional**: + Integración emergencias + 24/7 (ARS 12,000/mes)

#### Servicios Adicionales
- Reportes médicos personalizados
- Integración con seguros
- Servicios de emergencia premium
- Consultoría y capacitación

### Mercado Objetivo - Mar del Plata

#### Demografía
- Población mayor de 65 años: ~15% (estimado)
- Hogares con adultos mayores: ~25,000
- Residencias geriátricas: ~50 establecimientos

#### Competencia
- Sistemas de alarma tradicionales
- Servicios de teleasistencia básicos
- Cámaras de seguridad domésticas

#### Ventajas Competitivas
- Tecnología IoT moderna
- Integración múltiple de sensores
- Interfaz accesible para adultos mayores
- Soporte local en Mar del Plata

## 2. Arquitectura Técnica

### Dispositivos IoT

#### Sensores
- **Movimiento**: PIR, radar, ultrasonido
- **Presión arterial**: Bluetooth/WiFi
- **Gas**: CO, CO2, humo
- **Temperatura y humedad**
- **Presencia**: RFID, Bluetooth

#### Cámaras
- IP con visión nocturna
- Detección de movimiento
- Compresión H.264/H.265
- RTSP/HTTP/MQTT

#### Comunicación
- **Módulo SIM**: 4G/LTE para llamadas/SMS
- **WiFi**: Conexión local
- **Bluetooth**: Sensores cercanos
- **Zigbee**: Red de sensores

#### Mando Físico
- Botón de pánico grande
- Interfaz accesible
- Vibración y sonido
- Batería de larga duración

### Backend (FastAPI + PostgreSQL)

#### Microservicios
```
├── api-gateway/          # Entrada principal
├── user-service/         # Gestión de usuarios
├── device-service/       # Gestión de dispositivos
├── event-service/        # Procesamiento de eventos
├── alert-service/        # Gestión de alertas
├── video-service/        # Streaming y procesamiento
├── notification-service/ # Notificaciones
└── emergency-service/    # Llamadas/SMS
```

#### Base de Datos
```sql
-- Usuarios y roles
users, roles, user_roles

-- Dispositivos y configuraciones
devices, device_types, device_configs

-- Eventos y alertas
events, alerts, alert_rules

-- Monitoreo y reportes
health_records, activity_logs, reports

-- Configuración de emergencia
emergency_contacts, emergency_configs
```

#### APIs Principales
```
/api/v1/users/           # CRUD usuarios
/api/v1/devices/         # CRUD dispositivos
/api/v1/events/          # Eventos en tiempo real
/api/v1/alerts/          # Gestión alertas
/api/v1/video/           # Streaming/snapshots
/api/v1/emergency/       # Llamadas emergencia
/api/v1/reports/         # Reportes y analytics
```

### Frontend (SvelteKit)

#### Páginas Principales
- **Dashboard**: Estado general, alertas recientes
- **Dispositivos**: Gestión y configuración
- **Video**: Streaming en vivo, grabaciones
- **Alertas**: Historial y configuración
- **Reportes**: Salud, actividad, emergencias
- **Configuración**: Usuarios, emergencias, notificaciones

#### Características de Accesibilidad
- Interfaz simple y clara
- Botones grandes y contrastantes
- Soporte para lectores de pantalla
- Modo oscuro/claro
- Texto escalable

### Integraciones Externas

#### Servicios de Emergencia
- **107** (Emergencias Mar del Plata)
- **911** (Policía)
- **100** (Bomberos)
- **101** (Policía Federal)

#### Proveedores de Salud
- Hospitales locales
- Clínicas privadas
- Ambulancias
- Médicos de cabecera

#### Notificaciones
- **Push**: App móvil
- **SMS**: Twilio, local
- **Email**: SMTP
- **WhatsApp**: API Business

## 3. Flujo de Servicio

### Evento Detectado
1. Sensor detecta anomalía
2. Dispositivo envía evento por MQTT/HTTP
3. Backend procesa y clasifica evento
4. Sistema evalúa reglas de alerta
5. Si es crítico, activa emergencia inmediata

### Notificación
1. Alerta se envía a familiares/cuidadores
2. Push notification en app móvil
3. SMS/Email si configurado
4. Llamada automática si es crítico
5. Registro en base de datos

### Respuesta
1. Familiar puede ver video en vivo
2. Botón de emergencia manual disponible
3. Llamada directa a servicios de emergencia
4. Seguimiento hasta resolución

## 4. Roadmap de Desarrollo

### Fase 1 (MVP) - 3 meses
- [ ] Backend básico con usuarios y dispositivos
- [ ] Frontend dashboard simple
- [ ] Integración básica de sensores
- [ ] Sistema de alertas por email/SMS
- [ ] Pruebas con 5-10 usuarios

### Fase 2 (Beta) - 6 meses
- [ ] Integración de cámaras
- [ ] App móvil básica
- [ ] Sistema de reportes
- [ ] Integración con servicios de emergencia
- [ ] Pruebas con 50-100 usuarios

### Fase 3 (Producción) - 12 meses
- [ ] Mando físico accesible
- [ ] Detección automática de caídas
- [ ] Integración con proveedores de salud
- [ ] Sistema de facturación
- [ ] Lanzamiento comercial

### Fase 4 (Escalado) - 18 meses
- [ ] IA para detección de patrones
- [ ] Integración con seguros
- [ ] Expansión a otras ciudades
- [ ] API para terceros

## 5. Consideraciones Legales y de Privacidad

### RGPD/Ley de Protección de Datos
- Consentimiento explícito del usuario
- Derecho al olvido
- Portabilidad de datos
- Notificación de brechas

### Leyes Locales
- Ley de Teleasistencia
- Regulaciones de salud
- Normativas de emergencias
- Protección al consumidor

### Seguridad
- Encriptación end-to-end
- Autenticación multifactor
- Auditoría de accesos
- Backup y recuperación

## 6. Métricas de Éxito

### Técnicas
- Tiempo de respuesta < 30 segundos
- Disponibilidad > 99.9%
- Falsos positivos < 5%
- Usabilidad > 90%

### Negocio
- Retención de clientes > 85%
- NPS > 50
- Tiempo de resolución < 5 minutos
- Satisfacción > 4.5/5

### Sociales
- Reducción de tiempo de respuesta emergencias
- Mejora en calidad de vida
- Reducción de costos de salud
- Independencia de adultos mayores

---

*Documento en desarrollo - Versión 1.0*
*Última actualización: [Fecha]*
*Próxima revisión: [Fecha]* 