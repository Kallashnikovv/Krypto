import aiohttp
from fastapi import HTTPException

async def get_forex_data(pair: str):
    url = f"https://api.example.com/forex?pair={pair}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise HTTPException(status_code=response.status, detail="Error fetching Forex data")