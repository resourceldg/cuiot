"""
Utilidades para debug y pruebas del sistema.
Permite simular eventos, ubicaciones y datos sin dispositivos IoT.
"""

import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import time

from app.models import (
    CaredPerson, LocationTracking, Geofence, DebugEvent,
    EmergencyProtocol, Alert, User, CaregiverAssignment
)
from app.models.device import Device
from app.models.care_type import CareType
from app.models.status_type import StatusType


class DebugUtilities:
    """
    Clase de utilidades para debug y pruebas del sistema.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_test_cared_person(self, user_id: uuid.UUID, name: str = "Test Person") -> CaredPerson:
        """
        Crea una persona bajo cuidado para pruebas.
        
        Args:
            user_id: ID del usuario
            name: Nombre de la persona
            
        Returns:
            CaredPerson: Persona creada para pruebas
        """
        # Buscar el ID del care_type "elderly"
        elderly_care_type = self.db.query(CareType).filter(CareType.name == "elderly").first()
        if not elderly_care_type:
            # Fallback: usar el primer care_type disponible
            elderly_care_type = self.db.query(CareType).first()
        
        cared_person = CaredPerson(
            user_id=user_id,
            care_type_id=elderly_care_type.id if elderly_care_type else None,
            is_self_care=False,
            is_active=True
        )
        
        # Agregar contactos de emergencia
        cared_person.add_emergency_contact(
            name="Test Emergency Contact",
            phone="+5491112345678",
            relationship="Family",
            priority=1
        )
        
        # Agregar medicamentos
        cared_person.add_medication(
            name="Test Medication",
            dosage="10mg",
            frequency="daily",
            time="09:00"
        )
        
        # Configurar necesidades de accesibilidad
        cared_person.set_accessibility_need("visual", "large_text")
        cared_person.set_accessibility_need("motor", "voice_control")
        
        self.db.add(cared_person)
        self.db.commit()
        
        return cared_person
    
    def create_test_location_data(self, cared_person_id: uuid.UUID, 
                                 locations: List[Dict[str, Any]]) -> List[LocationTracking]:
        """
        Crea datos de ubicación de prueba.
        
        Args:
            cared_person_id: ID de la persona bajo cuidado
            locations: Lista de ubicaciones con lat, lng, timestamp
            
        Returns:
            List[LocationTracking]: Lista de ubicaciones creadas
        """
        location_records = []
        
        for loc_data in locations:
            location = LocationTracking.create_simulated_location(
                cared_person_id=cared_person_id,
                latitude=loc_data["latitude"],
                longitude=loc_data["longitude"],
                speed=loc_data.get("speed"),
                heading=loc_data.get("heading")
            )
            
            if "timestamp" in loc_data:
                location.created_at = loc_data["timestamp"]
            
            self.db.add(location)
            location_records.append(location)
        
        self.db.commit()
        return location_records
    
    def create_test_geofences(self, cared_person_id: uuid.UUID) -> List[Geofence]:
        """
        Crea geofences de prueba para una persona.
        
        Args:
            cared_person_id: ID de la persona bajo cuidado
            
        Returns:
            List[Geofence]: Lista de geofences creados
        """
        geofences = []
        
        # Geofence de casa
        home_geofence = Geofence.create_home_geofence(
            cared_person_id=cared_person_id,
            latitude=-34.6037,  # Buenos Aires
            longitude=-58.3816,
            radius=50.0
        )
        self.db.add(home_geofence)
        geofences.append(home_geofence)
        
        # Geofence de peligro
        danger_geofence = Geofence.create_debug_geofence(
            cared_person_id=cared_person_id,
            name="Zona Peligrosa",
            latitude=-34.6037,
            longitude=-58.3816,
            radius=200.0,
            notes="Zona de peligro para pruebas"
        )
        self.db.add(danger_geofence)
        geofences.append(danger_geofence)
        
        self.db.commit()
        return geofences
    
    def create_test_events(self, cared_person_id: uuid.UUID, 
                          event_count: int = 5) -> List[DebugEvent]:
        """
        Crea eventos de prueba para una persona.
        
        Args:
            cared_person_id: ID de la persona bajo cuidado
            event_count: Número de eventos a crear
            
        Returns:
            List[DebugEvent]: Lista de eventos creados
        """
        events = []
        event_types = ["fall", "medical", "wandering", "abuse", "fire"]
        
        for i in range(event_count):
            event_type = event_types[i % len(event_types)]
            
            if event_type == "fall":
                event = DebugEvent.create_fall_event(
                    cared_person_id=cared_person_id,
                    severity="medium",
                    notes=f"Evento de prueba #{i+1}"
                )
            elif event_type == "medical":
                event = DebugEvent.create_medical_event(
                    cared_person_id=cared_person_id,
                    medical_type="chest_pain",
                    severity="high",
                    notes=f"Evento de prueba #{i+1}"
                )
            elif event_type == "wandering":
                event = DebugEvent.create_wandering_event(
                    cared_person_id=cared_person_id,
                    latitude=-34.6037 + (i * 0.001),
                    longitude=-58.3816 + (i * 0.001),
                    distance_from_home=100.0 + (i * 50),
                    notes=f"Evento de prueba #{i+1}"
                )
            else:
                event = DebugEvent(
                    cared_person_id=cared_person_id,
                    event_type=event_type,
                    event_subtype=f"test_{event_type}",
                    severity_level="medium",
                    description=f"Evento de prueba {event_type} #{i+1}",
                    test_scenario="general_test",
                    debug_notes=f"Evento de prueba #{i+1}"
                )
            
            # Establecer timestamp diferente para cada evento
            event.created_at = datetime.utcnow() - timedelta(hours=i)
            
            self.db.add(event)
            events.append(event)
        
        self.db.commit()
        return events
    
    def simulate_location_tracking(self, cared_person_id: uuid.UUID, 
                                  hours: int = 24) -> List[LocationTracking]:
        """
        Simula seguimiento de ubicación durante un período de tiempo.
        
        Args:
            cared_person_id: ID de la persona bajo cuidado
            hours: Número de horas a simular
            
        Returns:
            List[LocationTracking]: Lista de ubicaciones simuladas
        """
        locations = []
        base_lat, base_lng = -34.6037, -58.3816  # Buenos Aires
        
        for hour in range(hours):
            # Simular movimiento aleatorio
            lat_offset = (hour % 6 - 3) * 0.001  # Movimiento en latitud
            lng_offset = (hour % 4 - 2) * 0.001  # Movimiento en longitud
            
            location = LocationTracking.create_simulated_location(
                cared_person_id=cared_person_id,
                latitude=base_lat + lat_offset,
                longitude=base_lng + lng_offset,
                speed=1.0 + (hour % 3),  # Velocidad variable
                heading=hour * 45 % 360  # Dirección variable
            )
            
            # Establecer timestamp
            location.created_at = datetime.utcnow() - timedelta(hours=hours-hour)
            
            self.db.add(location)
            locations.append(location)
        
        self.db.commit()
        return locations
    
    def create_test_protocol(self, institution_id: Optional[uuid.UUID] = None) -> EmergencyProtocol:
        """
        Crea un protocolo de emergencia de prueba.
        
        Args:
            institution_id: ID de la institución (opcional)
            
        Returns:
            EmergencyProtocol: Protocolo creado
        """
        protocol = EmergencyProtocol(
            name="Protocolo de Prueba",
            description="Protocolo de emergencia para pruebas y debug",
            institution_id=institution_id,
            crisis_type="medical",
            severity_level="high",
            response_time=5,
            auto_activate=True,
            is_active=True
        )
        
        # Agregar condiciones de activación
        protocol.set_activation_condition("heart_rate", 120, "greater_than")
        protocol.set_activation_condition("blood_pressure", "140/90", "equals")
        
        # Agregar pasos de escalación
        protocol.add_escalation_step(
            step_number=1,
            action="call",
            contact_type="emergency_contact",
            contact_value="primary",
            delay_minutes=0,
            description="Llamar al contacto de emergencia principal"
        )
        
        protocol.add_escalation_step(
            step_number=2,
            action="sms",
            contact_type="caregiver",
            contact_value="all",
            delay_minutes=2,
            description="Enviar SMS a todos los cuidadores"
        )
        
        protocol.add_escalation_step(
            step_number=3,
            action="call",
            contact_type="emergency_services",
            contact_value="911",
            delay_minutes=5,
            description="Llamar a servicios de emergencia"
        )
        
        self.db.add(protocol)
        self.db.commit()
        
        return protocol
    
    def generate_test_data(self, user_id: uuid.UUID) -> Dict[str, Any]:
        """
        Genera un conjunto completo de datos de prueba.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Dict[str, Any]: Datos generados
        """
        # Eliminar dispositivos de prueba previos
        self.db.query(Device).delete()
        self.db.commit()
        
        # Buscar el ID del status_type "active"
        active_status = self.db.query(StatusType).filter(StatusType.name == "active").first()
        if not active_status:
            # Fallback: usar el primer status_type disponible
            active_status = self.db.query(StatusType).first()
        
        # Generar un sufijo único para los device_id
        unique_suffix = str(int(time.time()))
        
        # Crear dispositivos de prueba con device_id únicos
        for i in range(4):
            device = Device(
                device_id=f"TEST_DEVICE_{i}_{unique_suffix}",
                device_type=["sensor", "tracker", "camera", "wearable"][i],
                model=f"Test Model {i}",
                manufacturer="Test Manufacturer",
                status_type_id=active_status.id if active_status else None,
                battery_level=80 + i * 5,
                signal_strength=90 + i * 3,
                is_active=True
            )
            self.db.add(device)
        self.db.commit()
        
        # Crear persona bajo cuidado
        cared_person = self.create_test_cared_person(user_id)
        
        # Crear geofences
        geofences = self.create_test_geofences(cared_person.id)
        
        # Crear eventos de prueba
        events = self.create_test_events(cared_person.id, 10)
        
        # Simular seguimiento de ubicación
        locations = self.simulate_location_tracking(cared_person.id, 48)
        
        # Crear protocolo de prueba
        protocol = self.create_test_protocol()
        
        return {
            "cared_person": cared_person,
            "geofences": geofences,
            "events": events,
            "locations": locations,
            "protocol": protocol
        }
    
    def cleanup_test_data(self, cared_person_id: uuid.UUID):
        """
        Limpia los datos de prueba para una persona.
        
        Args:
            cared_person_id: ID de la persona bajo cuidado
        """
        # Eliminar ubicaciones
        self.db.query(LocationTracking).filter(
            LocationTracking.cared_person_id == cared_person_id
        ).delete()
        
        # Eliminar geofences
        self.db.query(Geofence).filter(
            Geofence.cared_person_id == cared_person_id
        ).delete()
        
        # Eliminar eventos de debug
        self.db.query(DebugEvent).filter(
            DebugEvent.cared_person_id == cared_person_id
        ).delete()
        
        # Eliminar persona bajo cuidado
        self.db.query(CaredPerson).filter(
            CaredPerson.id == cared_person_id
        ).delete()
        
        self.db.commit()
    
    def get_debug_summary(self, cared_person_id: uuid.UUID) -> Dict[str, Any]:
        """
        Obtiene un resumen de los datos de debug para una persona.
        
        Args:
            cared_person_id: ID de la persona bajo cuidado
            
        Returns:
            Dict[str, Any]: Resumen de datos
        """
        # Contar ubicaciones
        location_count = self.db.query(LocationTracking).filter(
            LocationTracking.cared_person_id == cared_person_id
        ).count()
        
        # Contar geofences
        geofence_count = self.db.query(Geofence).filter(
            Geofence.cared_person_id == cared_person_id
        ).count()
        
        # Contar eventos
        event_count = self.db.query(DebugEvent).filter(
            DebugEvent.cared_person_id == cared_person_id
        ).count()
        
        # Última ubicación
        last_location = self.db.query(LocationTracking).filter(
            LocationTracking.cared_person_id == cared_person_id
        ).order_by(LocationTracking.created_at.desc()).first()
        
        # Último evento
        last_event = self.db.query(DebugEvent).filter(
            DebugEvent.cared_person_id == cared_person_id
        ).order_by(DebugEvent.created_at.desc()).first()
        
        return {
            "cared_person_id": str(cared_person_id),
            "location_count": location_count,
            "geofence_count": geofence_count,
            "event_count": event_count,
            "last_location": {
                "latitude": last_location.latitude,
                "longitude": last_location.longitude,
                "timestamp": last_location.created_at.isoformat()
            } if last_location else None,
            "last_event": {
                "type": last_event.event_type,
                "severity": last_event.severity_level,
                "timestamp": last_event.created_at.isoformat()
            } if last_event else None
        }
    
    def cleanup_all_test_data(self):
        """
        Limpia todos los datos de prueba relevantes del sistema, incluyendo dispositivos.
        """
        # Eliminar en orden correcto para respetar claves foráneas
        self.db.query(LocationTracking).delete()
        self.db.query(Geofence).delete()
        self.db.query(DebugEvent).delete()
        self.db.query(CaredPerson).delete()
        self.db.query(Device).delete()
        self.db.commit()


def create_debug_data_script():
    """
    Script para crear datos de debug desde línea de comandos.
    """
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    utilities = DebugUtilities(db)
    
    try:
        # Crear usuario de prueba (asumiendo que existe)
        test_user = db.query(User).first()
        if not test_user:
            print("No se encontró ningún usuario. Creando datos de prueba con ID dummy...")
            test_user_id = uuid.uuid4()
        else:
            test_user_id = test_user.id
        
        # Generar datos de prueba
        data = utilities.generate_test_data(test_user_id)
        
        print("✅ Datos de prueba creados exitosamente:")
        print(f"  - Persona bajo cuidado: {data['cared_person'].id}")
        print(f"  - Geofences: {len(data['geofences'])}")
        print(f"  - Eventos: {len(data['events'])}")
        print(f"  - Ubicaciones: {len(data['locations'])}")
        print(f"  - Protocolo: {data['protocol'].id}")
        
        # Mostrar resumen
        summary = utilities.get_debug_summary(data['cared_person'].id)
        print("\n📊 Resumen de datos:")
        print(f"  - Total ubicaciones: {summary['location_count']}")
        print(f"  - Total geofences: {summary['geofence_count']}")
        print(f"  - Total eventos: {summary['event_count']}")
        
        if summary['last_location']:
            print(f"  - Última ubicación: {summary['last_location']['latitude']}, {summary['last_location']['longitude']}")
        
        if summary['last_event']:
            print(f"  - Último evento: {summary['last_event']['type']} ({summary['last_event']['severity']})")
        
    except Exception as e:
        print(f"❌ Error creando datos de prueba: {e}")
    finally:
        db.close()


def create_sin_rol():
    """Crea el rol especial 'sin_rol' si no existe."""
    from app.core.database import get_db
    from app.models.role import Role
    import datetime
    import json
    db = next(get_db())
    try:
        existing = db.query(Role).filter(Role.name == 'sin_rol').first()
        if existing:
            print("El rol 'sin_rol' ya existe.")
            return
        now = datetime.datetime.utcnow()
        sin_rol = Role(
            name='sin_rol',
            description='Rol especial para usuarios sin rol asignado',
            permissions=json.dumps({}),
            is_system=True,
            created_at=now,
            updated_at=now,
            is_active=True
        )
        db.add(sin_rol)
        db.commit()
        print("✅ Rol especial 'sin_rol' creado correctamente.")
    except Exception as e:
        print(f"❌ Error creando 'sin_rol': {e}")
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "create_sin_rol":
        create_sin_rol()
    create_debug_data_script() 