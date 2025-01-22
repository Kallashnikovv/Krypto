from app.api.currency_api.cr_api import forex
from app.models.currencies import Forex
from datetime import datetime
import asyncio
from app.db.mongo_connection import database
import aiohttp

collection = database["currencies"]

async def save_data_to_mongo():
    try:
        await save_data()
    except (aiohttp.ClientConnectionError, aiohttp.ClientTimeout) as e:
        print(e)

async def save_data():
    data = await forex()
    timestamp = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
    docs = [
        Forex(timestamp=timestamp, symbol=symbol, price=float(price))
        for symbol, price in data['rates'].items() # rates {{symbol: price}, ... , ...}
    ]

    for currency in docs:
        currency_dict = currency.model_dump()
        collection.insert_one(currency_dict)
