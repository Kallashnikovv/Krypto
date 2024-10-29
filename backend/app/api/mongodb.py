from pydantic import BaseModel, Field
from pymongo import MongoClient, ASCENDING
from datetime import datetime
from typing import Optional
import asyncio
import aiohttp
import apikey

#Data Models
class CryptoRate(BaseModel):
    id: int
    name: str
    symbol: str
    price_usd: float
    percent_change_1h: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)

#MongoDB connection
client = MongoClient('mongodb+srv://dudamarcin539:H3eNOTJ6GpDKUBBJ@cluster.qimi8.mongodb.net/')
db = client['Crypto']
cryptocurrencies = db['cryptocurrencies']

#Indexes
cryptocurrencies.create_index([('id', ASCENDING)], unique=True)
cryptocurrencies.create_index([('symbol', ASCENDING)])
cryptocurrencies.create_index([('timestamp', ASCENDING)])
cryptocurrencies.create_index([('symbol', ASCENDING), ('timestamp', ASCENDING)])

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '5',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': apikey.key(),
}

async def fetch_data(session):
    async with session.get(url, params=parameters, headers=headers) as response:
        return await response.json()

async def save_data_to_mongo():
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session)
        for currency in data['data']:
            crypto_data = CryptoRate(
                id=currency['id'],
                name=currency['name'],
                symbol=currency['symbol'],
                price_usd=currency['quote']['USD']['price'],
                percent_change_1h=currency['quote']['USD'].get('percent_change_1h')
            )
            #upsert
            cryptocurrencies.update_one(
                {'id': crypto_data.id},
                {'$set': crypto_data.dict()},
                upsert=True
            )
try:
    asyncio.run(save_data_to_mongo())
except (aiohttp.ClientConnectionError, aiohttp.ClientTimeout) as e:
    print(e)
