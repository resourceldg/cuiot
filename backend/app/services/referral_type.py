from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.referral_type import ReferralType
from app.schemas.referral_type import ReferralTypeCreate, ReferralTypeUpdate

class ReferralTypeService:
    def __init__(self, db: Session):
        self.db = db

    def get_referral_types(self, skip: int = 0, limit: int = 100) -> List[ReferralType]:
        return self.db.query(ReferralType).offset(skip).limit(limit).all()

    def get_referral_type(self, referral_type_id: int) -> Optional[ReferralType]:
        return self.db.query(ReferralType).filter(ReferralType.id == referral_type_id).first()

    def create_referral_type(self, referral_type: ReferralTypeCreate) -> ReferralType:
        db_referral_type = ReferralType(**referral_type.dict())
        self.db.add(db_referral_type)
        self.db.commit()
        self.db.refresh(db_referral_type)
        return db_referral_type

    def update_referral_type(self, referral_type_id: int, referral_type: ReferralTypeUpdate) -> Optional[ReferralType]:
        db_referral_type = self.get_referral_type(referral_type_id)
        if not db_referral_type:
            return None
        
        update_data = referral_type.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_referral_type, field, value)
        
        self.db.commit()
        self.db.refresh(db_referral_type)
        return db_referral_type

    def delete_referral_type(self, referral_type_id: int) -> bool:
        db_referral_type = self.get_referral_type(referral_type_id)
        if not db_referral_type:
            return False
        
        self.db.delete(db_referral_type)
        self.db.commit()
        return True 