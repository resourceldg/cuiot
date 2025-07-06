from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.medication_log import MedicationLog
from app.schemas.medication_log import MedicationLogCreate, MedicationLogUpdate
from app.core.exceptions import NotFoundException

class MedicationLogService:
    @staticmethod
    def create(db: Session, medication_log: MedicationLogCreate) -> MedicationLog:
        """Create a new medication log entry"""
        db_medication_log = MedicationLog(**medication_log.model_dump())
        db.add(db_medication_log)
        db.commit()
        db.refresh(db_medication_log)
        return db_medication_log

    @staticmethod
    def get_by_id(db: Session, log_id: UUID) -> Optional[MedicationLog]:
        """Get medication log by ID"""
        return db.query(MedicationLog).filter(MedicationLog.id == log_id).first()

    @staticmethod
    def get_by_schedule_id(db: Session, schedule_id: UUID) -> List[MedicationLog]:
        """Get all medication logs for a specific schedule"""
        return db.query(MedicationLog).filter(
            MedicationLog.medication_schedule_id == schedule_id
        ).order_by(MedicationLog.taken_at.desc()).all()

    @staticmethod
    def get_by_cared_person_id(db: Session, cared_person_id: UUID, limit: int = 100) -> List[MedicationLog]:
        """Get medication logs for a cared person"""
        from app.models.medication_schedule import MedicationSchedule
        
        return db.query(MedicationLog).join(MedicationSchedule).filter(
            MedicationSchedule.cared_person_id == cared_person_id
        ).order_by(MedicationLog.taken_at.desc()).limit(limit).all()

    @staticmethod
    def get_recent_logs(db: Session, cared_person_id: UUID, days: int = 7) -> List[MedicationLog]:
        """Get recent medication logs for a cared person"""
        from datetime import datetime, timedelta
        from app.models.medication_schedule import MedicationSchedule
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        return db.query(MedicationLog).join(MedicationSchedule).filter(
            and_(
                MedicationSchedule.cared_person_id == cared_person_id,
                MedicationLog.taken_at >= cutoff_date
            )
        ).order_by(MedicationLog.taken_at.desc()).all()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[MedicationLog]:
        """Get all medication logs"""
        return db.query(MedicationLog).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, log_id: UUID, medication_log: MedicationLogUpdate) -> MedicationLog:
        """Update medication log"""
        db_medication_log = MedicationLogService.get_by_id(db, log_id)
        if not db_medication_log:
            raise NotFoundException(f"Medication log with id {log_id} not found")
        
        update_data = medication_log.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_medication_log, field, value)
        
        db.commit()
        db.refresh(db_medication_log)
        return db_medication_log

    @staticmethod
    def delete(db: Session, log_id: UUID) -> bool:
        """Delete medication log"""
        db_medication_log = MedicationLogService.get_by_id(db, log_id)
        if not db_medication_log:
            raise NotFoundException(f"Medication log with id {log_id} not found")
        
        db.delete(db_medication_log)
        db.commit()
        return True 