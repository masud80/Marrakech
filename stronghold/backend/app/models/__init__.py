import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ash_user:ash_password@postgres:5432/ash_inventory")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from .asset_inventory import Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine) 