from sqlalchemy.orm import Session
from app.models.report import Report
from app.schemas.report import ReportCreate
from app.models.user import User
from fastapi import HTTPException

class ReportService:
    @staticmethod
    def create_report(db: Session, report_data: ReportCreate, user: User):
        if not report_data.is_autocuidado and not report_data.cared_person_id:
            raise HTTPException(status_code=400, detail='Debe asociar el reporte a una persona bajo cuidado.')
        report = Report(
            title=report_data.title,
            description=report_data.description,
            report_type=report_data.report_type,
            attached_files=[file.model_dump() for file in report_data.attached_files],
            is_autocuidado=report_data.is_autocuidado,
            cared_person_id=report_data.cared_person_id,
            created_by_id=user.id
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def list_reports(db: Session):
        return db.query(Report).all()

    @staticmethod
    def get_report(db: Session, report_id: int):
        report = db.query(Report).filter(Report.id == report_id).first()
        if not report:
            raise HTTPException(status_code=404, detail='Reporte no encontrado')
        return report 