# Arquitectura Técnica Detallada - Sistema IoT de Monitoreo

## 1. Visión General del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Dispositivos  │    │    Backend      │    │    Frontend     │
│      IoT        │    │   (FastAPI)     │    │   (SvelteKit)   │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │   Sensores  │ │    │ │ API Gateway │ │    │ │   Dashboard │ │
│ │   Cámaras   │ │◄──►│ │ Microserv.  │ │◄──►│ │   App Web   │ │
│ │   Mandos    │ │    │ │ PostgreSQL  │ │    │ │   Móvil     │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MQTT Broker   │    │   Servicios     │    │   Notificaciones│
│   (Mosquitto)   │    │   Externos      │    │   (Push/SMS)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 2. Componentes del Sistema

### 2.1 Dispositivos IoT

#### Sensores de Movimiento
```python
# Ejemplo de estructura de datos
{
    "device_id": "motion_001",
    "type": "motion_sensor",
    "location": "living_room",
    "status": "active",
    "last_event": "2024-01-15T10:30:00Z",
    "sensitivity": 0.8,
    "battery_level": 85
}
```

#### Cámaras IP
```python
{
    "device_id": "camera_001",
    "type": "ip_camera",
    "model": "Hikvision DS-2CD2142FWD-I",
    "rtsp_url": "rtsp://192.168.1.100:554/stream1",
    "resolution": "1080p",
    "night_vision": true,
    "motion_detection": true
}
```

#### Medidor de Presión Arterial
```python
{
    "device_id": "bp_001",
    "type": "blood_pressure",
    "user_id": "user_123",
    "last_reading": {
        "systolic": 120,
        "diastolic": 80,
        "pulse": 72,
        "timestamp": "2024-01-15T10:30:00Z"
    },
    "thresholds": {
        "systolic_high": 140,
        "systolic_low": 90,
        "diastolic_high": 90,
        "diastolic_low": 60
    }
}
```

#### Sensor de Gas
```python
{
    "device_id": "gas_001",
    "type": "gas_sensor",
    "gases": ["CO", "CO2", "smoke"],
    "thresholds": {
        "CO": 50,  # ppm
        "CO2": 1000,  # ppm
        "smoke": 0.1  # mg/m³
    },
    "alarm_level": "critical"
}
```

### 2.2 Backend - Microservicios

#### API Gateway
```python
# FastAPI con rate limiting y autenticación
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

app = FastAPI(title="IoT Monitoring API")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    # Implementar rate limiting
    pass
```

#### User Service
```python
# Gestión de usuarios y autenticación
class UserService:
    async def create_user(self, user_data: UserCreate):
        # Crear usuario con roles
        pass
    
    async def authenticate(self, email: str, password: str):
        # Autenticación JWT
        pass
    
    async def get_user_devices(self, user_id: int):
        # Obtener dispositivos del usuario
        pass
```

#### Device Service
```python
# Gestión de dispositivos IoT
class DeviceService:
    async def register_device(self, device_data: DeviceCreate):
        # Registrar nuevo dispositivo
        pass
    
    async def update_device_status(self, device_id: str, status: str):
        # Actualizar estado del dispositivo
        pass
    
    async def get_device_events(self, device_id: str, limit: int = 100):
        # Obtener eventos del dispositivo
        pass
```

#### Event Service
```python
# Procesamiento de eventos en tiempo real
class EventService:
    async def process_event(self, event_data: EventCreate):
        # Procesar evento y determinar si genera alerta
        pass
    
    async def classify_event(self, event_type: str, data: dict):
        # Clasificar evento (normal, warning, critical)
        pass
    
    async def store_event(self, event: Event):
        # Almacenar evento en base de datos
        pass
```

#### Alert Service
```python
# Gestión de alertas y notificaciones
class AlertService:
    async def create_alert(self, alert_data: AlertCreate):
        # Crear nueva alerta
        pass
    
    async def send_notification(self, alert: Alert):
        # Enviar notificación (push, SMS, email)
        pass
    
    async def escalate_alert(self, alert_id: int):
        # Escalar alerta si no se resuelve
        pass
```

### 2.3 Base de Datos - Esquema

#### Tablas Principales
```sql
-- Usuarios y autenticación
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dispositivos
CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    model VARCHAR(100),
    location VARCHAR(100),
    user_id INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'active',
    config JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Eventos
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) DEFAULT 'info',
    data JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

-- Alertas
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id),
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    resolved_by INTEGER REFERENCES users(id)
);

-- Contactos de emergencia
CREATE TABLE emergency_contacts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    relationship VARCHAR(50),
    priority INTEGER DEFAULT 1,
    active BOOLEAN DEFAULT TRUE
);
```

### 2.4 Frontend - SvelteKit

#### Estructura de Componentes
```
src/
├── components/
│   ├── Dashboard/
│   │   ├── DeviceStatus.svelte
│   │   ├── AlertList.svelte
│   │   ├── VideoStream.svelte
│   │   └── EmergencyButton.svelte
│   ├── Devices/
│   │   ├── DeviceCard.svelte
│   │   ├── DeviceForm.svelte
│   │   └── DeviceConfig.svelte
│   ├── Alerts/
│   │   ├── AlertItem.svelte
│   │   ├── AlertHistory.svelte
│   │   └── AlertSettings.svelte
│   └── Common/
│       ├── Header.svelte
│       ├── Sidebar.svelte
│       └── Toast.svelte
├── stores/
│   ├── auth.js
│   ├── devices.js
│   ├── alerts.js
│   └── notifications.js
└── routes/
    ├── dashboard/
    ├── devices/
    ├── alerts/
    ├── video/
    └── settings/
```

#### Store de Estado (Svelte)
```javascript
// stores/devices.js
import { writable } from 'svelte/store';

export const devices = writable([]);
export const deviceStatus = writable({});

export const deviceStore = {
    subscribe: devices.subscribe,
    
    async loadDevices() {
        const response = await fetch('/api/v1/devices');
        const data = await response.json();
        devices.set(data);
    },
    
    async updateDevice(id, updates) {
        const response = await fetch(`/api/v1/devices/${id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updates)
        });
        // Actualizar store
    }
};
```

### 2.5 Comunicación IoT - MQTT

#### Topics MQTT
```
# Estructura de topics
viejos_son_los_trapos/
├── devices/
│   ├── {device_id}/
│   │   ├── status          # Estado del dispositivo
│   │   ├── events          # Eventos del dispositivo
│   │   ├── config          # Configuración
│   │   └── data            # Datos del sensor
├── alerts/
│   ├── {alert_id}          # Alertas
│   └── emergency           # Emergencias críticas
└── system/
    ├── heartbeat           # Latido del sistema
    └── maintenance         # Mantenimiento
```

#### Ejemplo de Mensaje MQTT
```json
{
    "topic": "viejos_son_los_trapos/devices/motion_001/events",
    "payload": {
        "event_type": "motion_detected",
        "timestamp": "2024-01-15T10:30:00Z",
        "data": {
            "motion_level": 0.85,
            "location": "living_room",
            "duration": 5.2
        },
        "device_id": "motion_001"
    }
}
```

### 2.6 Integraciones Externas

#### Servicios de Emergencia
```python
# emergency_service.py
class EmergencyService:
    async def call_emergency(self, phone_number: str, message: str):
        # Integración con Twilio para llamadas
        pass
    
    async def send_sms(self, phone_number: str, message: str):
        # Envío de SMS
        pass
    
    async def notify_emergency_services(self, alert: Alert):
        # Notificar servicios de emergencia locales
        pass
```

#### Notificaciones Push
```javascript
// notification_service.js
class NotificationService {
    async sendPushNotification(userId, notification) {
        // Enviar notificación push
    }
    
    async sendEmail(userId, subject, body) {
        // Enviar email
    }
    
    async sendSMS(phoneNumber, message) {
        // Enviar SMS
    }
}
```

### Almacenamiento de adjuntos en reportes

- Los archivos adjuntos de reportes se almacenan en el directorio `uploads/reports/` del backend.
- El modelo Report almacena metadatos de los archivos (nombre, url, tipo, tamaño).
- Los archivos se sirven vía endpoint estático `/static/reports/`.
- El frontend permite subir y visualizar adjuntos en la UI de reportes.
- Seguridad: solo usuarios autenticados pueden subir/ver adjuntos.

## 3. Seguridad y Privacidad

### 3.1 Autenticación y Autorización
- JWT tokens con refresh
- Autenticación multifactor (opcional)
- Roles y permisos granulares
- Rate limiting por IP/usuario

### 3.2 Encriptación
- HTTPS/TLS para todas las comunicaciones
- Encriptación de datos sensibles en BD
- Encriptación end-to-end para video
- Firmware seguro para dispositivos IoT

### 3.3 Privacidad
- Consentimiento explícito del usuario
- Anonimización de datos para analytics
- Retención limitada de datos
- Derecho al olvido implementado

## 4. Escalabilidad

### 4.1 Horizontal
- Load balancers para API
- Base de datos con replicación
- Microservicios independientes
- Cache distribuido (Redis)

### 4.2 Vertical
- Optimización de consultas
- Índices de base de datos
- Compresión de datos
- CDN para contenido estático

## 5. Monitoreo y Logs

### 5.1 Métricas
- Tiempo de respuesta API
- Uso de recursos (CPU, memoria, disco)
- Errores y excepciones
- Eventos de seguridad

### 5.2 Logs
- Logs estructurados (JSON)
- Centralización con ELK Stack
- Retención configurable
- Alertas automáticas

---

*Documento técnico - Versión 1.0*
*Última actualización: [Fecha]* 