from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .asset_inventory import Base
import datetime


class Portfolio(Base):
    __tablename__ = 'portfolios'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    # owner_id = Column(Integer, ForeignKey('users.id'))
    # Uncomment if user model exists
    holdings = relationship(
        'Holding', back_populates='portfolio', cascade='all, delete-orphan'
    )
    performance_metrics = relationship(
        'PerformanceMetric', back_populates='portfolio',
        cascade='all, delete-orphan'
    )


class Holding(Base):
    __tablename__ = 'holdings'
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    asset_id = Column(Integer, ForeignKey('assets.id'))
    quantity = Column(Float, nullable=False)
    portfolio = relationship('Portfolio', back_populates='holdings')
    transactions = relationship(
        'Transaction', back_populates='holding', cascade='all, delete-orphan'
    )


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    holding_id = Column(Integer, ForeignKey('holdings.id'))
    type = Column(String(10), nullable=False)  # 'buy' or 'sell'
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    holding = relationship('Holding', back_populates='transactions')


class PerformanceMetric(Base):
    __tablename__ = 'performance_metrics'
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    metric_name = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)
    as_of_date = Column(DateTime, default=datetime.datetime.utcnow)
    portfolio = relationship('Portfolio', back_populates='performance_metrics') 