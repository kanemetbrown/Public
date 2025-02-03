import yfinance as yf
import pandas as pd
import numpy as np

# use equity screen to gather list

# List
tickers = ["QQQ", "SPY", "IWM", "^DJI"]     
ticker_data = []

for ticker in tickers:

# Variables: 
    
#Price Data
    stock = yf.Ticker(ticker)
    close = stock.fast_info["lastPrice"]
    high = stock.fast_info["dayHigh"]
    low = stock.fast_info["dayLow"]
    dcr = int(((close - low) / (high - low)) * 100)

#Moving averages   
    #Get historical data and calulate moving averages
    price_history = stock.history(period="250d")                                                           #get historical data for calucalting 10 and 20ema
    price_history["ten_ema"] = price_history["Close"].ewm(span=10, adjust=False).mean()                   #calulates all emas and stores in new column
    price_history["twenty_ema"] = price_history["Close"].ewm(span=20, adjust=False).mean()
    price_history["fifty_sma"] = price_history["Close"].rolling(window=50).mean()
    price_history["two_hundred_sma"] = price_history["Close"].rolling(window=200).mean()
    #Grab latest EMA values and assign status
    ten_day = price_history["ten_ema"].iloc[-1]
    ten_day_status = "Above" if close > ten_day else "Equal" if close == ten_day else "Below"
    twenty_day = price_history["twenty_ema"].iloc[-1]
    twenty_day_status = "Above" if close > twenty_day else "Equal" if close == twenty_day else "Below"
    #Grab lastest SMA values and assign status
    fifty_day = price_history["fifty_sma"].iloc[-1]
    fifty_day_status = "Above" if close > fifty_day else "Equal" if close == fifty_day else "Below"
    two_hundred_day = price_history["two_hundred_sma"].iloc[-1]
    two_hundred_day_staus = "Above" if close > two_hundred_day else "Equal" if close == two_hundred_day else "Below"
    #Calculate EMA Trends 
    ten_ema_today = price_history["ten_ema"].iloc[-1]
    ten_ema_prior = price_history["ten_ema"].iloc[-2]
    ten_ema_trend = "Rising" if ten_ema_today > ten_ema_prior else "Flat" if ten_ema_today == ten_ema_prior else "Falling"
    twenty_ema_today = price_history["twenty_ema"].iloc[-1]
    twenty_ema_prior = price_history["twenty_ema"].iloc[-2]
    twenty_ema_trend = "Rising" if twenty_ema_today > twenty_ema_prior else "Flat" if twenty_ema_today == twenty_ema_prior else "Falling"
    #Caluclate SMA Trends
    fifty_sma_today = price_history["fifty_sma"].iloc[-1]
    fifty_sma_prior = price_history["fifty_sma"].iloc[-2]
    fifty_sma_trend = "Rising" if fifty_sma_today > fifty_sma_prior else "Flat" if fifty_sma_today == fifty_sma_prior else "Falling"
    two_hundred_sma_today = price_history["two_hundred_sma"].iloc[-1]
    two_hundred_sma_prior = price_history["two_hundred_sma"].iloc[-2]
    two_hundred_sma_trend = "Rising" if two_hundred_sma_today > two_hundred_sma_prior else "Flat" if two_hundred_sma_today == two_hundred_sma_prior else "Falling"
    
#Volume
    last_volume = stock.fast_info["lastVolume"]
    prior_volume = int(stock.history(period="3d")["Volume"].values[-2])              # stored as int because normally returens in NumPy type 
    volume_up_down = "Up" if last_volume > prior_volume else "Equal" if last_volume == prior_volume else "Down"
    average_volume_20d = sum(stock.history(period="20d")["Volume"]) / 20
    volume_ratio = last_volume / average_volume_20d

    
#Create a dictionary for this ticker with the desired data
    ticker_dict ={
        "name": ticker,
        "close": close,
        "dcr": dcr,
        "10d_status": ten_day_status,
        "10d_trend": ten_ema_trend,
        "20d_status": twenty_day_status,
        "20d_trend": twenty_ema_trend,
        "50d_status": fifty_day_status,
        "50d_trend": fifty_sma_trend,
        "200d_status": two_hundred_day_staus,
        "200d_trend": two_hundred_sma_trend,
        #"last_volume": last_volume,
        #"volume_prior": prior_volume,
        "volume_vs_prior": volume_up_down,
        "volume_ratio": volume_ratio,
    }

#Append dictionary to the list
    ticker_data.append(ticker_dict)



data_frame = pd.DataFrame.from_records(ticker_data)

print(data_frame)







