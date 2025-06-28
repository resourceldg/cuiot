# Modelo de Negocio y Arquitectura - Sistema de Monitoreo IoT para Cuidado Humano

## 1. Modelo de Negocio

### Usuarios Principales
- **Personas con necesidades de cuidado** (no solo adultos mayores)
  - Adultos mayores (65+ años)
  - Personas con discapacidad física o intelectual
  - Personas con condiciones médicas crónicas
  - Personas en recuperación post-quirúrgica
  - Personas con movilidad reducida temporal o permanente
  - Niños con necesidades especiales
  - Personas con trastornos del espectro autista
  - Personas con demencia o Alzheimer
- **Familiares y cuidadores** (hijos, nietos, personal de cuidado, tutores)
- **Centros de cuidado y atención**
  - Geriátricos y residencias
  - Centros de día
  - Centros de cuidados especiales
  - Escuelas especiales
  - Centros de rehabilitación
  - Hogares de tránsito
  - Centros de atención temprana
- **Proveedores de salud** (ambulancias, médicos, enfermeros, terapistas)
- **Servicios de emergencia** locales y regionales

### Servicios Ofrecidos

#### Básicos
- Monitoreo remoto 24/7 (hogar, residencia, centro de cuidado, etc.)
- Alertas automáticas en tiempo real
- Botón/mando de emergencia con llamada directa
- Panel web para familiares y cuidadores
- Reportes de actividad y salud
- Gestión de medicamentos y recordatorios

#### Avanzados
- Videovigilancia bajo demanda
- Detección automática de caídas y comportamientos anómalos
- Monitoreo de signos vitales (presión arterial, temperatura, frecuencia cardíaca)
- Detección de gases tóxicos y humo
- Integración con servicios de emergencia
- App móvil para familiares y cuidadores
- Sistema de geolocalización para personas con tendencia a deambular
- Monitoreo de patrones de sueño y actividad
- Detección de convulsiones o episodios médicos

#### Especializados por Tipo de Usuario
- **Para personas con autismo**: Detección de crisis, monitoreo de rutinas
- **Para personas con demencia**: Control de deambulación, recordatorios personalizados
- **Para niños especiales**: Monitoreo de seguridad, comunicación con padres
- **Para centros de día**: Gestión de grupos, reportes institucionales
- **Para escuelas especiales**: Integración con protocolos educativos

### Modelo de Ingresos

#### Venta de Hardware
- Dispositivos IoT (sensores, cámaras, mandos, wearables)
- Instalación y configuración
- Mantenimiento técnico
- Actualizaciones de firmware

#### Servicios de Suscripción por Usuario
- **Básico**: Monitoreo básico + alertas (ARS 3,500/mes por persona)
- **Premium**: + Videovigilancia + Reportes médicos (ARS 6,000/mes por persona)
- **Profesional**: + Integración emergencias + 24/7 + IA (ARS 9,000/mes por persona)

#### Servicios de Suscripción para Centros
- **Centro Pequeño** (5-20 personas): ARS 15,000/mes
- **Centro Mediano** (21-50 personas): ARS 35,000/mes
- **Centro Grande** (51+ personas): ARS 60,000/mes
- **Escuela Especial**: ARS 25,000/mes (incluye módulos educativos)

#### Servicios Adicionales
- Reportes médicos personalizados
- Integración con seguros o servicios sociales
- Servicios de emergencia premium
- Consultoría y capacitación
- Desarrollo de protocolos específicos por tipo de centro
- Integración con sistemas de gestión institucional

### Mercado Objetivo - Costa Atlántica y Provincia de Buenos Aires

#### Demografía y Mercado Potencial

##### Costa Atlántica
- **Mar del Plata**: ~650,000 habitantes
  - Población mayor de 65 años: ~97,500 (15%)
  - Personas con discapacidad: ~32,500 (5%)
  - Centros geriátricos: ~80 establecimientos
  - Centros de día: ~45 establecimientos
  - Escuelas especiales: ~25 establecimientos

- **Pinamar**: ~45,000 habitantes
  - Población mayor de 65 años: ~6,750 (15%)
  - Centros de cuidado: ~15 establecimientos

- **Villa Gesell**: ~35,000 habitantes
  - Población mayor de 65 años: ~5,250 (15%)
  - Centros de cuidado: ~12 establecimientos

- **San Clemente del Tuyú**: ~15,000 habitantes
  - Población mayor de 65 años: ~2,250 (15%)
  - Centros de cuidado: ~8 establecimientos

##### Provincia de Buenos Aires
- **Población total**: ~17,500,000 habitantes
- **Población mayor de 65 años**: ~2,625,000 (15%)
- **Personas con discapacidad**: ~875,000 (5%)
- **Centros geriátricos**: ~1,200 establecimientos
- **Centros de día**: ~800 establecimientos
- **Escuelas especiales**: ~400 establecimientos
- **Centros de rehabilitación**: ~300 establecimientos

#### Segmentos de Mercado

##### Hogares Particulares
- **Familias con adultos mayores**: ~500,000 hogares
- **Familias con personas con discapacidad**: ~200,000 hogares
- **Familias con niños especiales**: ~50,000 hogares

##### Centros de Cuidado
- **Geriátricos privados**: ~800 establecimientos
- **Centros de día**: ~600 establecimientos
- **Escuelas especiales**: ~300 establecimientos
- **Centros de rehabilitación**: ~200 establecimientos
- **Hogares de tránsito**: ~100 establecimientos

##### Instituciones Públicas
- **Hospitales públicos**: ~150 establecimientos
- **Centros de salud**: ~800 establecimientos
- **Escuelas públicas especiales**: ~200 establecimientos

#### Competencia
- Sistemas de alarma tradicionales
- Servicios de teleasistencia básicos
- Cámaras de seguridad domésticas
- Sistemas de monitoreo médico básicos
- Apps de cuidado familiar simples

#### Ventajas Competitivas
- Tecnología IoT moderna y escalable
- Integración múltiple de sensores y dispositivos
- Interfaz accesible para diferentes tipos de usuarios
- Soporte local en toda la región
- Personalización por tipo de necesidad
- Integración con sistemas institucionales
- Cumplimiento de normativas de accesibilidad

## 2. Arquitectura Técnica

### Dispositivos IoT

#### Sensores Especializados
- **Movimiento**: PIR, radar, ultrasonido, infrarrojo
- **Presión arterial**: Bluetooth/WiFi, con memoria de lecturas
- **Gas**: CO, CO2, humo, gas natural
- **Temperatura y humedad**: Ambiental y corporal
- **Presencia**: RFID, Bluetooth, NFC
- **Actividad física**: Acelerómetro, giroscopio
- **Frecuencia cardíaca**: Óptico, ECG
- **Nivel de oxígeno**: SpO2
- **Glucosa**: Monitoreo continuo (futuro)
- **Convulsiones**: Sensores de movimiento especializados
- **Deambulación**: Sensores de puertas y geolocalización

#### Cámaras Especializadas
- IP con visión nocturna y infrarroja
- Detección de movimiento y comportamiento
- Compresión H.264/H.265/H.266
- RTSP/HTTP/MQTT/WebRTC
- Análisis de video con IA
- Privacidad por defecto (mascarado automático)

#### Comunicación Avanzada
- **Módulo SIM**: 4G/LTE/5G para llamadas/SMS/datos
- **WiFi**: Conexión local de alta velocidad
- **Bluetooth**: Sensores cercanos y wearables
- **Zigbee/Z-Wave**: Red de sensores de bajo consumo
- **LoRaWAN**: Comunicación de largo alcance
- **NFC**: Identificación y configuración rápida

#### Mandos y Interfaces Físicas
- **Botón de pánico**: Grande, accesible, con vibración
- **Interfaz táctil**: Pantalla simple con iconos grandes
- **Control por voz**: Comandos de voz simples
- **Interfaz braille**: Para usuarios con discapacidad visual
- **Mando remoto**: Para control de TV y dispositivos
- **Pulsera inteligente**: Con botón de emergencia y geolocalización

### Backend (FastAPI + PostgreSQL)

#### Microservicios Especializados
```
├── api-gateway/              # Entrada principal con rate limiting
├── user-service/             # Gestión de usuarios y roles
├── device-service/           # Gestión de dispositivos IoT
├── event-service/            # Procesamiento de eventos en tiempo real
├── alert-service/            # Gestión de alertas y notificaciones
├── video-service/            # Streaming y procesamiento de video
├── notification-service/     # Notificaciones multi-canal
├── emergency-service/        # Llamadas/SMS de emergencia
├── health-service/           # Monitoreo de salud y reportes
├── location-service/         # Geolocalización y tracking
├── ai-service/               # Procesamiento con IA
├── center-service/           # Gestión de centros de cuidado
├── report-service/           # Generación de reportes
└── integration-service/      # Integraciones externas
```

#### Base de Datos Expandida
```sql
-- Usuarios y roles expandidos
users, roles, user_roles, user_permissions

-- Personas bajo cuidado (no solo adultos mayores)
cared_persons, care_types, medical_conditions, medications

-- Dispositivos y configuraciones avanzadas
devices, device_types, device_configs, device_maintenance

-- Eventos y alertas especializados
events, alerts, alert_rules, alert_escalations

-- Monitoreo de salud y actividad
health_records, activity_logs, sleep_patterns, vital_signs

-- Configuración de emergencia y contactos
emergency_contacts, emergency_configs, emergency_protocols

-- Centros de cuidado
care_centers, center_types, center_staff, center_patients

-- Video y multimedia
video_streams, video_events, video_recordings, video_analytics

-- Geolocalización
location_tracking, geofences, location_alerts

-- Reportes y analytics
reports, report_templates, analytics_data
```

#### APIs Principales Expandidas
```
/api/v1/users/               # CRUD usuarios con roles
/api/v1/cared-persons/       # CRUD personas bajo cuidado
/api/v1/devices/             # CRUD dispositivos IoT
/api/v1/events/              # Eventos en tiempo real
/api/v1/alerts/              # Gestión alertas
/api/v1/video/               # Streaming/snapshots/recordings
/api/v1/emergency/           # Llamadas emergencia
/api/v1/health/              # Monitoreo de salud
/api/v1/location/            # Geolocalización
/api/v1/reports/             # Reportes y analytics
/api/v1/centers/             # Gestión de centros
/api/v1/ai/                  # Servicios de IA
/api/v1/integrations/        # Integraciones externas
```

### Frontend (SvelteKit)

#### Páginas Principales Expandidas
- **Dashboard Personalizado**: Según tipo de usuario y necesidades
- **Gestión de Personas**: CRUD de personas bajo cuidado
- **Dispositivos**: Gestión y configuración avanzada
- **Video**: Streaming en vivo, grabaciones, análisis
- **Alertas**: Historial y configuración por tipo
- **Reportes**: Salud, actividad, emergencias, institucionales
- **Configuración**: Usuarios, emergencias, notificaciones
- **Centros**: Gestión para administradores de centros
- **Analytics**: Datos y estadísticas avanzadas
- **Accesibilidad**: Configuración de accesibilidad

#### Características de Accesibilidad Avanzadas
- Interfaz adaptable según tipo de discapacidad
- Botones grandes y contrastantes
- Soporte para lectores de pantalla
- Modo oscuro/claro automático
- Texto escalable (hasta 200%)
- Navegación por teclado completa
- Comandos de voz
- Interfaz táctil optimizada
- Modo de alto contraste
- Reducción de movimiento

### Integraciones Externas

#### Servicios de Emergencia Regionales
- **107** (Emergencias locales)
- **911** (Policía)
- **100** (Bomberos)
- **101** (Policía Federal)
- **106** (Emergencias médicas)
- Servicios privados de emergencia

#### Proveedores de Salud
- Hospitales públicos y privados
- Clínicas especializadas
- Ambulancias privadas
- Médicos de cabecera
- Especialistas por área
- Centros de rehabilitación

#### Centros de Cuidado
- APIs de gestión institucional
- Sistemas de turnos médicos
- Registros médicos electrónicos
- Sistemas de facturación
- Gestión de personal

#### Notificaciones Multi-canal
- **Push**: App móvil personalizada
- **SMS**: Twilio, proveedores locales
- **Email**: SMTP con plantillas
- **WhatsApp**: API Business
- **Telegram**: Bot personalizado
- **Llamadas**: IVR personalizado

## 3. Flujo de Servicio Expandido

### Evento Detectado
1. Sensor detecta anomalía o evento
2. Dispositivo envía evento por MQTT/HTTP con metadatos
3. Backend procesa y clasifica evento según tipo de persona
4. Sistema evalúa reglas de alerta personalizadas
5. Si es crítico, activa protocolo de emergencia específico

### Notificación Personalizada
1. Alerta se envía según preferencias del usuario
2. Notificación adaptada al tipo de necesidad
3. Escalación automática si no hay respuesta
4. Integración con servicios de emergencia locales
5. Registro completo en base de datos

### Respuesta Especializada
1. Familiar/cuidador puede ver video en vivo
2. Botón de emergencia manual disponible
3. Llamada directa a servicios específicos
4. Seguimiento hasta resolución
5. Reporte post-evento

## 4. Roadmap de Desarrollo Expandido

### Fase 1 (MVP Ampliado) - 4 meses
- [ ] Backend expandido con nuevos modelos
- [ ] Frontend con gestión de personas (no solo adultos mayores)
- [ ] Integración básica de múltiples tipos de sensores
- [ ] Sistema de alertas personalizado
- [ ] Pruebas con diferentes tipos de usuarios
- [ ] Integración con centros de cuidado básicos

### Fase 2 (Servicios Avanzados) - 8 meses
- [ ] Integración de cámaras con IA
- [ ] App móvil especializada
- [ ] Sistema de reportes institucionales
- [ ] Integración con servicios de emergencia regionales
- [ ] Geolocalización y tracking
- [ ] Pruebas con centros de cuidado

### Fase 3 (Producción Regional) - 12 meses
- [ ] Mando físico accesible
- [ ] Detección automática especializada
- [ ] Integración con proveedores de salud regionales
- [ ] Sistema de facturación para centros
- [ ] Lanzamiento comercial en Costa Atlántica
- [ ] Expansión a Provincia de Buenos Aires

### Fase 4 (Escalado Nacional) - 18 meses
- [ ] IA para detección de patrones específicos
- [ ] Integración con seguros nacionales
- [ ] Expansión a otras provincias
- [ ] API para terceros y partners
- [ ] Certificaciones de accesibilidad
- [ ] Integración con sistemas públicos

## 5. Consideraciones Legales y de Privacidad

### RGPD/Ley de Protección de Datos
- Consentimiento explícito del usuario o tutor legal
- Derecho al olvido implementado
- Portabilidad de datos médicos
- Notificación de brechas en 72 horas
- Oficial de protección de datos

### Leyes Locales y Regionales
- Ley de Discapacidad
- Ley de Protección al Adulto Mayor
- Regulaciones de salud provinciales
- Normativas de emergencias locales
- Protección al consumidor
- Ley de accesibilidad

### Seguridad Avanzada
- Encriptación end-to-end para video
- Autenticación multifactor obligatoria
- Auditoría de accesos completa
- Backup y recuperación automática
- Cumplimiento HIPAA (estándar médico)

## 6. Métricas de Éxito Expandidas

### Técnicas
- Tiempo de respuesta < 15 segundos
- Disponibilidad > 99.95%
- Falsos positivos < 3%
- Usabilidad > 95%
- Accesibilidad > 98%

### Negocio
- Retención de clientes > 90%
- NPS > 60
- Tiempo de resolución < 3 minutos
- Satisfacción > 4.7/5
- Expansión a 5 ciudades en 18 meses

### Sociales
- Reducción de tiempo de respuesta emergencias en 50%
- Mejora en calidad de vida de usuarios en 40%
- Reducción de costos de cuidado en 30%
- Independencia de usuarios en 60%
- Integración de 100+ centros de cuidado

---

*Documento en desarrollo - Versión 2.0*
*Última actualización: [Fecha]*
*Próxima revisión: [Fecha]* 