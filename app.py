import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema

def plot_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    
    if data.empty:
        print(f"No data found for ticker {ticker}")
        return

    # Plot Closing Price
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price')
    plt.title(f'{ticker} Closing Price')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.legend()
    plt.savefig(f'{ticker}_closing_price.png')
    plt.show()

    # Plot Trading Volume
    plt.figure(figsize=(14, 7))
    plt.plot(data['Volume'], label='Volume', color='orange')
    plt.title(f'{ticker} Trading Volume')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.legend()
    plt.savefig(f'{ticker}_trading_volume.png')
    plt.show()

    # Calculate Moving Averages
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()

    # Plot Closing Price with Moving Averages
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price')
    plt.plot(data['MA50'], label='50-Day Moving Average', color='red')
    plt.plot(data['MA200'], label='200-Day Moving Average', color='green')
    plt.title(f'{ticker} Closing Price with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.savefig(f'{ticker}_moving_averages.png')
    plt.show()

    # Calculate Daily Returns
    data['Daily Return'] = data['Close'].pct_change()

    # Plot Daily Returns
    plt.figure(figsize=(14, 7))
    plt.plot(data['Daily Return'], label='Daily Return', color='purple')
    plt.title(f'{ticker} Daily Returns')
    plt.xlabel('Date')
    plt.ylabel('Daily Return')
    plt.legend()
    plt.savefig(f'{ticker}_daily_returns.png')
    plt.show()

    # Find Local Extrema
    def find_local_extrema(data, order=5):
        local_maxima = argrelextrema(data['Close'].values, np.greater, order=order)[0]
        local_minima = argrelextrema(data['Close'].values, np.less, order=order)[0]
        return local_minima, local_maxima

    local_minima, local_maxima = find_local_extrema(data)

    # Plot Local Minima and Maxima
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label="Close Price", color='blue')
    plt.scatter(data.iloc[local_minima].index, data.iloc[local_minima]['Close'], label="Local Minima", color='red', marker='v', alpha=1)
    plt.scatter(data.iloc[local_maxima].index, data.iloc[local_maxima]['Close'], label="Local Maxima", color='green', marker='^', alpha=1)
    plt.title(f"{ticker} Local Minima and Maxima")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.savefig(f'{ticker}_local_minima_maxima.png')
    plt.show()

    # Plot Price Segments Between Minima
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price', color='blue')
    for i in range(len(local_minima) - 1):
        start = local_minima[i]
        end = local_minima[i + 1]
        plt.plot(data.index[start:end], data['Close'][start:end], color='orange' if data['Close'][start] < data['Close'][end] else 'purple', linestyle='--')

    plt.title(f"{ticker} Stock Price with Local Minima and Maxima Segments")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.legend()
    plt.savefig(f'{ticker}_price_segments.png')
    plt.show()

if __name__ == "__main__":
    ticker = input("Enter the ticker symbol: ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    plot_stock_data(ticker, start_date, end_date)
