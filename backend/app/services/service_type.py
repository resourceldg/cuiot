from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.service_type import ServiceType
from app.schemas.service_type import ServiceTypeCreate, ServiceTypeUpdate

class ServiceTypeService:
    def __init__(self, db: Session):
        self.db = db

    def get_service_types(self, skip: int = 0, limit: int = 100) -> List[ServiceType]:
        return self.db.query(ServiceType).offset(skip).limit(limit).all()

    def get_service_type(self, service_type_id: int) -> Optional[ServiceType]:
        return self.db.query(ServiceType).filter(ServiceType.id == service_type_id).first()

    def create_service_type(self, service_type: ServiceTypeCreate) -> ServiceType:
        db_service_type = ServiceType(**service_type.dict())
        self.db.add(db_service_type)
        self.db.commit()
        self.db.refresh(db_service_type)
        return db_service_type

    def update_service_type(self, service_type_id: int, service_type: ServiceTypeUpdate) -> Optional[ServiceType]:
        db_service_type = self.get_service_type(service_type_id)
        if not db_service_type:
            return None
        
        update_data = service_type.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_service_type, field, value)
        
        self.db.commit()
        self.db.refresh(db_service_type)
        return db_service_type

    def delete_service_type(self, service_type_id: int) -> bool:
        db_service_type = self.get_service_type(service_type_id)
        if not db_service_type:
            return False
        
        self.db.delete(db_service_type)
        self.db.commit()
        return True 