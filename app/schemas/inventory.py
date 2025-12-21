from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Shared properties
class MaterialBase(BaseModel):
    name: str
    sku: Optional[str] = None
    description: Optional[str] = None
    category: str
    unit_of_measure: str = "grams"
    reorder_level: float = 10.0
    cost_per_unit: float = 0.0
    preferred_vendor: Optional[str] = None

class MaterialCreate(MaterialBase):
    current_stock: float = 0.0

class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    current_stock: Optional[float] = None
    cost_per_unit: Optional[float] = None
    reorder_level: Optional[float] = None
    preferred_vendor: Optional[str] = None

class MaterialResponse(MaterialBase):
    id: int
    current_stock: float
    last_updated: datetime

    class Config:
        from_attributes = True