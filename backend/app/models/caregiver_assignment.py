from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class CaregiverAssignment(Base):
    """
    Modelo para asignaciones de cuidadores a personas bajo cuidado.
    
    Reglas de negocio implementadas:
    - Una persona puede tener múltiples cuidadores
    - Solo puede haber un cuidador principal por persona
    - Los cuidadores tienen horarios y responsabilidades específicas
    - Las asignaciones tienen fechas de inicio y fin
    """
    __tablename__ = "caregiver_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False)
    is_primary = Column(Boolean, default=False)
    assignment_type = Column(String(50), nullable=False)  # family, professional, volunteer, institution
    responsibilities = Column(JSONB, default=dict)
    schedule = Column(JSONB, default=dict)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True))  # Null para asignaciones indefinidas
    status = Column(String(20), default="active")  # active, inactive, suspended
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    caregiver = relationship("User", foreign_keys=[caregiver_id])
    cared_person = relationship("CaredPerson", back_populates="caregivers")
    
    def __repr__(self):
        return f"<CaregiverAssignment(id={self.id}, caregiver_id={self.caregiver_id}, cared_person_id={self.cared_person_id})>"
    
    def is_active_assignment(self) -> bool:
        """
        Verifica si la asignación está activa.
        
        Returns:
            bool: True si está activa, False en caso contrario
        """
        from datetime import datetime
        
        now = datetime.utcnow()
        
        # Verificar fecha de inicio
        if self.start_date and now < self.start_date:
            return False
        
        # Verificar fecha de fin
        if self.end_date and now > self.end_date:
            return False
        
        # Verificar estado
        return self.status == "active"
    
    def get_schedule(self) -> dict:
        """
        Obtiene el horario del cuidador.
        
        Returns:
            dict: Horario del cuidador
        """
        return self.schedule or {}
    
    def set_schedule(self, schedule: dict):
        """
        Establece el horario del cuidador.
        
        Args:
            schedule: Diccionario con el horario
        """
        self.schedule = schedule
    
    def get_responsibilities(self) -> list:
        """
        Obtiene las responsabilidades del cuidador.
        
        Returns:
            list: Lista de responsabilidades
        """
        if not self.responsibilities:
            return []
        
        return self.responsibilities.get("responsibilities", [])
    
    def add_responsibility(self, responsibility: str, description: str = None):
        """
        Agrega una responsabilidad al cuidador.
        
        Args:
            responsibility: Nombre de la responsabilidad
            description: Descripción opcional
        """
        if not self.responsibilities:
            self.responsibilities = {"responsibilities": []}
        
        resp = {
            "name": responsibility,
            "description": description,
            "active": True
        }
        
        self.responsibilities["responsibilities"].append(resp)
    
    @classmethod
    def get_assignment_types(cls) -> list:
        """
        Retorna los tipos de asignación disponibles.
        
        Returns:
            list: Lista de tipos de asignación
        """
        return [
            {"value": "family", "label": "Familiar", "description": "Miembro de la familia"},
            {"value": "professional", "label": "Profesional", "description": "Cuidador profesional contratado"},
            {"value": "volunteer", "label": "Voluntario", "description": "Cuidador voluntario"},
            {"value": "institution", "label": "Institución", "description": "Cuidador de institución"},
            {"value": "neighbor", "label": "Vecino", "description": "Vecino o amigo cercano"},
            {"value": "nurse", "label": "Enfermero/a", "description": "Enfermero/a profesional"},
            {"value": "therapist", "label": "Terapeuta", "description": "Terapeuta especializado"}
        ]
    
    @classmethod
    def get_status_options(cls) -> list:
        """
        Retorna las opciones de estado disponibles.
        
        Returns:
            list: Lista de estados
        """
        return [
            {"value": "active", "label": "Activo", "description": "Asignación activa"},
            {"value": "inactive", "label": "Inactivo", "description": "Asignación inactiva"},
            {"value": "suspended", "label": "Suspendido", "description": "Asignación temporalmente suspendida"},
            {"value": "pending", "label": "Pendiente", "description": "Asignación pendiente de activación"},
            {"value": "completed", "label": "Completado", "description": "Asignación finalizada"}
        ]
    
    @classmethod
    def get_primary_caregiver(cls, db, cared_person_id: uuid.UUID):
        """
        Obtiene el cuidador principal de una persona.
        
        Args:
            db: Sesión de base de datos
            cared_person_id: ID de la persona bajo cuidado
            
        Returns:
            CaregiverAssignment: El cuidador principal o None si no existe
        """
        return db.query(cls).filter(
            cls.cared_person_id == cared_person_id,
            cls.is_primary == True,
            cls.status == "active"
        ).first()
    
    @classmethod
    def get_active_caregivers(cls, db, cared_person_id: uuid.UUID) -> list:
        """
        Obtiene todos los cuidadores activos de una persona.
        
        Args:
            db: Sesión de base de datos
            cared_person_id: ID de la persona bajo cuidado
            
        Returns:
            list: Lista de cuidadores activos
        """
        return db.query(cls).filter(
            cls.cared_person_id == cared_person_id,
            cls.status == "active"
        ).all()
    
    @classmethod
    def set_primary_caregiver(cls, db, cared_person_id: uuid.UUID, caregiver_id: uuid.UUID) -> bool:
        """
        Establece un cuidador como principal.
        
        Args:
            db: Sesión de base de datos
            cared_person_id: ID de la persona bajo cuidado
            caregiver_id: ID del cuidador a establecer como principal
            
        Returns:
            bool: True si se estableció correctamente, False en caso contrario
        """
        # Remover cuidador principal actual
        current_primary = cls.get_primary_caregiver(db, cared_person_id)
        if current_primary:
            current_primary.is_primary = False
        
        # Establecer nuevo cuidador principal
        assignment = db.query(cls).filter(
            cls.cared_person_id == cared_person_id,
            cls.caregiver_id == caregiver_id,
            cls.status == "active"
        ).first()
        
        if assignment:
            assignment.is_primary = True
            db.commit()
            return True
        
        return False
    
    def validate_business_rules(self) -> list:
        """
        Valida las reglas de negocio para esta asignación.
        
        Returns:
            list: Lista de errores de validación (vacía si todo está bien)
        """
        errors = []
        
        # Regla: Fecha de inicio debe ser anterior a fecha de fin (si existe)
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            errors.append("La fecha de inicio debe ser anterior a la fecha de fin")
        
        # Regla: Debe tener al menos una responsabilidad
        if not self.get_responsibilities():
            errors.append("El cuidador debe tener al menos una responsabilidad asignada")
        
        return errors 