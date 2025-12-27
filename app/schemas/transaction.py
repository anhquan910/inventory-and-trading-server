from datetime import datetime
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
    amount_paid: float

class TransactionResponse(BaseModel):
    id: int
    transaction_type: str
    customer_name: str
    total_amount: float
    amount_paid: float
    balance_due: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True