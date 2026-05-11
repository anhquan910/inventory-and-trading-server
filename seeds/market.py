import pandas as pd
import os
from sqlalchemy.orm import Session
from sqlalchemy import text # Import text to execute raw SQL commands
from app.models.market_data import MarketData

def seed_market_data(db: Session, csv_path: str):
    # Load and seed historical market data from a CSV file.
    print(f"Checking Market Data from {csv_path}...")

    if not os.path.exists(csv_path):
        print(f"❌ CSV not found at: {csv_path}")
        return

    try:

        print("🧹 Truncating existing Market Data...")

        db.execute(text("TRUNCATE TABLE marketdata RESTART IDENTITY CASCADE;"))
        db.commit() 
        print("✅ Table truncated successfully.")


        df = pd.read_csv(csv_path)

        rename_map = {
            'date': 'date', 
            'open': 'gold_open', 
            'high': 'gold_high',
            'low': 'gold_low', 
            'close': 'gold_close', 
            'adj close': 'gold_adj_close',
            'volume': 'gold_volume', 
            'ma_7': 'ma_7', 
            'ma_30': 'ma_30', 
            'ma_90': 'ma_90', 
            'daily_return': 'daily_return', 
            'volatility_7': 'volatility_7', 
            'volatility_30': 'volatility_30', 
            'rsi': 'rsi', 
            'macd': 'macd', 
            'macd_signal': 'macd_signal', 
            'bb_upper': 'bb_upper', 
            'bb_lower': 'bb_lower'
        }

        df = df.rename(columns=rename_map)
        
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        df = df.where(pd.notnull(df), None)

        valid_columns = list(rename_map.values())
        df = df[[col for col in valid_columns if col in df.columns]]

        data_dicts = df.to_dict(orient='records')
        objects = [MarketData(**row) for row in data_dicts]

        print(f"🌱 Inserting {len(objects)} fresh market rows...")
        db.bulk_save_objects(objects)
        db.commit()
        print("✅ Market Data seeded successfully!")

    except Exception as e:
        print(f"❌ Error seeding market data: {e}")
        db.rollback()