from fastapi import FastAPI
from .api import asset_inventory

app = FastAPI(title="Ash Investments Backend")

app.include_router(asset_inventory.router, prefix="/assets", tags=["Asset Inventory"]) 