from pydantic import BaseModel

class ComponentCreate(BaseModel):
    material_id: int
    quantity: float

class ComponentResponse(BaseModel):
    id: int
    material_name: str
    quantity_used: float
    cost_at_time_of_calculation: float

    class Config:
        from_attributes = True
  
class ProductionRun(BaseModel):
    quantity: int