import pandas as pd
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.market_data import MarketData
import sys
import os

def seed_market_data(csv_file_path: str):
    print(f"Loading data from {csv_file_path}...")
    
    # 1. Read CSV using Pandas
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print("Error: CSV file not found.")
        return

    # 2. Rename CSV columns to match Database Columns
    # This map fixes the mismatch between 'Adj Close' in CSV and 'gold_adj_close' in DB
    rename_map = {
        'Date': 'date',
        'Open': 'gold_open',
        'High': 'gold_high',
        'Low': 'gold_low',
        'Close': 'gold_close',
        'Adj Close': 'gold_adj_close',
        'Volume': 'gold_volume',
        
        # Mapping correlated assets (simple case conversion)
        'SP_Ajclose': 'sp_adj_close',
        'DJ_Ajclose': 'dj_adj_close',
        'EG_Ajclose': 'eg_adj_close',
        'GDX_Adj Close': 'gdx_adj_close',
        'USO_Adj Close': 'uso_adj_close',
        'RHO_PRICE': 'rho_price' 
    }
    
    # Apply specific renames
    df = df.rename(columns=rename_map)
    
    # Apply generic cleaning (lowercase all other columns)
    # Example: 'SP_open' -> 'sp_open', 'EU_Trend' -> 'eu_trend'
    df.columns = [c.lower() for c in df.columns]

    # 3. Convert Date column to Python Date objects
    df['date'] = pd.to_datetime(df['date']).dt.date

    # 4. Handle "Trend" columns (ensure they are integers)
    # Sometimes CSVs have "Up"/"Down" strings, if so, map them here. 
    # If they are already numbers, this is safe.
    
    # 5. Insert into Database
    db = SessionLocal()
    try:
        # Check if data already exists to avoid duplicates
        if db.query(MarketData).first():
            print("Database already contains market data. Skipping seed.")
            return

        print("Converting to objects...")
        # Convert DataFrame to list of Dictionaries
        data_dicts = df.to_dict(orient='records')
        
        # Create Model Instances
        # We do this in batches if the file is huge (e.g. >10k rows)
        objects = [MarketData(**row) for row in data_dicts]
        
        print(f"Inserting {len(objects)} rows...")
        db.bulk_save_objects(objects)
        db.commit()
        print("Success! Data seeded.")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Point this to your actual CSV file location
    # Ideally, put the csv in the backend/ folder
    CSV_PATH = "Final_Dataset.csv" 
    
    if not os.path.exists(CSV_PATH):
        print(f"Please place your '{CSV_PATH}' file in the backend directory.")
    else:
        seed_market_data(CSV_PATH)