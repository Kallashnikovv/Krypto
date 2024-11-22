from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.currencies import Forex
from app.api.cryptocurrency_api.keys import mongopswd as pswd, mongousr as usr

router = APIRouter()

uri = f"mongodb+srv://{usr()}2:{pswd()}@cluster0.gt3kp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

database = client["Crypto"]

@router.get("/", response_description="List all currencies", response_model=List[Forex])
def list_curr():
    curr = list(database["currencies"].find(limit=6))
    return curr

@router.get("/{symbol}", response_description="Get a single currency by symbol", response_model=Forex)
def find_curr(symbol: str):
    if (curr := database["currencies"].find_one({"symbol": symbol})) is not None:
        return curr
    raise HTTPException(status_code=404, detail=f"Currency with symbol {symbol} not found")