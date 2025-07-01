from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, Float, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
import uuid


class ShiftObservation(Base):
    """
    Modelo para observaciones de turno clínico.
    
    Registra observaciones detalladas durante un turno de cuidado,
    incluyendo estado físico, mental, medicación, incidentes y archivos adjuntos.
    """
    
    __tablename__ = "shift_observations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Información del turno
    shift_type = Column(String(50), nullable=False, comment="Tipo de turno: morning, afternoon, night, 24h")
    shift_start = Column(DateTime, nullable=False, comment="Inicio del turno")
    shift_end = Column(DateTime, nullable=False, comment="Fin del turno")
    observation_date = Column(DateTime, nullable=False, default=datetime.utcnow, comment="Fecha de la observación")
    
    # Estado físico
    physical_condition = Column(String(50), comment="Estado físico: excellent, good, fair, poor, critical")
    mobility_level = Column(String(50), comment="Nivel de movilidad: independent, assisted, wheelchair, bedridden")
    pain_level = Column(Integer, comment="Nivel de dolor (0-10)")
    vital_signs = Column(JSONB, comment="Signos vitales: temperatura, presión, pulso, oxigenación")
    skin_condition = Column(String(200), comment="Condición de la piel")
    hygiene_status = Column(String(50), comment="Estado de higiene: excellent, good, fair, poor")
    
    # Estado mental y conductual
    mental_state = Column(String(50), comment="Estado mental: alert, confused, drowsy, agitated, calm")
    mood = Column(String(50), comment="Estado de ánimo: happy, sad, anxious, angry, neutral")
    behavior_notes = Column(Text, comment="Observaciones de comportamiento")
    cognitive_function = Column(String(50), comment="Función cognitiva: normal, mild_impairment, moderate_impairment, severe_impairment")
    communication_ability = Column(String(50), comment="Capacidad de comunicación: normal, limited, nonverbal")
    
    # Alimentación e hidratación
    appetite = Column(String(50), comment="Apetito: excellent, good, fair, poor, none")
    food_intake = Column(String(50), comment="Ingesta de alimentos: full_meal, partial_meal, snacks_only, refused")
    fluid_intake = Column(String(50), comment="Ingesta de líquidos: adequate, limited, poor, refused")
    swallowing_difficulty = Column(Boolean, default=False, comment="Dificultad para tragar")
    special_diet_notes = Column(Text, comment="Notas sobre dieta especial")
    
    # Eliminación
    bowel_movement = Column(String(50), comment="Movimiento intestinal: normal, constipated, diarrhea, none")
    urinary_output = Column(String(50), comment="Producción urinaria: normal, decreased, increased, none")
    incontinence_episodes = Column(Integer, default=0, comment="Episodios de incontinencia")
    catheter_status = Column(String(50), comment="Estado de catéter: none, foley, suprapubic, condom")
    
    # Medicación
    medications_taken = Column(JSONB, comment="Medicamentos tomados durante el turno")
    medications_missed = Column(JSONB, comment="Medicamentos no tomados")
    side_effects_observed = Column(Text, comment="Efectos secundarios observados")
    medication_notes = Column(Text, comment="Notas sobre medicación")
    
    # Actividades y estimulación
    activities_participated = Column(JSONB, comment="Actividades en las que participó")
    social_interaction = Column(String(50), comment="Interacción social: active, passive, withdrawn, aggressive")
    exercise_performed = Column(Boolean, default=False, comment="Ejercicio realizado")
    exercise_details = Column(Text, comment="Detalles del ejercicio")
    
    # Seguridad e incidentes
    safety_concerns = Column(Text, comment="Preocupaciones de seguridad")
    incidents_occurred = Column(Boolean, default=False, comment="Incidentes ocurridos")
    incident_details = Column(Text, comment="Detalles de incidentes")
    fall_risk_assessment = Column(String(50), comment="Evaluación de riesgo de caída: low, medium, high")
    restraint_used = Column(Boolean, default=False, comment="Uso de sujeción")
    restraint_details = Column(Text, comment="Detalles de sujeción")
    
    # Comunicación y coordinación
    family_contact = Column(Boolean, default=False, comment="Contacto con familia")
    family_notes = Column(Text, comment="Notas sobre contacto familiar")
    doctor_contact = Column(Boolean, default=False, comment="Contacto con médico")
    doctor_notes = Column(Text, comment="Notas sobre contacto médico")
    handover_notes = Column(Text, comment="Notas para el siguiente turno")
    
    # Archivos adjuntos
    attached_files = Column(JSONB, comment="Archivos adjuntos: fotos, videos, documentos")
    
    # Estado y validación
    status = Column(String(50), default="draft", comment="Estado: draft, completed, reviewed, archived")
    is_verified = Column(Boolean, default=False, comment="Observación verificada")
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), comment="Usuario que verificó")
    verified_at = Column(DateTime, comment="Fecha de verificación")
    
    # Relaciones
    cared_person_id = Column(UUID(as_uuid=True), ForeignKey("cared_persons.id"), nullable=False)
    caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), comment="Institución asociada")
    
    # Auditoría
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relaciones SQLAlchemy
    cared_person = relationship("CaredPerson", back_populates="shift_observations")
    caregiver = relationship("User", foreign_keys=[caregiver_id], back_populates="shift_observations")
    institution = relationship("Institution", back_populates="shift_observations")
    verifier = relationship("User", foreign_keys=[verified_by])
    
    def __repr__(self):
        return f"<ShiftObservation(id={self.id}, cared_person_id={self.cared_person_id}, shift_type={self.shift_type}, date={self.observation_date})>" 