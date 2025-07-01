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
from app.services.auth import AuthService
from app.services.restraint_protocol import RestraintProtocolService
from app.schemas.restraint_protocol import (
    RestraintProtocolCreate, RestraintProtocolUpdate, RestraintProtocolResponse, 
    RestraintProtocolSummary
)
from app.models.user import User

router = APIRouter()
UPLOAD_DIR = 'uploads/restraint_protocols/'
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post('/', response_model=RestraintProtocolResponse, status_code=status.HTTP_201_CREATED)
def create_restraint_protocol(
    protocol_type: str = Form(..., description="Tipo de protocolo: physical, chemical, environmental, behavioral, mechanical, electronic, social, other"),
    title: str = Form(..., max_length=200, description="Título del protocolo"),
    description: Optional[str] = Form(None, description="Descripción detallada"),
    justification: str = Form(..., description="Justificación clínica requerida"),
    risk_assessment: Optional[str] = Form(None, description="Evaluación de riesgos"),
    start_date: str = Form(..., description="Fecha de inicio (ISO format)"),
    end_date: Optional[str] = Form(None, description="Fecha de fin (ISO format, opcional)"),
    review_frequency: Optional[str] = Form(None, description="Frecuencia de revisión: daily, weekly, biweekly, monthly, quarterly, as_needed"),
    next_review_date: Optional[str] = Form(None, description="Próxima fecha de revisión (ISO format)"),
    responsible_professional: str = Form(..., max_length=200, description="Profesional responsable"),
    professional_license: Optional[str] = Form(None, max_length=100, description="Licencia profesional"),
    supervising_doctor: Optional[str] = Form(None, max_length=200, description="Médico supervisor"),
    status: str = Form("active", description="Estado: active, suspended, completed, terminated, pending, under_review"),
    compliance_status: str = Form("compliant", description="Cumplimiento: compliant, non_compliant, under_review, pending_assessment"),
    notes: Optional[str] = Form(None, description="Notas adicionales"),
    cared_person_id: str = Form(..., description="ID de la persona bajo cuidado"),
    institution_id: Optional[int] = Form(None, description="ID de la institución (opcional)"),
    files: List[UploadFile] = File([], description="Archivos adjuntos (opcional)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Crear un nuevo protocolo de sujeción y prevención de incidentes.
    
    Este endpoint permite crear protocolos de seguridad para personas bajo cuidado,
    incluyendo sujeción física, química, ambiental y conductual.
    
    Requiere justificación clínica y supervisión profesional.
    """
    
    # Validate protocol_type before creating Pydantic model
    valid_protocol_types = ['physical', 'chemical', 'environmental', 'behavioral', 'mechanical', 'electronic', 'social', 'other']
    if protocol_type not in valid_protocol_types:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["body", "protocol_type"],
                    "msg": f"protocol_type debe ser uno de: {valid_protocol_types}",
                    "type": "value_error"
                }
            ]
        )
    
    # Parse dates
    try:
        start_date_parsed = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_date_parsed = None
        if end_date:
            end_date_parsed = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        next_review_date_parsed = None
        if next_review_date:
            next_review_date_parsed = datetime.fromisoformat(next_review_date.replace('Z', '+00:00'))
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
                'url': f'/static/restraint_protocols/{file_id}_{file.filename}',
                'content_type': file.content_type,
                'size': file.spool_max_size if hasattr(file, 'spool_max_size') else None
            })
    
    # Create protocol data
    try:
        protocol_data = RestraintProtocolCreate(
            protocol_type=protocol_type,
            title=title,
            description=description,
            justification=justification,
            risk_assessment=risk_assessment,
            start_date=start_date_parsed,
            end_date=end_date_parsed,
            review_frequency=review_frequency,
            next_review_date=next_review_date_parsed,
            responsible_professional=responsible_professional,
            professional_license=professional_license,
            supervising_doctor=supervising_doctor,
            status=status,
            compliance_status=compliance_status,
            notes=notes,
            cared_person_id=UUID(cared_person_id),
            institution_id=institution_id,
            attached_files=attached_files
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
        # Validate protocol data
        RestraintProtocolService.validate_protocol_data(protocol_data)
        
        # Create protocol
        protocol = RestraintProtocolService.create_restraint_protocol(
            db, protocol_data, current_user, attached_files
        )
        
        return protocol
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get('/', response_model=List[RestraintProtocolResponse])
def get_restraint_protocols(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    cared_person_id: Optional[UUID] = Query(None, description="Filtrar por persona bajo cuidado"),
    institution_id: Optional[int] = Query(None, description="Filtrar por institución"),
    protocol_type: Optional[str] = Query(None, description="Filtrar por tipo de protocolo"),
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    active_only: bool = Query(False, description="Solo protocolos activos"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Obtener lista de protocolos de sujeción con filtros opcionales.
    
    Permite filtrar por persona bajo cuidado, institución, tipo de protocolo,
    estado y obtener solo protocolos activos.
    """
    
    protocols = RestraintProtocolService.get_restraint_protocols(
        db, skip=skip, limit=limit, cared_person_id=cared_person_id,
        institution_id=institution_id, protocol_type=protocol_type,
        status=status, active_only=active_only
    )
    
    return protocols

@router.get('/{protocol_id}', response_model=RestraintProtocolResponse)
def get_restraint_protocol(
    protocol_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Obtener un protocolo de sujeción específico por ID.
    """
    
    protocol = RestraintProtocolService.get_restraint_protocol_by_id(db, protocol_id)
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocolo no encontrado")
    
    return protocol

@router.put('/{protocol_id}', response_model=RestraintProtocolResponse)
def update_restraint_protocol(
    protocol_id: UUID,
    protocol_update: RestraintProtocolUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Actualizar un protocolo de sujeción existente.
    
    Solo permite actualizar campos específicos manteniendo la trazabilidad.
    """
    
    protocol = RestraintProtocolService.update_restraint_protocol(
        db, protocol_id, protocol_update, current_user
    )
    
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocolo no encontrado")
    
    return protocol

@router.delete('/{protocol_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_restraint_protocol(
    protocol_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Eliminar un protocolo de sujeción.
    
    Solo administradores pueden eliminar protocolos.
    """
    
    if not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Solo administradores pueden eliminar protocolos")
    
    success = RestraintProtocolService.delete_restraint_protocol(db, protocol_id)
    if not success:
        raise HTTPException(status_code=404, detail="Protocolo no encontrado")

@router.post('/{protocol_id}/suspend', response_model=RestraintProtocolResponse)
def suspend_restraint_protocol(
    protocol_id: UUID,
    reason: str = Form(..., description="Razón de la suspensión"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Suspender un protocolo de sujeción activo.
    
    Requiere justificación clínica para la suspensión.
    """
    
    protocol = RestraintProtocolService.suspend_restraint_protocol(
        db, protocol_id, current_user, reason
    )
    
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocolo no encontrado")
    
    return protocol

@router.post('/{protocol_id}/complete', response_model=RestraintProtocolResponse)
def complete_restraint_protocol(
    protocol_id: UUID,
    completion_notes: str = Form(..., description="Notas de finalización"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Finalizar un protocolo de sujeción.
    
    Marca el protocolo como completado con fecha de fin y notas.
    """
    
    protocol = RestraintProtocolService.complete_restraint_protocol(
        db, protocol_id, current_user, completion_notes
    )
    
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocolo no encontrado")
    
    return protocol

@router.post('/{protocol_id}/compliance', response_model=RestraintProtocolResponse)
def update_compliance_status(
    protocol_id: UUID,
    compliance_status: str = Form(..., description="Nuevo estado de cumplimiento"),
    compliance_notes: Optional[str] = Form(None, description="Notas de cumplimiento"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Actualizar el estado de cumplimiento de un protocolo.
    
    Estados permitidos: compliant, non_compliant, under_review, pending_assessment
    """
    
    try:
        protocol = RestraintProtocolService.update_compliance_status(
            db, protocol_id, compliance_status, current_user, compliance_notes
        )
        
        if not protocol:
            raise HTTPException(status_code=404, detail="Protocolo no encontrado")
        
        return protocol
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/cared-person/{cared_person_id}', response_model=List[RestraintProtocolResponse])
def get_protocols_by_cared_person(
    cared_person_id: UUID,
    active_only: bool = Query(False, description="Solo protocolos activos"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Obtener todos los protocolos de sujeción de una persona bajo cuidado.
    """
    
    if active_only:
        protocols = RestraintProtocolService.get_active_restraint_protocols(db, cared_person_id)
    else:
        protocols = RestraintProtocolService.get_restraint_protocols(db, cared_person_id=cared_person_id)
    
    return protocols

@router.get('/requiring-review', response_model=List[RestraintProtocolResponse])
def get_protocols_requiring_review(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Obtener protocolos que requieren revisión.
    
    Lista protocolos activos cuya fecha de próxima revisión ha vencido.
    """
    
    protocols = RestraintProtocolService.get_protocols_requiring_review(db)
    return protocols

@router.get('/summary/overview', response_model=RestraintProtocolSummary)
def get_protocol_summary(
    cared_person_id: Optional[UUID] = Query(None, description="ID de persona bajo cuidado para filtrar"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """
    Obtener resumen estadístico de protocolos de sujeción.
    
    Incluye totales, protocolos activos, distribución por tipo y estado,
    y protocolos que requieren revisión.
    """
    
    summary = RestraintProtocolService.get_protocol_summary(db, cared_person_id)
    return summary 