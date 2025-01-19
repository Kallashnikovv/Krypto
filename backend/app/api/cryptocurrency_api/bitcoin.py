from backend.app.api.keys import crypto_key as key
import asyncio
import aiohttp

url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
selected_crypto = 'ADA,AVAX,BNB,BTC,DOGE,ETH,HEX,SOL,USDC,USDT,XRP' # chosen cryptocurrencies

parameters = {
  'symbol': selected_crypto,
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': key(),
}

async def fetch_data(session):
  async with session.get(url, params=parameters, headers=headers) as response:
    return await response.json()

async def get_data():
  try:
    async with aiohttp.ClientSession() as session:
      data = await fetch_data(session)

    for symbols in data['data']:
      currency = data['data'][symbols][0]

      id = currency['id']
      symbol = currency['symbol']
      name = currency['name']
      price = currency['quote']['USD']['price']
      percentage = currency['quote']['USD']['percent_change_1h']
      
  except (aiohttp.ClientConnectionError, aiohttp.ClientTimeout) as e:
    print(e)
