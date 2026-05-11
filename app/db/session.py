from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the SQLAlchemy engine using app configuration.
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# Create a session factory for application database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)