from datetime import date
from enum import unique

from pymongo import MongoClient, ASCENDING
import asyncio
import aiohttp
import apikey
from backend.app.models.cryptocurrencies import CryptoRate
from bitcoin import fetch_data
import json


#MongoDB connection
client = MongoClient('mongodb+srv://dudamarcin539:H3eNOTJ6GpDKUBBJ@cluster.qimi8.mongodb.net/')
db = client['Crypto']
cryptocurrencies = db['cryptocurrencies']

#Indexes
cryptocurrencies.create_index([('id', ASCENDING)], unique=False)
cryptocurrencies.create_index([('symbol', ASCENDING)])
cryptocurrencies.create_index([('timestamp', ASCENDING)])
cryptocurrencies.create_index([('symbol', ASCENDING), ('timestamp', ASCENDING)])

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/historical'
parameters = {
    'time_start': '2023-10-01T00:00',
    'time_end': '2023-10-03T00:00',
    'start': '1',
    'limit': '5',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': apikey.key(),
}

async def save_data_to_mongo():
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session)
        for currency in data['data']:
            crypto_data = CryptoRate(
                id=currency['id'],
                name=currency['name'],
                symbol=currency['symbol'],
                price_usd=currency['quote']['USD']['price'],
                percent_change_1h=currency['quote']['USD'].get('percent_change_1h'),
                percent_change_24h=currency['quote']['USD'].get('percent_change_24h')
             )
            cryptocurrencies.insert_one(crypto_data.dict())
try:
    asyncio.run(save_data_to_mongo())
except (aiohttp.ClientConnectionError, aiohttp.ClientTimeout) as e:
    print(e)