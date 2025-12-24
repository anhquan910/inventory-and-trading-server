from pydantic import BaseModel
from typing import List, Optional, Literal

class TransactionItemCreate(BaseModel):
    product_id: Optional[int] = None
    material_id: Optional[int] = None
    quantity: float
    unit_price: float

class TransactionCreate(BaseModel):
    customer_name: str
    items: List[TransactionItemCreate]
    type: Literal["RETAIL", "TRADE"]