from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisResponse, DiagnosisUpdate
from app.models.diagnosis import Diagnosis
from app.models.user import User
from app.services.auth import AuthService
from app.services.diagnosis import DiagnosisService
import shutil, os, uuid
from fastapi.encoders import jsonable_encoder
from datetime import datetime

router = APIRouter()
UPLOAD_DIR = 'uploads/diagnoses/'
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post('/', response_model=DiagnosisResponse)
def create_diagnosis(
    diagnosis_text: str = Form(...),
    diagnosis_type: str = Form('inicial'),
    cared_person_id: str = Form(...),
    files: List[UploadFile] = File([]),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    attachments = []
    if files:
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
        diagnosis_text=diagnosis_text,
        diagnosis_type=diagnosis_type,
        cared_person_id=cared_person_id,
        attachments=attachments
    )
    diagnosis = DiagnosisService.create_diagnosis(db, diagnosis_data, current_user)
    return diagnosis

@router.get('/', response_model=List[DiagnosisResponse])
def list_diagnoses(cared_person_id: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(AuthService.get_current_active_user)):
    diagnoses = DiagnosisService.list_diagnoses(db, cared_person_id)
    return diagnoses

@router.get('/{diagnosis_id}', response_model=DiagnosisResponse)
def get_diagnosis(diagnosis_id: str, db: Session = Depends(get_db), current_user: User = Depends(AuthService.get_current_active_user)):
    diagnosis = DiagnosisService.get_diagnosis(db, diagnosis_id)
    return diagnosis

@router.put('/{diagnosis_id}', response_model=DiagnosisResponse)
def update_diagnosis(diagnosis_id: str, diagnosis_update: DiagnosisUpdate, db: Session = Depends(get_db), current_user: User = Depends(AuthService.get_current_active_user)):
    diagnosis = DiagnosisService.update_diagnosis(db, diagnosis_id, diagnosis_update, current_user)
    return diagnosis

@router.delete('/{diagnosis_id}', response_model=dict)
def delete_diagnosis(diagnosis_id: str, db: Session = Depends(get_db), current_user: User = Depends(AuthService.get_current_active_user)):
    DiagnosisService.delete_diagnosis(db, diagnosis_id)
    return {"ok": True} 