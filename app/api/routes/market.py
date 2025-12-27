from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.deps import get_db
from app.models.market_data import MarketData 
from app.services.prediction import train_and_predict

router = APIRouter()

@router.get("/trend")
def get_market_trend(db: Session = Depends(get_db)):
    history = db.query(MarketData)\
        .order_by(MarketData.date.desc())\
        .limit(90)\
        .all()
    
    history_data = [
        {
            "date": h.date.strftime("%Y-%m-%d"),
            "price": h.gold_close,
            "is_forecast": False
        }
        for h in sorted(history, key=lambda x: x.date)
    ]

    forecast, accuracy_score = train_and_predict(db, days_to_predict=7)
    
    full_data = history_data + forecast
    
    return {
        "data": full_data,
        "model_accuracy": round(accuracy_score * 100, 1),
        "last_updated": datetime.now().strftime("%H:%M")
    }