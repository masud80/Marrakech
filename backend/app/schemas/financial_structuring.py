from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class InstrumentBase(BaseModel):
    type: str
    name: str
    amount: float
    currency: str
    terms: Optional[str] = None

class InstrumentCreate(InstrumentBase):
    deal_id: int

class InstrumentUpdate(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    terms: Optional[str] = None

class Instrument(InstrumentBase):
    id: int
    deal_id: int
    class Config:
        orm_mode = True

class ScenarioBase(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Optional[str] = None
    created_at: Optional[datetime] = None

class ScenarioCreate(ScenarioBase):
    deal_id: int

class ScenarioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[str] = None
    created_at: Optional[datetime] = None

class Scenario(ScenarioBase):
    id: int
    deal_id: int
    class Config:
        orm_mode = True

class DocumentBase(BaseModel):
    name: str
    doc_type: str
    content: Optional[str] = None
    created_at: Optional[datetime] = None

class DocumentCreate(DocumentBase):
    deal_id: int

class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    doc_type: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[datetime] = None

class Document(DocumentBase):
    id: int
    deal_id: int
    class Config:
        orm_mode = True

class DealBase(BaseModel):
    name: str
    description: Optional[str] = None

class DealCreate(DealBase):
    pass

class DealUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Deal(DealBase):
    id: int
    instruments: List[Instrument] = []
    scenarios: List[Scenario] = []
    documents: List[Document] = []
    class Config:
        orm_mode = True 