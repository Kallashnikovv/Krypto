import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF
from backend.app.db.mongo_connection import database


collection = database["cryptocurrencies"]

cryptocurrencies = collection.find()
data = pd.DataFrame(cryptocurrencies)
data = data.drop(columns='_id')
data['timestamp'] = pd.to_datetime(data['timestamp'])  # Ensure timestamp is datetime

def showAllCoinInfoToday(data):
    today = data[data['timestamp'].dt.date == datetime.today().date()]
    return today

def showPriceInfoToday(data):
    today = showAllCoinInfoToday(data)
    return today[['name', 'price', 'percentage']]

def showPriceInfoTodayMat(data):
    today = showAllCoinInfoToday(data)
    names = today['name']
    prices = today['price']
    percentages = today['percentage']
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
    plt.close()

def priceDiffYestTod(data):
    today = data[data['timestamp'].dt.date == datetime.today().date()]
    yesterday = data[data['timestamp'].dt.date == (datetime.today().date() - timedelta(days=1))]

    results = []
    for symbol in today['symbol'].unique():
        todayPrice = today[today['symbol'] == symbol]['price'].iloc[0]
        yesterdayPrice = yesterday[yesterday['symbol'] == symbol]['price'].iloc[0] if not yesterday[yesterday['symbol'] == symbol].empty else None

        if yesterdayPrice is not None:
            priceDiff = todayPrice - yesterdayPrice
            percentageDiff = (priceDiff / yesterdayPrice) * 100
            results.append({
                'symbol': symbol,
                'name': today[today['symbol'] == symbol]['name'].iloc[0],
                'price_diff': priceDiff,
                'percentage_diff': percentageDiff
            })
    return pd.DataFrame(results)

def summary_statistics(data):
    today = showAllCoinInfoToday(data)
    avg_price = today['price'].mean()
    most_expensive = today.loc[today['price'].idxmax()]
    max_percent_increase = today.loc[today['percentage'].idxmax()]
    max_percent_decrease = today.loc[today['percentage'].idxmin()]

    return {
        "avg_price": avg_price,
        "most_expensive": most_expensive,
        "max_percent_increase": max_percent_increase,
        "max_percent_decrease": max_percent_decrease
        }

class PDF(FPDF):
    def add_summary(self, stats):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Summary Statistics', 0, 1)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f"Average Price: ${stats['avg_price']:.2f}", 0, 1)
        self.cell(0, 10, f"Most Expensive: {stats['most_expensive']['name']} (${stats['most_expensive']['price']:.2f})", 0, 1)
        self.cell(0, 10, f"Highest Price Increase (In %): {stats['max_percent_increase']['name']} ({stats['max_percent_increase']['percentage']:.2f}%)", 0, 1)
        self.cell(0, 10, f"Highest Price Decrease (In %): {stats['max_percent_decrease']['name']} ({stats['max_percent_decrease']['percentage']:.2f}%)", 0, 1)
        self.ln(10)

    def add_table(self, data):
        self.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, 'Today\'s Data', 0, 1)
        self.cell(40, 8, 'Symbol', 1)
        self.cell(40, 8, 'Name', 1)
        self.cell(40, 8, 'Price', 1)
        self.cell(40, 8, 'Percentage', 1)
        self.cell(30, 8, 'Timestamp', 1)
        self.ln()
        self.set_font('Arial', '', 12)
        for _, row in data.iterrows():
            self.cell(40, 10, row['symbol'], 1)
            self.cell(40, 10, row['name'], 1)
            self.cell(40, 10, f"${row['price']:.2f}", 1)
            self.cell(40, 10, f"{row['percentage']:.2f}%", 1)
            self.cell(30, 10, row['timestamp'].strftime('%Y-%m-%d'), 1)
            self.ln()

    def add_table_diff(self, data):
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, 'Price Difference from Yesterday', 0, 1)
        self.set_font('Arial', 'B', 12)
        self.cell(40, 8, 'Symbol', 1)
        self.cell(40, 8, 'Name', 1)
        self.cell(40, 8, 'Price Difference', 1)
        self.cell(60, 8, 'Percentage Difference', 1)
        self.ln()
        self.set_font('Arial', '', 12)
        for _, row in data.iterrows():
            self.cell(40, 10, row['symbol'], 1)
            self.cell(40, 10, row['name'], 1)
            self.cell(40, 10, f"${row['price_diff']:.2f}", 1)
            self.cell(60, 10, f"{row['percentage_diff']:.2f}%", 1)
            self.ln()

# Generate Report
today_data = showAllCoinInfoToday(data)
showPriceInfoTodayMat(data)
price_diff_data = priceDiffYestTod(data)
stats = summary_statistics(data)

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 10, 'Cryptocurrency Prices Report', 0, 1, 'C')
pdf.ln(5)
pdf.add_summary(stats)
pdf.ln(5)
pdf.add_table(today_data)
pdf.ln(5)
pdf.image('cryptocurrency_info_today.png', w=160, h=100)
pdf.ln(20)
pdf.add_table_diff(price_diff_data)
pdf.output('cryptocurrency_report.pdf', 'F')
