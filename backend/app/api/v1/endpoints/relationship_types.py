from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.relationship_type import RelationshipTypeService
from app.schemas.relationship_type import RelationshipTypeCreate, RelationshipTypeUpdate, RelationshipTypeResponse

router = APIRouter()

@router.post('/', response_model=RelationshipTypeResponse, status_code=status.HTTP_201_CREATED)
def create_relationship_type(relationship_type: RelationshipTypeCreate, db: Session = Depends(get_db)):
    return RelationshipTypeService.create_relationship_type(db, relationship_type)

@router.get('/', response_model=List[RelationshipTypeResponse])
def get_relationship_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return RelationshipTypeService.get_relationship_types(db, skip, limit)

@router.get('/{relationship_type_id}', response_model=RelationshipTypeResponse)
def get_relationship_type(relationship_type_id: int, db: Session = Depends(get_db)):
    relationship_type = RelationshipTypeService.get_relationship_type(db, relationship_type_id)
    if not relationship_type:
        raise HTTPException(status_code=404, detail='RelationshipType not found')
    return relationship_type

@router.put('/{relationship_type_id}', response_model=RelationshipTypeResponse)
def update_relationship_type(relationship_type_id: int, relationship_type: RelationshipTypeUpdate, db: Session = Depends(get_db)):
    updated = RelationshipTypeService.update_relationship_type(db, relationship_type_id, relationship_type)
    if not updated:
        raise HTTPException(status_code=404, detail='RelationshipType not found')
    return updated

@router.delete('/{relationship_type_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_relationship_type(relationship_type_id: int, db: Session = Depends(get_db)):
    deleted = RelationshipTypeService.delete_relationship_type(db, relationship_type_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='RelationshipType not found') 