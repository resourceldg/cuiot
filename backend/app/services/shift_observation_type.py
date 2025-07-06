from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.shift_observation_type import ShiftObservationType
from app.schemas.shift_observation_type import ShiftObservationTypeCreate, ShiftObservationTypeUpdate

class ShiftObservationTypeService:
    def __init__(self, db: Session):
        self.db = db

    def get_shift_observation_types(self, skip: int = 0, limit: int = 100) -> List[ShiftObservationType]:
        return self.db.query(ShiftObservationType).offset(skip).limit(limit).all()

    def get_shift_observation_type(self, shift_observation_type_id: int) -> Optional[ShiftObservationType]:
        return self.db.query(ShiftObservationType).filter(ShiftObservationType.id == shift_observation_type_id).first()

    def create_shift_observation_type(self, shift_observation_type: ShiftObservationTypeCreate) -> ShiftObservationType:
        db_shift_observation_type = ShiftObservationType(**shift_observation_type.dict())
        self.db.add(db_shift_observation_type)
        self.db.commit()
        self.db.refresh(db_shift_observation_type)
        return db_shift_observation_type

    def update_shift_observation_type(self, shift_observation_type_id: int, shift_observation_type: ShiftObservationTypeUpdate) -> Optional[ShiftObservationType]:
        db_shift_observation_type = self.get_shift_observation_type(shift_observation_type_id)
        if not db_shift_observation_type:
            return None
        
        update_data = shift_observation_type.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_shift_observation_type, field, value)
        
        self.db.commit()
        self.db.refresh(db_shift_observation_type)
        return db_shift_observation_type

    def delete_shift_observation_type(self, shift_observation_type_id: int) -> bool:
        db_shift_observation_type = self.get_shift_observation_type(shift_observation_type_id)
        if not db_shift_observation_type:
            return False
        
        self.db.delete(db_shift_observation_type)
        self.db.commit()
        return True 