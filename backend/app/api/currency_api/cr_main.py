from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tasks import fetch_currency_rates, notify_if_threshold_exceeded
from celery.result import AsyncResult

app = FastAPI()

# Ustawienie folderu static dla favicon
app.mount("/static", StaticFiles(directory="static"), name="static")

# Twój klucz API z Currency Freaks
API_KEY = "c5feddd53b494b80ab303789d4a0645d"
# Waluty, które będą monitorowane
SELECTED_CURRENCIES = "EUR,USD,PLN,JPY,KRW,CAD,NZD"

@app.get("/")
def read_root():
    return {"message": "Currency Rates and Threshold Notification Service"}

@app.get("/currency_rates/")
def get_currency_rates():
    """
    Endpoint do pobierania szczegółowych danych o kursach walut.
    """
    result = fetch_currency_rates.delay(API_KEY, SELECTED_CURRENCIES)
    
    # Zwracamy tylko task_id i informację, że zadanie zostało uruchomione
    return {"task_id": result.id, "message": "Zadanie uruchomione! Sprawdź status zadania."}

@app.get("/check_task/{task_id}")
def check_task_status(task_id: str):
    """
    Endpoint do sprawdzania statusu zadania Celery.
    """
    result = AsyncResult(task_id)
    
    if result.state == "SUCCESS":
        return {"task_id": task_id, "status": "completed", "result": result.result}
    elif result.state == "FAILURE":
        return {"task_id": task_id, "status": "failed", "error": str(result.result)}
    else:
        return {"task_id": task_id, "status": result.state}

@app.post("/check_thresholds/")
def check_thresholds(recipient_email: str):
    """
    Endpoint do sprawdzania progów cenowych i wysyłania powiadomień.
    """
    result = notify_if_threshold_exceeded.delay(API_KEY, SELECTED_CURRENCIES, recipient_email)
    return {"task_id": result.id, "message": "Zadanie sprawdzania progów zostało uruchomione!"}
