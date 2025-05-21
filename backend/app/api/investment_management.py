from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..schemas.investment_management import (
    Portfolio, PortfolioCreate, PortfolioUpdate,
    Holding, HoldingCreate, HoldingUpdate,
    Transaction, TransactionCreate, TransactionUpdate,
    PerformanceMetric, PerformanceMetricCreate, PerformanceMetricUpdate
)
from ..models.investment_management import (
    Portfolio as PortfolioModel,
    Holding as HoldingModel,
    Transaction as TransactionModel,
    PerformanceMetric as PerformanceMetricModel
)
from ..models import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Portfolio Endpoints
@router.get('/portfolios/', response_model=List[Portfolio])
def list_portfolios(db: Session = Depends(get_db)):
    return db.query(PortfolioModel).all()

@router.post('/portfolios/', response_model=Portfolio)
def create_portfolio(portfolio: PortfolioCreate, db: Session = Depends(get_db)):
    db_portfolio = PortfolioModel(**portfolio.dict())
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

@router.get('/portfolios/{portfolio_id}', response_model=Portfolio)
def get_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = db.query(PortfolioModel).filter(PortfolioModel.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail='Portfolio not found')
    return portfolio

@router.put('/portfolios/{portfolio_id}', response_model=Portfolio)
def update_portfolio(portfolio_id: int, portfolio_update: PortfolioUpdate, db: Session = Depends(get_db)):
    portfolio = db.query(PortfolioModel).filter(PortfolioModel.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail='Portfolio not found')
    for key, value in portfolio_update.dict(exclude_unset=True).items():
        setattr(portfolio, key, value)
    db.commit()
    db.refresh(portfolio)
    return portfolio

@router.delete('/portfolios/{portfolio_id}', response_model=dict)
def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = db.query(PortfolioModel).filter(PortfolioModel.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail='Portfolio not found')
    db.delete(portfolio)
    db.commit()
    return {'detail': 'Portfolio deleted'}

# Holding Endpoints
@router.get('/holdings/', response_model=List[Holding])
def list_holdings(db: Session = Depends(get_db)):
    return db.query(HoldingModel).all()

@router.post('/holdings/', response_model=Holding)
def create_holding(holding: HoldingCreate, db: Session = Depends(get_db)):
    db_holding = HoldingModel(**holding.dict())
    db.add(db_holding)
    db.commit()
    db.refresh(db_holding)
    return db_holding

@router.get('/holdings/{holding_id}', response_model=Holding)
def get_holding(holding_id: int, db: Session = Depends(get_db)):
    holding = db.query(HoldingModel).filter(HoldingModel.id == holding_id).first()
    if not holding:
        raise HTTPException(status_code=404, detail='Holding not found')
    return holding

@router.put('/holdings/{holding_id}', response_model=Holding)
def update_holding(holding_id: int, holding_update: HoldingUpdate, db: Session = Depends(get_db)):
    holding = db.query(HoldingModel).filter(HoldingModel.id == holding_id).first()
    if not holding:
        raise HTTPException(status_code=404, detail='Holding not found')
    for key, value in holding_update.dict(exclude_unset=True).items():
        setattr(holding, key, value)
    db.commit()
    db.refresh(holding)
    return holding

@router.delete('/holdings/{holding_id}', response_model=dict)
def delete_holding(holding_id: int, db: Session = Depends(get_db)):
    holding = db.query(HoldingModel).filter(HoldingModel.id == holding_id).first()
    if not holding:
        raise HTTPException(status_code=404, detail='Holding not found')
    db.delete(holding)
    db.commit()
    return {'detail': 'Holding deleted'}

# Transaction Endpoints
@router.get('/transactions/', response_model=List[Transaction])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(TransactionModel).all()

@router.post('/transactions/', response_model=Transaction)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = TransactionModel(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get('/transactions/{transaction_id}', response_model=Transaction)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail='Transaction not found')
    return transaction

@router.put('/transactions/{transaction_id}', response_model=Transaction)
def update_transaction(transaction_id: int, transaction_update: TransactionUpdate, db: Session = Depends(get_db)):
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail='Transaction not found')
    for key, value in transaction_update.dict(exclude_unset=True).items():
        setattr(transaction, key, value)
    db.commit()
    db.refresh(transaction)
    return transaction

@router.delete('/transactions/{transaction_id}', response_model=dict)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail='Transaction not found')
    db.delete(transaction)
    db.commit()
    return {'detail': 'Transaction deleted'}

# PerformanceMetric Endpoints
@router.get('/performance_metrics/', response_model=List[PerformanceMetric])
def list_performance_metrics(db: Session = Depends(get_db)):
    return db.query(PerformanceMetricModel).all()

@router.post('/performance_metrics/', response_model=PerformanceMetric)
def create_performance_metric(metric: PerformanceMetricCreate, db: Session = Depends(get_db)):
    db_metric = PerformanceMetricModel(**metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.get('/performance_metrics/{metric_id}', response_model=PerformanceMetric)
def get_performance_metric(metric_id: int, db: Session = Depends(get_db)):
    metric = db.query(PerformanceMetricModel).filter(PerformanceMetricModel.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail='Performance metric not found')
    return metric

@router.put('/performance_metrics/{metric_id}', response_model=PerformanceMetric)
def update_performance_metric(metric_id: int, metric_update: PerformanceMetricUpdate, db: Session = Depends(get_db)):
    metric = db.query(PerformanceMetricModel).filter(PerformanceMetricModel.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail='Performance metric not found')
    for key, value in metric_update.dict(exclude_unset=True).items():
        setattr(metric, key, value)
    db.commit()
    db.refresh(metric)
    return metric

@router.delete('/performance_metrics/{metric_id}', response_model=dict)
def delete_performance_metric(metric_id: int, db: Session = Depends(get_db)):
    metric = db.query(PerformanceMetricModel).filter(PerformanceMetricModel.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail='Performance metric not found')
    db.delete(metric)
    db.commit()
    return {'detail': 'Performance metric deleted'} 