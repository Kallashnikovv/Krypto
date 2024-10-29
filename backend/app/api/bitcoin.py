import apikey
import asyncio
import aiohttp
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5', # number of cryptocurrencies showed
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': apikey.key(),
}

async def fetch_data(session):
  async with session.get(url, params=parameters, headers=headers) as response:
    return await response.json()

try:
  async def get_data():
    async with aiohttp.ClientSession() as session:
      data = await fetch_data(session)

      for currency in data['data']:
        id = currency['id']
        name = currency['name']
        symbol = currency['symbol']
        price = currency['quote']['USD']['price']
        percentage = round(currency['quote']['USD']['percent_change_1h'],2)

  asyncio.run(get_data())
    
except (aiohttp.ClientConnectionError, aiohttp.ClientTimeout) as e:
  print(e)
