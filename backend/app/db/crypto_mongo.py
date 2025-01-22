from pymongo import ASCENDING
import asyncio
import aiohttp
import app.api.keys as keys
from app.models.cryptocurrencies import CryptoRate
from app.api.cryptocurrency_api.bitcoin import fetch_data
import app.api.keys as keys
from datetime import datetime
from app.db.mongo_connection import database

#MongoDB connection
cryptocurrencies = database['cryptocurrencies']

#Indexes
cryptocurrencies.create_index([('id', ASCENDING)], unique=False)
cryptocurrencies.create_index([('symbol', ASCENDING)])

url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
selected_crypto = 'ADA,AVAX,BNB,BTC,DOGE,ETH,HEX,SOL,USDC,USDT,XRP' # chosen cryptocurrencies

parameters = {
  'symbol': selected_crypto,
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': keys.crypto_key()
}

async def save_data_to_mongo():
    try:
        await save_data()
    except (aiohttp.ClientConnectionError, aiohttp.ClientTimeout) as e:
        print(e)

async def save_data():
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session)
        for symbols in data['data']:
            currency = data['data'][symbols][0]
            crypto_data = CryptoRate(
            id = currency['id'],
            symbol = currency['symbol'],
            name = currency['name'],
            price = currency['quote']['USD']['price'],
            percentage = currency['quote']['USD']['percent_change_1h'],
            timestamp = datetime.now()
             )
            cryptocurrencies.insert_one(crypto_data.model_dump())
