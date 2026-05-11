from pydantic import BaseModel

# Schemas for production recipes and run requests.
class ComponentCreate(BaseModel):
    material_id: int  # ID of the material to include in the recipe.
    quantity: float  # Quantity of the material required per unit of product.

class ComponentResponse(BaseModel):
    id: int  # Unique identifier for the component.
    material_name: str  # Name of the material.
    quantity_used: float  # Quantity used in the recipe.
    cost_at_time_of_calculation: float  # Cost per unit at the time of calculation.

    class Config:
        from_attributes = True
  
class ProductionRun(BaseModel):
    quantity: int