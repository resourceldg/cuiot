from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from app.schemas.cared_person import CaredPersonResponse

class FileMeta(BaseModel):
    filename: str
    url: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None

class ReportBase(BaseModel):
    title: str
    description: Optional[str] = None
    report_type: str = 'general'
    attached_files: List[FileMeta] = []
    is_autocuidado: bool = False
    cared_person_id: Optional[int] = None

class ReportCreate(ReportBase):
    pass

class ReportUpdate(ReportBase):
    pass

class ReportResponse(ReportBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by_id: int
    cared_person: Optional[CaredPersonResponse] = None

    class Config:
        orm_mode = True 