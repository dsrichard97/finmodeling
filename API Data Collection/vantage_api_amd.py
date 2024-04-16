import requests
import pandas as pd
from datetime import datetime, timedelta

# Replace 'YOUR_API_KEY' with your Alpha Vantage API key
API_KEY = 'YOUR_API_KEY'
SYMBOL = 'AMD'  # Set the symbol to AMD

def get_monthly_stock_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def clean_data(data):
    df = pd.DataFrame(data['Monthly Time Series']).T
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df.index = pd.to_datetime(df.index)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def main():
    # Fetch data
    raw_data = get_monthly_stock_data(SYMBOL, API_KEY)
    # Clean data
    clean_df = clean_data(raw_data)
    # Since we are analyzing three years of data
    three_years_ago = datetime.now() - timedelta(days=3*365)
    filtered_df = clean_df[clean_df.index >= three_years_ago]
    print(filtered_df.head())
    return filtered_df

# Uncomment the line below to run the function
df = main()





