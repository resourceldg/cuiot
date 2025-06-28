from sqlalchemy import Column, String, Text, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Geofence(Base):
    """
    Modelo para zonas de seguridad (geofences).
    
    Reglas de negocio implementadas:
    - Zonas de seguridad configurables para personas bajo cuidado
    - Diferentes tipos de geofence (casa, trabajo, peligro, etc.)
    - Alertas automáticas al entrar/salir de zonas
    - Soporte para debug y pruebas
    """
    __tablename__ = "geofences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    geofence_type = Column(String(50), nullable=False, index=True)  # home, work, danger, safe, custom
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    radius = Column(Float, nullable=False)  # radio en metros
    is_active = Column(Boolean, default=True)
    alert_on_entry = Column(Boolean, default=True)  # alerta al entrar
    alert_on_exit = Column(Boolean, default=True)  # alerta al salir
    alert_recipients = Column(JSONB, default=dict)  # destinatarios de alertas
    schedule = Column(JSONB, default=dict)  # horario de activación
    is_debug = Column(Boolean, default=False)  # para pruebas y desarrollo
    debug_notes = Column(Text)  # notas para debug
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    cared_person = relationship("CaredPerson", back_populates="geofences")
    
    def __repr__(self):
        return f"<Geofence(id={self.id}, name='{self.name}', type='{self.geofence_type}', cared_person_id={self.cared_person_id})>"
    
    def get_alert_recipients(self) -> list:
        """
        Obtiene la lista de destinatarios de alertas.
        
        Returns:
            list: Lista de destinatarios
        """
        if not self.alert_recipients:
            return []
        
        return self.alert_recipients.get("recipients", [])
    
    def add_alert_recipient(self, recipient_type: str, recipient_id: str, 
                           notification_method: str = "all"):
        """
        Agrega un destinatario de alerta.
        
        Args:
            recipient_type: Tipo de destinatario (caregiver, family, emergency_contact, etc.)
            recipient_id: ID del destinatario
            notification_method: Método de notificación (email, sms, push, all)
        """
        if not self.alert_recipients:
            self.alert_recipients = {"recipients": []}
        
        recipient = {
            "type": recipient_type,
            "id": recipient_id,
            "notification_method": notification_method,
            "active": True
        }
        
        self.alert_recipients["recipients"].append(recipient)
    
    def get_schedule(self) -> dict:
        """
        Obtiene el horario de activación del geofence.
        
        Returns:
            dict: Horario de activación
        """
        return self.schedule or {}
    
    def set_schedule(self, schedule: dict):
        """
        Establece el horario de activación del geofence.
        
        Args:
            schedule: Diccionario con el horario
        """
        self.schedule = schedule
    
    def is_active_now(self) -> bool:
        """
        Verifica si el geofence está activo en este momento.
        
        Returns:
            bool: True si está activo, False en caso contrario
        """
        if not self.is_active:
            return False
        
        schedule = self.get_schedule()
        if not schedule:
            return True  # Sin horario = siempre activo
        
        # Aquí se implementaría la lógica de verificación de horario
        # Por ahora retornamos True si no hay horario específico
        return True
    
    def check_location(self, latitude: float, longitude: float) -> dict:
        """
        Verifica si una ubicación está dentro del geofence.
        
        Args:
            latitude: Latitud de la ubicación
            longitude: Longitud de la ubicación
            
        Returns:
            dict: Resultado de la verificación
        """
        import math
        
        # Calcular distancia al centro del geofence
        R = 6371000  # Radio de la Tierra en metros
        
        lat1_rad = math.radians(self.latitude)
        lat2_rad = math.radians(latitude)
        delta_lat = math.radians(latitude - self.latitude)
        delta_lng = math.radians(longitude - self.longitude)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        is_inside = distance <= self.radius
        
        return {
            "is_inside": is_inside,
            "distance": distance,
            "radius": self.radius,
            "should_alert": is_inside and self.is_active_now()
        }
    
    def get_coordinates(self) -> tuple:
        """
        Obtiene las coordenadas del centro del geofence.
        
        Returns:
            tuple: (latitude, longitude)
        """
        return (self.latitude, self.longitude)
    
    def set_coordinates(self, latitude: float, longitude: float):
        """
        Establece las coordenadas del centro del geofence.
        
        Args:
            latitude: Latitud del centro
            longitude: Longitud del centro
        """
        self.latitude = latitude
        self.longitude = longitude
    
    @classmethod
    def get_geofence_types(cls) -> list:
        """
        Retorna los tipos de geofence disponibles.
        
        Returns:
            list: Lista de tipos de geofence
        """
        return [
            {"value": "home", "label": "Casa", "description": "Zona segura - casa"},
            {"value": "work", "label": "Trabajo", "description": "Zona segura - trabajo"},
            {"value": "school", "label": "Escuela", "description": "Zona segura - escuela"},
            {"value": "hospital", "label": "Hospital", "description": "Zona segura - hospital"},
            {"value": "danger", "label": "Peligro", "description": "Zona de peligro"},
            {"value": "restricted", "label": "Restringida", "description": "Zona restringida"},
            {"value": "safe", "label": "Segura", "description": "Zona segura general"},
            {"value": "custom", "label": "Personalizada", "description": "Zona personalizada"},
            {"value": "debug", "label": "Debug", "description": "Zona para pruebas"}
        ]
    
    @classmethod
    def create_debug_geofence(cls, cared_person_id: uuid.UUID, name: str, 
                             latitude: float, longitude: float, radius: float = 100.0,
                             notes: str = None) -> "Geofence":
        """
        Crea un geofence de debug para pruebas.
        
        Args:
            cared_person_id: ID de la persona bajo cuidado
            name: Nombre del geofence
            latitude: Latitud del centro
            longitude: Longitud del centro
            radius: Radio en metros
            notes: Notas de debug
            
        Returns:
            Geofence: Instancia de geofence de debug
        """
        return cls(
            cared_person_id=cared_person_id,
            name=name,
            description=f"Geofence de debug para pruebas - {notes or 'Sin notas'}",
            geofence_type="debug",
            latitude=latitude,
            longitude=longitude,
            radius=radius,
            is_debug=True,
            debug_notes=notes,
            alert_on_entry=True,
            alert_on_exit=True,
            alert_recipients={
                "recipients": [
                    {
                        "type": "debug",
                        "id": "debug_recipient",
                        "notification_method": "all",
                        "active": True
                    }
                ]
            }
        )
    
    @classmethod
    def create_home_geofence(cls, cared_person_id: uuid.UUID, latitude: float, 
                            longitude: float, radius: float = 50.0) -> "Geofence":
        """
        Crea un geofence de casa.
        
        Args:
            cared_person_id: ID de la persona bajo cuidado
            latitude: Latitud de la casa
            longitude: Longitud de la casa
            radius: Radio en metros
            
        Returns:
            Geofence: Instancia de geofence de casa
        """
        return cls(
            cared_person_id=cared_person_id,
            name="Casa",
            description="Zona segura - Casa",
            geofence_type="home",
            latitude=latitude,
            longitude=longitude,
            radius=radius,
            alert_on_entry=False,  # No alertar al entrar a casa
            alert_on_exit=True,    # Alertar al salir de casa
            alert_recipients={
                "recipients": [
                    {
                        "type": "primary_caregiver",
                        "id": "auto",
                        "notification_method": "all",
                        "active": True
                    }
                ]
            }
        )
    
    @classmethod
    def get_active_geofences(cls, db, cared_person_id: uuid.UUID) -> list:
        """
        Obtiene los geofences activos de una persona.
        
        Args:
            db: Sesión de base de datos
            cared_person_id: ID de la persona bajo cuidado
            
        Returns:
            list: Lista de geofences activos
        """
        return db.query(cls).filter(
            cls.cared_person_id == cared_person_id,
            cls.is_active == True
        ).all()
    
    @classmethod
    def get_debug_geofences(cls, db, cared_person_id: uuid.UUID = None) -> list:
        """
        Obtiene geofences de debug para pruebas.
        
        Args:
            db: Sesión de base de datos
            cared_person_id: ID de la persona bajo cuidado (opcional)
            
        Returns:
            list: Lista de geofences de debug
        """
        query = db.query(cls).filter(cls.is_debug == True)
        
        if cared_person_id:
            query = query.filter(cls.cared_person_id == cared_person_id)
        
        return query.all()
    
    def validate_business_rules(self) -> list:
        """
        Valida las reglas de negocio para este geofence.
        
        Returns:
            list: Lista de errores de validación (vacía si todo está bien)
        """
        errors = []
        
        # Regla: Latitud debe estar entre -90 y 90
        if self.latitude < -90 or self.latitude > 90:
            errors.append("La latitud debe estar entre -90 y 90 grados")
        
        # Regla: Longitud debe estar entre -180 y 180
        if self.longitude < -180 or self.longitude > 180:
            errors.append("La longitud debe estar entre -180 y 180 grados")
        
        # Regla: Radio debe ser positivo
        if self.radius <= 0:
            errors.append("El radio debe ser un valor positivo")
        
        # Regla: Debe tener al menos un destinatario de alerta si las alertas están habilitadas
        if (self.alert_on_entry or self.alert_on_exit) and not self.get_alert_recipients():
            errors.append("Un geofence con alertas debe tener al menos un destinatario")
        
        return errors 