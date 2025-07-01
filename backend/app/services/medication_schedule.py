from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.medication_schedule import MedicationSchedule
from app.schemas.medication_schedule import MedicationScheduleCreate, MedicationScheduleUpdate
from app.core.exceptions import NotFoundException

class MedicationScheduleService:
    @staticmethod
    def create(db: Session, medication_schedule: MedicationScheduleCreate) -> MedicationSchedule:
        """Create a new medication schedule"""
        db_medication_schedule = MedicationSchedule(**medication_schedule.dict())
        db.add(db_medication_schedule)
        db.commit()
        db.refresh(db_medication_schedule)
        return db_medication_schedule

    @staticmethod
    def get_by_id(db: Session, schedule_id: UUID) -> Optional[MedicationSchedule]:
        """Get medication schedule by ID"""
        return db.query(MedicationSchedule).filter(
            and_(
                MedicationSchedule.id == schedule_id,
                MedicationSchedule.is_active == 'active'
            )
        ).first()

    @staticmethod
    def get_by_cared_person_id(db: Session, cared_person_id: UUID) -> List[MedicationSchedule]:
        """Get all medication schedules for a cared person"""
        return db.query(MedicationSchedule).filter(
            and_(
                MedicationSchedule.cared_person_id == cared_person_id,
                MedicationSchedule.is_active == 'active'
            )
        ).all()

    @staticmethod
    def get_active_schedules(db: Session, cared_person_id: UUID) -> List[MedicationSchedule]:
        """Get active medication schedules for a cared person"""
        from datetime import date
        today = date.today()
        
        return db.query(MedicationSchedule).filter(
            and_(
                MedicationSchedule.cared_person_id == cared_person_id,
                MedicationSchedule.is_active == 'active',
                MedicationSchedule.start_date <= today,
                (MedicationSchedule.end_date.is_(None) | (MedicationSchedule.end_date >= today))
            )
        ).all()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[MedicationSchedule]:
        """Get all active medication schedules"""
        return db.query(MedicationSchedule).filter(
            MedicationSchedule.is_active == 'active'
        ).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, schedule_id: UUID, medication_schedule: MedicationScheduleUpdate) -> MedicationSchedule:
        """Update medication schedule"""
        db_medication_schedule = MedicationScheduleService.get_by_id(db, schedule_id)
        if not db_medication_schedule:
            raise NotFoundException(f"Medication schedule with id {schedule_id} not found")
        
        update_data = medication_schedule.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_medication_schedule, field, value)
        
        db.commit()
        db.refresh(db_medication_schedule)
        return db_medication_schedule

    @staticmethod
    def delete(db: Session, schedule_id: UUID) -> bool:
        """Soft delete medication schedule"""
        db_medication_schedule = MedicationScheduleService.get_by_id(db, schedule_id)
        if not db_medication_schedule:
            raise NotFoundException(f"Medication schedule with id {schedule_id} not found")
        
        db_medication_schedule.is_active = 'inactive'
        db.commit()
        return True 