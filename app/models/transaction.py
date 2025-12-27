from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base_class import Base

class TransactionStatus(str, enum.Enum):
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"

class TransactionType(str, enum.Enum):
    RETAIL = "RETAIL"
    TRADE = "TRADE"

class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    
    transaction_type = Column(String, nullable=False)
    customer_name = Column(String, nullable=True)
    total_amount = Column(Float, default=0.0)

    status = Column(String, default=TransactionStatus.COMPLETED, index=True)
    amount_paid = Column(Float, default=0.0)
    balance_due = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by_id = Column(Integer, ForeignKey("user.id"))
    
    items = relationship("TransactionItem", back_populates="transaction")
    creator = relationship("User")

class TransactionItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transaction.id"))
    
    product_id = Column(Integer, ForeignKey("product.id"), nullable=True)
    
    material_id = Column(Integer, ForeignKey("material.id"), nullable=True)
    
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    transaction = relationship("Transaction", back_populates="items")
    product = relationship("Product")
    material = relationship("Material")