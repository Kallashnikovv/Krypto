from fastapi import APIRouter, HTTPException
from typing import List
from app.models.cryptocurrencies import CryptoRate
from app.db.mongo_connection import database
from app.db.crypto_mongo import save_data_to_mongo as save_crypto_data

router = APIRouter()

@router.get("/", response_description="List all crypto", response_model=List[CryptoRate])
async def list_crypto():
    crypto = list(database["cryptocurrencies"].find(limit=20))
    return crypto

@router.get("/{symbol}", response_description="Get a single crypto by symbol", response_model=CryptoRate)
async def find_crypto(symbol: str):
    if (crypto := database["cryptocurrencies"].find_one({"symbol": symbol})) is not None:
        return crypto
    raise HTTPException(status_code=404, detail=f"Crypto with symbol {symbol} not found")

@router.api_route("/update", methods=["POST"])
async def update_crypto():
    await save_crypto_data()
    return {"message": "Data updated successfully"}
