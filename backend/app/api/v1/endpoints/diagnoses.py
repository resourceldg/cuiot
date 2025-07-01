from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.diagnosis import DiagnosisCreate, Diagnosis, DiagnosisUpdate, AttachmentMeta
from app.models.diagnosis import Diagnosis as DiagnosisModel
from app.models.user import User
from app.services.auth import AuthService
from app.services.diagnosis import DiagnosisService
import shutil, os, uuid
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from uuid import UUID

router = APIRouter()
UPLOAD_DIR = 'uploads/diagnoses/'
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post('/', response_model=Diagnosis)
def create_diagnosis(
    diagnosis_name: str = Form(...),
    description: Optional[str] = Form(None),
    severity_level: Optional[str] = Form(None),
    diagnosis_date: Optional[str] = Form(None),
    doctor_name: Optional[str] = Form(None),
    medical_notes: Optional[str] = Form(None),
    cie10_code: Optional[str] = Form(None),
    cared_person_id: str = Form(...),
    is_active: bool = Form(True),
    files: List[UploadFile] = File([]),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    attachments = []
    for file in files:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, file_id + '_' + file.filename)
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        attachments.append({
            'filename': file.filename,
            'url': f'/static/diagnoses/{file_id}_{file.filename}',
            'content_type': file.content_type,
            'size': file.spool_max_size if hasattr(file, 'spool_max_size') else None
        })
    diagnosis_data = DiagnosisCreate(
        diagnosis_name=diagnosis_name,
        description=description,
        severity_level=severity_level,
        diagnosis_date=diagnosis_date,
        doctor_name=doctor_name,
        medical_notes=medical_notes,
        cie10_code=cie10_code,
        attachments=[AttachmentMeta(**a) for a in attachments],
        is_active=is_active,
        cared_person_id=UUID(cared_person_id)
    )
    diagnosis = DiagnosisService.create_diagnosis(db, diagnosis_data, current_user)
    return diagnosis

@router.get('/', response_model=List[Diagnosis])
def get_diagnoses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all diagnoses"""
    return DiagnosisService.get_diagnoses(db, skip=skip, limit=limit)

@router.get('/{diagnosis_id}', response_model=Diagnosis)
def get_diagnosis(
    diagnosis_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific diagnosis by ID"""
    diagnosis = DiagnosisService.get_diagnosis_by_id(db, diagnosis_id)
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return diagnosis

@router.put('/{diagnosis_id}', response_model=Diagnosis)
def update_diagnosis(
    diagnosis_id: UUID,
    diagnosis_update: DiagnosisUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    """Update a diagnosis"""
    diagnosis = DiagnosisService.update_diagnosis(db, diagnosis_id, diagnosis_update, current_user)
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return diagnosis

@router.delete('/{diagnosis_id}')
def delete_diagnosis(
    diagnosis_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a diagnosis"""
    success = DiagnosisService.delete_diagnosis(db, diagnosis_id)
    if not success:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return {"message": "Diagnosis deleted successfully"}

@router.get('/cared-person/{cared_person_id}', response_model=List[Diagnosis])
def get_diagnoses_by_cared_person(
    cared_person_id: UUID,
    db: Session = Depends(get_db)
):
    """Get all diagnoses for a specific cared person"""
    return DiagnosisService.get_diagnoses_by_cared_person(db, cared_person_id) 