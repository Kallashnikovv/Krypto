from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import APIRouter, HTTPException
from typing import List
from ..models.cryptocurrencies import CryptoRate

router = APIRouter()

uri = "mongodb+srv://julka2222:atlasatlasmongo@cluster0.gt3kp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

database = client["Crypto"]

@router.get("/", response_description="List all crypto", response_model=List[CryptoRate])
def list_books():
    crypto = list(database["cryptocurrencies"].find(limit=20))
    return crypto

@router.get("/{symbol}", response_description="Get a single crypto by symbol", response_model=CryptoRate)
def find_book(symbol: str):
    if (crypto := database["cryptocurrencies"].find_one({"symbol": symbol})) is not None:
        return crypto
    raise HTTPException(status_code=404, detail=f"Crypto with symbol {symbol} not found")