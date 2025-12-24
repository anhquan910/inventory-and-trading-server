from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class ProductMaterial(Base):
    """
    The 'Recipe' Table (Bill of Materials).
    Links a Product to its raw Materials.
    """
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("material.id"), nullable=False)
    
    quantity_used = Column(Float, nullable=False) 
    
    product = relationship("Product", back_populates="components")
    material = relationship("Material")