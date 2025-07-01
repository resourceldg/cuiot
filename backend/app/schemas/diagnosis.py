from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class FileMeta(BaseModel):
    filename: str
    url: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None

class DiagnosisBase(BaseModel):
    diagnosis_text: str
    diagnosis_type: str = 'inicial'
    attachments: List[FileMeta] = []
    is_active: str = 'active'
    cared_person_id: UUID

class DiagnosisCreate(DiagnosisBase):
    pass

class DiagnosisUpdate(DiagnosisBase):
    pass

class DiagnosisResponse(DiagnosisBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by_id: UUID

    class Config:
        from_attributes = True 