import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

# List of tickers to track
tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']

# Set up SQLite DB
engine = create_engine('sqlite:///stock_data.db', echo=False)

def fetch_and_store(ticker):
    print(f"Fetching data for {ticker}")
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5y")
    
    # Add ticker name as a column
    hist['Ticker'] = ticker
    hist.reset_index(inplace=True)
    
    # Save to SQL
    hist.to_sql('stock_prices', engine, if_exists='append', index=False)

if __name__ == "__main__":
    for ticker in tickers:
        fetch_and_store(ticker)
    print("All data saved to stock_data.db")
