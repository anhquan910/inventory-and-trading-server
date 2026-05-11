from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Pydantic schemas for material inventory management.
# Shared properties
class MaterialBase(BaseModel):
    name: str  # Name of the material.
    sku: Optional[str] = None  # Stock Keeping Unit identifier.
    description: Optional[str] = None  # Description of the material.
    category: str  # Category classification (e.g., Metal, Gemstone).
    unit_of_measure: str = "grams"  # Unit for measuring quantity.
    reorder_level: float = 10.0  # Minimum stock level before reordering.
    cost_per_unit: float = 0.0  # Cost per unit of the material.
    preferred_vendor: Optional[str] = None  # Preferred supplier for the material.

class MaterialCreate(MaterialBase):
    current_stock: float = 0.0  # Initial stock quantity when creating the material.

class MaterialUpdate(BaseModel):
    name: Optional[str] = None  # Updated name of the material.
    sku: Optional[str] = None  # Updated SKU.
    description: Optional[str] = None  # Updated description.
    category: Optional[str] = None  # Updated category.
    current_stock: Optional[float] = None  # Updated current stock level.
    cost_per_unit: Optional[float] = None  # Updated cost per unit.
    reorder_level: Optional[float] = None  # Updated reorder level.
    preferred_vendor: Optional[str] = None  # Updated preferred vendor.

class MaterialResponse(MaterialBase):
    id: int  # Unique identifier for the material.
    current_stock: float  # Current stock quantity.
    last_updated: datetime  # Timestamp of last update.

    class Config:
        from_attributes = True

class AuditItem(BaseModel):
    material_id: int  # ID of the material being audited.
    counted_quantity: float  # Actual counted quantity during stocktake.
    reason: Optional[str] = "Stocktake Adjustment"  # Reason for the adjustment.

class AuditSubmission(BaseModel):
    items: List[AuditItem]  # List of audit items for the stocktake submission.