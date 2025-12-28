from sqlalchemy import Column, DateTime, Integer, Float, ForeignKey, func
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

class ProductionLog(Base):
    """
    Records every time a finished good is produced.
    Acts as the 'Job History'.
    """
    id = Column(Integer, primary_key=True, index=True)
    
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity_produced = Column(Integer, nullable=False)
    
    unit_cost_snapshot = Column(Float, nullable=False) 
    total_cost = Column(Float, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    
    product = relationship("Product")
    creator = relationship("User")