from fastapi import FastAPI
from .api import asset_inventory
from .api import data_ingestion

app = FastAPI(title="Ash Investments Backend")

app.include_router(
    asset_inventory.router, prefix="/assets", tags=["Asset Inventory"]
)
app.include_router(
    data_ingestion.router, prefix="/api", tags=["Data Ingestion"]
) 