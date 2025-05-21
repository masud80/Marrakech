from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, \
    Text
from sqlalchemy.orm import relationship
from .asset_inventory import Base
import datetime


class Deal(Base):
    __tablename__ = 'deals'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    # owner_id = Column(Integer, ForeignKey('users.id'))
    # Uncomment if user model exists
    instruments = relationship(
        'Instrument', back_populates='deal', cascade='all, delete-orphan'
    )
    scenarios = relationship(
        'Scenario', back_populates='deal', cascade='all, delete-orphan'
    )
    documents = relationship(
        'Document', back_populates='deal', cascade='all, delete-orphan'
    )


class Instrument(Base):
    __tablename__ = 'instruments'
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey('deals.id'))
    type = Column(String(50), nullable=False)  # e.g., 'equity', 'debt'
    name = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    terms = Column(Text)
    deal = relationship('Deal', back_populates='instruments')


class Scenario(Base):
    __tablename__ = 'scenarios'
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey('deals.id'))
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    parameters = Column(Text)  # JSON or stringified params
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    deal = relationship('Deal', back_populates='scenarios')


class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    deal_id = Column(Integer, ForeignKey('deals.id'))
    name = Column(String(100), nullable=False)
    doc_type = Column(String(50), nullable=False)
    # e.g., 'term_sheet', 'contract'
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    deal = relationship('Deal', back_populates='documents') 