from fastapi import APIRouter, HTTPException
from typing import List
from backend.app.models.currencies import Forex
from backend.app.db.mongo_connection import database
from backend.app.db.forex_mongo import save_data_to_mongo as save_forex_data

router = APIRouter()

@router.get("/", response_description="List all currencies", response_model=List[Forex])
async def list_curr():
    curr = list(database["currencies"].find(limit=6))
    return curr

@router.get("/{symbol}", response_description="Get a single currency by symbol", response_model=Forex)
async def find_curr(symbol: str):
    if (curr := database["currencies"].find_one({"symbol": symbol})) is not None:
        return curr
    raise HTTPException(status_code=404, detail=f"Currency with symbol {symbol} not found")

@router.api_route("/update", methods=["POST"])
async def update_curr():
    await save_forex_data()
    return {"message": "Data updated successfully"}
