from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from uuid import UUID
import uuid
import os
import shutil
from pydantic import ValidationError

from app.core.database import get_db
from app.models.user import User
from app.services.auth import AuthService
from app.services.shift_observation import ShiftObservationService
from app.schemas.shift_observation import (
    ShiftObservationCreate,
    ShiftObservationUpdate,
    ShiftObservationResponse,
    ShiftObservationListResponse,
    ShiftObservationSummary,
    ShiftType,
    ObservationStatus
)
from app.core.exceptions import NotFoundException

router = APIRouter()

# Configuración de directorio de uploads
UPLOAD_DIR = "uploads/shift_observations"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post('/', response_model=ShiftObservationResponse, status_code=status.HTTP_201_CREATED)
def create_shift_observation(
    shift_type: Optional[str] = Form(None, description="Tipo de turno: morning, afternoon, night, 24h"),
    shift_observation_type_id: Optional[int] = Form(None, description="ID del tipo de observación de turno normalizado"),
    shift_start: str = Form(..., description="Inicio del turno (ISO format)"),
    shift_end: str = Form(..., description="Fin del turno (ISO format)"),
    observation_date: Optional[str] = Form(None, description="Fecha de observación (ISO format, opcional)"),
    
    # Estado físico
    physical_condition: Optional[str] = Form(None, description="Estado físico: excellent, good, fair, poor, critical"),
    mobility_level: Optional[str] = Form(None, description="Nivel de movilidad: independent, assisted, wheelchair, bedridden"),
    pain_level: Optional[int] = Form(None, ge=0, le=10, description="Nivel de dolor (0-10)"),
    vital_signs: Optional[str] = Form(None, description="Signos vitales (JSON)"),
    skin_condition: Optional[str] = Form(None, max_length=200, description="Condición de la piel"),
    hygiene_status_type_id: Optional[int] = Form(None, description="ID del tipo de status de higiene normalizado"),
    
    # Estado mental y conductual
    mental_state: Optional[str] = Form(None, description="Estado mental: alert, confused, drowsy, agitated, calm"),
    mood: Optional[str] = Form(None, description="Estado de ánimo: happy, sad, anxious, angry, neutral"),
    behavior_notes: Optional[str] = Form(None, description="Observaciones de comportamiento"),
    cognitive_function: Optional[str] = Form(None, description="Función cognitiva: normal, mild_impairment, moderate_impairment, severe_impairment"),
    communication_ability: Optional[str] = Form(None, description="Capacidad de comunicación: normal, limited, nonverbal"),
    
    # Alimentación e hidratación
    appetite: Optional[str] = Form(None, description="Apetito: excellent, good, fair, poor, none"),
    food_intake: Optional[str] = Form(None, description="Ingesta de alimentos: full_meal, partial_meal, snacks_only, refused"),
    fluid_intake: Optional[str] = Form(None, description="Ingesta de líquidos: adequate, limited, poor, refused"),
    swallowing_difficulty: Optional[bool] = Form(False, description="Dificultad para tragar"),
    special_diet_notes: Optional[str] = Form(None, description="Notas sobre dieta especial"),
    
    # Eliminación
    bowel_movement: Optional[str] = Form(None, description="Movimiento intestinal: normal, constipated, diarrhea, none"),
    urinary_output: Optional[str] = Form(None, description="Producción urinaria: normal, decreased, increased, none"),
    incontinence_episodes: Optional[int] = Form(0, ge=0, description="Episodios de incontinencia"),
    catheter_status: Optional[str] = Form(None, description="Estado de catéter: none, foley, suprapubic, condom"),
    
    # Medicación
    medications_taken: Optional[str] = Form(None, description="Medicamentos tomados (JSON)"),
    medications_missed: Optional[str] = Form(None, description="Medicamentos no tomados (JSON)"),
    side_effects_observed: Optional[str] = Form(None, description="Efectos secundarios observados"),
    medication_notes: Optional[str] = Form(None, description="Notas sobre medicación"),
    
    # Actividades y estimulación
    activities_participated: Optional[str] = Form(None, description="Actividades en las que participó (JSON)"),
    social_interaction: Optional[str] = Form(None, description="Interacción social: active, passive, withdrawn, aggressive"),
    exercise_performed: Optional[bool] = Form(False, description="Ejercicio realizado"),
    exercise_details: Optional[str] = Form(None, description="Detalles del ejercicio"),
    
    # Seguridad e incidentes
    safety_concerns: Optional[str] = Form(None, description="Preocupaciones de seguridad"),
    incidents_occurred: Optional[bool] = Form(False, description="Incidentes ocurridos"),
    incident_details: Optional[str] = Form(None, description="Detalles de incidentes"),
    fall_risk_assessment: Optional[str] = Form(None, description="Evaluación de riesgo de caída: low, medium, high"),
    restraint_used: Optional[bool] = Form(False, description="Uso de sujeción"),
    restraint_details: Optional[str] = Form(None, description="Detalles de sujeción"),
    
    # Comunicación y coordinación
    family_contact: Optional[bool] = Form(False, description="Contacto con familia"),
    family_notes: Optional[str] = Form(None, description="Notas sobre contacto familiar"),
    doctor_contact: Optional[bool] = Form(False, description="Contacto con médico"),
    doctor_notes: Optional[str] = Form(None, description="Notas sobre contacto médico"),
    handover_notes: Optional[str] = Form(None, description="Notas para el siguiente turno"),
    
    # Relaciones
    cared_person_id: str = Form(..., description="ID de la persona bajo cuidado"),
    institution_id: Optional[int] = Form(None, description="ID de la institución (opcional)"),
    
    # Archivos adjuntos
    files: List[UploadFile] = File([], description="Archivos adjuntos (opcional)"),
    
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Crear una nueva observación de turno clínico.

    Este endpoint permite a los cuidadores registrar observaciones detalladas
    durante sus turnos, incluyendo estado físico, mental, medicación, incidentes
    y archivos adjuntos para documentación clínica.

    Requiere autenticación y permisos de cuidador para la persona bajo cuidado.
    """
    
    # Validate shift_type if provided
    if shift_type:
        valid_shift_types = ['morning', 'afternoon', 'night', '24h']
        if shift_type not in valid_shift_types:
            raise HTTPException(
                status_code=422,
                detail=[
                    {
                        "loc": ["body", "shift_type"],
                        "msg": f"shift_type debe ser uno de: {valid_shift_types}",
                        "type": "value_error"
                    }
                ]
            )
    
    # Ensure we have either shift_type or shift_observation_type_id
    if not shift_type and not shift_observation_type_id:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["body", "shift_type"],
                    "msg": "Se requiere shift_type o shift_observation_type_id",
                    "type": "value_error"
                }
            ]
        )
    
    # If shift_observation_type_id is not provided, use the first available one
    if not shift_observation_type_id:
        from app.models.shift_observation_type import ShiftObservationType
        first_type = db.query(ShiftObservationType).first()
        if first_type:
            shift_observation_type_id = first_type.id
        else:
            raise HTTPException(
                status_code=422,
                detail=[
                    {
                        "loc": ["body", "shift_observation_type_id"],
                        "msg": "No hay tipos de observación de turno disponibles",
                        "type": "value_error"
                    }
                ]
            )
    
    # Parse dates
    try:
        shift_start_parsed = datetime.fromisoformat(shift_start.replace('Z', '+00:00'))
        shift_end_parsed = datetime.fromisoformat(shift_end.replace('Z', '+00:00'))
        observation_date_parsed = datetime.utcnow()
        if observation_date:
            observation_date_parsed = datetime.fromisoformat(observation_date.replace('Z', '+00:00'))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Formato de fecha inválido: {str(e)}")
    
    # Process attached files
    attached_files = []
    if files:
        for file in files:
            file_id = str(uuid.uuid4())
            file_path = os.path.join(UPLOAD_DIR, file_id + '_' + file.filename)
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file.file, f)
            attached_files.append({
                'filename': file.filename,
                'url': f'/static/shift_observations/{file_id}_{file.filename}',
                'content_type': file.content_type,
                'size': file.spool_max_size if hasattr(file, 'spool_max_size') else None
            })
    
    # Parse JSON fields
    import json
    vital_signs_parsed = None
    if vital_signs:
        try:
            vital_signs_parsed = json.loads(vital_signs)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Formato JSON inválido en vital_signs")
    
    medications_taken_parsed = None
    if medications_taken:
        try:
            medications_taken_parsed = json.loads(medications_taken)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Formato JSON inválido en medications_taken")
    
    medications_missed_parsed = None
    if medications_missed:
        try:
            medications_missed_parsed = json.loads(medications_missed)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Formato JSON inválido en medications_missed")
    
    activities_participated_parsed = None
    if activities_participated:
        try:
            activities_participated_parsed = json.loads(activities_participated)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Formato JSON inválido en activities_participated")
    
    # Create observation data
    try:
        observation_data = ShiftObservationCreate(
            shift_type=shift_type or "morning",  # Default value if not provided
            shift_start=shift_start_parsed,
            shift_end=shift_end_parsed,
            observation_date=observation_date_parsed,
            shift_observation_type_id=shift_observation_type_id,
            
            # Estado físico
            physical_condition=physical_condition,
            mobility_level=mobility_level,
            pain_level=pain_level,
            vital_signs=vital_signs_parsed,
            skin_condition=skin_condition,
            hygiene_status_type_id=hygiene_status_type_id,
            
            # Estado mental y conductual
            mental_state=mental_state,
            mood=mood,
            behavior_notes=behavior_notes,
            cognitive_function=cognitive_function,
            communication_ability=communication_ability,
            
            # Alimentación e hidratación
            appetite=appetite,
            food_intake=food_intake,
            fluid_intake=fluid_intake,
            swallowing_difficulty=swallowing_difficulty,
            special_diet_notes=special_diet_notes,
            
            # Eliminación
            bowel_movement=bowel_movement,
            urinary_output=urinary_output,
            incontinence_episodes=incontinence_episodes,
            catheter_status=catheter_status,
            
            # Medicación
            medications_taken=medications_taken_parsed,
            medications_missed=medications_missed_parsed,
            side_effects_observed=side_effects_observed,
            medication_notes=medication_notes,
            
            # Actividades y estimulación
            activities_participated=activities_participated_parsed,
            social_interaction=social_interaction,
            exercise_performed=exercise_performed,
            exercise_details=exercise_details,
            
            # Seguridad e incidentes
            safety_concerns=safety_concerns,
            incidents_occurred=incidents_occurred,
            incident_details=incident_details,
            fall_risk_assessment=fall_risk_assessment,
            restraint_used=restraint_used,
            restraint_details=restraint_details,
            
            # Comunicación y coordinación
            family_contact=family_contact,
            family_notes=family_notes,
            doctor_contact=doctor_contact,
            doctor_notes=doctor_notes,
            handover_notes=handover_notes,
            
            # Relaciones
            cared_person_id=UUID(cared_person_id),
            institution_id=institution_id
        )
    except ValidationError as e:
        # Convert Pydantic validation errors to FastAPI format
        errors = []
        for error in e.errors():
            errors.append({
                "loc": error["loc"],
                "msg": error["msg"],
                "type": error["type"]
            })
        raise HTTPException(status_code=422, detail=errors)
    
    try:
        # Create observation
        observation = ShiftObservationService.create_shift_observation(
            db, observation_data, current_user, attached_files
        )
        
        return observation
    except (ValidationError, NotFoundException, PermissionError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get('/', response_model=ShiftObservationListResponse)
def get_shift_observations(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros"),
    cared_person_id: Optional[str] = Query(None, description="Filtrar por persona bajo cuidado"),
    caregiver_id: Optional[str] = Query(None, description="Filtrar por cuidador"),
    institution_id: Optional[int] = Query(None, description="Filtrar por institución"),
    shift_type: Optional[str] = Query(None, description="Filtrar por tipo de turno"),
    status_type_id: Optional[int] = Query(None, description="Filtrar por ID de tipo de estado"),
    start_date: Optional[str] = Query(None, description="Fecha de inicio (ISO format)"),
    end_date: Optional[str] = Query(None, description="Fecha de fin (ISO format)"),
    incidents_only: Optional[bool] = Query(None, description="Solo observaciones con incidentes"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Obtener listado de observaciones de turno con filtros.

    Permite consultar observaciones de turno con múltiples filtros
    para facilitar el seguimiento clínico y la auditoría.
    """
    
    # Parse optional parameters
    cared_person_uuid = None
    if cared_person_id:
        try:
            cared_person_uuid = UUID(cared_person_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de persona bajo cuidado inválido")
    
    caregiver_uuid = None
    if caregiver_id:
        try:
            caregiver_uuid = UUID(caregiver_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de cuidador inválido")
    
    # Parse dates
    start_date_parsed = None
    if start_date:
        try:
            start_date_parsed = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha de inicio inválido")
    
    end_date_parsed = None
    if end_date:
        try:
            end_date_parsed = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha de fin inválido")
    
    # Convert shift_type and status to enums if present
    shift_type_enum = None
    if shift_type:
        try:
            shift_type_enum = ShiftType(shift_type)
        except ValueError:
            raise HTTPException(status_code=400, detail="shift_type inválido")
    # status_type_id is already an integer, no need for enum conversion
    
    try:
        observations = ShiftObservationService.get_shift_observations(
            db=db,
            skip=skip,
            limit=limit,
            cared_person_id=cared_person_uuid,
            caregiver_id=caregiver_uuid,
            institution_id=institution_id,
            shift_type=shift_type_enum,
            status_type_id=status_type_id,
            start_date=start_date_parsed,
            end_date=end_date_parsed,
            incidents_only=incidents_only
        )
        
        return observations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get('/{observation_id}', response_model=ShiftObservationResponse)
def get_shift_observation(
    observation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Obtener una observación de turno específica por ID.

    Retorna todos los detalles de una observación de turno,
    incluyendo información del cuidador y archivos adjuntos.
    """
    
    try:
        observation_uuid = UUID(observation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de observación inválido")
    
    try:
        observation = ShiftObservationService.get_shift_observation(db, observation_uuid)
        return observation
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.put('/{observation_id}', response_model=ShiftObservationResponse)
def update_shift_observation(
    observation_id: str,
    observation_data: ShiftObservationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Actualizar una observación de turno existente.

    Permite modificar observaciones que no han sido verificadas.
    Solo el cuidador que creó la observación puede editarla.
    """
    
    try:
        observation_uuid = UUID(observation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de observación inválido")
    
    try:
        observation = ShiftObservationService.update_shift_observation(
            db, observation_uuid, observation_data, current_user
        )
        return observation
    except (NotFoundException, PermissionError, ValidationError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.delete('/{observation_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_shift_observation(
    observation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Eliminar (desactivar) una observación de turno.

    Solo se pueden eliminar observaciones que no han sido verificadas.
    La eliminación es lógica (soft delete).
    """
    
    try:
        observation_uuid = UUID(observation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de observación inválido")
    
    try:
        ShiftObservationService.delete_shift_observation(db, observation_uuid, current_user)
        return None
    except (NotFoundException, PermissionError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.post('/{observation_id}/verify', response_model=ShiftObservationResponse)
def verify_shift_observation(
    observation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Verificar una observación de turno.

    Marca la observación como verificada y cambia su estado a 'reviewed'.
    Solo se puede verificar una vez por observación.
    """
    
    try:
        observation_uuid = UUID(observation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de observación inválido")
    
    try:
        observation = ShiftObservationService.verify_shift_observation(
            db, observation_uuid, current_user
        )
        return observation
    except (NotFoundException, ValidationError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get('/cared-person/{cared_person_id}/summary', response_model=List[ShiftObservationSummary])
def get_observations_by_cared_person(
    cared_person_id: str,
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Límite de registros"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Obtener resumen de observaciones por persona bajo cuidado.

    Retorna un listado resumido de observaciones para una persona específica,
    útil para seguimiento clínico y reportes.
    """
    
    try:
        cared_person_uuid = UUID(cared_person_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de persona bajo cuidado inválido")
    
    try:
        summaries = ShiftObservationService.get_observations_by_cared_person(
            db, cared_person_uuid, skip, limit
        )
        return summaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}") 