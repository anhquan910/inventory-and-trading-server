# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth, users, inventory
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(inventory.router, prefix=f"{settings.API_V1_STR}/inventory", tags=["inventory"])

@app.get("/")
def root():
    return {"message": "Welcome to the Jewellery Inventory API"}