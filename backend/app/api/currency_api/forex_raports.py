import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF
from app.db.mongo_connection import database

collection = database["currencies"]

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
    ax1.set_ylabel('One USD equivalent', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.xticks(rotation=45, ha='right')

    fig.tight_layout()
    plt.title('Currency Info Today')
    plt.legend(loc='upper left')
    plt.savefig('currency_info_today.png', bbox_inches='tight')
    plt.show()


def priceDiffYestTod(data):
    today = data[data['timestamp'].dt.date == datetime.today().date()]
    yesterday = data[data['timestamp'].dt.date == (datetime.today().date() - timedelta(days=1))]

    results = []

    for symbol in today['symbol'].unique():
        today_row = today[today['symbol'] == symbol]
        yesterday_row = yesterday[yesterday['symbol'] == symbol]

        if not today_row.empty and not yesterday_row.empty:
            today_price = today_row['price'].iloc[0]
            yesterday_price = yesterday_row['price'].iloc[0]

            price_diff = yesterday_price - today_price
            percentage_diff = (price_diff / yesterday_price) * 100

            results.append({
                'symbol': symbol,
                'name': today_row['symbol'].iloc[0],
                'price_diff': price_diff,
                'percentage_diff': percentage_diff
            })

    return pd.DataFrame(results)


def summary_statistics(data):
    today = showAllCoinInfoToday(data)
    price_diffs = priceDiffYestTod(data)

    most_needed = today.loc[today['price'].idxmax()]
    least_needed = today.loc[today['price'].idxmin()]
    max_diff = price_diffs.loc[price_diffs['percentage_diff'].idxmax()] if not price_diffs.empty else None
    min_diff = price_diffs.loc[price_diffs['percentage_diff'].idxmin()] if not price_diffs.empty else None

    return {
        "most_needed": most_needed,
        "least_needed": least_needed,
        "max_diff": max_diff,
        "min_diff": min_diff,
    }



class PDF(FPDF):
    def add_summary(self, stats):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Summary Statistics', 0, 1)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f"Currency Requiring Most Units for 1 USD: {stats['most_needed']['symbol']} ({stats['most_needed']['price']:.2f})", 0, 1)
        self.cell(0, 10, f"Currency Requiring Least Units for 1 USD: {stats['least_needed']['symbol']} ({stats['least_needed']['price']:.2f})", 0, 1)
        if stats['max_diff'] is not None:
            self.cell(0, 10, f"Highest Percentage Increase: {stats['max_diff']['symbol']} ({stats['max_diff']['percentage_diff']:.2f}%)", 0, 1)
        if stats['min_diff'] is not None:
            self.cell(0, 10, f"Highest Percentage Decrease: {stats['min_diff']['symbol']} ({stats['min_diff']['percentage_diff']:.2f}%)", 0, 1)

    def add_table(self, data):
        self.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, 'Today\'s Data', 0, 1)
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
            self.cell(40, 10, f"{row['price_diff']:.2f}", 1)
            self.cell(60, 10, f"{row['percentage_diff']:.2f}%", 1)
            self.ln()

today_data = showAllCoinInfoToday(data)
showPriceInfoTodayMat(today_data)
price_diff_data = priceDiffYestTod(data)
stats = summary_statistics(data)

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 10, 'Currency Prices Report', 0, 1, 'C')
pdf.ln(5)
pdf.add_summary(stats)
pdf.ln(5)
pdf.add_table(today_data)
pdf.ln(5)
pdf.image('currency_info_today.png', w=160, h=100)
pdf.ln(15)
pdf.add_table_diff(price_diff_data)
pdf.output('currency_report.pdf', 'F')

