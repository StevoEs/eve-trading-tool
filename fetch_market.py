import asyncio
import aiohttp
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Item, Region, MarketData, OrderHistory
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# EVE Online ESI API base URL
ESI_BASE_URL = "https://esi.evetech.net/latest"

# Region IDs for major trading hubs
REGIONS = {
    10000002: "The Forge (Jita)",
    10000043: "Domain (Amarr)",
    10000032: "Sinq Laison (Dodixie)",
    10000030: "Heimatar (Rens)",
    10000042: "Metropolis (Hek)"
}

class MarketDataFetcher:
    def __init__(self):
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_types(self):
        """Fetch all market type IDs"""
        url = f"{ESI_BASE_URL}/universe/types/"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Fetched {len(data)} type IDs")
                    return data
                else:
                    logger.error(f"Failed to fetch types: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching types: {e}")
            return []
    
    async def fetch_type_info(self, type_id):
        """Fetch detailed information about a specific type"""
        url = f"{ESI_BASE_URL}/universe/types/{type_id}/"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"Failed to fetch type info for {type_id}: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching type info for {type_id}: {e}")
            return None
    
    async def fetch_market_orders(self, region_id, type_id):
        """Fetch market orders for a specific type in a region"""
        url = f"{ESI_BASE_URL}/markets/{region_id}/orders/"
        params = {"type_id": type_id}
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"Failed to fetch orders for region {region_id}, type {type_id}: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching orders for region {region_id}, type {type_id}: {e}")
            return []
    
    async def fetch_market_history(self, region_id, type_id):
        """Fetch market history for a specific type in a region"""
        url = f"{ESI_BASE_URL}/markets/{region_id}/history/"
        params = {"type_id": type_id}
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"Failed to fetch history for region {region_id}, type {type_id}: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching history for region {region_id}, type {type_id}: {e}")
            return []

def process_orders(orders):
    """Process orders and calculate statistics"""
    if not orders:
        return None
    
    buy_orders = [order for order in orders if not order.get('is_buy_order', True)]
    sell_orders = [order for order in orders if order.get('is_buy_order', True)]
    
    def calculate_stats(order_list):
        if not order_list:
            return None, None, None, 0, 0
        
        prices = [order['price'] for order in order_list]
        volumes = [order['volume_remain'] for order in order_list]
        
        return (
            max(prices),
            min(prices),
            sum(price * volume for price, volume in zip(prices, volumes)) / sum(volumes) if sum(volumes) > 0 else 0,
            sum(volumes),
            len(order_list)
        )
    
    buy_stats = calculate_stats(buy_orders)
    sell_stats = calculate_stats(sell_orders)
    
    return {
        'buy_max': buy_stats[0],
        'buy_min': buy_stats[1],
        'buy_avg': buy_stats[2],
        'buy_volume': buy_stats[3],
        'buy_orders': buy_stats[4],
        'sell_max': sell_stats[0],
        'sell_min': sell_stats[1],
        'sell_avg': sell_stats[2],
        'sell_volume': sell_stats[3],
        'sell_orders': sell_stats[4]
    }

async def update_items_database():
    """Update the items database with current type information"""
    logger.info("Starting items database update...")
    
    async with MarketDataFetcher() as fetcher:
        # Get all type IDs
        type_ids = await fetcher.fetch_types()
        
        # Filter for market types only (basic filtering)
        market_type_ids = type_ids[:1000]  # Limit for testing
        
        db = SessionLocal()
        try:
            for type_id in market_type_ids:
                # Check if item already exists
                existing_item = db.query(Item).filter(Item.type_id == type_id).first()
                if existing_item:
                    continue
                
                # Fetch type information
                type_info = await fetcher.fetch_type_info(type_id)
                if not type_info:
                    continue
                
                # Create new item
                item = Item(
                    type_id=type_id,
                    name=type_info.get('name', f'Unknown Item {type_id}'),
                    group_id=type_info.get('group_id'),
                    market_group_id=type_info.get('market_group_id'),
                    volume=type_info.get('volume'),
                    description=type_info.get('description', ''),
                    published=type_info.get('published', True)
                )
                
                db.add(item)
                
                if len(market_type_ids) % 100 == 0:
                    db.commit()
                    logger.info(f"Processed {len(market_type_ids)} items...")
            
            db.commit()
            logger.info("Items database update completed")
            
        except Exception as e:
            logger.error(f"Error updating items database: {e}")
            db.rollback()
        finally:
            db.close()

async def fetch_market_data():
    """Main function to fetch all market data"""
    logger.info("Starting market data fetch...")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Initialize regions
    db = SessionLocal()
    try:
        for region_id, region_name in REGIONS.items():
            existing_region = db.query(Region).filter(Region.region_id == region_id).first()
            if not existing_region:
                region = Region(region_id=region_id, name=region_name)
                db.add(region)
        db.commit()
    except Exception as e:
        logger.error(f"Error initializing regions: {e}")
        db.rollback()
    finally:
        db.close()
    
    # Update items database
    await update_items_database()
    
    # Fetch market data
    async with MarketDataFetcher() as fetcher:
        db = SessionLocal()
        try:
            # Get all items from database
            items = db.query(Item).limit(100).all()  # Limit for testing
            
            for item in items:
                logger.info(f"Processing item: {item.name} (ID: {item.type_id})")
                
                for region_id in REGIONS.keys():
                    try:
                        # Fetch current orders
                        orders = await fetcher.fetch_market_orders(region_id, item.type_id)
                        order_stats = process_orders(orders)
                        
                        if order_stats:
                            # Save market data
                            market_data = MarketData(
                                type_id=item.type_id,
                                region_id=region_id,
                                **order_stats
                            )
                            db.add(market_data)
                        
                        # Fetch historical data
                        history = await fetcher.fetch_market_history(region_id, item.type_id)
                        for hist_entry in history[-30:]:  # Last 30 days
                            existing_history = db.query(OrderHistory).filter(
                                OrderHistory.type_id == item.type_id,
                                OrderHistory.region_id == region_id,
                                OrderHistory.date == datetime.fromisoformat(hist_entry['date'])
                            ).first()
                            
                            if not existing_history:
                                order_history = OrderHistory(
                                    type_id=item.type_id,
                                    region_id=region_id,
                                    date=datetime.fromisoformat(hist_entry['date']),
                                    average=hist_entry.get('average'),
                                    highest=hist_entry.get('highest'),
                                    lowest=hist_entry.get('lowest'),
                                    order_count=hist_entry.get('order_count'),
                                    volume=hist_entry.get('volume')
                                )
                                db.add(order_history)
                        
                        # Commit every 10 items to avoid large transactions
                        if item.type_id % 10 == 0:
                            db.commit()
                            logger.info(f"Committed data for item {item.type_id}")
                    
                    except Exception as e:
                        logger.error(f"Error processing item {item.type_id} in region {region_id}: {e}")
                        continue
            
            db.commit()
            logger.info("Market data fetch completed successfully")
            
        except Exception as e:
            logger.error(f"Error in market data fetch: {e}")
            db.rollback()
        finally:
            db.close()

if __name__ == "__main__":
    asyncio.run(fetch_market_data())

