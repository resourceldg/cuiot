from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.report import ReportCreate, ReportResponse, ReportUpdate
from app.models.report import Report
from app.models.user import User
from app.services.auth import AuthService
from app.models.cared_person import CaredPerson
import shutil, os, uuid
from fastapi.encoders import jsonable_encoder
from app.services.audit_log import log_change
import json

router = APIRouter()
UPLOAD_DIR = 'uploads/reports/'
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post('/', response_model=ReportResponse)
def create_report(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    report_type: str = Form('general'),
    is_autocuidado: bool = Form(False),
    cared_person_id: Optional[int] = Form(None),
    files: List[UploadFile] = File([]),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_active_user)
):
    if not is_autocuidado and not cared_person_id:
        raise HTTPException(status_code=400, detail='Debe asociar el reporte a una persona bajo cuidado.')
    attached_files = []
    if files:
        for file in files:
            file_id = str(uuid.uuid4())
            file_path = os.path.join(UPLOAD_DIR, file_id + '_' + file.filename)
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file.file, f)
            attached_files.append({
                'filename': file.filename,
                'url': f'/static/reports/{file_id}_{file.filename}',
                'content_type': file.content_type,
                'size': file.spool_max_size if hasattr(file, 'spool_max_size') else None
            })
    report = Report(
        title=title,
        description=description,
        report_type=report_type,
        attached_files=attached_files,
        is_autocuidado=is_autocuidado,
        cared_person_id=cared_person_id,
        created_by_id=current_user.id
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    log_change(db, 'Report', report.id, 'create', current_user.id, old_data=None, new_data=report.__dict__, description='Creación de reporte')
    return report

@router.get('/', response_model=List[ReportResponse])
def list_reports(db: Session = Depends(get_db), current_user: User = Depends(AuthService.get_current_active_user)):
    reports = db.query(Report).all()
    result = []
    for report in reports:
        data = jsonable_encoder(report)
        if report.cared_person_id:
            cared_person = db.query(CaredPerson).filter(CaredPerson.id == report.cared_person_id).first()
            data['cared_person'] = cared_person
        else:
            data['cared_person'] = None
        result.append(data)
    return result

@router.get('/{report_id}', response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db), current_user: User = Depends(AuthService.get_current_active_user)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail='Reporte no encontrado')
    return report

@router.put('/{report_id}', response_model=ReportResponse)
def update_report(report_id: int, report_update: ReportUpdate, db: Session = Depends(get_db), current_user: User = Depends(AuthService.get_current_active_user)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail='Reporte no encontrado')
    old_data = report.__dict__.copy()
    for field, value in report_update.dict(exclude_unset=True).items():
        setattr(report, field, value)
    db.commit()
    db.refresh(report)
    log_change(db, 'Report', report.id, 'update', current_user.id, old_data=old_data, new_data=report.__dict__, description='Actualización de reporte')
    return report

@router.delete('/{report_id}', response_model=dict)
def delete_report(report_id: int, db: Session = Depends(get_db), current_user: User = Depends(AuthService.get_current_active_user)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail='Reporte no encontrado')
    old_data = report.__dict__.copy()
    db.delete(report)
    db.commit()
    log_change(db, 'Report', report_id, 'delete', current_user.id, old_data=old_data, new_data=None, description='Eliminación de reporte')
    return {"ok": True} 