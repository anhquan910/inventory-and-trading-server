from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class Material(Base):
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    category = Column(String, index=True) 
    unit_of_measure = Column(String, default="grams")
    
    current_stock = Column(Float, default=0.0)
    reorder_level = Column(Float, default=10.0)
    
    # (Price + Shipping + Tax)
    cost_per_unit = Column(Float, default=0.0) 
    
    preferred_vendor = Column(String, nullable=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())