from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List

from app.api.deps import get_db
from app.models.transaction import Transaction
from app.models.production import ProductionLog

router = APIRouter()

@router.get("/financials")
def get_financial_summary(
    period: str = "30d",
    db: Session = Depends(get_db)
):
    now = datetime.now()
    if period == "7d":
        start_date = now - timedelta(days=7)
    elif period == "30d":
        start_date = now - timedelta(days=30)
    else:
        start_date = now - timedelta(days=365)

    revenue_query = db.query(
        func.date(Transaction.created_at).label('date'),
        func.sum(Transaction.total_amount).label('revenue')
    ).filter(
        Transaction.created_at >= start_date
    ).group_by(func.date(Transaction.created_at)).all()

    cost_query = db.query(
        func.date(ProductionLog.created_at).label('date'),
        func.sum(ProductionLog.total_cost).label('cost')
    ).filter(
        ProductionLog.created_at >= start_date
    ).group_by(func.date(ProductionLog.created_at)).all()

    data_map = {}
    
    for r in revenue_query:
        d = r.date
        if d not in data_map: data_map[d] = {"revenue": 0, "cost": 0}
        data_map[d]["revenue"] = r.revenue or 0

    for c in cost_query:
        d = c.date
        if d not in data_map: data_map[d] = {"revenue": 0, "cost": 0}
        data_map[d]["cost"] = c.cost or 0

    chart_data = [
        {
            "date": k, 
            "revenue": v["revenue"], 
            "cost": v["cost"], 
            "profit": v["revenue"] - v["cost"]
        } 
        for k, v in data_map.items()
    ]
    chart_data.sort(key=lambda x: x["date"])

    total_revenue = sum(d["revenue"] for d in chart_data)
    total_cost = sum(d["cost"] for d in chart_data)
    gross_profit = total_revenue - total_cost

    return {
        "chart_data": chart_data,
        "summary": {
            "total_revenue": total_revenue,
            "total_cost": total_cost,
            "gross_profit": gross_profit,
            "margin": (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
        }
    }