from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class EmergencyProtocol(Base):
    """
    Modelo para protocolos de emergencia configurables.
    
    Reglas de negocio implementadas:
    - Los protocolos son configurables por institución
    - Cada protocolo tiene pasos específicos de escalación
    - Los protocolos se activan automáticamente según condiciones
    - Soporte para diferentes tipos de crisis
    """
    __tablename__ = "emergency_protocols"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    institution_id = Column(UUID(as_uuid=True), ForeignKey("institutions.id"))
    crisis_type = Column(String(50), nullable=False, index=True)  # medical, fall, wandering, abuse, etc.
    severity_level = Column(String(20), nullable=False)  # low, medium, high, critical
    activation_conditions = Column(JSONB, default=dict)
    escalation_steps = Column(JSONB, default=dict)
    response_time = Column(Integer)  # tiempo en minutos
    auto_activate = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    institution = relationship("Institution", back_populates="protocols")
    alerts = relationship("Alert", back_populates="protocol")
    
    def __repr__(self):
        return f"<EmergencyProtocol(id={self.id}, name='{self.name}', crisis_type='{self.crisis_type}')>"
    
    def get_activation_conditions(self) -> dict:
        """
        Obtiene las condiciones de activación del protocolo.
        
        Returns:
            dict: Condiciones de activación
        """
        return self.activation_conditions or {}
    
    def set_activation_condition(self, condition_type: str, value: any, operator: str = "equals"):
        """
        Establece una condición de activación.
        
        Args:
            condition_type: Tipo de condición (sensor_value, time, location, etc.)
            value: Valor de la condición
            operator: Operador de comparación (equals, greater_than, less_than, etc.)
        """
        if not self.activation_conditions:
            self.activation_conditions = {"conditions": []}
        
        condition = {
            "type": condition_type,
            "value": value,
            "operator": operator,
            "active": True
        }
        
        self.activation_conditions["conditions"].append(condition)
    
    def get_escalation_steps(self) -> list:
        """
        Obtiene los pasos de escalación del protocolo.
        
        Returns:
            list: Lista de pasos de escalación
        """
        if not self.escalation_steps:
            return []
        
        return self.escalation_steps.get("steps", [])
    
    def add_escalation_step(self, step_number: int, action: str, contact_type: str, 
                           contact_value: str, delay_minutes: int = 0, 
                           description: str = None):
        """
        Agrega un paso de escalación al protocolo.
        
        Args:
            step_number: Número del paso
            action: Acción a realizar (call, sms, email, notification)
            contact_type: Tipo de contacto (emergency_contact, caregiver, institution, etc.)
            contact_value: Valor del contacto
            delay_minutes: Retraso en minutos antes de ejecutar
            description: Descripción del paso
        """
        if not self.escalation_steps:
            self.escalation_steps = {"steps": []}
        
        step = {
            "step_number": step_number,
            "action": action,
            "contact_type": contact_type,
            "contact_value": contact_value,
            "delay_minutes": delay_minutes,
            "description": description,
            "active": True
        }
        
        self.escalation_steps["steps"].append(step)
    
    def should_activate(self, event_data: dict) -> bool:
        """
        Determina si el protocolo debe activarse basado en los datos del evento.
        
        Args:
            event_data: Datos del evento que puede activar el protocolo
            
        Returns:
            bool: True si debe activarse, False en caso contrario
        """
        if not self.auto_activate or not self.is_active:
            return False
        
        conditions = self.get_activation_conditions()
        if not conditions:
            return True  # Sin condiciones = siempre activar
        
        for condition in conditions.get("conditions", []):
            if not condition.get("active", True):
                continue
            
            condition_type = condition.get("type")
            expected_value = condition.get("value")
            operator = condition.get("operator", "equals")
            
            actual_value = event_data.get(condition_type)
            
            if not self._evaluate_condition(actual_value, expected_value, operator):
                return False
        
        return True
    
    def _evaluate_condition(self, actual_value: any, expected_value: any, operator: str) -> bool:
        """
        Evalúa una condición específica.
        
        Args:
            actual_value: Valor actual
            expected_value: Valor esperado
            operator: Operador de comparación
            
        Returns:
            bool: True si la condición se cumple
        """
        if operator == "equals":
            return actual_value == expected_value
        elif operator == "not_equals":
            return actual_value != expected_value
        elif operator == "greater_than":
            return actual_value > expected_value
        elif operator == "less_than":
            return actual_value < expected_value
        elif operator == "contains":
            return expected_value in actual_value if actual_value else False
        elif operator == "in":
            return actual_value in expected_value if isinstance(expected_value, list) else False
        elif operator == "not_in":
            return actual_value not in expected_value if isinstance(expected_value, list) else False
        
        return False
    
    @classmethod
    def get_crisis_types(cls) -> list:
        """
        Retorna los tipos de crisis disponibles.
        
        Returns:
            list: Lista de tipos de crisis
        """
        return [
            {"value": "medical", "label": "Médica", "description": "Emergencia médica"},
            {"value": "fall", "label": "Caída", "description": "Caída o accidente"},
            {"value": "wandering", "label": "Deambulación", "description": "Persona perdida o deambulando"},
            {"value": "abuse", "label": "Abuso", "description": "Sospecha de abuso o maltrato"},
            {"value": "fire", "label": "Incendio", "description": "Incendio o emergencia de fuego"},
            {"value": "gas", "label": "Gas", "description": "Fuga de gas o intoxicación"},
            {"value": "intrusion", "label": "Intrusión", "description": "Intrusión o robo"},
            {"value": "medical_alert", "label": "Alerta Médica", "description": "Alerta médica del dispositivo"},
            {"value": "medication", "label": "Medicación", "description": "Problema con medicación"},
            {"value": "communication", "label": "Comunicación", "description": "Problema de comunicación"},
            {"value": "environmental", "label": "Ambiental", "description": "Problema ambiental"},
            {"value": "other", "label": "Otro", "description": "Otro tipo de emergencia"}
        ]
    
    @classmethod
    def get_severity_levels(cls) -> list:
        """
        Retorna los niveles de severidad disponibles.
        
        Returns:
            list: Lista de niveles de severidad
        """
        return [
            {"value": "low", "label": "Baja", "description": "Emergencia menor"},
            {"value": "medium", "label": "Media", "description": "Emergencia moderada"},
            {"value": "high", "label": "Alta", "description": "Emergencia grave"},
            {"value": "critical", "label": "Crítica", "description": "Emergencia crítica"}
        ]
    
    @classmethod
    def get_by_crisis_type(cls, db, crisis_type: str, institution_id: uuid.UUID = None) -> list:
        """
        Obtiene protocolos por tipo de crisis.
        
        Args:
            db: Sesión de base de datos
            crisis_type: Tipo de crisis
            institution_id: ID de la institución (opcional)
            
        Returns:
            list: Lista de protocolos
        """
        query = db.query(cls).filter(
            cls.crisis_type == crisis_type,
            cls.is_active == True
        )
        
        if institution_id:
            query = query.filter(cls.institution_id == institution_id)
        
        return query.all()
    
    @classmethod
    def get_by_severity(cls, db, severity_level: str, institution_id: uuid.UUID = None) -> list:
        """
        Obtiene protocolos por nivel de severidad.
        
        Args:
            db: Sesión de base de datos
            severity_level: Nivel de severidad
            institution_id: ID de la institución (opcional)
            
        Returns:
            list: Lista de protocolos
        """
        query = db.query(cls).filter(
            cls.severity_level == severity_level,
            cls.is_active == True
        )
        
        if institution_id:
            query = query.filter(cls.institution_id == institution_id)
        
        return query.all()
    
    def validate_business_rules(self) -> list:
        """
        Valida las reglas de negocio para este protocolo.
        
        Returns:
            list: Lista de errores de validación (vacía si todo está bien)
        """
        errors = []
        
        # Regla: Debe tener al menos un paso de escalación
        if not self.get_escalation_steps():
            errors.append("El protocolo debe tener al menos un paso de escalación")
        
        # Regla: Los pasos deben estar ordenados correctamente
        steps = self.get_escalation_steps()
        step_numbers = [step.get("step_number", 0) for step in steps]
        if step_numbers != sorted(step_numbers):
            errors.append("Los pasos de escalación deben estar ordenados secuencialmente")
        
        # Regla: Debe tener un tiempo de respuesta definido
        if not self.response_time or self.response_time <= 0:
            errors.append("El protocolo debe tener un tiempo de respuesta válido")
        
        return errors 