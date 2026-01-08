from pydantic import BaseModel
from datetime import datetime
from typing import Optional
# Base schema with common attributes
class IncidentBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "Low"
# Schema for CREATING an incident (what the user sends)
class IncidentCreate(IncidentBase):
    pass
# Schema for READING an incident (what the API returns)
class Incident(IncidentBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        # Tells Pydantic to read data from SQLAlchemy models
        from_attributes = True

class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None