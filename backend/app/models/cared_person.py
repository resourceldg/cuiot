from sqlalchemy import Column, String, Text, Boolean, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from app.core.database import Base
import uuid


class CaredPerson(Base):
    """
    Modelo para personas bajo cuidado, independientemente de su edad o condición.
    
    Reglas de negocio implementadas:
    - Una persona bajo cuidado debe tener al menos un cuidador asignado
    - Una persona puede ser responsable de sí misma (autocuidado)
    - Una persona puede o no pertenecer a una institución
    - Una persona debe tener al menos un servicio contratado activo
    - Los datos médicos y de accesibilidad se almacenan en JSONB
    """
    __tablename__ = "cared_persons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    care_type = Column(String(50), nullable=False, index=True)  # elderly, disability, autism, medical, recovery
    disability_type = Column(String(100))  # physical, intellectual, visual, hearing, multiple
    medical_conditions = Column(JSONB, default=dict)
    medications = Column(JSONB, default=dict)
    emergency_contacts = Column(JSONB, default=dict)
    care_preferences = Column(JSONB, default=dict)
    accessibility_needs = Column(JSONB, default=dict)
    guardian_info = Column(JSONB, default=dict)
    is_self_care = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    user = relationship("User", back_populates="cared_persons")
    caregivers = relationship("CaregiverAssignment", back_populates="cared_person", cascade="all, delete-orphan")
    devices = relationship("Device", back_populates="cared_person", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="cared_person", cascade="all, delete-orphan")
    location_tracking = relationship("LocationTracking", back_populates="cared_person", cascade="all, delete-orphan")
    geofences = relationship("Geofence", back_populates="cared_person", cascade="all, delete-orphan")
    service_subscriptions = relationship("ServiceSubscription", back_populates="cared_person", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<CaredPerson(id={self.id}, care_type='{self.care_type}', user_id={self.user_id})>"
    
    def get_primary_caregiver(self):
        """
        Obtiene el cuidador principal de la persona.
        
        Returns:
            CaregiverAssignment: El cuidador principal o None si no existe
        """
        for caregiver in self.caregivers:
            if caregiver.is_primary:
                return caregiver
        return None
    
    def get_emergency_contacts(self) -> list:
        """
        Obtiene la lista de contactos de emergencia.
        
        Returns:
            list: Lista de contactos de emergencia
        """
        if not self.emergency_contacts:
            return []
        
        contacts = self.emergency_contacts.get("contacts", [])
        return sorted(contacts, key=lambda x: x.get("priority", 999))
    
    def add_emergency_contact(self, name: str, phone: str, relationship: str, priority: int = 1):
        """
        Agrega un contacto de emergencia.
        
        Args:
            name: Nombre del contacto
            phone: Teléfono del contacto
            relationship: Relación con la persona
            priority: Prioridad del contacto (1 = más importante)
        """
        if not self.emergency_contacts:
            self.emergency_contacts = {"contacts": []}
        
        contact = {
            "name": name,
            "phone": phone,
            "relationship": relationship,
            "priority": priority,
            "active": True
        }
        
        self.emergency_contacts["contacts"].append(contact)
    
    def get_medications(self) -> list:
        """
        Obtiene la lista de medicamentos.
        
        Returns:
            list: Lista de medicamentos
        """
        if not self.medications:
            return []
        
        return self.medications.get("medications", [])
    
    def add_medication(self, name: str, dosage: str, frequency: str, time: str = None):
        """
        Agrega un medicamento.
        
        Args:
            name: Nombre del medicamento
            dosage: Dosis
            frequency: Frecuencia (daily, twice_daily, etc.)
            time: Hora específica si aplica
        """
        if not self.medications:
            self.medications = {"medications": []}
        
        medication = {
            "name": name,
            "dosage": dosage,
            "frequency": frequency,
            "time": time,
            "active": True
        }
        
        self.medications["medications"].append(medication)
    
    def get_accessibility_needs(self) -> dict:
        """
        Obtiene las necesidades de accesibilidad.
        
        Returns:
            dict: Necesidades de accesibilidad
        """
        return self.accessibility_needs or {}
    
    def set_accessibility_need(self, need_type: str, value: any):
        """
        Establece una necesidad de accesibilidad.
        
        Args:
            need_type: Tipo de necesidad (visual, auditory, motor, cognitive)
            value: Valor de la necesidad
        """
        if not self.accessibility_needs:
            self.accessibility_needs = {}
        
        self.accessibility_needs[need_type] = value
    
    @classmethod
    def get_care_types(cls) -> list:
        """
        Retorna los tipos de cuidado disponibles.
        
        Returns:
            list: Lista de tipos de cuidado
        """
        return [
            {"value": "elderly", "label": "Adulto Mayor", "description": "Personas mayores de 65 años"},
            {"value": "disability", "label": "Discapacidad", "description": "Personas con discapacidad física o intelectual"},
            {"value": "autism", "label": "Autismo", "description": "Personas con trastornos del espectro autista"},
            {"value": "medical", "label": "Condición Médica", "description": "Personas con condiciones médicas crónicas"},
            {"value": "recovery", "label": "Recuperación", "description": "Personas en recuperación post-quirúrgica"},
            {"value": "temporary", "label": "Temporal", "description": "Cuidado temporal por lesión o enfermedad"},
            {"value": "special_needs", "label": "Necesidades Especiales", "description": "Niños o adultos con necesidades especiales"}
        ]
    
    @classmethod
    def get_disability_types(cls) -> list:
        """
        Retorna los tipos de discapacidad disponibles.
        
        Returns:
            list: Lista de tipos de discapacidad
        """
        return [
            {"value": "physical", "label": "Física", "description": "Discapacidad física o motora"},
            {"value": "intellectual", "label": "Intelectual", "description": "Discapacidad intelectual o cognitiva"},
            {"value": "visual", "label": "Visual", "description": "Discapacidad visual"},
            {"value": "hearing", "label": "Auditiva", "description": "Discapacidad auditiva"},
            {"value": "speech", "label": "Del Habla", "description": "Discapacidad del habla"},
            {"value": "multiple", "label": "Múltiple", "description": "Múltiples discapacidades"},
            {"value": "other", "label": "Otra", "description": "Otro tipo de discapacidad"}
        ]
    
    def validate_business_rules(self) -> list:
        """
        Valida las reglas de negocio para esta persona.
        
        Returns:
            list: Lista de errores de validación (vacía si todo está bien)
        """
        errors = []
        
        # Regla: Debe tener al menos un cuidador (a menos que sea autocuidado)
        if not self.is_self_care and not self.caregivers:
            errors.append("Una persona bajo cuidado debe tener al menos un cuidador asignado")
        
        # Regla: Debe tener al menos un servicio contratado
        if not self.service_subscriptions:
            errors.append("Una persona bajo cuidado debe tener al menos un servicio contratado")
        
        # Regla: Debe tener contactos de emergencia
        if not self.get_emergency_contacts():
            errors.append("Una persona bajo cuidado debe tener al menos un contacto de emergencia")
        
        return errors 