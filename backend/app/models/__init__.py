import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .asset_inventory import Base
from .investment_management import (
    Portfolio, Holding, Transaction, PerformanceMetric
)
from .financial_structuring import (
    Deal, Instrument, Scenario, Document
)

# Determine host based on environment
IN_DOCKER = os.environ.get("IN_DOCKER", "0") == "1"
db_host = "postgres" if IN_DOCKER else "localhost"
db_user = os.environ.get("POSTGRES_USER", "ash_user")
db_pass = os.environ.get("POSTGRES_PASSWORD", "ash_password")
db_name = os.environ.get("POSTGRES_DB", "ash_inventory")
db_port = os.environ.get("POSTGRES_PORT", "5432")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine) 