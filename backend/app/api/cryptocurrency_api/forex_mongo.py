import pymongo
from app.api.cryptocurrency_api.keys import mongopswd as pswd, mongousr as usr
from app.api.currency_api.cr_api import forex
from app.models.currencies import Forex
from datetime import datetime
import asyncio

client = pymongo.MongoClient(f"mongodb+srv://{usr()}:{pswd()}@cluster0.gt3kp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

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
        currency_dict = currency.dict()
        collection.insert_one(currency_dict)

async def main():
    await save_data()

asyncio.run(main())