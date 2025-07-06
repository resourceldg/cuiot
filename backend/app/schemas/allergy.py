from typing import Optional
from datetime import date
from pydantic import BaseModel, UUID4

class AllergyBase(BaseModel):
    allergen_name: str
    allergy_type: str
    severity: str
    reaction_description: Optional[str] = None
    diagnosis_date: Optional[date] = None

class AllergyCreate(AllergyBase):
    cared_person_id: UUID4

class AllergyUpdate(BaseModel):
    allergen_name: Optional[str] = None
    allergy_type: Optional[str] = None
    severity: Optional[str] = None
    reaction_description: Optional[str] = None
    diagnosis_date: Optional[date] = None

class Allergy(AllergyBase):
    id: UUID4
    cared_person_id: UUID4
    is_active: bool

    class Config:
        from_attributes = True
