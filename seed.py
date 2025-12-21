import sys
import os

# 1. Setup Path so we can import 'app' and 'seeds'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from seeds.inventory import seed_inventory
from seeds.market import seed_market_data

def main():
    db = SessionLocal()
    try:
        print("--- STARTING SEED PROCESS ---")
        
        seed_inventory(db)
      
        csv_path = os.path.join(os.path.dirname(__file__), "Final_Dataset.csv")
        seed_market_data(db, csv_path)

        print("--- SEED PROCESS COMPLETED ---")
    finally:
        db.close()

if __name__ == "__main__":
    main()