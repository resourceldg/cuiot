from sqlalchemy.orm import Session
from app.models.diagnosis import Diagnosis
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisUpdate
from app.models.user import User
from fastapi import HTTPException
from datetime import datetime
from uuid import UUID

class DiagnosisService:
    @staticmethod
    def create_diagnosis(db: Session, diagnosis_data: DiagnosisCreate, user: User):
        diagnosis = Diagnosis(
            diagnosis_name=diagnosis_data.diagnosis_name,
            description=diagnosis_data.description,
            severity_level=diagnosis_data.severity_level,
            diagnosis_date=diagnosis_data.diagnosis_date,
            doctor_name=diagnosis_data.doctor_name,
            medical_notes=diagnosis_data.medical_notes,
            cie10_code=diagnosis_data.cie10_code,
            attachments=[a.model_dump() for a in (diagnosis_data.attachments or [])],
            is_active=diagnosis_data.is_active,
            cared_person_id=diagnosis_data.cared_person_id,
            created_by_id=user.id,
            created_at=datetime.utcnow()
        )
        db.add(diagnosis)
        db.commit()
        db.refresh(diagnosis)
        return diagnosis

    @staticmethod
    def get_diagnoses(db: Session, cared_person_id: str = None, skip: int = 0, limit: int = 100):
        query = db.query(Diagnosis)
        if cared_person_id:
            query = query.filter(Diagnosis.cared_person_id == cared_person_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def list_diagnoses(db: Session, cared_person_id: UUID = None):
        query = db.query(Diagnosis)
        if cared_person_id:
            query = query.filter(Diagnosis.cared_person_id == cared_person_id)
        return query.all()

    @staticmethod
    def get_diagnosis(db: Session, diagnosis_id: UUID):
        diagnosis = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
        if not diagnosis:
            raise HTTPException(status_code=404, detail='Diagnóstico no encontrado')
        return diagnosis

    @staticmethod
    def update_diagnosis(db: Session, diagnosis_id: str, diagnosis_update: DiagnosisUpdate, user: User):
        diagnosis = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
        if not diagnosis:
            return None
        for field, value in diagnosis_update.model_dump(exclude_unset=True).items():
            setattr(diagnosis, field, value)
        diagnosis.updated_by_id = user.id
        diagnosis.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(diagnosis)
        return diagnosis

    @staticmethod
    def delete_diagnosis(db: Session, diagnosis_id: UUID):
        diagnosis = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
        if not diagnosis:
            raise HTTPException(status_code=404, detail='Diagnóstico no encontrado')
        db.delete(diagnosis)
        db.commit()
        return True

    @staticmethod
    def get_diagnosis_by_id(db: Session, diagnosis_id: str):
        return db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()

    @staticmethod
    def get_diagnoses_by_cared_person(db: Session, cared_person_id: str):
        return db.query(Diagnosis).filter(Diagnosis.cared_person_id == cared_person_id).all() 