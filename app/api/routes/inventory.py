from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.inventory import Material
from app.schemas.inventory import MaterialCreate, MaterialResponse, MaterialUpdate

router = APIRouter()

@router.get("/", response_model=List[MaterialResponse])
def read_materials(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
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