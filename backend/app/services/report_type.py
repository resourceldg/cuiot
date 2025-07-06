from sqlalchemy.orm import Session
from app.models.report_type import ReportType
from app.schemas.report_type import ReportTypeCreate, ReportTypeUpdate
from typing import List, Optional

class ReportTypeService:
    @staticmethod
    def create_report_type(db: Session, report_type: ReportTypeCreate) -> ReportType:
        db_report_type = ReportType(**report_type.model_dump())
        db.add(db_report_type)
        db.commit()
        db.refresh(db_report_type)
        return db_report_type

    @staticmethod
    def get_report_type(db: Session, report_type_id: int) -> Optional[ReportType]:
        return db.query(ReportType).filter(ReportType.id == report_type_id).first()

    @staticmethod
    def get_report_types(db: Session, skip: int = 0, limit: int = 100) -> List[ReportType]:
        return db.query(ReportType).offset(skip).limit(limit).all()

    @staticmethod
    def update_report_type(db: Session, report_type_id: int, report_type: ReportTypeUpdate) -> Optional[ReportType]:
        db_report_type = db.query(ReportType).filter(ReportType.id == report_type_id).first()
        if db_report_type:
            update_data = report_type.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_report_type, field, value)
            db.commit()
            db.refresh(db_report_type)
        return db_report_type

    @staticmethod
    def delete_report_type(db: Session, report_type_id: int) -> bool:
        db_report_type = db.query(ReportType).filter(ReportType.id == report_type_id).first()
        if db_report_type:
            db.delete(db_report_type)
            db.commit()
            return True
        return False 