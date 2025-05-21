from fastapi import FastAPI
from .api import asset_inventory
from .api import data_ingestion
from backend.app.api import investment_management, financial_structuring

app = FastAPI(title="Ash Investments Backend")

app.include_router(
    asset_inventory.router, prefix="/api/assets", tags=["Asset Inventory"]
)
app.include_router(
    data_ingestion.router, prefix="/api/data-ingestion", tags=["Data Ingestion"]
)
app.include_router(investment_management.router, prefix="/api/investment")
app.include_router(financial_structuring.router, prefix="/api/structuring") 