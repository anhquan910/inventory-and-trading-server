from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from app.api.deps import get_db, get_current_active_user
from app.models.transaction import Transaction, TransactionItem, TransactionStatus, TransactionType
from app.models.product import Product
from app.models.inventory import Material
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter()

@router.post("/", response_model=dict)
def create_transaction(
    txn_in: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    total = sum(item.quantity * item.unit_price for item in txn_in.items)
    balance = total - txn_in.amount_paid

    status = TransactionStatus.COMPLETED
    if balance > 0:
        status = TransactionStatus.PENDING

    db_txn = Transaction(
        transaction_type=txn_in.type,
        customer_name=txn_in.customer_name,
        total_amount=total,
        amount_paid=txn_in.amount_paid,
        balance_due=balance,
        status=status,
        created_by_id=current_user.id
    )
    db.add(db_txn)
    db.flush()
    
    for item in txn_in.items:
        db_item = TransactionItem(
            transaction_id=db_txn.id,
            product_id=item.product_id,
            material_id=item.material_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.quantity * item.unit_price
        )
        db.add(db_item)
        
        if txn_in.type == "RETAIL":
            if not item.product_id:
                raise HTTPException(400, "Retail transaction must have product_id")
            product = db.query(Product).get(item.product_id)
            if product.stock_quantity < item.quantity:
                raise HTTPException(400, f"Not enough stock for {product.name}")
            product.stock_quantity -= int(item.quantity)
            
        elif txn_in.type == "TRADE":
            if not item.material_id:
                 raise HTTPException(400, "Trade transaction must have material_id")
            material = db.query(Material).get(item.material_id)
            
            material.current_stock += item.quantity

    db.commit()
    return {"status": "success", "id": db_txn.id}

@router.get("/", response_model=List[TransactionResponse])
def get_transaction_history(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)
    if status:
        query = query.filter(Transaction.status == status)
        
    return query.order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()

@router.patch("/{transaction_id}/pay")
def mark_transaction_paid(transaction_id: int, db: Session = Depends(get_db)):
    txn = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not txn:
        raise HTTPException(404, "Transaction not found")
        
    txn.amount_paid = txn.total_amount
    txn.balance_due = 0
    txn.status = TransactionStatus.COMPLETED
    
    db.commit()
    return {"status": "paid"}