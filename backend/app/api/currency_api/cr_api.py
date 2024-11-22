import aiohttp
from app.api.cryptocurrency_api.keys import forex_key as key

currencies = "EUR,PLN,JPY,KRW,CAD,NZD"  # currencies
key = key()

url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={key()}&symbols={currencies}"

async def fetch_currency_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data

async def forex():
    currency_data = await fetch_currency_data()
    return currency_data