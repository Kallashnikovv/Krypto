from fastapi import FastAPI, HTTPException
import http.client
import json

app = FastAPI()

CURRENCY_FREAKS_API_KEY = 'c5feddd53b494b80ab303789d4a0645d'  # klucz API
SELECTED_CURRENCIES = "EUR,USD,PLN,JPY,KRW,CAD,NZD"

@app.get("/crypto_rates")
async def get_crypto_rates():
    conn = http.client.HTTPSConnection("api.currencyfreaks.com")
    payload = ''
    headers = {}
    url = f"/v2.0/rates/latest?apikey={CURRENCY_FREAKS_API_KEY}&symbols={SELECTED_CURRENCIES}"
    from fastapi import FastAPI, HTTPException
import http.client
import json

app = FastAPI()

CURRENCY_FREAKS_API_KEY = 'c5feddd53b494b80ab303789d4a0645d'  # klucz API
SELECTED_CURRENCIES = "EUR,PLN,JPY,KRW,CAD,NZD"  # waluty

@app.get("/currency_rates")
async def get_currency_rates():
    conn = http.client.HTTPSConnection("api.currencyfreaks.com")
    payload = ''
    headers = {}
    url = f"/v2.0/rates/latest?apikey={CURRENCY_FREAKS_API_KEY}&symbols={SELECTED_CURRENCIES}"
    
    try:
        conn.request("GET", url, payload, headers)
        res = conn.getresponse()
        data = res.read()
        
        if res.status != 200:
            raise HTTPException(status_code=res.status, detail=data.decode("utf-8"))
        
        # Przetworzenie danych
        response_data = json.loads(data.decode("utf-8"))
        result = {
            "date": response_data.get("date"),
            "base": response_data.get("base"),
            "rates": {symbol: response_data["rates"].get(symbol) for symbol in SELECTED_CURRENCIES.split(",")}
        }
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()