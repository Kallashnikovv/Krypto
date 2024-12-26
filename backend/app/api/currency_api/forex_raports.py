from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

client = MongoClient("mongodb://localhost:27017/")
db = client["Crypto"]
collection = db["currencies"]

currencies = collection.find()
data = pd.DataFrame(currencies)
data = data.drop(columns='_id')

def showAllCoinInfoToday(data):
    today = data[data['timestamp'].dt.date == datetime.today().date()]
    return today

def showPriceInfoToday(data):
    today = showPriceInfoToday(data)
    return today['symbol', 'price']

def showPriceInfoTodayMat(data):
    symbols = data['symbol']
    prices = data['price']
    
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.bar(symbols, prices, color=color, label='Price')
    ax1.set_xlabel('Currency Name')
    ax1.set_ylabel('Price (USD)', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.xticks(rotation=45, ha='right')

    fig.tight_layout()
    plt.title('Currency Info Today')
    plt.legend(loc='upper left')
    plt.show()

today_data = showAllCoinInfoToday(data)
print(showPriceInfoTodayMat(today_data))

#print(showAllCoinInfoToday(data))

def avgPriceAllCoinsToday(data):
    today = data[data['timestamp'].dt.date == datetime.today().date()]
    avg = today['price'].mean()
    return avg

#print(avgPriceAllCoinsToday(data))

def avgPricePerCoinToday(data):
    #not really an avg since we only can get one info per coin per day
    today = data[['symbol', 'price']][data['timestamp'].dt.date == datetime.today().date()]
    return today

#print(avgPricePerCoinToday(data))

def mostExpensiveToday(data):
    today = data[data['timestamp'].dt.date == datetime.today().date()]
    index = today['price'].idxmax()
    mostExpensive = today.loc[index, ['price', 'symbol']]

    return mostExpensive

#print(mostExpensiveToday(data))

def priceDiffYestTod(data): #today and yesterday
    today = data[data['timestamp'].dt.date == datetime.today().date()]
    x = datetime.today().date() - timedelta(days=1)
    yesterday = data[data['timestamp'].dt.date == x]

    results = []

    for symbol in today['symbol']:
        todayPrice = today[today['symbol'] == symbol]['price']
        yesterdayPrice = yesterday[yesterday['symbol'] == symbol]['price']
        
        priceDiff = todayPrice - yesterdayPrice
        
        results.append({
            'symbol': symbol,
            'name': today[today['symbol'] == symbol],
            'price_diff': priceDiff,
        })
            
    
    return pd.DataFrame(results)