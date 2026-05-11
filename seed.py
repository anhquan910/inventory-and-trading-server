import sys
import os

# 1. Setup Path so we can import local packages from this repository.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from seeds.inventory import seed_inventory
from seeds.market import seed_market_data

def main():
    # Create a database session and apply the initial data seeds.
    db = SessionLocal()
    try:
        print("--- STARTING SEED PROCESS ---")

        # Seed material inventory and product inventory records.
        seed_inventory(db)

        # Seed gold market data from the included CSV dataset.
        csv_path = os.path.join(os.path.dirname(__file__), "gold_price_forecasting_dataset.csv")
        seed_market_data(db, csv_path)

        print("--- SEED PROCESS COMPLETED ---")
    finally:
        # Ensure the database session is always closed.
        db.close()

if __name__ == "__main__":
    main()