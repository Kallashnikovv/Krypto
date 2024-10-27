import apikey

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5', # number of cryptocurrencies showed
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': apikey.key(),
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  # print(data)
  # remove below (until 'except') and uncomment line above after testing the code
  print(f"{'ID':<5} {'Name':<20} {'Symbol':<8} {'Price (USD)':<12} {'Percent change (1 hr)':<15}")
  print('-' * 80)

  for currency in data['data']:
    id = currency['id']
    name = currency['name']
    symbol = currency['symbol']
    price = currency['quote']['USD']['price']
    percentage = round(currency['quote']['USD']['percent_change_1h'],2)

    if percentage < 0:
      color = '\033[31m'
    elif percentage > 0:
      color = '\033[32m'
    else:
      color = '\033[33m'

    print(f"{color}{id:<5} {name:<20} {symbol:<8} {round(price,2):<12} {percentage:<15}{'\033[0m'}")
    
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)