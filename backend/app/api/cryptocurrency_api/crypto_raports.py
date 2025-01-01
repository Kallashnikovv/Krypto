from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF

client = MongoClient("mongodb://localhost:27017/")

# currencies

db = client["Crypto"]
collection = db["cryptocurrencies"]

cryptocurrencies = collection.find()
data = pd.DataFrame(cryptocurrencies)
data = data.drop(columns='_id')

def showAllCoinInfoToday():
    today = data[data['timestamp'].dt.date == datetime.today().date()]
    return today

def showPriceInfoToday(data):
    today = showPriceInfoToday(data)
    return today[['name', 'price', 'percentage']]

def showPriceInfoTodayMat(data):
    names = data['name']
    prices = data['price']
    percentages = data['percentage']
    
    fig, ax1 = plt.subplots(figsize=(12, 8))

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
    plt.savefig('cryptocurrency_info_today.png', bbox_inches='tight')
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

class PDF(FPDF):
    def add_table(self, data):
        self.set_font('Arial', 'B', 12)
        self.cell(40, 8, 'Symbol', 1)
        self.cell(40, 8, 'Name', 1)
        self.cell(40, 8, 'Price', 1)
        self.cell(40, 8, 'Percentage', 1)
        self.cell(30, 8, 'Timestamp', 1)
        self.ln()
        self.set_font('Arial', '', 12)
        for index, row in data.iterrows():
            self.cell(40, 10, row['symbol'], 1)
            self.cell(40, 10, row['name'], 1)
            self.cell(40, 10, f"{row['price']:.2f}", 1)
            self.cell(40, 10, f"{row['percentage']:.2f}", 1)
            self.cell(30, 10, row['timestamp'].strftime('%Y-%m-%d'), 1)
            self.ln()
pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 12)
pdf.cell(40, 10, 'Cryptocurrencies Report', 0, 1)
pdf.ln(5)
pdf.add_table(today_data)
pdf.ln(5)
pdf.image('cryptocurrency_info_today.png', w = 160, h = 100)
pdf.output('cryptocurrency_report.pdf', 'F')