from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    
    type_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer)
    market_group_id = Column(Integer)
    volume = Column(Float)
    description = Column(Text)
    published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to market data
    market_data = relationship("MarketData", back_populates="item")

class Region(Base):
    __tablename__ = "regions"
    
    region_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to market data
    market_data = relationship("MarketData", back_populates="region")

class MarketData(Base):
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("items.type_id"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.region_id"), nullable=False)
    
    # Buy order data
    buy_max = Column(Float)  # Highest buy price
    buy_min = Column(Float)  # Lowest buy price
    buy_avg = Column(Float)  # Average buy price
    buy_volume = Column(Integer)  # Total buy volume
    buy_orders = Column(Integer)  # Number of buy orders
    
    # Sell order data
    sell_max = Column(Float)  # Highest sell price
    sell_min = Column(Float)  # Lowest sell price
    sell_avg = Column(Float)  # Average sell price
    sell_volume = Column(Integer)  # Total sell volume
    sell_orders = Column(Integer)  # Number of sell orders
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    item = relationship("Item", back_populates="market_data")
    region = relationship("Region", back_populates="market_data")

class OrderHistory(Base):
    __tablename__ = "order_history"
    
    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("items.type_id"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.region_id"), nullable=False)
    
    # Historical data
    date = Column(DateTime, nullable=False, index=True)
    average = Column(Float)
    highest = Column(Float)
    lowest = Column(Float)
    order_count = Column(Integer)
    volume = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)

