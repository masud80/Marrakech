from pydantic import BaseModel
from typing import Optional

class AssetBase(BaseModel):
    name: str
    type: str
    value: float
    currency: str
    description: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    value: Optional[float] = None
    currency: Optional[str] = None
    description: Optional[str] = None

class Asset(AssetBase):
    id: int

    class Config:
        orm_mode = True 