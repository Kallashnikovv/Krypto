from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import APIRouter, HTTPException
from typing import List
from ..models.cryptocurrencies import CryptoRate
from app.api.cryptocurrency_api.keys import mongopswd as pswd, mongousr as usr

router = APIRouter()

uri = "mongodb+srv://{usr()}:{pswd()}@cluster0.gt3kp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

database = client["Crypto"]

@router.get("/", response_description="List all crypto", response_model=List[CryptoRate])
def list_crypto():
    crypto = list(database["cryptocurrencies"].find(limit=20))
    return crypto

@router.get("/{symbol}", response_description="Get a single crypto by symbol", response_model=CryptoRate)
def find_crypto(symbol: str):
    if (crypto := database["cryptocurrencies"].find_one({"symbol": symbol})) is not None:
        return crypto
    raise HTTPException(status_code=404, detail=f"Crypto with symbol {symbol} not found")