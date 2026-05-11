from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.inventory import Material
from app.models.user import User
from app.schemas.inventory import AuditSubmission, MaterialCreate, MaterialResponse, MaterialUpdate

# Inventory management endpoints for material stock and audits.
router = APIRouter()

@router.get("/", response_model=List[MaterialResponse])
def read_materials(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    # Retrieve a paged list of materials in inventory.
    materials = db.query(Material).offset(skip).limit(limit).all()
    return materials

@router.post("/", response_model=MaterialResponse)
def create_material(
    material_in: MaterialCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    material = Material(**material_in.model_dump())
    db.add(material)
    db.commit()
    db.refresh(material)
    return material

@router.patch("/{material_id}", response_model=MaterialResponse)
def update_material(
    material_id: int, 
    material_in: MaterialUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    # Update fields only if provided
    update_data = material_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(material, key, value)
        
    db.add(material)
    db.commit()
    db.refresh(material)
    return material

@router.post("/audit")
def submit_stocktake_audit(
    audit: AuditSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Apply stocktake audit adjustments for inventory materials.
    updated_count = 0
    
    for item in audit.items:
        material = db.query(Material).filter(Material.id == item.material_id).first()
        if not material:
            continue
            
        if material.current_stock != item.counted_quantity:
            material.current_stock = item.counted_quantity
            material.last_updated = func.now()
            updated_count += 1
            
    db.commit()
    return {"status": "success", "updated_items": updated_count}