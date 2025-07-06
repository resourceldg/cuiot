from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.caregiver_assignment_type import CaregiverAssignmentType
from app.schemas.caregiver_assignment_type import CaregiverAssignmentTypeCreate, CaregiverAssignmentTypeUpdate

class CaregiverAssignmentTypeService:
    def __init__(self, db: Session):
        self.db = db

    def get_caregiver_assignment_types(self, skip: int = 0, limit: int = 100) -> List[CaregiverAssignmentType]:
        return self.db.query(CaregiverAssignmentType).offset(skip).limit(limit).all()

    def get_caregiver_assignment_type(self, caregiver_assignment_type_id: int) -> Optional[CaregiverAssignmentType]:
        return self.db.query(CaregiverAssignmentType).filter(CaregiverAssignmentType.id == caregiver_assignment_type_id).first()

    def create_caregiver_assignment_type(self, caregiver_assignment_type: CaregiverAssignmentTypeCreate) -> CaregiverAssignmentType:
        db_caregiver_assignment_type = CaregiverAssignmentType(**caregiver_assignment_type.dict())
        self.db.add(db_caregiver_assignment_type)
        self.db.commit()
        self.db.refresh(db_caregiver_assignment_type)
        return db_caregiver_assignment_type

    def update_caregiver_assignment_type(self, caregiver_assignment_type_id: int, caregiver_assignment_type: CaregiverAssignmentTypeUpdate) -> Optional[CaregiverAssignmentType]:
        db_caregiver_assignment_type = self.get_caregiver_assignment_type(caregiver_assignment_type_id)
        if not db_caregiver_assignment_type:
            return None
        
        update_data = caregiver_assignment_type.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_caregiver_assignment_type, field, value)
        
        self.db.commit()
        self.db.refresh(db_caregiver_assignment_type)
        return db_caregiver_assignment_type

    def delete_caregiver_assignment_type(self, caregiver_assignment_type_id: int) -> bool:
        db_caregiver_assignment_type = self.get_caregiver_assignment_type(caregiver_assignment_type_id)
        if not db_caregiver_assignment_type:
            return False
        
        self.db.delete(db_caregiver_assignment_type)
        self.db.commit()
        return True 