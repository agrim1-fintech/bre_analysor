# schemas/domain.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DomainBase(BaseModel):
    domain_name: str = Field(..., min_length=1, max_length=50)
    domain_key: str = Field(..., min_length=3, max_length=255)
    # database_name: str = Field(..., min_length=1, max_length=100)


class DomainCreate(DomainBase):
    pass

# 🔹 Update Schema
class DomainUpdate(BaseModel):
    domain_name: Optional[str] = None
    domain_key: Optional[str] = None
    # database_name: Optional[str] = None
    is_active: Optional[bool] = None

# 🔹 Response Schema
class DomainResponse(DomainBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # ✅ Pydantic v2    