from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class DebugEvent(Base):
    """
    Modelo para eventos de debug y pruebas.
    
    Reglas de negocio implementadas:
    - Simulación de eventos sin dispositivos IoT
    - Pruebas de protocolos de emergencia
    - Validación de alertas y notificaciones
    - Datos de prueba para desarrollo frontend
    """
    __tablename__ = "debug_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False)
    event_type = Column(String(50), nullable=False, index=True)  # fall, medical, wandering, etc.
    event_subtype = Column(String(50))  # subtipo específico del evento
    severity_level = Column(String(20), default="medium")  # low, medium, high, critical
    description = Column(Text)
    event_data = Column(JSONB, default=dict)  # datos específicos del evento
    location_data = Column(JSONB, default=dict)  # datos de ubicación si aplica
    sensor_data = Column(JSONB, default=dict)  # datos simulados de sensores
    is_simulated = Column(Boolean, default=True)  # siempre es simulado
    should_trigger_alert = Column(Boolean, default=True)  # si debe disparar alerta
    should_trigger_protocol = Column(Boolean, default=True)  # si debe disparar protocolo
    test_scenario = Column(String(100))  # escenario de prueba
    debug_notes = Column(Text)  # notas para debug
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    cared_person = relationship("CaredPerson")
    
    def __repr__(self):
        return f"<DebugEvent(id={self.id}, event_type='{self.event_type}', cared_person_id={self.cared_person_id})>"
    
    def get_event_data(self) -> dict:
        """
        Obtiene los datos específicos del evento.
        
        Returns:
            dict: Datos del evento
        """
        return self.event_data or {}
    
    def set_event_data(self, data: dict):
        """
        Establece los datos específicos del evento.
        
        Args:
            data: Diccionario con datos del evento
        """
        self.event_data = data
    
    def get_location_data(self) -> dict:
        """
        Obtiene los datos de ubicación del evento.
        
        Returns:
            dict: Datos de ubicación
        """
        return self.location_data or {}
    
    def set_location_data(self, latitude: float, longitude: float, accuracy: float = 5.0):
        """
        Establece los datos de ubicación del evento.
        
        Args:
            latitude: Latitud
            longitude: Longitud
            accuracy: Precisión en metros
        """
        self.location_data = {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": accuracy,
            "timestamp": self.created_at.isoformat() if self.created_at else None
        }
    
    def get_sensor_data(self) -> dict:
        """
        Obtiene los datos simulados de sensores.
        
        Returns:
            dict: Datos de sensores
        """
        return self.sensor_data or {}
    
    def set_sensor_data(self, sensor_type: str, value: any, unit: str = None):
        """
        Establece datos simulados de sensores.
        
        Args:
            sensor_type: Tipo de sensor
            value: Valor del sensor
            unit: Unidad de medida
        """
        if not self.sensor_data:
            self.sensor_data = {"sensors": []}
        
        sensor = {
            "type": sensor_type,
            "value": value,
            "unit": unit,
            "timestamp": self.created_at.isoformat() if self.created_at else None
        }
        
        self.sensor_data["sensors"].append(sensor)
    
    def to_alert_data(self) -> dict:
        """
        Convierte el evento de debug a formato de alerta.
        
        Returns:
            dict: Datos en formato de alerta
        """
        return {
            "event_type": self.event_type,
            "event_subtype": self.event_subtype,
            "severity_level": self.severity_level,
            "description": self.description,
            "event_data": self.get_event_data(),
            "location_data": self.get_location_data(),
            "sensor_data": self.get_sensor_data(),
            "is_debug": True,
            "debug_event_id": str(self.id)
        }
    
    def to_protocol_data(self) -> dict:
        """
        Convierte el evento de debug a formato de protocolo.
        
        Returns:
            dict: Datos en formato de protocolo
        """
        return {
            "crisis_type": self.event_type,
            "severity_level": self.severity_level,
            "event_data": self.get_event_data(),
            "location_data": self.get_location_data(),
            "sensor_data": self.get_sensor_data(),
            "is_debug": True,
            "debug_event_id": str(self.id)
        }
    
    @classmethod
    def get_event_types(cls) -> list:
        """
        Retorna los tipos de evento disponibles para debug.
        
        Returns:
            list: Lista de tipos de evento
        """
        return [
            {"value": "fall", "label": "Caída", "description": "Simulación de caída"},
            {"value": "medical", "label": "Médico", "description": "Emergencia médica"},
            {"value": "wandering", "label": "Deambulación", "description": "Persona perdida"},
            {"value": "abuse", "label": "Abuso", "description": "Sospecha de abuso"},
            {"value": "fire", "label": "Incendio", "description": "Emergencia de fuego"},
            {"value": "gas", "label": "Gas", "description": "Fuga de gas"},
            {"value": "intrusion", "label": "Intrusión", "description": "Intrusión detectada"},
            {"value": "medical_alert", "label": "Alerta Médica", "description": "Alerta médica"},
            {"value": "medication", "label": "Medicación", "description": "Problema con medicación"},
            {"value": "communication", "label": "Comunicación", "description": "Problema de comunicación"},
            {"value": "environmental", "label": "Ambiental", "description": "Problema ambiental"},
            {"value": "test", "label": "Prueba", "description": "Evento de prueba general"}
        ]
    
    @classmethod
    def get_severity_levels(cls) -> list:
        """
        Retorna los niveles de severidad disponibles.
        
        Returns:
            list: Lista de niveles de severidad
        """
        return [
            {"value": "low", "label": "Baja", "description": "Evento de baja severidad"},
            {"value": "medium", "label": "Media", "description": "Evento de severidad media"},
            {"value": "high", "label": "Alta", "description": "Evento de alta severidad"},
            {"value": "critical", "label": "Crítica", "description": "Evento crítico"}
        ]
    
    @classmethod
    def create_fall_event(cls, cared_person_id: uuid.UUID, latitude: float = None, 
                         longitude: float = None, severity: str = "medium",
                         notes: str = None) -> "DebugEvent":
        """
        Crea un evento de caída para pruebas.
        
        Args:
            cared_person_id: ID de la persona bajo cuidado
            latitude: Latitud (opcional)
            longitude: Longitud (opcional)
            severity: Nivel de severidad
            notes: Notas de debug
            
        Returns:
            DebugEvent: Instancia de evento de caída
        """
        event = cls(
            cared_person_id=cared_person_id,
            event_type="fall",
            event_subtype="simulated_fall",
            severity_level=severity,
            description="Simulación de caída para pruebas",
            test_scenario="fall_detection",
            debug_notes=notes,
            event_data={
                "fall_detected": True,
                "impact_force": 0.8,
                "duration": 30,
                "location": "living_room" if latitude is None else "custom_location"
            }
        )
        
        if latitude and longitude:
            event.set_location_data(latitude, longitude)
        
        event.set_sensor_data("accelerometer", 2.5, "g")
        event.set_sensor_data("gyroscope", 180, "degrees/s")
        
        return event
    
    @classmethod
    def create_medical_event(cls, cared_person_id: uuid.UUID, medical_type: str = "general",
                           severity: str = "high", notes: str = None) -> "DebugEvent":
        """
        Crea un evento médico para pruebas.
        
        Args:
            cared_person_id: ID de la persona bajo cuidado
            medical_type: Tipo de emergencia médica
            severity: Nivel de severidad
            notes: Notas de debug
            
        Returns:
            DebugEvent: Instancia de evento médico
        """
        event = cls(
            cared_person_id=cared_person_id,
            event_type="medical",
            event_subtype=medical_type,
            severity_level=severity,
            description=f"Simulación de emergencia médica: {medical_type}",
            test_scenario="medical_emergency",
            debug_notes=notes,
            event_data={
                "medical_type": medical_type,
                "symptoms": ["dizziness", "chest_pain"],
                "duration": 120,
                "requires_immediate_attention": True
            }
        )
        
        event.set_sensor_data("heart_rate", 120, "bpm")
        event.set_sensor_data("blood_pressure", "140/90", "mmHg")
        event.set_sensor_data("temperature", 37.5, "°C")
        
        return event
    
    @classmethod
    def create_wandering_event(cls, cared_person_id: uuid.UUID, latitude: float, 
                             longitude: float, distance_from_home: float = 500.0,
                             notes: str = None) -> "DebugEvent":
        """
        Crea un evento de deambulación para pruebas.
        
        Args:
            cared_person_id: ID de la persona bajo cuidado
            latitude: Latitud actual
            longitude: Longitud actual
            distance_from_home: Distancia desde casa en metros
            notes: Notas de debug
            
        Returns:
            DebugEvent: Instancia de evento de deambulación
        """
        event = cls(
            cared_person_id=cared_person_id,
            event_type="wandering",
            event_subtype="person_left_safe_zone",
            severity_level="high",
            description="Simulación de deambulación - persona salió de zona segura",
            test_scenario="wandering_detection",
            debug_notes=notes,
            event_data={
                "distance_from_home": distance_from_home,
                "time_away": 45,
                "direction": "north",
                "speed": 1.2
            }
        )
        
        event.set_location_data(latitude, longitude)
        event.set_sensor_data("gps_accuracy", 5.0, "meters")
        event.set_sensor_data("movement_speed", 1.2, "m/s")
        
        return event
    
    @classmethod
    def get_debug_events(cls, db, cared_person_id: uuid.UUID = None, 
                        event_type: str = None, limit: int = 100) -> list:
        """
        Obtiene eventos de debug para pruebas.
        
        Args:
            db: Sesión de base de datos
            cared_person_id: ID de la persona bajo cuidado (opcional)
            event_type: Tipo de evento (opcional)
            limit: Límite de registros
            
        Returns:
            list: Lista de eventos de debug
        """
        query = db.query(cls)
        
        if cared_person_id:
            query = query.filter(cls.cared_person_id == cared_person_id)
        
        if event_type:
            query = query.filter(cls.event_type == event_type)
        
        return query.order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def get_test_scenarios(cls) -> list:
        """
        Retorna escenarios de prueba disponibles.
        
        Returns:
            list: Lista de escenarios de prueba
        """
        return [
            {"value": "fall_detection", "label": "Detección de Caída", "description": "Prueba de detección de caídas"},
            {"value": "medical_emergency", "label": "Emergencia Médica", "description": "Prueba de emergencias médicas"},
            {"value": "wandering_detection", "label": "Detección de Deambulación", "description": "Prueba de deambulación"},
            {"value": "geofence_alert", "label": "Alerta de Geofence", "description": "Prueba de alertas de geofence"},
            {"value": "protocol_activation", "label": "Activación de Protocolo", "description": "Prueba de activación de protocolos"},
            {"value": "notification_test", "label": "Prueba de Notificaciones", "description": "Prueba de sistema de notificaciones"},
            {"value": "sensor_simulation", "label": "Simulación de Sensores", "description": "Prueba de datos de sensores"},
            {"value": "location_tracking", "label": "Seguimiento de Ubicación", "description": "Prueba de seguimiento de ubicación"}
        ]
    
    def validate_business_rules(self) -> list:
        """
        Valida las reglas de negocio para este evento de debug.
        
        Returns:
            list: Lista de errores de validación (vacía si todo está bien)
        """
        errors = []
        
        # Regla: Debe ser un evento simulado
        if not self.is_simulated:
            errors.append("Los eventos de debug deben ser simulados")
        
        # Regla: Debe tener un tipo de evento válido
        valid_types = [et["value"] for et in self.get_event_types()]
        if self.event_type not in valid_types:
            errors.append("El tipo de evento debe ser válido")
        
        # Regla: Debe tener un nivel de severidad válido
        valid_severities = [sl["value"] for sl in self.get_severity_levels()]
        if self.severity_level not in valid_severities:
            errors.append("El nivel de severidad debe ser válido")
        
        # Regla: Si tiene datos de ubicación, deben ser válidos
        location_data = self.get_location_data()
        if location_data:
            lat = location_data.get("latitude")
            lng = location_data.get("longitude")
            if lat is not None and (lat < -90 or lat > 90):
                errors.append("La latitud debe estar entre -90 y 90 grados")
            if lng is not None and (lng < -180 or lng > 180):
                errors.append("La longitud debe estar entre -180 y 180 grados")
        
        return errors 