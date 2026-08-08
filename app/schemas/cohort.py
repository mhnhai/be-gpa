from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CohortBase(BaseModel):
    code: str
    name: Optional[str] = None
    is_active: bool = True


class CohortCreate(CohortBase):
    pass


class CohortUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None


class CohortResponse(CohortBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
