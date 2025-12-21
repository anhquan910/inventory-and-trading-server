from sqlalchemy.orm import Session
from app.models.inventory import Material

def seed_inventory(db: Session):
    materials = [
        {
            "name": "18k Yellow Gold Grain",
            "sku": "MT-GLD-18Y",
            "category": "Metal",
            "description": "Casting grain for general jewellery production",
            "unit_of_measure": "grams",
            "current_stock": 50.0,
            "reorder_level": 20.0,
            "cost_per_unit": 65.50,
            "preferred_vendor": "Cooksongold"
        },
        {
            "name": "Sterling Silver Grain (925)",
            "sku": "MT-SIL-925",
            "category": "Metal",
            "description": "Standard sterling silver casting grain",
            "unit_of_measure": "grams",
            "current_stock": 500.0,
            "reorder_level": 100.0,
            "cost_per_unit": 0.85,
            "preferred_vendor": "Cooksongold"
        },
        {
            "name": "Diamond Melee (1.5mm)",
            "sku": "GM-DIA-1.5",
            "category": "Gemstone",
            "description": "Round brilliant cut, G/H color, SI clarity",
            "unit_of_measure": "carats",
            "current_stock": 5.0,
            "reorder_level": 1.0,
            "cost_per_unit": 450.00,
            "preferred_vendor": "Euro Mounts"
        },
        {
            "name": "Lobster Clasp (9mm Gold)",
            "sku": "FD-CLP-18Y",
            "category": "Finding",
            "description": "18k Yellow Gold heavy lobster clasp",
            "unit_of_measure": "pcs",
            "current_stock": 20.0,
            "reorder_level": 5.0,
            "cost_per_unit": 35.00,
            "preferred_vendor": "Rashbel"
        }
    ]

    print("Checking Inventory...")
    if db.query(Material).first():
        print("⚠️ Inventory table already has data. Skipping.")
        return

    print(f"🌱 Seeding {len(materials)} materials...")
    for data in materials:
        material = Material(**data)
        db.add(material)
    
    db.commit()
    print("✅ Inventory seeded successfully!")