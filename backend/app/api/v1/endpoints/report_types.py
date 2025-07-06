from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.report_type import ReportTypeService
from app.schemas.report_type import ReportTypeCreate, ReportTypeUpdate, ReportTypeResponse

router = APIRouter()

@router.post('/', response_model=ReportTypeResponse, status_code=status.HTTP_201_CREATED)
def create_report_type(report_type: ReportTypeCreate, db: Session = Depends(get_db)):
    return ReportTypeService.create_report_type(db, report_type)

@router.get('/', response_model=List[ReportTypeResponse])
def get_report_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ReportTypeService.get_report_types(db, skip, limit)

@router.get('/{report_type_id}', response_model=ReportTypeResponse)
def get_report_type(report_type_id: int, db: Session = Depends(get_db)):
    report_type = ReportTypeService.get_report_type(db, report_type_id)
    if not report_type:
        raise HTTPException(status_code=404, detail='ReportType not found')
    return report_type

@router.put('/{report_type_id}', response_model=ReportTypeResponse)
def update_report_type(report_type_id: int, report_type: ReportTypeUpdate, db: Session = Depends(get_db)):
    updated = ReportTypeService.update_report_type(db, report_type_id, report_type)
    if not updated:
        raise HTTPException(status_code=404, detail='ReportType not found')
    return updated

@router.delete('/{report_type_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_report_type(report_type_id: int, db: Session = Depends(get_db)):
    deleted = ReportTypeService.delete_report_type(db, report_type_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='ReportType not found') 