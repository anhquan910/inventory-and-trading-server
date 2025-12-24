from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, index=True)
    image_url = Column(String, nullable=True)
    
    retail_price = Column(Float, default=0.0)     
    manufacture_cost = Column(Float, default=0.0) 
    
    stock_quantity = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    components = relationship("ProductMaterial", back_populates="product", cascade="all, delete-orphan")
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    creator = relationship("User", back_populates="products")