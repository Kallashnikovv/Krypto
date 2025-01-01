import pymongo
from backend.app.api.cryptocurrency_api.keys import mongopswd as pswd, mongousr as usr
from backend.app.api.currency_api.cr_api import forex
from backend.app.models.currencies import Forex
from datetime import datetime
import asyncio

client = pymongo.MongoClient('localhost:27017')

db = client["Crypto"]
collection = db["currencies"]

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

async def main():
    await save_data()

asyncio.run(main())