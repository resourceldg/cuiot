from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


class ShiftType(str, Enum):
    """Tipos de turno disponibles"""
    MORNING = "morning"
    AFTERNOON = "afternoon"
    NIGHT = "night"
    TWENTY_FOUR_HOURS = "24h"


class PhysicalCondition(str, Enum):
    """Estados físicos"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


class MobilityLevel(str, Enum):
    """Niveles de movilidad"""
    INDEPENDENT = "independent"
    ASSISTED = "assisted"
    WHEELCHAIR = "wheelchair"
    BEDRIDDEN = "bedridden"


class MentalState(str, Enum):
    """Estados mentales"""
    ALERT = "alert"
    CONFUSED = "confused"
    DROWSY = "drowsy"
    AGITATED = "agitated"
    CALM = "calm"


class Mood(str, Enum):
    """Estados de ánimo"""
    HAPPY = "happy"
    SAD = "sad"
    ANXIOUS = "anxious"
    ANGRY = "angry"
    NEUTRAL = "neutral"


class CognitiveFunction(str, Enum):
    """Funciones cognitivas"""
    NORMAL = "normal"
    MILD_IMPAIRMENT = "mild_impairment"
    MODERATE_IMPAIRMENT = "moderate_impairment"
    SEVERE_IMPAIRMENT = "severe_impairment"


class CommunicationAbility(str, Enum):
    """Capacidades de comunicación"""
    NORMAL = "normal"
    LIMITED = "limited"
    NONVERBAL = "nonverbal"


class Appetite(str, Enum):
    """Niveles de apetito"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    NONE = "none"


class FoodIntake(str, Enum):
    """Tipos de ingesta de alimentos"""
    FULL_MEAL = "full_meal"
    PARTIAL_MEAL = "partial_meal"
    SNACKS_ONLY = "snacks_only"
    REFUSED = "refused"


class FluidIntake(str, Enum):
    """Tipos de ingesta de líquidos"""
    ADEQUATE = "adequate"
    LIMITED = "limited"
    POOR = "poor"
    REFUSED = "refused"


class BowelMovement(str, Enum):
    """Tipos de movimiento intestinal"""
    NORMAL = "normal"
    CONSTIPATED = "constipated"
    DIARRHEA = "diarrhea"
    NONE = "none"


class UrinaryOutput(str, Enum):
    """Tipos de producción urinaria"""
    NORMAL = "normal"
    DECREASED = "decreased"
    INCREASED = "increased"
    NONE = "none"


class CatheterStatus(str, Enum):
    """Estados de catéter"""
    NONE = "none"
    FOLEY = "foley"
    SUPRAPUBIC = "suprapubic"
    CONDOM = "condom"


class SocialInteraction(str, Enum):
    """Tipos de interacción social"""
    ACTIVE = "active"
    PASSIVE = "passive"
    WITHDRAWN = "withdrawn"
    AGGRESSIVE = "aggressive"


class FallRiskAssessment(str, Enum):
    """Evaluaciones de riesgo de caída"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ObservationStatus(str, Enum):
    """Estados de la observación"""
    DRAFT = "draft"
    COMPLETED = "completed"
    REVIEWED = "reviewed"
    ARCHIVED = "archived"


class HygieneStatus(str, Enum):
    """Estados de higiene"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class ShiftObservationBase(BaseModel):
    """Esquema base para observaciones de turno"""
    
    shift_type: ShiftType = Field(..., description="Tipo de turno")
    shift_start: datetime = Field(..., description="Inicio del turno")
    shift_end: datetime = Field(..., description="Fin del turno")
    observation_date: datetime = Field(default_factory=datetime.utcnow, description="Fecha de la observación")
    
    # Estado físico
    physical_condition: Optional[PhysicalCondition] = Field(None, description="Estado físico")
    mobility_level: Optional[MobilityLevel] = Field(None, description="Nivel de movilidad")
    pain_level: Optional[int] = Field(None, ge=0, le=10, description="Nivel de dolor (0-10)")
    vital_signs: Optional[Dict[str, Any]] = Field(None, description="Signos vitales")
    skin_condition: Optional[str] = Field(None, max_length=200, description="Condición de la piel")
    hygiene_status: Optional[HygieneStatus] = Field(None, description="Estado de higiene")
    
    # Estado mental y conductual
    mental_state: Optional[MentalState] = Field(None, description="Estado mental")
    mood: Optional[Mood] = Field(None, description="Estado de ánimo")
    behavior_notes: Optional[str] = Field(None, description="Observaciones de comportamiento")
    cognitive_function: Optional[CognitiveFunction] = Field(None, description="Función cognitiva")
    communication_ability: Optional[CommunicationAbility] = Field(None, description="Capacidad de comunicación")
    
    # Alimentación e hidratación
    appetite: Optional[Appetite] = Field(None, description="Apetito")
    food_intake: Optional[FoodIntake] = Field(None, description="Ingesta de alimentos")
    fluid_intake: Optional[FluidIntake] = Field(None, description="Ingesta de líquidos")
    swallowing_difficulty: Optional[bool] = Field(False, description="Dificultad para tragar")
    special_diet_notes: Optional[str] = Field(None, description="Notas sobre dieta especial")
    
    # Eliminación
    bowel_movement: Optional[BowelMovement] = Field(None, description="Movimiento intestinal")
    urinary_output: Optional[UrinaryOutput] = Field(None, description="Producción urinaria")
    incontinence_episodes: Optional[int] = Field(0, ge=0, description="Episodios de incontinencia")
    catheter_status: Optional[CatheterStatus] = Field(None, description="Estado de catéter")
    
    # Medicación
    medications_taken: Optional[List[Dict[str, Any]]] = Field(None, description="Medicamentos tomados")
    medications_missed: Optional[List[Dict[str, Any]]] = Field(None, description="Medicamentos no tomados")
    side_effects_observed: Optional[str] = Field(None, description="Efectos secundarios observados")
    medication_notes: Optional[str] = Field(None, description="Notas sobre medicación")
    
    # Actividades y estimulación
    activities_participated: Optional[List[Dict[str, Any]]] = Field(None, description="Actividades en las que participó")
    social_interaction: Optional[SocialInteraction] = Field(None, description="Interacción social")
    exercise_performed: Optional[bool] = Field(False, description="Ejercicio realizado")
    exercise_details: Optional[str] = Field(None, description="Detalles del ejercicio")
    
    # Seguridad e incidentes
    safety_concerns: Optional[str] = Field(None, description="Preocupaciones de seguridad")
    incidents_occurred: Optional[bool] = Field(False, description="Incidentes ocurridos")
    incident_details: Optional[str] = Field(None, description="Detalles de incidentes")
    fall_risk_assessment: Optional[FallRiskAssessment] = Field(None, description="Evaluación de riesgo de caída")
    restraint_used: Optional[bool] = Field(False, description="Uso de sujeción")
    restraint_details: Optional[str] = Field(None, description="Detalles de sujeción")
    
    # Comunicación y coordinación
    family_contact: Optional[bool] = Field(False, description="Contacto con familia")
    family_notes: Optional[str] = Field(None, description="Notas sobre contacto familiar")
    doctor_contact: Optional[bool] = Field(False, description="Contacto con médico")
    doctor_notes: Optional[str] = Field(None, description="Notas sobre contacto médico")
    handover_notes: Optional[str] = Field(None, description="Notas para el siguiente turno")
    
    # Archivos adjuntos
    attached_files: Optional[List[Dict[str, Any]]] = Field(None, description="Archivos adjuntos")
    
    # Estado
    status: Optional[ObservationStatus] = Field(ObservationStatus.DRAFT, description="Estado de la observación")
    
    # Relaciones
    cared_person_id: UUID = Field(..., description="ID de la persona bajo cuidado")
    institution_id: Optional[int] = Field(None, description="ID de la institución")
    
    @validator('shift_end')
    def validate_shift_end(cls, v, values):
        """Validar que el fin del turno sea posterior al inicio"""
        if 'shift_start' in values and v <= values['shift_start']:
            raise ValueError('El fin del turno debe ser posterior al inicio')
        return v
    
    @validator('pain_level')
    def validate_pain_level(cls, v):
        """Validar nivel de dolor entre 0 y 10"""
        if v is not None and (v < 0 or v > 10):
            raise ValueError('El nivel de dolor debe estar entre 0 y 10')
        return v
    
    @validator('incontinence_episodes')
    def validate_incontinence_episodes(cls, v):
        """Validar episodios de incontinencia no negativos"""
        if v is not None and v < 0:
            raise ValueError('Los episodios de incontinencia no pueden ser negativos')
        return v


class ShiftObservationCreate(ShiftObservationBase):
    """Esquema para crear una observación de turno"""
    pass


class ShiftObservationUpdate(BaseModel):
    """Esquema para actualizar una observación de turno"""
    
    shift_type: Optional[ShiftType] = None
    shift_start: Optional[datetime] = None
    shift_end: Optional[datetime] = None
    observation_date: Optional[datetime] = None
    
    # Estado físico
    physical_condition: Optional[PhysicalCondition] = None
    mobility_level: Optional[MobilityLevel] = None
    pain_level: Optional[int] = Field(None, ge=0, le=10)
    vital_signs: Optional[Dict[str, Any]] = None
    skin_condition: Optional[str] = Field(None, max_length=200)
    hygiene_status: Optional[HygieneStatus] = None
    
    # Estado mental y conductual
    mental_state: Optional[MentalState] = None
    mood: Optional[Mood] = None
    behavior_notes: Optional[str] = None
    cognitive_function: Optional[CognitiveFunction] = None
    communication_ability: Optional[CommunicationAbility] = None
    
    # Alimentación e hidratación
    appetite: Optional[Appetite] = None
    food_intake: Optional[FoodIntake] = None
    fluid_intake: Optional[FluidIntake] = None
    swallowing_difficulty: Optional[bool] = None
    special_diet_notes: Optional[str] = None
    
    # Eliminación
    bowel_movement: Optional[BowelMovement] = None
    urinary_output: Optional[UrinaryOutput] = None
    incontinence_episodes: Optional[int] = Field(None, ge=0)
    catheter_status: Optional[CatheterStatus] = None
    
    # Medicación
    medications_taken: Optional[List[Dict[str, Any]]] = None
    medications_missed: Optional[List[Dict[str, Any]]] = None
    side_effects_observed: Optional[str] = None
    medication_notes: Optional[str] = None
    
    # Actividades y estimulación
    activities_participated: Optional[List[Dict[str, Any]]] = None
    social_interaction: Optional[SocialInteraction] = None
    exercise_performed: Optional[bool] = None
    exercise_details: Optional[str] = None
    
    # Seguridad e incidentes
    safety_concerns: Optional[str] = None
    incidents_occurred: Optional[bool] = None
    incident_details: Optional[str] = None
    fall_risk_assessment: Optional[FallRiskAssessment] = None
    restraint_used: Optional[bool] = None
    restraint_details: Optional[str] = None
    
    # Comunicación y coordinación
    family_contact: Optional[bool] = None
    family_notes: Optional[str] = None
    doctor_contact: Optional[bool] = None
    doctor_notes: Optional[str] = None
    handover_notes: Optional[str] = None
    
    # Archivos adjuntos
    attached_files: Optional[List[Dict[str, Any]]] = None
    
    # Estado
    status: Optional[ObservationStatus] = None


class ShiftObservationResponse(ShiftObservationBase):
    """Esquema de respuesta para observaciones de turno"""
    
    id: UUID
    caregiver_id: UUID
    is_verified: bool
    verified_by: Optional[UUID] = None
    verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    # Información del cuidador
    caregiver_name: Optional[str] = None
    caregiver_email: Optional[str] = None
    
    # Información de la persona bajo cuidado
    cared_person_name: Optional[str] = None
    
    # Información de la institución
    institution_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class ShiftObservationListResponse(BaseModel):
    """Esquema para listado de observaciones de turno"""
    
    observations: List[ShiftObservationResponse]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        from_attributes = True


class ShiftObservationSummary(BaseModel):
    """Esquema para resumen de observaciones de turno"""
    
    id: UUID
    shift_type: ShiftType
    shift_start: datetime
    shift_end: datetime
    observation_date: datetime
    physical_condition: Optional[PhysicalCondition] = None
    mental_state: Optional[MentalState] = None
    incidents_occurred: bool
    status: ObservationStatus
    caregiver_name: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True 