"""
API router for asset inventory CRUD operations.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..schemas.asset_inventory import Asset, AssetCreate, AssetUpdate
from ..models.asset_inventory import Asset as AssetModel
from ..models import SessionLocal

router = APIRouter()

# Dependency to get DB session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[Asset])
def list_assets(db: Session = Depends(get_db)):
    assets = db.query(AssetModel).all()
    return assets

@router.post("/", response_model=Asset)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    db_asset = AssetModel(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/{asset_id}", response_model=Asset)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(AssetModel).filter(AssetModel.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.put("/{asset_id}", response_model=Asset)
def update_asset(asset_id: int, asset_update: AssetUpdate, db: Session = Depends(get_db)):
    asset = db.query(AssetModel).filter(AssetModel.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    for key, value in asset_update.dict(exclude_unset=True).items():
        setattr(asset, key, value)
    db.commit()
    db.refresh(asset)
    return asset

@router.delete("/{asset_id}", response_model=dict)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(AssetModel).filter(AssetModel.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(asset)
    db.commit()
    return {"detail": "Asset deleted"} 