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
    
    async def validate_legal_capacity(self, user_id: str, care_type: str):
        # Validar capacidad legal según tipo de cuidado
        pass
```

#### Package Service (NUEVO - ENTIDAD CENTRAL)
```python
# Gestión de paquetes como unidad central del negocio
class PackageService:
    async def create_package(self, package_data: PackageCreate):
        # Crear nuevo paquete
        pass
    
    async def subscribe_user_to_package(self, user_id: str, package_id: str):
        # Suscribir usuario a paquete
        pass
    
    async def validate_package_limits(self, user_id: str, package_id: str):
        # Validar límites del paquete
        pass
    
    async def calculate_package_cost(self, package_id: str, duration: str):
        # Calcular costo del paquete
        pass
    
    async def check_legal_capacity_for_purchase(self, user_id: str, care_type: str):
        # Verificar capacidad legal para contratar
        pass
```

#### Referral Service (IMPLEMENTADO)
```python
# Sistema de referidos y comisiones
class ReferralService:
    async def generate_referral_code(self, referrer_type: str, referrer_id: str):
        # Generar código único de referido
        pass
    
    async def validate_referral_code(self, code: str):
        # Validar código de referido
        pass
    
    async def process_referral_conversion(self, referral_id: str):
        # Procesar conversión de referido
        pass
    
    async def calculate_commission(self, subscription_amount: float, referrer_type: str):
        # Calcular comisión automática
        pass
    
    async def pay_commission(self, commission_id: str):
        # Pagar comisión
        pass
```

#### Scoring Service (IMPLEMENTADO)
```python
# Sistema de scoring y reviews
class ScoringService:
    async def create_caregiver_review(self, review_data: CaregiverReviewCreate):
        # Crear review de cuidador
        pass
    
    async def calculate_caregiver_score(self, caregiver_id: str):
        # Calcular score automático del cuidador
        pass
    
    async def create_institution_review(self, review_data: InstitutionReviewCreate):
        # Crear review de institución
        pass
    
    async def calculate_institution_score(self, institution_id: str):
        # Calcular score automático de institución
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

### 2.3 Base de Datos - Esquema Actualizado

#### Tablas Principales
```sql
-- Usuarios y autenticación
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Roles y permisos
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    description TEXT,
    permissions JSONB
);

-- Relación usuarios-roles
CREATE TABLE user_roles (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    role_id UUID REFERENCES roles(id),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by UUID REFERENCES users(id),
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Personas bajo cuidado
CREATE TABLE cared_persons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id), -- Representante legal para cuidado delegado
    care_type VARCHAR(20) NOT NULL DEFAULT 'delegated', -- self_care, delegated
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(20),
    phone VARCHAR(20),
    email VARCHAR(100),
    medical_conditions JSONB,
    medications JSONB,
    allergies TEXT,
    blood_type VARCHAR(10),
    care_level VARCHAR(50),
    mobility_level VARCHAR(50),
    address TEXT,
    latitude FLOAT,
    longitude FLOAT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Paquetes (NUEVA ENTIDAD CENTRAL)
CREATE TABLE packages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    package_type VARCHAR(50) NOT NULL, -- basic, familiar, premium, professional, institutional
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price_monthly INTEGER NOT NULL, -- Precio en centavos
    price_yearly INTEGER,
    currency VARCHAR(3) DEFAULT 'ARS',
    features JSONB,
    limitations JSONB,
    max_users INTEGER,
    max_devices INTEGER,
    max_storage_gb INTEGER,
    support_level VARCHAR(50), -- email, chat, phone, 24/7
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Paquetes de usuarios
CREATE TABLE user_packages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    package_id UUID REFERENCES packages(id),
    start_date DATE NOT NULL,
    end_date DATE,
    auto_renew BOOLEAN DEFAULT true,
    status VARCHAR(20) DEFAULT 'active', -- active, suspended, cancelled, expired
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Paquetes de instituciones
CREATE TABLE institution_packages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    institution_id INTEGER REFERENCES institutions(id),
    package_id UUID REFERENCES packages(id),
    start_date DATE NOT NULL,
    end_date DATE,
    auto_renew BOOLEAN DEFAULT true,
    status VARCHAR(20) DEFAULT 'active',
    payment_method VARCHAR(50),
    max_patients INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Referidos (IMPLEMENTADO)
CREATE TABLE referrals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    referral_code VARCHAR(20) UNIQUE NOT NULL,
    referrer_type VARCHAR(20) NOT NULL, -- caregiver, institution, family, cared_person
    referrer_id UUID NOT NULL,
    referred_email VARCHAR(100) NOT NULL,
    referred_name VARCHAR(100),
    referred_phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'pending', -- pending, registered, converted, expired
    registered_at TIMESTAMP,
    converted_at TIMESTAMP,
    expired_at TIMESTAMP,
    commission_amount DECIMAL(10,2),
    commission_paid BOOLEAN DEFAULT false,
    commission_paid_at TIMESTAMP,
    notes TEXT,
    source VARCHAR(50), -- email, whatsapp, phone, in_person
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comisiones de referidos (IMPLEMENTADO)
CREATE TABLE referral_commissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    referral_id UUID REFERENCES referrals(id),
    recipient_type VARCHAR(20) NOT NULL, -- caregiver, institution, family
    recipient_id UUID NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    commission_type VARCHAR(20) NOT NULL, -- first_month, recurring, bonus
    percentage DECIMAL(5,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, paid, cancelled
    paid_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scores de cuidadores (IMPLEMENTADO)
CREATE TABLE caregiver_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    caregiver_id UUID REFERENCES users(id),
    experience_score DECIMAL(3,2),
    quality_score DECIMAL(3,2),
    reliability_score DECIMAL(3,2),
    availability_score DECIMAL(3,2),
    specialization_score DECIMAL(3,2),
    overall_score DECIMAL(3,2),
    total_reviews INTEGER DEFAULT 0,
    last_calculated TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews de cuidadores (IMPLEMENTADO)
CREATE TABLE caregiver_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    caregiver_id UUID REFERENCES users(id),
    reviewer_id UUID REFERENCES users(id),
    cared_person_id UUID REFERENCES cared_persons(id),
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    categories JSONB,
    is_recommended BOOLEAN NOT NULL,
    service_date DATE,
    service_hours DECIMAL(5,2),
    service_type VARCHAR(50),
    is_verified BOOLEAN DEFAULT false,
    is_public BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scores de instituciones (IMPLEMENTADO)
CREATE TABLE institution_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    institution_id INTEGER REFERENCES institutions(id),
    medical_quality_score DECIMAL(3,2),
    infrastructure_score DECIMAL(3,2),
    staff_score DECIMAL(3,2),
    attention_score DECIMAL(3,2),
    price_score DECIMAL(3,2),
    overall_score DECIMAL(3,2),
    total_reviews INTEGER DEFAULT 0,
    last_calculated TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews de instituciones (IMPLEMENTADO)
CREATE TABLE institution_reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    institution_id INTEGER REFERENCES institutions(id),
    reviewer_id UUID REFERENCES users(id),
    cared_person_id UUID REFERENCES cared_persons(id),
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    categories JSONB,
    is_recommended BOOLEAN NOT NULL,
    service_date DATE,
    service_type VARCHAR(50),
    is_verified BOOLEAN DEFAULT false,
    is_public BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dispositivos IoT
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    model VARCHAR(100),
    manufacturer VARCHAR(100),
    firmware_version VARCHAR(50),
    config JSONB,
    location VARCHAR(100),
    battery_level INTEGER CHECK (battery_level >= 0 AND battery_level <= 100),
    last_maintenance TIMESTAMP,
    warranty_expiry TIMESTAMP,
    accessibility_features JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Eventos
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL, -- low, medium, high, critical
    device_id VARCHAR(100),
    cared_person_id UUID REFERENCES cared_persons(id),
    location_data JSONB,
    sensor_data JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT false,
    notes TEXT
);

-- Alertas
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID REFERENCES events(id),
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- pending, sent, acknowledged, resolved
    recipients JSONB,
    sent_at TIMESTAMP,
    acknowledged_at TIMESTAMP,
    resolved_at TIMESTAMP,
    escalation_level INTEGER DEFAULT 1
);

-- Facturación
CREATE TABLE billing_records (
    id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    billing_type VARCHAR(50) NOT NULL, -- subscription, service, usage, etc.
    description TEXT,
    amount INTEGER NOT NULL, -- Monto en centavos
    currency VARCHAR(3) DEFAULT 'ARS',
    tax_amount INTEGER DEFAULT 0,
    total_amount INTEGER NOT NULL,
    billing_date DATE NOT NULL,
    due_date DATE,
    paid_date DATE,
    status VARCHAR(20) DEFAULT 'pending', -- pending, paid, overdue, cancelled
    payment_method VARCHAR(50),
    transaction_id VARCHAR(100),
    user_id UUID REFERENCES users(id),
    institution_id INTEGER REFERENCES institutions(id),
    service_subscription_id INTEGER REFERENCES service_subscriptions(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2.4 Reglas de Negocio Implementadas

#### Validación de Capacidad Legal
```python
class LegalCapacityValidator:
    @staticmethod
    async def validate_user_capacity(user_id: str, care_type: str) -> bool:
        """
        Valida la capacidad legal del usuario para contratar paquetes
        """
        if care_type == "self_care":
            # Verificar edad y capacidad legal
            return await LegalCapacityValidator._check_self_care_capacity(user_id)
        elif care_type == "delegated":
            # Verificar que tenga representante legal
            return await LegalCapacityValidator._check_delegated_care_representation(user_id)
        return False
    
    @staticmethod
    async def _check_self_care_capacity(user_id: str) -> bool:
        # Implementar lógica de validación de capacidad legal
        pass
    
    @staticmethod
    async def _check_delegated_care_representation(user_id: str) -> bool:
        # Verificar que tenga representante legal vinculado
        pass
```

#### Sistema de Paquetes
```python
class PackageManager:
    @staticmethod
    async def can_user_subscribe_to_package(user_id: str, package_id: str) -> bool:
        """
        Verifica si un usuario puede suscribirse a un paquete
        """
        # Verificar capacidad legal
        user = await UserService.get_user(user_id)
        if not await LegalCapacityValidator.validate_user_capacity(user_id, user.care_type):
            return False
        
        # Verificar límites del paquete
        package = await PackageService.get_package(package_id)
        current_usage = await PackageManager._get_current_usage(user_id)
        
        if current_usage.users >= package.max_users:
            return False
        
        if current_usage.devices >= package.max_devices:
            return False
        
        return True
    
    @staticmethod
    async def _get_current_usage(user_id: str) -> dict:
        # Obtener uso actual del usuario
        pass
```

#### Sistema de Referidos
```python
class ReferralManager:
    @staticmethod
    async def process_referral_conversion(referral_id: str) -> bool:
        """
        Procesa la conversión de un referido
        """
        referral = await ReferralService.get_referral(referral_id)
        
        # Calcular comisión
        commission_amount = await ReferralService.calculate_commission_amount(
            subscription_amount=referral.subscription_amount,
            referrer_type=referral.referrer_type,
            commission_type="first_month"
        )
        
        # Crear comisión
        commission = await ReferralService.create_commission(
            referral_id=referral_id,
            recipient_type=referral.referrer_type,
            recipient_id=referral.referrer_id,
            amount=commission_amount,
            commission_type="first_month"
        )
        
        # Actualizar estado del referido
        await ReferralService.update_referral_status(
            referral_id=referral_id,
            status="converted",
            commission_amount=commission_amount
        )
        
        return True
```

### 2.5 API Endpoints Principales

#### Paquetes (NUEVA ENTIDAD CENTRAL)
```python
# GET /api/v1/packages/ - Listar paquetes disponibles
# GET /api/v1/packages/{package_id} - Detalle de paquete
# POST /api/v1/packages/ - Crear paquete (Admin)
# PUT /api/v1/packages/{package_id} - Actualizar paquete
# DELETE /api/v1/packages/{package_id} - Eliminar paquete

# GET /api/v1/user-packages/ - Paquetes contratados por usuario
# POST /api/v1/user-packages/ - Contratar paquete
# PUT /api/v1/user-packages/{subscription_id} - Actualizar suscripción
# PATCH /api/v1/user-packages/{subscription_id}/cancel - Cancelar suscripción
```

#### Referidos (IMPLEMENTADO)
```python
# POST /api/v1/referrals/generate-code - Generar código de referido
# POST /api/v1/referrals/validate - Validar código de referido
# GET /api/v1/referrals/my-referrals - Referidos del usuario
# GET /api/v1/referrals/stats - Estadísticas de referidos
# PATCH /api/v1/referrals/{referral_id}/update-status - Actualizar estado

# GET /api/v1/referral-commissions/my-commissions - Comisiones del usuario
# PATCH /api/v1/referral-commissions/{commission_id}/mark-paid - Marcar como pagada
# GET /api/v1/referral-commissions/stats - Estadísticas de comisiones
```

#### Scoring y Reviews (IMPLEMENTADO)
```python
# POST /api/v1/caregiver-reviews/ - Crear review de cuidador
# GET /api/v1/caregiver-reviews/caregiver/{caregiver_id} - Reviews de cuidador
# GET /api/v1/caregiver-scores/{caregiver_id} - Score de cuidador

# POST /api/v1/institution-reviews/ - Crear review de institución
# GET /api/v1/institution-reviews/institution/{institution_id} - Reviews de institución
# GET /api/v1/institution-scores/{institution_id} - Score de institución
```

#### Validaciones de Capacidad Legal
```python
# POST /api/v1/legal-capacity/verify - Verificar capacidad legal
# POST /api/v1/legal-capacity/validate-representative - Validar representante legal
# GET /api/v1/legal-capacity/representative/{cared_person_id} - Obtener representante
```

### 2.6 Seguridad y Autenticación

#### JWT Authentication
```python
from fastapi_jwt_auth import AuthJWT

@AuthJWT.load_config
def get_config():
    return Settings()

@app.post('/login')
def login(user_credentials: UserLogin, Authorize: AuthJWT = Depends()):
    # Validar credenciales
    user = authenticate_user(user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generar tokens
    access_token = Authorize.create_access_token(subject=user.id)
    refresh_token = Authorize.create_refresh_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
```

#### Role-Based Access Control
```python
def require_role(required_role: str):
    def role_checker(Authorize: AuthJWT = Depends()):
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        user_roles = get_user_roles(user_id)
        
        if required_role not in user_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        return user_id
    return role_checker

@app.get("/admin/dashboard")
def admin_dashboard(user_id: str = Depends(require_role("admin"))):
    # Solo administradores pueden acceder
    return get_admin_dashboard_data()
```

### 2.7 Monitoreo y Logging

#### Health Checks
```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "2.0.0"
    }

@app.get("/health/db")
def database_health():
    try:
        # Verificar conexión a base de datos
        db.execute("SELECT 1")
        return {"database": "healthy"}
    except Exception as e:
        return {"database": "unhealthy", "error": str(e)}
```

#### Logging
```python
import logging
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logging.info(
        f"{request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Time: {process_time:.3f}s"
    )
    
    return response
```

---

## 3. Consideraciones de Escalabilidad

### 3.1 Base de Datos
- **Particionamiento**: Eventos y alertas por fecha
- **Índices**: Optimizados para consultas frecuentes
- **Replicación**: Read replicas para consultas de solo lectura
- **Backup**: Automático diario con retención de 30 días

### 3.2 Caché
- **Redis**: Para sesiones y datos frecuentemente accedidos
- **TTL**: Configurado según tipo de dato
- **Invalidación**: Automática cuando se actualizan datos

### 3.3 Microservicios
- **Comunicación**: HTTP/REST entre servicios
- **Service Discovery**: Registro automático de servicios
- **Load Balancing**: Distribución de carga automática
- **Circuit Breaker**: Manejo de fallos en servicios externos

---

*Arquitectura Técnica - CUIOT v2.0*
*Última actualización: [Fecha]*
*Próxima revisión: [Fecha]* 