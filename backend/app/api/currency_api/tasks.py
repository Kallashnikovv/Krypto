from celery import Celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import http.client
import json

# Konfiguracja Celery z brokerem i backendem
app = Celery('tasks', 
             broker='redis://localhost:6379/0',  # Broker Redis
             backend='redis://localhost:6379/0')  # Backend Redis

@app.task
def fetch_currency_rates(api_key: str, selected_currencies: str):
    """
    Funkcja do pobierania pełnych danych o kursach walut.
    """
    try:
        conn = http.client.HTTPSConnection("api.currencyfreaks.com")
        url = f"/v2.0/rates/latest?apikey={api_key}&symbols={selected_currencies}"
        conn.request("GET", url)
        
        res = conn.getresponse()
        data = res.read()

        if res.status != 200:
            raise Exception(f"API error: {data.decode('utf-8')}")
        
        response_data = json.loads(data.decode("utf-8"))
        return response_data
    
    except Exception as e:
        raise Exception(f"Błąd podczas pobierania kursów walut: {str(e)}")
    finally:
        conn.close()

@app.task
def notify_if_threshold_exceeded(api_key: str, selected_currencies: str, recipient_email: str):
    """
    Funkcja do sprawdzania progów walutowych i wysyłania powiadomień.
    """
    try:
        # Pobierz kursy walut
        currency_data = fetch_currency_rates(api_key, selected_currencies)

        # Przykładowe progi dla walut (dostosuj do swoich potrzeb)
        thresholds = {
            'EUR': 4.5,
            'USD': 4.0,
            'PLN': 1.0
        }

        # Sprawdzanie, czy którykolwiek kurs przekracza próg
        for currency, rate in currency_data['rates'].items():
            if currency in thresholds and rate > thresholds[currency]:
                send_email(recipient_email, currency, rate)

    except Exception as e:
        print(f"Błąd podczas sprawdzania progów: {e}")

def send_email(recipient_email: str, currency: str, rate: float):
    """
    Funkcja do wysyłania powiadomień email.
    """
    sender_email = "twoj_email@example.com"  # Użyj swojego adresu email
    password = "twoje_hasło_emailowe"       # Hasło do konta email

    subject = f"Alert: Kurs {currency} przekroczył próg!"
    body = f"Kurs waluty {currency} wynosi {rate}, co przekracza ustalony próg."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"Powiadomienie wysłane na adres {recipient_email}")
    except Exception as e:
        print(f"Błąd podczas wysyłania emaila: {e}")
