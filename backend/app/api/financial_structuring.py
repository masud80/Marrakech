from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..schemas.financial_structuring import (
    Deal, DealCreate, DealUpdate,
    Instrument, InstrumentCreate, InstrumentUpdate,
    Scenario, ScenarioCreate, ScenarioUpdate,
    Document, DocumentCreate, DocumentUpdate
)
from ..models.financial_structuring import (
    Deal as DealModel,
    Instrument as InstrumentModel,
    Scenario as ScenarioModel,
    Document as DocumentModel
)
from ..models import SessionLocal


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Deal Endpoints
@router.get('/deals/', response_model=List[Deal])
def list_deals(db: Session = Depends(get_db)):
    return db.query(DealModel).all()


@router.post('/deals/', response_model=Deal)
def create_deal(deal: DealCreate, db: Session = Depends(get_db)):
    db_deal = DealModel(**deal.dict())
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal


@router.get('/deals/{deal_id}', response_model=Deal)
def get_deal(deal_id: int, db: Session = Depends(get_db)):
    deal = db.query(DealModel).filter(DealModel.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail='Deal not found')
    return deal


@router.put('/deals/{deal_id}', response_model=Deal)
def update_deal(deal_id: int, deal_update: DealUpdate, db: Session = Depends(get_db)):
    deal = db.query(DealModel).filter(DealModel.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail='Deal not found')
    for key, value in deal_update.dict(exclude_unset=True).items():
        setattr(deal, key, value)
    db.commit()
    db.refresh(deal)
    return deal


@router.delete('/deals/{deal_id}', response_model=dict)
def delete_deal(deal_id: int, db: Session = Depends(get_db)):
    deal = db.query(DealModel).filter(DealModel.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail='Deal not found')
    db.delete(deal)
    db.commit()
    return {'detail': 'Deal deleted'}


# Instrument Endpoints
@router.get('/instruments/', response_model=List[Instrument])
def list_instruments(db: Session = Depends(get_db)):
    return db.query(InstrumentModel).all()


@router.post('/instruments/', response_model=Instrument)
def create_instrument(instrument: InstrumentCreate, db: Session = Depends(get_db)):
    db_instrument = InstrumentModel(**instrument.dict())
    db.add(db_instrument)
    db.commit()
    db.refresh(db_instrument)
    return db_instrument


@router.get('/instruments/{instrument_id}', response_model=Instrument)
def get_instrument(instrument_id: int, db: Session = Depends(get_db)):
    instrument = db.query(InstrumentModel).filter(
        InstrumentModel.id == instrument_id
    ).first()
    if not instrument:
        raise HTTPException(status_code=404, detail='Instrument not found')
    return instrument


@router.put('/instruments/{instrument_id}', response_model=Instrument)
def update_instrument(
    instrument_id: int,
    instrument_update: InstrumentUpdate,
    db: Session = Depends(get_db)
):
    instrument = db.query(InstrumentModel).filter(
        InstrumentModel.id == instrument_id
    ).first()
    if not instrument:
        raise HTTPException(status_code=404, detail='Instrument not found')
    for key, value in instrument_update.dict(exclude_unset=True).items():
        setattr(instrument, key, value)
    db.commit()
    db.refresh(instrument)
    return instrument


@router.delete('/instruments/{instrument_id}', response_model=dict)
def delete_instrument(instrument_id: int, db: Session = Depends(get_db)):
    instrument = db.query(InstrumentModel).filter(
        InstrumentModel.id == instrument_id
    ).first()
    if not instrument:
        raise HTTPException(status_code=404, detail='Instrument not found')
    db.delete(instrument)
    db.commit()
    return {'detail': 'Instrument deleted'}


# Scenario Endpoints
@router.get('/scenarios/', response_model=List[Scenario])
def list_scenarios(db: Session = Depends(get_db)):
    return db.query(ScenarioModel).all()


@router.post('/scenarios/', response_model=Scenario)
def create_scenario(scenario: ScenarioCreate, db: Session = Depends(get_db)):
    db_scenario = ScenarioModel(**scenario.dict())
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    return db_scenario


@router.get('/scenarios/{scenario_id}', response_model=Scenario)
def get_scenario(scenario_id: int, db: Session = Depends(get_db)):
    scenario = db.query(ScenarioModel).filter(
        ScenarioModel.id == scenario_id
    ).first()
    if not scenario:
        raise HTTPException(status_code=404, detail='Scenario not found')
    return scenario


@router.put('/scenarios/{scenario_id}', response_model=Scenario)
def update_scenario(
    scenario_id: int,
    scenario_update: ScenarioUpdate,
    db: Session = Depends(get_db)
):
    scenario = db.query(ScenarioModel).filter(
        ScenarioModel.id == scenario_id
    ).first()
    if not scenario:
        raise HTTPException(status_code=404, detail='Scenario not found')
    for key, value in scenario_update.dict(exclude_unset=True).items():
        setattr(scenario, key, value)
    db.commit()
    db.refresh(scenario)
    return scenario


@router.delete('/scenarios/{scenario_id}', response_model=dict)
def delete_scenario(scenario_id: int, db: Session = Depends(get_db)):
    scenario = db.query(ScenarioModel).filter(
        ScenarioModel.id == scenario_id
    ).first()
    if not scenario:
        raise HTTPException(status_code=404, detail='Scenario not found')
    db.delete(scenario)
    db.commit()
    return {'detail': 'Scenario deleted'}


# Document Endpoints
@router.get('/documents/', response_model=List[Document])
def list_documents(db: Session = Depends(get_db)):
    return db.query(DocumentModel).all()


@router.post('/documents/', response_model=Document)
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    db_document = DocumentModel(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


@router.get('/documents/{document_id}', response_model=Document)
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail='Document not found')
    return document


@router.put('/documents/{document_id}', response_model=Document)
def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    db: Session = Depends(get_db)
):
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail='Document not found')
    for key, value in document_update.dict(exclude_unset=True).items():
        setattr(document, key, value)
    db.commit()
    db.refresh(document)
    return document


@router.delete('/documents/{document_id}', response_model=dict)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail='Document not found')
    db.delete(document)
    db.commit()
    return {'detail': 'Document deleted'} 