# Reglas de Negocio - Sistema de Monitoreo Integral de Cuidado Humano

---

## 1. Usuarios
- Un usuario debe estar registrado con datos personales mínimos (nombre, apellido, email, teléfono).
- Un usuario puede ser:
  - Persona bajo cuidado (paciente/beneficiario)
  - Familiar/tutor
  - Cuidador profesional
  - Administrador de centro/institución
  - Personal de salud
- Un usuario puede tener uno o más roles.
- Un usuario puede o no pertenecer a una institución (centro de cuidado, escuela especial, etc.).
- Un usuario puede ser responsable de sí mismo (autocuidado) o tener uno o más cuidadores asignados.
- Un usuario debe tener al menos un servicio contratado activo.

## 2. Servicios
- Un servicio es una suscripción activa a un plan (básico, premium, institucional, etc.).
- Un usuario debe tener al menos un servicio contratado para acceder a funcionalidades del sistema.
- Un servicio debe estar asociado a al menos un dispositivo IoT activo.
- Un servicio puede estar asociado a una persona bajo cuidado o a una institución (servicio institucional).
- Un servicio puede incluir módulos adicionales (videovigilancia, reportes médicos, geolocalización, etc.).
- Un servicio puede estar en estado: activo, suspendido, cancelado, pendiente de pago.

## 3. Dispositivos
- Un dispositivo debe estar registrado y asociado a un servicio activo.
- Un dispositivo puede ser de diferentes tipos: sensor, cámara, botón de pánico, wearable, etc.
- Un dispositivo debe tener un identificador único (device_id).
- Un dispositivo puede estar asociado a una persona bajo cuidado o a una institución.
- Un dispositivo debe reportar su estado (online/offline, batería, última comunicación).
- Un dispositivo puede tener configuraciones personalizadas por usuario o institución.

## 4. Cuidadores y Responsables
- Toda persona bajo cuidado debe tener al menos un cuidador asignado (puede ser el mismo usuario si es autocuidado).
- Un cuidador puede ser familiar, profesional, tutor legal o personal institucional.
- Un cuidador puede estar asignado a varias personas bajo cuidado.
- Un usuario puede ser cuidador y persona bajo cuidado simultáneamente.
- Un cuidador debe tener datos de contacto y disponibilidad horaria.

## 5. Instituciones y Centros
- Una institución puede ser: geriátrico, centro de día, escuela especial, centro de rehabilitación, hogar de tránsito, etc.
- Una persona bajo cuidado puede o no pertenecer a una institución.
- Una institución debe tener al menos un responsable administrativo registrado.
- Una institución puede tener múltiples servicios contratados (por grupo, por paciente, por módulo).
- Una institución puede gestionar múltiples personas bajo cuidado y cuidadores.

## 6. Eventos y Alertas
- Todo evento relevante (caída, crisis, alerta médica, botón de pánico, etc.) debe ser registrado con timestamp y metadatos.
- Una alerta debe estar asociada a un evento, un dispositivo y una persona bajo cuidado.
- Una alerta debe ser notificada a los cuidadores y responsables según reglas de escalamiento.
- Una alerta puede escalarse automáticamente si no es atendida en un tiempo definido.
- Todo evento debe quedar registrado para auditoría y reportes.

## 7. Protocolos Configurables
- **Protocolos de Emergencia**: Cada usuario/institución debe poder configurar protocolos específicos para diferentes tipos de crisis (caída, convulsión, deambulación, crisis de autismo, etc.).
- **Secuencia de Contacto**: Los protocolos deben permitir definir secuencia de contactos (familiar → cuidador → emergencias → servicios especializados).
- **Tiempos de Escalación**: Configuración de tiempos de espera antes de escalar a siguiente nivel (ej: 2 min → familiar, 5 min → emergencias).
- **Acciones Automáticas**: Configuración de acciones automáticas (grabar video, activar sirena, enviar ubicación, etc.).
- **Protocolos por Tipo de Usuario**: Diferentes protocolos según tipo de cuidado (adulto mayor, autismo, discapacidad, etc.).
- **Protocolos Institucionales**: Centros pueden tener protocolos estándar que se aplican a todos sus usuarios.
- **Dashboard de Configuración**: Los protocolos deben ser configurables desde un dashboard intuitivo por usuarios autorizados.

## 8. Geolocalización y Geofencing
- Un usuario con servicio de geolocalización debe tener al menos un dispositivo de tracking activo.
- Un geofence debe estar asociado a una persona bajo cuidado y tener un radio configurable.
- Las violaciones de geofence deben generar alertas según protocolos configurados.
- La ubicación debe registrarse con timestamp y precisión.
- Los datos de ubicación deben respetar límites de retención configurados.

## 9. Tipos de Crisis y Eventos Especializados
- **Crisis de Autismo**: Detección de patrones de comportamiento, activación de protocolos específicos.
- **Convulsiones**: Detección por sensores especializados, activación de protocolo médico.
- **Deambulación**: Detección de salida de área segura, activación de protocolo de búsqueda.
- **Caídas**: Detección por acelerómetro, activación de protocolo de emergencia.
- **Crisis de Ansiedad**: Detección por patrones de respiración/movimiento, activación de protocolo de calma.
- **Episodios de Agresión**: Detección por audio/movimiento, activación de protocolo de seguridad.
- **Falta de Medicación**: Detección por horarios, activación de recordatorios escalados.

## 10. Reportes y Analytics
- Todo evento debe ser reportable con filtros por fecha, tipo, usuario, institución.
- Los reportes deben ser configurables por rol (familiar ve solo su familiar, admin ve todo el centro).
- Los reportes médicos deben cumplir estándares HIPAA/legales locales.
- Los analytics deben permitir identificar patrones y tendencias.
- Los reportes institucionales deben incluir métricas de ocupación, eventos, eficiencia.

## 11. Facturación y Planes
- Un plan debe tener límites claros de dispositivos, usuarios, almacenamiento, eventos.
- La facturación debe ser flexible: por usuario, por institución, por módulo.
- Los planes deben permitir escalabilidad (agregar/quitar módulos, usuarios, dispositivos).
- La facturación debe incluir costos de hardware, servicios, integraciones.
- Los descuentos institucionales deben ser configurables.

## 12. Soporte Técnico y Mantenimiento
- **Niveles de Soporte**: El sistema debe ofrecer diferentes niveles de soporte según el plan contratado (básico, premium, 24/7).
- **SLA de Respuesta**: Tiempos de respuesta definidos por criticidad (crítico: 15 min, alto: 2 horas, medio: 24 horas, bajo: 72 horas).
- **Canales de Soporte**: Múltiples canales disponibles (teléfono, email, chat, ticket, WhatsApp, videollamada).
- **Soporte Especializado**: Personal técnico capacitado en diferentes tipos de cuidado y necesidades especiales.
- **Capacitación**: Programas de capacitación obligatorios para usuarios institucionales y opcionales para familiares.
- **Documentación**: Manuales de usuario, guías técnicas, videos tutoriales, FAQ actualizados.
- **Mantenimiento Preventivo**: Monitoreo proactivo de dispositivos, actualizaciones automáticas, backups programados.
- **Escalamiento Técnico**: Procedimientos claros para escalar problemas complejos a especialistas.
- **Soporte Multilingüe**: Soporte en español y portugués para la región.
- **Soporte Remoto**: Capacidad de acceso remoto para diagnóstico y resolución de problemas.
- **Reposición de Hardware**: Políticas claras de reposición de dispositivos defectuosos.
- **Actualizaciones**: Notificación previa de mantenimientos programados y actualizaciones del sistema.

## 13. Accesibilidad y Personalización
- El sistema debe permitir configurar preferencias de accesibilidad por usuario (modo alto contraste, texto grande, lector de pantalla, comandos de voz, etc.).
- Las notificaciones deben adaptarse a las capacidades del usuario (visual, auditiva, cognitiva).
- El sistema debe permitir configurar contactos de emergencia y protocolos personalizados por usuario o institución.

## 14. Seguridad y Privacidad
- Todo acceso a datos personales y médicos debe estar autenticado y autorizado según rol.
- Los datos sensibles deben estar encriptados en tránsito y en reposo.
- El usuario o su tutor legal debe poder ejercer el derecho al olvido y portabilidad de datos.
- Toda acción relevante debe quedar registrada para auditoría.
- Los datos médicos deben cumplir estándares de confidencialidad locales.

## 15. Compliance y Regulaciones
- El sistema debe cumplir con regulaciones locales de protección de datos.
- Los datos médicos deben cumplir estándares de la industria de salud.
- El sistema debe permitir auditorías regulatorias.
- Los protocolos deben ser auditables y trazables.
- El sistema debe cumplir con estándares de accesibilidad (WCAG, etc.).

## 16. Integraciones y Escalabilidad
- El sistema debe poder integrarse con servicios externos (emergencias, salud, seguros, etc.).
- Las reglas de negocio deben ser adaptables para nuevos tipos de usuario, dispositivos y servicios.
- El sistema debe soportar escalabilidad horizontal para instituciones grandes.
- Las integraciones deben ser configurables y no bloqueantes.

---

## Ejemplos de Reglas en Práctica

- **Ejemplo 1:**
  - Juan es una persona bajo cuidado, tiene contratado el servicio premium, está asociado a un sensor de movimiento y una cámara, y su hija Ana es su cuidadora principal. Su protocolo de emergencia está configurado para contactar primero a Ana, luego a emergencias si no responde en 3 minutos.

- **Ejemplo 2:**
  - El Hogar "Sol Naciente" tiene 20 residentes, cada uno con al menos un dispositivo y un cuidador asignado. El centro tiene un servicio institucional y varios módulos extra. Tiene protocolos estándar para caídas y deambulación que se aplican a todos los residentes.

- **Ejemplo 3:**
  - Pedro es usuario autocuidado, tiene un wearable y un botón de pánico, y no pertenece a ninguna institución. Su protocolo está configurado para contactar directamente a emergencias en caso de botón de pánico.

- **Ejemplo 4:**
  - María tiene autismo y su protocolo está configurado para detectar crisis por patrones de movimiento, contactar primero a su terapeuta, y activar música relajante automáticamente.

- **Ejemplo 5:**
  - El Centro "Esperanza" tiene soporte técnico premium 24/7, con SLA de 15 minutos para problemas críticos. Recibe capacitación mensual para el personal y tiene acceso a soporte remoto para diagnóstico rápido.

---

## Notas para Desarrolladores
- Toda validación de reglas de negocio debe implementarse tanto a nivel backend (modelos, servicios, validaciones) como en la interfaz de usuario.
- Si durante el desarrollo surge un caso no contemplado, actualizar este documento antes de modificar el código.
- Mantener este documento versionado y revisado en cada release.
- Los protocolos deben ser implementados como máquinas de estado configurables.
- Las reglas de escalamiento deben ser implementadas con timeouts y reintentos configurables.
- El sistema de soporte debe integrarse con el sistema de tickets y monitoreo.

---

*Última actualización: [Fecha]* 