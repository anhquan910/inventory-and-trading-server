from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.models.production import ProductMaterial
from app.models.inventory import Material
from app.schemas.production import ComponentCreate, ComponentResponse, ProductionRun

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def read_products(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.post("/", response_model=ProductResponse)
def create_product(
    product_in: ProductCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if db.query(Product).filter(Product.sku == product_in.sku).first():
        raise HTTPException(status_code=400, detail="Product with this SKU already exists.")

    product = Product(**product_in.model_dump(), created_by_id=current_user.id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    update_data = product_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/{product_id}/components", response_model=List[ComponentResponse])
def get_product_recipe(product_id: int, db: Session = Depends(get_db)):
    components = db.query(ProductMaterial).filter(ProductMaterial.product_id == product_id).all()
    
    return [
        ComponentResponse(
            id=c.id,
            material_name=c.material.name,
            quantity_used=c.quantity_used,
            cost_at_time_of_calculation=c.quantity_used * c.material.cost_per_unit
        )
        for c in components
    ]

@router.post("/{product_id}/components")
def add_component_to_recipe(
    product_id: int, 
    component_in: ComponentCreate, 
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    material = db.query(Material).filter(Material.id == component_in.material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    recipe_item = ProductMaterial(
        product_id=product_id,
        material_id=component_in.material_id,
        quantity_used=component_in.quantity
    )
    
    db.add(recipe_item)
    db.commit()
    
    current_cost = product.manufacture_cost or 0.0
    added_cost = component_in.quantity * material.cost_per_unit
    product.manufacture_cost = current_cost + added_cost
    db.add(product)
    db.commit()

    return {"status": "success", "added_cost": added_cost}


@router.delete("/{product_id}/components/{component_id}")
def remove_component_from_recipe(
    product_id: int,
    component_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Find the link
    link = db.query(ProductMaterial).filter(
        ProductMaterial.product_id == product_id,
        ProductMaterial.id == component_id
    ).first()
    
    if not link:
        raise HTTPException(status_code=404, detail="Component not found in recipe")

    product = db.query(Product).filter(Product.id == product_id).first()
    cost_to_remove = link.quantity_used * link.material.cost_per_unit
    
    if product.manufacture_cost:
        product.manufacture_cost = max(0, product.manufacture_cost - cost_to_remove)
    
    db.delete(link)
    db.add(product)
    db.commit()
    
    return {"status": "deleted"}


@router.post("/{product_id}/produce")
def record_production_run(
    product_id: int,
    production: ProductionRun,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    recipe_items = db.query(ProductMaterial).filter(
        ProductMaterial.product_id == product_id
    ).all()

    if not recipe_items:
        raise HTTPException(status_code=400, detail="This product has no recipe defined. Cannot calculate material usage.")

    for item in recipe_items:
        required_qty = item.quantity_used * production.quantity
        if item.material.current_stock < required_qty:
            raise HTTPException(
                status_code=400, 
                detail=f"Insufficient stock for {item.material.name}. Required: {required_qty}, Available: {item.material.current_stock}"
            )

    for item in recipe_items:
        total_deduction = item.quantity_used * production.quantity
        item.material.current_stock -= total_deduction

    product.stock_quantity += production.quantity

    db.commit()
    
    return {"status": "success", "new_stock_quantity": product.stock_quantity}