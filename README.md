# Web-based Inventory and Trading Dashboard for Jewellery Businesses

## Clone the Repository

```bash
git clone https://github.com/yourusername/jewellery-dashboard.git
cd jewellery-dashboard
```

## Setup

Make sure that your computer have:

- Python
- Docker and Docker Compose (can be installed with Rancher Desktop)

```bash
docker-compose up -d

cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Run Migrations (Create DB Tables)
alembic upgrade head

# Seed gold price data into database: https://www.kaggle.com/datasets/vishardmehta/gold-price-forecasting-dataset/data
python .\seed.py

# Start the Server
uvicorn app.main:app --reload
```

### UPDATE

Dataset have been updated, please run

```bash
alembic upgrade head

# Seed gold price data into database: https://www.kaggle.com/datasets/vishardmehta/gold-price-forecasting-dataset/data
python .\seed.py
```

again if you already run it once to keep the seed data up-to-date.
