from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.production import ProductionLog
from pydantic import BaseModel
from datetime import datetime

# Production job history endpoints.
router = APIRouter()

class JobResponse(BaseModel):
    id: int
    product_name: str
    quantity: int
    total_cost: float
    created_at: datetime
    created_by: str

    class Config:
        from_attributes = True

@router.get("/jobs", response_model=List[JobResponse])
def get_production_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Fetch production log entries and build the response payload.
    logs = db.query(ProductionLog).order_by(ProductionLog.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        JobResponse(
            id=log.id,
            product_name=log.product.name,
            quantity=log.quantity_produced,
            total_cost=log.total_cost,
            created_at=log.created_at,
            created_by=log.creator.email if log.creator else "System"
        )
        for log in logs
    ]