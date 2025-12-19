import pandas as pd
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(script_dir)

sys.path.append(project_root)

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.market_data import MarketData

def seed_market_data(csv_file_path: str):
    print(f"Loading data from: {csv_file_path}")
    
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"❌ Error: Could not find file at {csv_file_path}")
        return

    rename_map = {
        'Date': 'date',
        'Open': 'gold_open',
        'High': 'gold_high',
        'Low': 'gold_low',
        'Close': 'gold_close',
        'Adj Close': 'gold_adj_close',
        'Volume': 'gold_volume',
        'SP_Ajclose': 'sp_adj_close',
        'DJ_Ajclose': 'dj_adj_close',
        'EG_Ajclose': 'eg_adj_close',
        'GDX_Adj Close': 'gdx_adj_close',
        'USO_Adj Close': 'uso_adj_close',
        'RHO_PRICE': 'rho_price' 
    }
    
    df = df.rename(columns=rename_map)
    df.columns = [c.lower() for c in df.columns]
    df['date'] = pd.to_datetime(df['date']).dt.date

    db = SessionLocal()
    try:
        if db.query(MarketData).first():
            print("⚠️ Database already contains market data. Skipping seed.")
            return

        print("Converting to objects...")
        df = df.where(pd.notnull(df), None)

        data_dicts = df.to_dict(orient='records')
        objects = [MarketData(**row) for row in data_dicts]
        
        print(f"Inserting {len(objects)} rows...")
        db.bulk_save_objects(objects)
        db.commit()
        print("✅ Success! Data seeded.")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    csv_path = os.path.join(script_dir, "Final_Dataset.csv")
    
    if not os.path.exists(csv_path):
        print(f"❌ File not found at: {csv_path}")
        print("Please ensure 'Final_Dataset.csv' is inside the 'dataset' folder.")
    else:
        seed_market_data(csv_path)