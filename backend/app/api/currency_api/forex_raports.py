from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF

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
    
    fig, ax1 = plt.subplots(figsize=(12, 8))

    color = 'tab:blue'
    ax1.bar(symbols, prices, color=color, label='Price')
    ax1.set_xlabel('Currency Name')
    ax1.set_ylabel('Price (USD)', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.xticks(rotation=45, ha='right')

    fig.tight_layout()
    plt.title('Currency Info Today')
    plt.legend(loc='upper left')
    plt.savefig('currency_info_today.png', bbox_inches='tight')
    plt.show()

today_data = showAllCoinInfoToday(data)
showPriceInfoTodayMat(today_data)

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

class PDF(FPDF):
    def add_table(self, data):
        self.set_font('Arial', 'B', 12)
        self.cell(40, 10, 'Symbol', 1)
        self.cell(40, 10, 'Price', 1)
        self.cell(40, 10, 'Timestamp', 1)
        self.ln()
        self.set_font('Arial', '', 12)
        for index, row in data.iterrows():
            self.cell(40, 10, row['symbol'], 1)
            self.cell(40, 10, f"{row['price']:.2f}", 1)
            self.cell(40, 10, row['timestamp'].strftime('%Y-%m-%d'), 1)
            self.ln()
pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 12)
pdf.cell(40, 10, 'Currency Prices Report', 0, 1)
pdf.ln(20)
pdf.add_table(today_data)
pdf.ln(20)
pdf.image('currency_info_today.png', w = 160, h = 100)
pdf.output('currency_report.pdf', 'F')
