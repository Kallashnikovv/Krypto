from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

client = MongoClient("mongodb://localhost:27017/")

# currencies

db = client["Crypto"]
collection = db["cryptocurrencies"]

cryptocurrencies = collection.find()
data = pd.DataFrame(cryptocurrencies)
data = data.drop(columns='_id')

def showAllCoinInfoToday():
    today = data[data['date'].dt.date == datetime.today().date()]
    return today

def showPriceInfoToday(data):
    today = showPriceInfoToday(data)
    return today[['name', 'price', 'percentage']]

def showPriceInfoTodayMat(data):
    names = data['name']
    prices = data['price']
    percentages = data['percentage']
    
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.bar(names, prices, color=color, label='Price')
    ax1.set_xlabel('Cryptocurrency Name')
    ax1.set_ylabel('Price (USD)', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.xticks(rotation=45, ha='right')

    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.plot(names, percentages, color=color, marker='o', label='Percentage Change')
    ax2.set_ylabel('Percentage Change (%)', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title('Cryptocurrency Info Today')
    plt.legend(loc='upper left')
    plt.show()

today_data = showAllCoinInfoToday()
print(showPriceInfoTodayMat(today_data))

#print(showAllCoinInfoToday(data))

def avgPriceAllCoinsToday(data):
    today = data[data['date'].dt.date == datetime.today().date()]
    avg = today['price'].mean()
    return avg

#print(avgPriceAllCoinsToday(data))

def avgPricePerCoinToday(data):
    #not really an avg since we only can get one info per coin per day
    today = data[['symbol', 'name', 'price']][data['date'].dt.date == datetime.today().date()]
    return today

#print(avgPricePerCoinToday(data))

def mostExpensiveToday(data):
    today = data[data['date'].dt.date == datetime.today().date()]
    index = today['price'].idxmax()
    mostExpensive = today.loc[index, ['price', 'name', 'symbol']]

    return mostExpensive

#print(mostExpensiveToday(data))

def priceDiffYestTod(data): #today and yesterday
    today = data[data['date'].dt.date == datetime.today().date()]
    x = datetime.today().date() - timedelta(days=1)
    yesterday = data[data['date'].dt.date == x]

    results = []

    for symbol in today['symbol']:
        todayPrice = today[today['symbol'] == symbol]['price']
        yesterdayPrice = yesterday[yesterday['symbol'] == symbol]['price']
        
        priceDiff = todayPrice - yesterdayPrice
        percentageDiff = (priceDiff / yesterdayPrice) * 100
        
        results.append({
            'symbol': symbol,
            'name': today[today['symbol'] == symbol]['name'],
            'price_diff': priceDiff,
            'percentage_diff': percentageDiff
        })
            
    
    return pd.DataFrame(results)