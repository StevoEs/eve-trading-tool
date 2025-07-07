from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from datetime import datetime, timedelta
import asyncio
import uvicorn

from database import get_db, engine
from models import Base, Item, Region, MarketData, OrderHistory
from fetch_market import fetch_market_data

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EVE Online Trading Tool API",
    description="API for EVE Online market data analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "EVE Online Trading Tool API", "status": "running"}

@app.get("/items")
async def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all items with optional search"""
    query = db.query(Item)
    
    if search:
        query = query.filter(Item.name.ilike(f"%{search}%"))
    
    items = query.offset(skip).limit(limit).all()
    total = query.count()
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@app.get("/regions")
async def get_regions(db: Session = Depends(get_db)):
    """Get all regions"""
    regions = db.query(Region).all()
    return {"regions": regions}

@app.get("/market-data/{type_id}")
async def get_market_data(
    type_id: int,
    region_id: Optional[int] = None,
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get market data for a specific item"""
    query = db.query(MarketData).filter(MarketData.type_id == type_id)
    
    if region_id:
        query = query.filter(MarketData.region_id == region_id)
    
    # Get data from the last N days
    since_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(MarketData.timestamp >= since_date)
    
    market_data = query.order_by(desc(MarketData.timestamp)).all()
    
    return {"market_data": market_data}

@app.get("/arbitrage")
async def get_arbitrage_opportunities(
    min_profit: float = Query(1000000, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Find arbitrage opportunities between regions"""
    # Get latest market data for each item/region combination
    subquery = db.query(
        MarketData.type_id,
        MarketData.region_id,
        func.max(MarketData.timestamp).label('latest_timestamp')
    ).group_by(MarketData.type_id, MarketData.region_id).subquery()
    
    latest_data = db.query(MarketData).join(
        subquery,
        (MarketData.type_id == subquery.c.type_id) &
        (MarketData.region_id == subquery.c.region_id) &
        (MarketData.timestamp == subquery.c.latest_timestamp)
    ).all()
    
    # Calculate arbitrage opportunities
    arbitrage_ops = []
    
    # Group by type_id
    data_by_type = {}
    for data in latest_data:
        if data.type_id not in data_by_type:
            data_by_type[data.type_id] = []
        data_by_type[data.type_id].append(data)
    
    for type_id, type_data in data_by_type.items():
        if len(type_data) < 2:
            continue
        
        # Find best buy and sell opportunities
        for buy_data in type_data:
            for sell_data in type_data:
                if buy_data.region_id == sell_data.region_id:
                    continue
                
                if buy_data.buy_max and sell_data.sell_min:
                    profit = buy_data.buy_max - sell_data.sell_min
                    if profit >= min_profit:
                        item = db.query(Item).filter(Item.type_id == type_id).first()
                        buy_region = db.query(Region).filter(Region.region_id == buy_data.region_id).first()
                        sell_region = db.query(Region).filter(Region.region_id == sell_data.region_id).first()
                        
                        arbitrage_ops.append({
                            "item": item,
                            "buy_region": buy_region,
                            "sell_region": sell_region,
                            "buy_price": buy_data.buy_max,
                            "sell_price": sell_data.sell_min,
                            "profit": profit,
                            "profit_margin": (profit / sell_data.sell_min) * 100 if sell_data.sell_min > 0 else 0,
                            "buy_volume": buy_data.buy_volume,
                            "sell_volume": sell_data.sell_volume
                        })
    
    # Sort by profit and limit results
    arbitrage_ops.sort(key=lambda x: x["profit"], reverse=True)
    
    return {"arbitrage_opportunities": arbitrage_ops[:limit]}

@app.get("/price-trends/{type_id}")
async def get_price_trends(
    type_id: int,
    region_id: int,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get price trends for an item in a specific region"""
    since_date = datetime.utcnow() - timedelta(days=days)
    
    # Get historical data
    history = db.query(OrderHistory).filter(
        OrderHistory.type_id == type_id,
        OrderHistory.region_id == region_id,
        OrderHistory.date >= since_date
    ).order_by(OrderHistory.date).all()
    
    # Get recent market data
    market_data = db.query(MarketData).filter(
        MarketData.type_id == type_id,
        MarketData.region_id == region_id,
        MarketData.timestamp >= since_date
    ).order_by(MarketData.timestamp).all()
    
    return {
        "historical_data": history,
        "market_data": market_data
    }

@app.get("/market-health")
async def get_market_health(db: Session = Depends(get_db)):
    """Get overall market health statistics"""
    # Get latest data timestamp
    latest_data = db.query(func.max(MarketData.timestamp)).scalar()
    
    # Count active items and regions
    active_items = db.query(func.count(func.distinct(MarketData.type_id))).scalar()
    active_regions = db.query(func.count(func.distinct(MarketData.region_id))).scalar()
    
    # Get total volume and orders
    total_buy_volume = db.query(func.sum(MarketData.buy_volume)).scalar() or 0
    total_sell_volume = db.query(func.sum(MarketData.sell_volume)).scalar() or 0
    total_orders = db.query(func.sum(MarketData.buy_orders + MarketData.sell_orders)).scalar() or 0
    
    return {
        "last_update": latest_data,
        "active_items": active_items,
        "active_regions": active_regions,
        "total_buy_volume": total_buy_volume,
        "total_sell_volume": total_sell_volume,
        "total_orders": total_orders
    }

@app.post("/update-market-data")
async def trigger_market_update():
    """Manually trigger market data update"""
    try:
        await fetch_market_data()
        return {"message": "Market data update completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market data update failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

