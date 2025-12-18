# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth, users

app = FastAPI(title=settings.PROJECT_NAME)

# Include Routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])

@app.get("/")
def root():
    return {"message": "Welcome to the Jewellery Inventory API"}