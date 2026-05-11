from sqlalchemy import Column, DateTime, Integer, Float, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# Production-related models for recipes and manufacturing logs.
class ProductMaterial(Base):
    """
    The 'Recipe' Table (Bill of Materials).
    Links a Product to its raw Materials.
    """
    id = Column(Integer, primary_key=True, index=True)  # Primary key for the recipe component.
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)  # Foreign key to the product being produced.
    material_id = Column(Integer, ForeignKey("material.id"), nullable=False)  # Foreign key to the material used.
    
    quantity_used = Column(Float, nullable=False)  # Amount of material required per unit of product.
    
    product = relationship("Product", back_populates="components")  # Relationship to the product.
    material = relationship("Material")  # Relationship to the material.

class ProductionLog(Base):
    """
    Records every time a finished good is produced.
    Acts as the 'Job History'.
    """
    id = Column(Integer, primary_key=True, index=True)  # Primary key for the production log entry.
    
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)  # Foreign key to the product produced.
    quantity_produced = Column(Integer, nullable=False)  # Number of units produced in this job.
    
unit_cost_snapshot = Column(Float, nullable=False)  # Cost per unit at the time of production.
    total_cost = Column(Float, nullable=False)  # Total cost for this production run.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Timestamp of production.
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)  # User who initiated the production.
    
    product = relationship("Product")  # Relationship to the product.
    creator = relationship("User")  # Relationship to the user who created the log.