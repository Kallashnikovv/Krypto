from pymongo import MongoClient, ASCENDING
import asyncio
import aiohttp
import apikey
from backend.app.models.cryptocurrencies import CryptoRate
from bitcoin import fetch_data
import json

#MongoDB connection
client = MongoClient('localhost:27017')
db = client['Crypto']
cryptocurrencies = db['cryptocurrencies']

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
  'X-CMC_PRO_API_KEY': apikey.key(),
}

async def save_data_to_mongo():
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session)
        for symbols in data['data']:
            currency = data['data'][symbols][0]
            crypto_data = CryptoRate(
            id = currency['id'],
            symbol = currency['symbol'],
            name = currency['name'],
            price = currency['quote']['USD']['price'],
            percentage = currency['quote']['USD']['percent_change_1h']
             )
            cryptocurrencies.insert_one(crypto_data.dict())
try:
    asyncio.run(save_data_to_mongo())
except (aiohttp.ClientConnectionError, aiohttp.ClientTimeout) as e:
    print(e)