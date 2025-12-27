import pandas as pd
import numpy as np
import os
import joblib 
import time
from sqlalchemy.orm import Session
from sklearn.ensemble import RandomForestRegressor
from datetime import timedelta
from app.models.market_data import MarketData

MODEL_PATH = "gold_price_model.joblib"
MAX_MODEL_AGE_SECONDS = 24 * 60 * 60 

def get_or_train_model(X, y):
    if os.path.exists(MODEL_PATH):
        file_age = time.time() - os.path.getmtime(MODEL_PATH)
        if file_age < MAX_MODEL_AGE_SECONDS:
            return joblib.load(MODEL_PATH)

    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model

def train_and_predict(db: Session, days_to_predict: int = 7):
    query = db.query(
        MarketData.date, 
        MarketData.gold_close, 
        MarketData.sp_close,   
        MarketData.usdi_price, 
        MarketData.uso_close,  
        MarketData.eu_price,   
        MarketData.plt_price   
    ).order_by(MarketData.date.asc())
    
    df = pd.read_sql(query.statement, db.bind)
    
    if df.empty or len(df) < 30:
        return [], 0.0

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    
    target_col = 'gold_close'
    feature_cols = ['gold_close', 'sp_close', 'usdi_price', 'uso_close', 'eu_price', 'plt_price']
    generated_features = []

    for col in feature_cols:
        df[f'{col}_lag1'] = df[col].shift(1)
        generated_features.append(f'{col}_lag1')
        df[f'{col}_lag7'] = df[col].shift(7)
        generated_features.append(f'{col}_lag7')
        df[f'{col}_ma5'] = df[col].rolling(window=5).mean().shift(1)
        generated_features.append(f'{col}_ma5')

    df.dropna(inplace=True)

    X = df[generated_features]
    y = df[target_col]

    model = get_or_train_model(X, y) 
    score = model.score(X, y)

    future_predictions = []
    
    current_feats = df.iloc[-1][generated_features].copy()
    last_date = df.index[-1]

    for i in range(1, days_to_predict + 1):
        input_df = pd.DataFrame([current_feats.values], columns=generated_features)
        
        pred_price = model.predict(input_df)[0]
        
        next_date = last_date + timedelta(days=i)
        
        future_predictions.append({
            "date": next_date.strftime("%Y-%m-%d"),
            "price": round(pred_price, 2),
            "is_forecast": True
        })
        
        current_feats['gold_close_lag1'] = pred_price 

    return future_predictions, score