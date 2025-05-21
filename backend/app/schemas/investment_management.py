from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class HoldingBase(BaseModel):
    asset_id: int
    quantity: float

class HoldingCreate(HoldingBase):
    pass

class HoldingUpdate(BaseModel):
    asset_id: Optional[int] = None
    quantity: Optional[float] = None

class Holding(HoldingBase):
    id: int
    portfolio_id: int
    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    type: str
    quantity: float
    price: float
    date: Optional[datetime] = None

class TransactionCreate(TransactionBase):
    holding_id: int

class TransactionUpdate(BaseModel):
    type: Optional[str] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    date: Optional[datetime] = None

class Transaction(TransactionBase):
    id: int
    holding_id: int
    class Config:
        orm_mode = True

class PerformanceMetricBase(BaseModel):
    metric_name: str
    value: float
    as_of_date: Optional[datetime] = None

class PerformanceMetricCreate(PerformanceMetricBase):
    portfolio_id: int

class PerformanceMetricUpdate(BaseModel):
    metric_name: Optional[str] = None
    value: Optional[float] = None
    as_of_date: Optional[datetime] = None

class PerformanceMetric(PerformanceMetricBase):
    id: int
    portfolio_id: int
    class Config:
        orm_mode = True

class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Portfolio(PortfolioBase):
    id: int
    holdings: List[Holding] = []
    performance_metrics: List[PerformanceMetric] = []
    class Config:
        orm_mode = True 