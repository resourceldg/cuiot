from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from uuid import UUID
import uuid
import os
import shutil

from app.models.shift_observation import ShiftObservation
from app.models.user import User
from app.models.cared_person import CaredPerson
from app.models.institution import Institution
from app.models.status_type import StatusType
from app.schemas.shift_observation import (
    ShiftObservationCreate, 
    ShiftObservationUpdate, 
    ShiftObservationResponse,
    ShiftObservationListResponse,
    ShiftObservationSummary,
    ShiftType,
    ObservationStatus
)
from app.core.exceptions import ValidationException, NotFoundException, AuthorizationException


class ShiftObservationService:
    """
    Servicio para gestión de observaciones de turno clínico.
    
    Maneja la lógica de negocio para crear, actualizar, consultar y eliminar
    observaciones de turno con validaciones clínicas y de seguridad.
    """
    
    @staticmethod
    def create_shift_observation(
        db: Session, 
        observation_data: ShiftObservationCreate, 
        caregiver: User,
        attached_files: Optional[List[Dict[str, Any]]] = None
    ) -> ShiftObservationResponse:
        """
        Crear una nueva observación de turno.
        
        Args:
            db: Sesión de base de datos
            observation_data: Datos de la observación
            caregiver: Usuario cuidador que crea la observación
            attached_files: Archivos adjuntos (opcional)
            
        Returns:
            ShiftObservationResponse: Observación creada
            
        Raises:
            ValidationException: Si los datos no son válidos
            NotFoundException: Si la persona bajo cuidado no existe
            AuthorizationException: Si el cuidador no tiene permisos
        """
        
        # Validar datos de la observación
        ShiftObservationService._validate_observation_data(observation_data)
        
        # Verificar que la persona bajo cuidado existe
        cared_person = db.query(CaredPerson).filter(
            CaredPerson.id == observation_data.cared_person_id,
            CaredPerson.is_active == True
        ).first()
        
        if not cared_person:
            raise NotFoundException("Persona bajo cuidado no encontrada")
        
        # Verificar permisos del cuidador
        ShiftObservationService._validate_caregiver_permissions(db, caregiver, cared_person)
        
        # Verificar que no haya una observación duplicada para el mismo turno
        existing_observation = db.query(ShiftObservation).filter(
            and_(
                ShiftObservation.cared_person_id == observation_data.cared_person_id,
                ShiftObservation.caregiver_id == caregiver.id,
                ShiftObservation.shift_type == observation_data.shift_type,
                ShiftObservation.observation_date == observation_data.observation_date,
                ShiftObservation.is_active == True
            )
        ).first()
        
        if existing_observation:
            raise ValidationException("Ya existe una observación para este turno y fecha")
        
        # Buscar el ID del status_type "draft" por defecto
        draft_status = db.query(StatusType).filter(StatusType.name == "draft").first()
        if not draft_status:
            # Fallback: usar el primer status_type disponible
            draft_status = db.query(StatusType).first()
        
        # Crear la observación
        observation = ShiftObservation(
            id=uuid.uuid4(),
            shift_type=observation_data.shift_type,
            shift_start=observation_data.shift_start,
            shift_end=observation_data.shift_end,
            observation_date=observation_data.observation_date,
            shift_observation_type_id=observation_data.shift_observation_type_id,
            
            # Estado físico
            physical_condition=observation_data.physical_condition,
            mobility_level=observation_data.mobility_level,
            pain_level=observation_data.pain_level,
            vital_signs=observation_data.vital_signs,
            skin_condition=observation_data.skin_condition,
            hygiene_status_type_id=observation_data.hygiene_status_type_id,
            
            # Estado mental y conductual
            mental_state=observation_data.mental_state,
            mood=observation_data.mood,
            behavior_notes=observation_data.behavior_notes,
            cognitive_function=observation_data.cognitive_function,
            communication_ability=observation_data.communication_ability,
            
            # Alimentación e hidratación
            appetite=observation_data.appetite,
            food_intake=observation_data.food_intake,
            fluid_intake=observation_data.fluid_intake,
            swallowing_difficulty=observation_data.swallowing_difficulty,
            special_diet_notes=observation_data.special_diet_notes,
            
            # Eliminación
            bowel_movement=observation_data.bowel_movement,
            urinary_output=observation_data.urinary_output,
            incontinence_episodes=observation_data.incontinence_episodes,
            catheter_status_type_id=observation_data.catheter_status_type_id,
            
            # Medicación
            medications_taken=observation_data.medications_taken,
            medications_missed=observation_data.medications_missed,
            side_effects_observed=observation_data.side_effects_observed,
            medication_notes=observation_data.medication_notes,
            
            # Actividades y estimulación
            activities_participated=observation_data.activities_participated,
            social_interaction=observation_data.social_interaction,
            exercise_performed=observation_data.exercise_performed,
            exercise_details=observation_data.exercise_details,
            
            # Seguridad e incidentes
            safety_concerns=observation_data.safety_concerns,
            incidents_occurred=observation_data.incidents_occurred,
            incident_details=observation_data.incident_details,
            fall_risk_assessment=observation_data.fall_risk_assessment,
            restraint_used=observation_data.restraint_used,
            restraint_details=observation_data.restraint_details,
            
            # Comunicación y coordinación
            family_contact=observation_data.family_contact,
            family_notes=observation_data.family_notes,
            doctor_contact=observation_data.doctor_contact,
            doctor_notes=observation_data.doctor_notes,
            handover_notes=observation_data.handover_notes,
            
            # Archivos adjuntos
            attached_files=attached_files or [],
            
            # Estado (normalizado)
            status_type_id=observation_data.status_type_id or (draft_status.id if draft_status else None),
            
            # Relaciones
            cared_person_id=observation_data.cared_person_id,
            caregiver_id=caregiver.id,
            institution_id=observation_data.institution_id,
            
            # Auditoría
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_active=True
        )
        
        db.add(observation)
        db.commit()
        db.refresh(observation)
        
        return ShiftObservationService._format_observation_response(db, observation)
    
    @staticmethod
    def get_shift_observation(db: Session, observation_id: UUID) -> ShiftObservationResponse:
        """
        Obtener una observación de turno por ID.
        
        Args:
            db: Sesión de base de datos
            observation_id: ID de la observación
            
        Returns:
            ShiftObservationResponse: Observación encontrada
            
        Raises:
            NotFoundException: Si la observación no existe
        """
        
        observation = db.query(ShiftObservation).filter(
            and_(
                ShiftObservation.id == observation_id,
                ShiftObservation.is_active == True
            )
        ).first()
        
        if not observation:
            raise NotFoundException("Observación de turno no encontrada")
        
        return ShiftObservationService._format_observation_response(db, observation)
    
    @staticmethod
    def get_shift_observations(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        cared_person_id: Optional[UUID] = None,
        caregiver_id: Optional[UUID] = None,
        institution_id: Optional[int] = None,
        shift_type: Optional[ShiftType] = None,
        status_type_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        incidents_only: Optional[bool] = None
    ) -> ShiftObservationListResponse:
        """
        Obtener listado de observaciones de turno con filtros.
        
        Args:
            db: Sesión de base de datos
            skip: Registros a saltar
            limit: Límite de registros
            cared_person_id: Filtrar por persona bajo cuidado
            caregiver_id: Filtrar por cuidador
            institution_id: Filtrar por institución
            shift_type: Filtrar por tipo de turno
            status: Filtrar por estado
            start_date: Fecha de inicio
            end_date: Fecha de fin
            incidents_only: Solo observaciones con incidentes
            
        Returns:
            ShiftObservationListResponse: Listado de observaciones
        """
        
        query = db.query(ShiftObservation).filter(ShiftObservation.is_active == True)
        
        # Aplicar filtros
        if cared_person_id:
            query = query.filter(ShiftObservation.cared_person_id == cared_person_id)
        
        if caregiver_id:
            query = query.filter(ShiftObservation.caregiver_id == caregiver_id)
        
        if institution_id:
            query = query.filter(ShiftObservation.institution_id == institution_id)
        
        if shift_type:
            query = query.filter(ShiftObservation.shift_type == shift_type)
        
        if status_type_id:
            query = query.filter(ShiftObservation.status_type_id == status_type_id)
        
        if start_date:
            query = query.filter(ShiftObservation.observation_date >= start_date)
        
        if end_date:
            query = query.filter(ShiftObservation.observation_date <= end_date)
        
        if incidents_only:
            query = query.filter(ShiftObservation.incidents_occurred == True)
        
        # Ordenar por fecha de observación (más reciente primero)
        query = query.order_by(desc(ShiftObservation.observation_date))
        
        # Contar total
        total = query.count()
        
        # Aplicar paginación
        observations = query.offset(skip).limit(limit).all()
        
        # Formatear respuestas
        formatted_observations = [
            ShiftObservationService._format_observation_response(db, obs)
            for obs in observations
        ]
        
        return ShiftObservationListResponse(
            observations=formatted_observations,
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=(total + limit - 1) // limit
        )
    
    @staticmethod
    def update_shift_observation(
        db: Session,
        observation_id: UUID,
        observation_data: ShiftObservationUpdate,
        current_user: User
    ) -> ShiftObservationResponse:
        """
        Actualizar una observación de turno.
        
        Args:
            db: Sesión de base de datos
            observation_id: ID de la observación
            observation_data: Datos a actualizar
            current_user: Usuario que actualiza
            
        Returns:
            ShiftObservationResponse: Observación actualizada
            
        Raises:
            NotFoundException: Si la observación no existe
            AuthorizationException: Si el usuario no tiene permisos
            ValidationException: Si los datos no son válidos
        """
        
        observation = db.query(ShiftObservation).filter(
            and_(
                ShiftObservation.id == observation_id,
                ShiftObservation.is_active == True
            )
        ).first()
        
        if not observation:
            raise NotFoundException("Observación de turno no encontrada")
        
        # Verificar permisos (solo el cuidador que creó la observación puede editarla)
        if observation.caregiver_id != current_user.id:
            raise AuthorizationException("No tienes permisos para editar esta observación")
        
        # Verificar que la observación no esté verificada
        if observation.is_verified:
            raise ValidationException("No se puede editar una observación verificada")
        
        # Actualizar campos
        update_data = observation_data.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if hasattr(observation, field):
                setattr(observation, field, value)
        
        observation.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(observation)
        
        return ShiftObservationService._format_observation_response(db, observation)
    
    @staticmethod
    def delete_shift_observation(db: Session, observation_id: UUID, current_user: User) -> bool:
        """
        Eliminar (desactivar) una observación de turno.
        
        Args:
            db: Sesión de base de datos
            observation_id: ID de la observación
            current_user: Usuario que elimina
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            NotFoundException: Si la observación no existe
            AuthorizationException: Si el usuario no tiene permisos
        """
        
        observation = db.query(ShiftObservation).filter(
            and_(
                ShiftObservation.id == observation_id,
                ShiftObservation.is_active == True
            )
        ).first()
        
        if not observation:
            raise NotFoundException("Observación de turno no encontrada")
        
        # Verificar permisos
        if observation.caregiver_id != current_user.id:
            raise AuthorizationException("No tienes permisos para eliminar esta observación")
        
        # Verificar que la observación no esté verificada
        if observation.is_verified:
            raise AuthorizationException("No se puede eliminar una observación verificada")
        
        # Desactivar (soft delete)
        observation.is_active = False
        observation.updated_at = datetime.utcnow()
        
        db.commit()
        
        return True
    
    @staticmethod
    def verify_shift_observation(
        db: Session,
        observation_id: UUID,
        current_user: User
    ) -> ShiftObservationResponse:
        """
        Verificar una observación de turno.
        
        Args:
            db: Sesión de base de datos
            observation_id: ID de la observación
            current_user: Usuario que verifica
            
        Returns:
            ShiftObservationResponse: Observación verificada
            
        Raises:
            NotFoundException: Si la observación no existe
            ValidationException: Si la observación ya está verificada
        """
        
        observation = db.query(ShiftObservation).filter(
            and_(
                ShiftObservation.id == observation_id,
                ShiftObservation.is_active == True
            )
        ).first()
        
        if not observation:
            raise NotFoundException("Observación de turno no encontrada")
        
        if observation.is_verified:
            raise ValidationException("La observación ya está verificada")
        
        # Verificar la observación
        observation.is_verified = True
        observation.verified_by = current_user.id
        observation.verified_at = datetime.utcnow()
        
        # Buscar el ID del status_type "reviewed"
        reviewed_status = db.query(StatusType).filter(StatusType.name == "reviewed").first()
        if reviewed_status:
            observation.status_type_id = reviewed_status.id
        
        observation.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(observation)
        
        return ShiftObservationService._format_observation_response(db, observation)
    
    @staticmethod
    def get_observations_by_cared_person(
        db: Session,
        cared_person_id: UUID,
        skip: int = 0,
        limit: int = 50
    ) -> List[ShiftObservationSummary]:
        """
        Obtener resumen de observaciones por persona bajo cuidado.
        
        Args:
            db: Sesión de base de datos
            cared_person_id: ID de la persona bajo cuidado
            skip: Registros a saltar
            limit: Límite de registros
            
        Returns:
            List[ShiftObservationSummary]: Lista de resúmenes de observaciones
        """
        
        observations = db.query(ShiftObservation).filter(
            and_(
                ShiftObservation.cared_person_id == cared_person_id,
                ShiftObservation.is_active == True
            )
        ).order_by(desc(ShiftObservation.observation_date)).offset(skip).limit(limit).all()
        
        summaries = []
        for obs in observations:
            caregiver = db.query(User).filter(User.id == obs.caregiver_id).first()
            
            summary = ShiftObservationSummary(
                id=obs.id,
                shift_type=obs.shift_type,
                shift_start=obs.shift_start,
                shift_end=obs.shift_end,
                observation_date=obs.observation_date,
                physical_condition=obs.physical_condition,
                mental_state=obs.mental_state,
                incidents_occurred=obs.incidents_occurred,
                status=obs.status,
                caregiver_name=f"{caregiver.first_name} {caregiver.last_name}" if caregiver else None,
                created_at=obs.created_at
            )
            summaries.append(summary)
        
        return summaries
    
    @staticmethod
    def _validate_observation_data(observation_data: ShiftObservationCreate) -> None:
        """
        Validar datos de la observación.
        
        Args:
            observation_data: Datos a validar
            
        Raises:
            ValidationException: Si los datos no son válidos
        """
        
        # Validar fechas del turno
        if observation_data.shift_end <= observation_data.shift_start:
            raise ValidationException("El fin del turno debe ser posterior al inicio")
        
        # Validar duración del turno (máximo 24 horas)
        shift_duration = observation_data.shift_end - observation_data.shift_start
        if shift_duration > timedelta(hours=24):
            raise ValidationException("La duración del turno no puede exceder 24 horas")
        
        # Validar nivel de dolor
        if observation_data.pain_level is not None and (observation_data.pain_level < 0 or observation_data.pain_level > 10):
            raise ValidationException("El nivel de dolor debe estar entre 0 y 10")
        
        # Validar episodios de incontinencia
        if observation_data.incontinence_episodes is not None and observation_data.incontinence_episodes < 0:
            raise ValidationException("Los episodios de incontinencia no pueden ser negativos")
    
    @staticmethod
    def _validate_caregiver_permissions(db: Session, caregiver: User, cared_person: CaredPerson) -> None:
        """
        Validar permisos del cuidador.
        
        Args:
            db: Sesión de base de datos
            caregiver: Usuario cuidador
            cared_person: Persona bajo cuidado
            
        Raises:
            AuthorizationException: Si el cuidador no tiene permisos
        """
        
        # Verificar que el cuidador esté activo
        if not caregiver.is_active:
            raise AuthorizationException("El cuidador debe estar activo")
        
        # Verificar que el cuidador tenga relación con la persona bajo cuidado
        # (esto se puede expandir según las reglas de negocio específicas)
        if cared_person.user_id != caregiver.id:
            # Verificar si hay una asignación de cuidador
            from app.models.caregiver_assignment import CaregiverAssignment
            assignment = db.query(CaregiverAssignment).filter(
                and_(
                    CaregiverAssignment.caregiver_id == caregiver.id,
                    CaregiverAssignment.cared_person_id == cared_person.id,
                    CaregiverAssignment.is_active == True
                )
            ).first()
            
            if not assignment:
                raise AuthorizationException("El cuidador no tiene permisos para esta persona bajo cuidado")
    
    @staticmethod
    def _format_observation_response(db: Session, observation: ShiftObservation) -> ShiftObservationResponse:
        """
        Formatear respuesta de observación con información adicional.
        
        Args:
            db: Sesión de base de datos
            observation: Observación a formatear
            
        Returns:
            ShiftObservationResponse: Respuesta formateada
        """
        
        # Obtener información del cuidador
        caregiver = db.query(User).filter(User.id == observation.caregiver_id).first()
        caregiver_name = f"{caregiver.first_name} {caregiver.last_name}" if caregiver else None
        caregiver_email = caregiver.email if caregiver else None
        
        # Obtener información de la persona bajo cuidado
        cared_person = db.query(CaredPerson).filter(CaredPerson.id == observation.cared_person_id).first()
        cared_person_name = f"{cared_person.first_name} {cared_person.last_name}" if cared_person else None
        
        # Obtener información de la institución
        institution_name = None
        if observation.institution_id:
            institution = db.query(Institution).filter(Institution.id == observation.institution_id).first()
            institution_name = institution.name if institution else None
        
        return ShiftObservationResponse(
            id=observation.id,
            shift_type=observation.shift_type,
            shift_start=observation.shift_start,
            shift_end=observation.shift_end,
            observation_date=observation.observation_date,
            shift_observation_type_id=observation.shift_observation_type_id,
            
            # Estado físico
            physical_condition=observation.physical_condition,
            mobility_level=observation.mobility_level,
            pain_level=observation.pain_level,
            vital_signs=observation.vital_signs,
            skin_condition=observation.skin_condition,
            hygiene_status_type_id=observation.hygiene_status_type_id,
            
            # Estado mental y conductual
            mental_state=observation.mental_state,
            mood=observation.mood,
            behavior_notes=observation.behavior_notes,
            cognitive_function=observation.cognitive_function,
            communication_ability=observation.communication_ability,
            
            # Alimentación e hidratación
            appetite=observation.appetite,
            food_intake=observation.food_intake,
            fluid_intake=observation.fluid_intake,
            swallowing_difficulty=observation.swallowing_difficulty,
            special_diet_notes=observation.special_diet_notes,
            
            # Eliminación
            bowel_movement=observation.bowel_movement,
            urinary_output=observation.urinary_output,
            incontinence_episodes=observation.incontinence_episodes,
            catheter_status_type_id=observation.catheter_status_type_id,
            
            # Medicación
            medications_taken=observation.medications_taken,
            medications_missed=observation.medications_missed,
            side_effects_observed=observation.side_effects_observed,
            medication_notes=observation.medication_notes,
            
            # Actividades y estimulación
            activities_participated=observation.activities_participated,
            social_interaction=observation.social_interaction,
            exercise_performed=observation.exercise_performed,
            exercise_details=observation.exercise_details,
            
            # Seguridad e incidentes
            safety_concerns=observation.safety_concerns,
            incidents_occurred=observation.incidents_occurred,
            incident_details=observation.incident_details,
            fall_risk_assessment=observation.fall_risk_assessment,
            restraint_used=observation.restraint_used,
            restraint_details=observation.restraint_details,
            
            # Comunicación y coordinación
            family_contact=observation.family_contact,
            family_notes=observation.family_notes,
            doctor_contact=observation.doctor_contact,
            doctor_notes=observation.doctor_notes,
            handover_notes=observation.handover_notes,
            
            # Archivos adjuntos
            attached_files=observation.attached_files,
            
            # Estado (normalizado)
            status_type_id=observation.status_type_id,
            
            # Relaciones
            cared_person_id=observation.cared_person_id,
            institution_id=observation.institution_id,
            
            # Información adicional
            caregiver_id=observation.caregiver_id,
            caregiver_name=caregiver_name,
            caregiver_email=caregiver_email,
            cared_person_name=cared_person_name,
            institution_name=institution_name,
            
            # Verificación
            is_verified=observation.is_verified,
            verified_by=observation.verified_by,
            verified_at=observation.verified_at,
            
            # Auditoría
            created_at=observation.created_at,
            updated_at=observation.updated_at,
            is_active=observation.is_active
        ) 