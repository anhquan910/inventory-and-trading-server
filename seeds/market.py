import pandas as pd
import os
from sqlalchemy.orm import Session
from app.models.market_data import MarketData

def seed_market_data(db: Session, csv_path: str):
    print(f"Checking Market Data from {csv_path}...")

    if db.query(MarketData).first():
        print("⚠️ Market Data already exists. Skipping.")
        return

    if not os.path.exists(csv_path):
        print(f"❌ CSV not found at: {csv_path}")
        return

    try:
        df = pd.read_csv(csv_path)
        
        rename_map = {
            'Date': 'date', 'Open': 'gold_open', 'High': 'gold_high',
            'Low': 'gold_low', 'Close': 'gold_close', 'Adj Close': 'gold_adj_close',
            'Volume': 'gold_volume', 'SP_Ajclose': 'sp_adj_close',
            'DJ_Ajclose': 'dj_adj_close', 'EG_Ajclose': 'eg_adj_close',
            'GDX_Adj Close': 'gdx_adj_close', 'USO_Adj Close': 'uso_adj_close',
            'RHO_PRICE': 'rho_price'
        }
        df = df.rename(columns=rename_map)
        df.columns = [c.lower() for c in df.columns]
        df['date'] = pd.to_datetime(df['date']).dt.date
        df = df.where(pd.notnull(df), None)

        data_dicts = df.to_dict(orient='records')
        objects = [MarketData(**row) for row in data_dicts]

        print(f"🌱 Inserting {len(objects)} market rows...")
        db.bulk_save_objects(objects)
        db.commit()
        print("✅ Market Data seeded successfully!")

    except Exception as e:
        print(f"❌ Error seeding market data: {e}")
        db.rollback()