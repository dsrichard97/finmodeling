import requests
import pandas as pd
from datetime import datetime
from pandas.tseries.offsets import DateOffset

API_KEY = 'PKK29WJL5N244LAV'
SYMBOL = 'AMD'

def get_monthly_stock_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}")
    data = response.json()
    # Debug print to see the structure of API response
    print(data)
    if "Monthly Time Series" not in data:
        raise Exception("Monthly data not found in the response. Check the API and parameters.")
    return data['Monthly Time Series']  # Return the relevant part of the data

def clean_data(data):
    df = pd.DataFrame(data).T  # Transpose because the dates are keys in the response
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df.index = pd.to_datetime(df.index)  # Convert index to datetime
    df.index.name = 'Date'
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert all columns to numeric, handling errors
    return df

def save_to_excel(df, filename):
    # Save DataFrame to Excel file using 'openpyxl' as the engine
    df.to_excel(filename, engine='openpyxl')

def main():
    raw_data = get_monthly_stock_data(SYMBOL, API_KEY)
    clean_df = clean_data(raw_data)
    three_years_ago = datetime.now() - DateOffset(years=3)  # More accurate way to subtract years
    filtered_df = clean_df[clean_df.index >= three_years_ago]
    print(filtered_df.head(10))  # Print first 10 rows to inspect
    return filtered_df

# Uncomment the line below to run the function
df = main()


