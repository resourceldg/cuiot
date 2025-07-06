import os
# Configurar entorno de testing
os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = "postgresql://viejos_trapos_user:viejos_trapos_pass@postgres_test:5432/viejos_trapos_test_db"

import pytest
import pytest_asyncio
from httpx import AsyncClient
from main import app
from app.core.database import get_db, engine, SessionLocal
from app.models.base import Base
from sqlalchemy import text
from app.models.referral_type import ReferralType
from app.models.status_type import StatusType
from app.models.care_type import CareType
from app.models.device_type import DeviceType
from app.models.alert_type import AlertType
from app.models.event_type import EventType
from app.models.reminder_type import ReminderType
from app.models.service_type import ServiceType
from app.models.caregiver_assignment_type import CaregiverAssignmentType
from app.models.shift_observation_type import ShiftObservationType
from app.models.report_type import ReportType
from app.models.relationship_type import RelationshipType

# Configurar base de datos de testing usando migraciones de Alembic
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Configura la base de datos de testing usando migraciones de Alembic"""
    import subprocess
    import sys
    
    print("🔧 Configurando base de datos de testing con Alembic...")
    
    # Ejecutar migraciones de Alembic en la base de datos de testing
    try:
        result = subprocess.run([
            sys.executable, "-m", "alembic", "upgrade", "head"
        ], capture_output=True, text=True, cwd=".", env={
            **os.environ,
            "ENVIRONMENT": "test"
        })
        
        if result.returncode != 0:
            print(f"❌ Error en migración: {result.stderr}")
            raise Exception("Falló la migración de Alembic")
        
        print("✅ Base de datos de testing configurada correctamente")
    except Exception as e:
        print(f"❌ Error configurando base de datos: {e}")
        raise
    
    # Inicializar catálogos normalizados una sola vez para toda la sesión de tests
    print("📚 Inicializando catálogos normalizados...")
    from app.models.alert_type import AlertType
    from app.models.care_type import CareType
    from app.models.status_type import StatusType
    from app.models.reminder_type import ReminderType
    from app.models.event_type import EventType
    from app.models.device_type import DeviceType
    
    db = SessionLocal()
    try:
        # Alert types
        alert_types = [
            {"name": "no_movement", "description": "No movement detected"},
            {"name": "audit_test", "description": "Audit test alert"},
        ]
        for at in alert_types:
            if not db.query(AlertType).filter_by(name=at["name"]).first():
                db.add(AlertType(**at))
        # Care types
        care_types = [
            {"name": "self_care", "description": "Self care"},
            {"name": "delegated", "description": "Delegated care"},
        ]
        for ct in care_types:
            if not db.query(CareType).filter_by(name=ct["name"]).first():
                db.add(CareType(**ct))
        # Status types
        status_types = [
            {"name": "draft", "description": "Draft status", "category": "general"},
            {"name": "active", "description": "Active status", "category": "general"},
            {"name": "inactive", "description": "Inactive status", "category": "general"},
            {"name": "pending", "description": "Pending status", "category": "general"},
            {"name": "cancelled", "description": "Cancelled status", "category": "general"},
            {"name": "suspended", "description": "Suspended status", "category": "general"},
            {"name": "expired", "description": "Expired status", "category": "general"},
            {"name": "completed", "description": "Completed status", "category": "general"},
            {"name": "reviewed", "description": "Reviewed status", "category": "general"},
            {"name": "archived", "description": "Archived status", "category": "general"},
            {"name": "verified", "description": "Verified status", "category": "general"},
            {"name": "unverified", "description": "Unverified status", "category": "general"}
        ]
        for st in status_types:
            if not db.query(StatusType).filter_by(name=st["name"]).first():
                db.add(StatusType(**st))
        # Reminder types
        reminder_types = [
            {"name": "medication", "description": "Medication reminder"},
            {"name": "appointment", "description": "Appointment reminder"},
        ]
        for rt in reminder_types:
            if not db.query(ReminderType).filter_by(name=rt["name"]).first():
                db.add(ReminderType(**rt))
        # Event types
        event_types = [
            {"name": "fall", "description": "Fall event"},
            {"name": "emergency", "description": "Emergency event"},
        ]
        for et in event_types:
            if not db.query(EventType).filter_by(name=et["name"]).first():
                db.add(EventType(**et))
        # Device types
        device_types = [
            {"name": "sensor", "description": "Sensor device"},
            {"name": "tracker", "description": "Tracker device"},
            {"name": "camera", "description": "Camera device"},
            {"name": "smartphone", "description": "Smartphone device"},
            {"name": "tablet", "description": "Tablet device"},
            {"name": "wearable", "description": "Wearable device"},
            {"name": "medical_device", "description": "Medical device"},
            {"name": "environmental_sensor", "description": "Environmental sensor"},
            {"name": "door_sensor", "description": "Door sensor"},
            {"name": "motion_sensor", "description": "Motion sensor"},
            {"name": "temperature_sensor", "description": "Temperature sensor"},
            {"name": "heart_rate_monitor", "description": "Heart rate monitor"},
            {"name": "fall_detector", "description": "Fall detector"},
            {"name": "gps_tracker", "description": "GPS tracker"}
        ]
        for dt in device_types:
            if not db.query(DeviceType).filter_by(name=dt["name"]).first():
                db.add(DeviceType(**dt))
        db.commit()
        print("✅ Catálogos normalizados inicializados correctamente")
    except Exception as e:
        print(f"❌ Error inicializando catálogos: {e}")
        db.rollback()
        raise
    finally:
        db.close()
    
    yield
    
    # Cleanup: limpiar datos pero mantener estructura
    print("🧹 Limpiando datos de testing...")
    try:
        db = SessionLocal()
        db.execute(text("SET session_replication_role = replica;"))
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE;"))
        db.execute(text("SET session_replication_role = DEFAULT;"))
        db.commit()
    except Exception as e:
        print(f"⚠️  Warning: No se pudo limpiar la base de datos: {e}")

@pytest.fixture
def db_session():
    """Fixture para obtener una sesión de base de datos y cerrarla correctamente."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
async def clean_db():
    """Clean database before each test using PostgreSQL"""
    db = next(get_db())
    try:
        db.execute(text("SET session_replication_role = replica;"))
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE;"))
        db.execute(text("SET session_replication_role = DEFAULT;"))
        db.commit()
    except Exception as e:
        print(f"Warning: Could not clean database: {e}")
        db.rollback()
    finally:
        db.close()
    
    # Repoblar catálogos normalizados después de limpiar
    from app.models.alert_type import AlertType
    from app.models.care_type import CareType
    from app.models.status_type import StatusType
    from app.models.reminder_type import ReminderType
    from app.models.event_type import EventType
    from app.models.device_type import DeviceType
    
    db = SessionLocal()
    try:
        # Alert types
        alert_types = [
            {"name": "no_movement", "description": "No movement detected"},
            {"name": "audit_test", "description": "Audit test alert"},
        ]
        for at in alert_types:
            if not db.query(AlertType).filter_by(name=at["name"]).first():
                db.add(AlertType(**at))
        # Care types
        care_types = [
            {"name": "self_care", "description": "Self care"},
            {"name": "delegated", "description": "Delegated care"},
        ]
        for ct in care_types:
            if not db.query(CareType).filter_by(name=ct["name"]).first():
                db.add(CareType(**ct))
        # Status types
        status_types = [
            {"name": "draft", "description": "Draft status", "category": "general"},
            {"name": "active", "description": "Active status", "category": "general"},
            {"name": "inactive", "description": "Inactive status", "category": "general"},
            {"name": "pending", "description": "Pending status", "category": "general"},
            {"name": "cancelled", "description": "Cancelled status", "category": "general"},
            {"name": "suspended", "description": "Suspended status", "category": "general"},
            {"name": "expired", "description": "Expired status", "category": "general"},
            {"name": "completed", "description": "Completed status", "category": "general"},
            {"name": "reviewed", "description": "Reviewed status", "category": "general"},
            {"name": "archived", "description": "Archived status", "category": "general"},
            {"name": "verified", "description": "Verified status", "category": "general"},
            {"name": "unverified", "description": "Unverified status", "category": "general"}
        ]
        for st in status_types:
            if not db.query(StatusType).filter_by(name=st["name"]).first():
                db.add(StatusType(**st))
        # Reminder types
        reminder_types = [
            {"name": "medication", "description": "Medication reminder"},
            {"name": "appointment", "description": "Appointment reminder"},
        ]
        for rt in reminder_types:
            if not db.query(ReminderType).filter_by(name=rt["name"]).first():
                db.add(ReminderType(**rt))
        # Event types
        event_types = [
            {"name": "fall", "description": "Fall event"},
            {"name": "emergency", "description": "Emergency event"},
        ]
        for et in event_types:
            if not db.query(EventType).filter_by(name=et["name"]).first():
                db.add(EventType(**et))
        # Device types
        device_types = [
            {"name": "sensor", "description": "Sensor device"},
            {"name": "tracker", "description": "Tracker device"},
            {"name": "camera", "description": "Camera device"},
            {"name": "smartphone", "description": "Smartphone device"},
            {"name": "tablet", "description": "Tablet device"},
            {"name": "wearable", "description": "Wearable device"},
            {"name": "medical_device", "description": "Medical device"},
            {"name": "environmental_sensor", "description": "Environmental sensor"},
            {"name": "door_sensor", "description": "Door sensor"},
            {"name": "motion_sensor", "description": "Motion sensor"},
            {"name": "temperature_sensor", "description": "Temperature sensor"},
            {"name": "heart_rate_monitor", "description": "Heart rate monitor"},
            {"name": "fall_detector", "description": "Fall detector"},
            {"name": "gps_tracker", "description": "GPS tracker"}
        ]
        for dt in device_types:
            if not db.query(DeviceType).filter_by(name=dt["name"]).first():
                db.add(DeviceType(**dt))
        db.commit()
    except Exception as e:
        print(f"Warning: Could not repopulate catalogs: {e}")
        db.rollback()
    finally:
        db.close()
    
    yield

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

@pytest_asyncio.fixture
async def auth_headers(async_client, db_session):
    """Create a test user and return authentication headers"""
    # Registrar usuario primero
    register_response = await async_client.post("/api/v1/auth/register", json={
        "email": "testuser@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",
        "phone": "123456789"
    })
    
    # Verificar que el registro fue exitoso
    if register_response.status_code != 201:
        print(f"Warning: User registration failed with status {register_response.status_code}")
        print(f"Response: {register_response.text}")
    
    # Create basic role and assign it
    db = db_session
    from app.models.user import User
    from app.models.role import Role
    from app.models.user_role import UserRole
    import json
    from datetime import datetime
    
    # Find the user
    db_user = db.query(User).filter_by(email="testuser@example.com").first()
    
    # Create basic role if it doesn't exist
    basic_role = db.query(Role).filter_by(name="basic").first()
    if not basic_role:
        basic_role = Role(
            name="basic",
            description="Basic user role",
            permissions=json.dumps({
                "users": {"read": True},
                "profile": {"read": True, "write": True},
                "devices": {"read": True},
                "alerts": {"read": True}
            }),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(basic_role)
        db.commit()
        db.refresh(basic_role)
    
    # Assign role to user
    user_role = UserRole(
        user_id=db_user.id,
        role_id=basic_role.id,
        created_at=datetime.now()
    )
    db.add(user_role)
    db.commit()
    
    # Login para obtener token
    login_response = await async_client.post("/api/v1/auth/login", json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    
    # Verificar que el login fue exitoso
    if login_response.status_code != 200:
        print(f"Warning: User login failed with status {login_response.status_code}")
        print(f"Response: {login_response.text}")
        # Si falla, intentar con credenciales alternativas
        login_response = await async_client.post("/api/v1/auth/login", json={
            "email": "testuser@example.com",
            "password": "testpassword"
        })
    
    try:
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    except (KeyError, ValueError) as e:
        print(f"Error extracting token from response: {e}")
        print(f"Response status: {login_response.status_code}")
        print(f"Response body: {login_response.text}")
        # Retornar headers vacíos si falla
        return {"Authorization": "Bearer invalid_token"}

@pytest_asyncio.fixture
async def admin_auth(async_client, db_session):
    """Create an admin user and return authentication headers"""
    # Registrar usuario admin primero
    register_response = await async_client.post("/api/v1/auth/register", json={
        "email": "admin@example.com",
        "password": "adminpassword",
        "first_name": "Admin",
        "last_name": "User",
        "phone": "987654321",
        "username": "adminuser"
    })
    
    # Verificar que el registro fue exitoso
    if register_response.status_code != 201:
        print(f"Warning: Admin registration failed with status {register_response.status_code}")
        print(f"Response: {register_response.text}")
    
    # Create admin role and assign it
    db = db_session
    from app.models.user import User
    from app.models.role import Role
    from app.models.user_role import UserRole
    import json
    from datetime import datetime
    
    # Find the admin user
    db_user = db.query(User).filter_by(email="admin@example.com").first()
    
    # Crear rol admin si no existe
    admin_role = db.query(Role).filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(
            name="admin",
            description="Administrator role",
            permissions=json.dumps({
                "users": {"read": True, "write": True, "delete": True},
                "profile": {"read": True, "write": True},
                "devices": {"read": True, "write": True, "delete": True},
                "alerts": {"read": True, "write": True},
                "packages": {"read": True, "write": True, "delete": True},
                "cared_persons": {"read": True, "write": True, "delete": True},
                "institutions": {"read": True, "write": True, "delete": True},
                "protocols": {"read": True, "write": True, "delete": True},
                "reports": {"read": True, "write": True},
                "system": {"read": True, "write": True, "delete": True}
            }),
            is_system=False,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)
    
    # Asignar rol admin al usuario
    user_role = UserRole(
        user_id=db_user.id,
        role_id=admin_role.id,
        is_active=True,
        created_at=datetime.now()
    )
    db.add(user_role)
    db.commit()
    
    # Login para obtener token
    login_response = await async_client.post("/api/v1/auth/login", json={
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    
    # Verificar que el login fue exitoso
    if login_response.status_code != 200:
        print(f"Warning: Admin login failed with status {login_response.status_code}")
        print(f"Response: {login_response.text}")
    
    try:
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    except (KeyError, ValueError) as e:
        print(f"Error extracting admin token from response: {e}")
        print(f"Response status: {login_response.status_code}")
        print(f"Response body: {login_response.text}")
        # Retornar headers vacíos si falla
        return {"Authorization": "Bearer invalid_token"}

@pytest.fixture(scope="function", autouse=True)
def clean_database(db_session):
    """
    Fixture que limpia completamente la base de datos antes de cada test.
    Usa un enfoque más robusto para evitar errores de transacción.
    """
    try:
        db_session.rollback()
        db_session.execute(text("SET session_replication_role = replica;"))
        db_session.commit()
        tables_to_clean = [
            "audit_logs",
            "medication_logs", 
            "location_tracking",
            "user_package_add_ons",
            "user_packages",
            "caregiver_assignments",
            "cared_person_institutions",
            "institution_reviews",
            "caregiver_reviews",
            "caregiver_scores",
            "institution_scores",
            "activity_participations",
            "shift_observations",
            "restraint_protocols",
            "medical_referrals",
            "referrals",
            "reminders",
            "alerts",
            "events",
            "devices",
            "diagnoses",
            "medication_schedules",
            "medications",
            "allergies",
            "medical_conditions",
            "medical_profiles",
            "geofences",
            "device_configs",
            "debug_events",
            "billing_records",
            "packages",
            "cared_persons",
            "caregivers",
            "institutions",
            "users",
            "user_roles",
            "roles",
            "enumeration_values",
            "enumeration_types",
            "referral_types",
            "status_types",
            "care_types",
            "device_types",
            "alert_types",
            "event_types",
            "reminder_types",
            "service_types",
            "caregiver_assignment_types",
            "shift_observation_types",
            "report_types",
            "relationship_types",
            "difficulty_levels"
        ]
        for table in tables_to_clean:
            try:
                result = db_session.execute(text(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = '{table}'
                    );
                """))
                table_exists = result.scalar()
                if table_exists:
                    db_session.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
                    print(f"✅ Cleaned table: {table}")
                else:
                    print(f"⚠️  Table does not exist: {table}")
            except Exception as e:
                print(f"⚠️  Warning: Could not clean table {table}: {e}")
                continue
        db_session.execute(text("SET session_replication_role = DEFAULT;"))
        db_session.commit()
        print("✅ Database cleaned successfully")
    except Exception as e:
        print(f"❌ Error in database cleanup: {e}")
        try:
            db_session.rollback()
            db_session.execute(text("SET session_replication_role = DEFAULT;"))
            db_session.commit()
        except Exception as rollback_error:
            print(f"❌ Error during rollback: {rollback_error}")
            db_session.rollback()
    return db_session

@pytest.fixture(scope="function")
def normalized_catalogs(clean_database):
    """
    Fixture que inicializa todos los catálogos normalizados principales.
    Depende de clean_database para asegurar que la base esté limpia.
    """
    db = clean_database
    
    # Definir los catálogos principales con sus valores
    catalogs = {
        "referral_types": [
            {"name": "family", "description": "Referral from family member"},
            {"name": "professional", "description": "Referral from healthcare professional"},
            {"name": "institution", "description": "Referral from institution"},
            {"name": "self", "description": "Self-referral"}
        ],
        "status_types": [
            {"name": "draft", "description": "Draft status", "category": "general"},
            {"name": "active", "description": "Active status", "category": "general"},
            {"name": "inactive", "description": "Inactive status", "category": "general"},
            {"name": "pending", "description": "Pending status", "category": "general"},
            {"name": "cancelled", "description": "Cancelled status", "category": "general"},
            {"name": "suspended", "description": "Suspended status", "category": "general"},
            {"name": "expired", "description": "Expired status", "category": "general"},
            {"name": "completed", "description": "Completed status", "category": "general"},
            {"name": "reviewed", "description": "Reviewed status", "category": "general"},
            {"name": "archived", "description": "Archived status", "category": "general"},
            {"name": "verified", "description": "Verified status", "category": "general"},
            {"name": "unverified", "description": "Unverified status", "category": "general"}
        ],
        "care_types": [
            {"name": "autocuidado", "description": "Self-care"},
            {"name": "delegated", "description": "Delegated care"},
            {"name": "assisted", "description": "Assisted care"},
            {"name": "supervised", "description": "Supervised care"}
        ],
        "device_types": [
            {"name": "sensor", "description": "Sensor device"},
            {"name": "monitor", "description": "Monitoring device"},
            {"name": "alert", "description": "Alert device"},
            {"name": "tracker", "description": "Tracking device"}
        ],
        "alert_types": [
            {"name": "medical", "description": "Medical alert"},
            {"name": "safety", "description": "Safety alert"},
            {"name": "fall", "description": "Fall alert"},
            {"name": "medication", "description": "Medication alert"}
        ],
        "event_types": [
            {"name": "incident", "description": "Incident event"},
            {"name": "medication", "description": "Medication event"},
            {"name": "visit", "description": "Visit event"},
            {"name": "emergency", "description": "Emergency event"}
        ],
        "reminder_types": [
            {"name": "medication", "description": "Medication reminder"},
            {"name": "appointment", "description": "Appointment reminder"},
            {"name": "activity", "description": "Activity reminder"},
            {"name": "checkup", "description": "Checkup reminder"}
        ],
        "service_types": [
            {"name": "basic", "description": "Basic service"},
            {"name": "premium", "description": "Premium service"},
            {"name": "specialized", "description": "Specialized service"},
            {"name": "emergency", "description": "Emergency service"}
        ],
        "caregiver_assignment_types": [
            {"name": "primary", "description": "Primary caregiver"},
            {"name": "secondary", "description": "Secondary caregiver"},
            {"name": "temporary", "description": "Temporary caregiver"},
            {"name": "specialist", "description": "Specialist caregiver"}
        ],
        "shift_observation_types": [
            {"name": "morning", "description": "Morning shift observation"},
            {"name": "afternoon", "description": "Afternoon shift observation"},
            {"name": "night", "description": "Night shift observation"},
            {"name": "24h", "description": "24-hour shift observation"}
        ],
        "report_types": [
            {"name": "daily", "description": "Daily report"},
            {"name": "weekly", "description": "Weekly report"},
            {"name": "monthly", "description": "Monthly report"},
            {"name": "incident", "description": "Incident report"}
        ],
        "relationship_types": [
            {"name": "son", "description": "Son"},
            {"name": "daughter", "description": "Daughter"},
            {"name": "spouse", "description": "Spouse"},
            {"name": "parent", "description": "Parent"},
            {"name": "sibling", "description": "Sibling"},
            {"name": "friend", "description": "Friend"},
            {"name": "neighbor", "description": "Neighbor"},
            {"name": "other", "description": "Other"}
        ]
    }
    
    # Inicializar cada catálogo
    catalog_ids = {}
    
    # Mapeo directo de nombres de catálogos a clases de modelo
    catalog_to_model = {
        "referral_types": ReferralType,
        "status_types": StatusType,
        "care_types": CareType,
        "device_types": DeviceType,
        "alert_types": AlertType,
        "event_types": EventType,
        "reminder_types": ReminderType,
        "service_types": ServiceType,
        "caregiver_assignment_types": CaregiverAssignmentType,
        "shift_observation_types": ShiftObservationType,
        "report_types": ReportType,
        "relationship_types": RelationshipType,
    }
    
    for catalog_name, items in catalogs.items():
        model_class = catalog_to_model[catalog_name]
        
        for item in items:
            existing = db.query(model_class).filter_by(name=item["name"]).first()
            if not existing:
                new_item = model_class(**item)
                db.add(new_item)
        
        db.commit()
        
        # Obtener el primer ID para usar en tests
        first_item = db.query(model_class).first()
        if first_item:
            catalog_ids[f"{catalog_name.replace('_types', '_type_id')}"] = first_item.id
    
    return catalog_ids 

@pytest.fixture(scope="function")
def clean_users_database(db_session):
    """
    Fixture específico para tests de usuarios que limpia completamente
    la tabla users y evita duplicados de email.
    """
    try:
        # Rollback de cualquier transacción pendiente
        db_session.rollback()
        
        # Limpiar específicamente la tabla users primero
        try:
            db_session.execute(text("TRUNCATE TABLE users CASCADE"))
            print("✅ Cleaned users table")
        except Exception as e:
            print(f"⚠️  Could not clean users table: {e}")
        
        # También limpiar tablas relacionadas con usuarios
        user_related_tables = [
            "user_packages",
            "user_package_add_ons",
            "caregiver_assignments",
            "cared_persons"
        ]
        
        for table in user_related_tables:
            try:
                db_session.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
                print(f"✅ Cleaned table: {table}")
            except Exception as e:
                if "does not exist" in str(e):
                    print(f"⚠️  Table does not exist: {table}")
                else:
                    print(f"❌ Error cleaning table {table}: {e}")
        
        db_session.commit()
        print("✅ Users database cleaned successfully")
        
    except Exception as e:
        print(f"❌ Error in users database cleanup: {e}")
        db_session.rollback()
        raise 