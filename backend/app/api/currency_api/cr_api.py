import logging
import os
from fastapi import FastAPI, HTTPException
from aiohttp import ClientSession
from celery import Celery
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import asyncio
from fastapi.staticfiles import StaticFiles
from typing import List

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["forex"]
collection = db["rates"]

API_KEY = "c5feddd53b494b80ab303789d4a0645d"
BASE_URL = "https://api.currencyfreaks.com/latest"

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/currency_rates")
async def get_currency_rates():
    return {"rates": "Rates will be here"}

@app.get("/forex/{base_currency}")
async def get_forex_rates(base_currency: str):
    """
    Endpoint do pobierania kursów walut dla konkretnej waluty bazowej.
    """
    try:
        task = fetch_forex_rates.apply_async(args=[base_currency])
        logger.info(f"Task {task.id} started for base currency: {base_currency}")
        return {"task_id": task.id, "status": "Processing"}
    except Exception as e:
        logger.error(f"Error in get_forex_rates for {base_currency}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """
    Endpoint do sprawdzania statusu zadania Celery.
    """
    try:
        task_result = fetch_forex_rates.AsyncResult(task_id)

        if task_result.state == "PENDING":
            return {"task_id": task_id, "status": "Pending"}
        elif task_result.state == "SUCCESS":
            return {"task_id": task_id, "status": "Success", "result": task_result.result}
        elif task_result.state == "FAILURE":
            return {"task_id": task_id, "status": "Failure", "error": str(task_result.info)}

        return {"task_id": task_id, "status": task_result.state}
    except Exception as e:
        logger.error(f"Error in get_task_status for task_id {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@celery.task
def fetch_forex_rates(base_currency: str):
    """
    Zadanie Celery do pobrania kursów walut z currencyfreaks.com i zapisania do MongoDB.
    """
    async def fetch_data():
        try:
            async with ClientSession() as session:
                params = {"apikey": API_KEY, "base": base_currency}
                async with session.get(BASE_URL, params=params) as response:
                    if response.status != 200:
                        logger.error(f"Failed to fetch data for {base_currency}. Status code: {response.status}")
                        raise HTTPException(status_code=response.status, detail=await response.text())
                    return await response.json()
        except Exception as e:
            logger.error(f"Error fetching data for {base_currency}: {str(e)}")
            raise

    try:
        forex_data = asyncio.run(fetch_data())

        document = {
            "_id": ObjectId(),
            "date": datetime.utcnow().isoformat(),
            "base": forex_data.get("base"),
            "rates": forex_data.get("rates"),
            "timestamp": forex_data.get("date")
        }

        collection.insert_one(document)
        logger.info(f"Forex data for {base_currency} inserted into MongoDB")

        check_price_thresholds(forex_data.get("rates"), base_currency)

        return document
    except Exception as e:
        logger.error(f"Error in fetch_forex_rates for {base_currency}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error in fetching or saving data")

def check_price_thresholds(rates: dict, base_currency: str):
    """
    Funkcja do sprawdzania, czy kursy walut przekroczyły ustalone progi cenowe.
    Powiadomienia.
    """
    price_thresholds = {
        "USD": 1.20,
        "EUR": 4.50,
        "PLN": 5.00
    }

    for currency, rate in rates.items():
        if currency in price_thresholds and rate >= price_thresholds[currency]:
            logger.info(f"Alert! {currency} has crossed the threshold. Current rate: {rate}")
            send_price_alert(currency, rate, base_currency)

def send_price_alert(currency: str, rate: float, base_currency: str):
    """
    Funkcja do wysyłania powiadomień gdy próg cenowy został przekroczony.
    """
    logger.info(f"Sending price alert for {currency}: {rate} (Base: {base_currency})")

