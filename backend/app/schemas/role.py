from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from .base import BaseResponse, BaseCreate, BaseUpdate

class RoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    permissions: Optional[str] = None  # JSON string
    is_system: bool = False

class RoleCreate(RoleBase, BaseCreate):
    pass

class RoleUpdate(RoleBase, BaseUpdate):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    is_system: Optional[bool] = None

class RoleResponse(RoleBase, BaseResponse):
    pass

class RoleInDB(RoleBase, BaseResponse):
    pass
