from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.care_type import CareTypeService
from app.schemas.care_type import CareTypeCreate, CareTypeUpdate, CareTypeResponse

router = APIRouter()

@router.post('/', response_model=CareTypeResponse, status_code=status.HTTP_201_CREATED)
def create_care_type(care_type: CareTypeCreate, db: Session = Depends(get_db)):
    return CareTypeService.create_care_type(db, care_type)

@router.get('/', response_model=List[CareTypeResponse])
def get_care_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return CareTypeService.get_care_types(db, skip, limit)

@router.get('/{care_type_id}', response_model=CareTypeResponse)
def get_care_type(care_type_id: int, db: Session = Depends(get_db)):
    care_type = CareTypeService.get_care_type(db, care_type_id)
    if not care_type:
        raise HTTPException(status_code=404, detail='CareType not found')
    return care_type

@router.put('/{care_type_id}', response_model=CareTypeResponse)
def update_care_type(care_type_id: int, care_type: CareTypeUpdate, db: Session = Depends(get_db)):
    updated = CareTypeService.update_care_type(db, care_type_id, care_type)
    if not updated:
        raise HTTPException(status_code=404, detail='CareType not found')
    return updated

@router.delete('/{care_type_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_care_type(care_type_id: int, db: Session = Depends(get_db)):
    deleted = CareTypeService.delete_care_type(db, care_type_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='CareType not found') 