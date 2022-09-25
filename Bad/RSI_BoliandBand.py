import cryptocompare
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from visulization import ShowEverything

INT_TICKER_TRADE = 1
DAYS_BB = 30
TICKERS_LENGHT = 9

def split_tickers(SEQ=6):
    tickers = pd.read_csv("tickers.csv", index_col=0)
    lst_ticker = []
    for i in range(0,len(tickers), SEQ):
        lst_ticker.append(tickers.values[i:i+SEQ])

    return lst_ticker


def get_data(names):
    main_df = pd.DataFrame()
    for name in names:
        data_frame = cryptocompare.get_historical_price_hour(name[0], currency='USDT', limit=350, 
                                                            exchange='CCCAGG')

        data_frame = pd.DataFrame(data_frame) 
        print(name)      
        data_frame.set_index("time", inplace=True) 
        data_frame.rename(columns={"close":f"{name[0]}-close", 
                                   "low":f"{name[0]}-low",
                                   "high":f"{name[0]}-high"},
                                   inplace=True)

        data_frame = data_frame[[f"{name[0]}-close", f"{name[0]}-high", f"{name[0]}-low"]]
        if len(main_df)==0:
            main_df = data_frame
        else:
            main_df = main_df.join(data_frame)

    return main_df


def RSI(df, periods=14, ema=True, col="BTC"):
    close_delta = df[f'{col}-close'].diff()

    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    if ema==True:
        ma_up = up.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
    else:
        ma_up = up.rolling(window=periods, adjust=False).mean()
        ma_down = down.rolling(window=periods, adjust=False).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi


def BB(data, days=20, col="BTC"):
    data["MA"] = data[f"{col}-close"].rolling(window=days).mean()
    data["STD"] = data[f"{col}-close"].rolling(window=days).std()
    data[f"{col}-Upper"] = data["MA"] + 2*df["STD"]
    data[f"{col}-Lower"] = data["MA"] - 2*df["STD"]
    data.dropna(inplace=True)
    Upper = data[f"{col}-Upper"]
    Lower = data[f"{col}-Lower"]
    return Upper, Lower


def get_Indicators(df):
    for tick in ticker[INT_TICKER_TRADE]:
        df[f"{tick[0]}-RSI"] = RSI(df, periods=13, ema=True, col=tick[0])
        df[f"{tick[0]}-upper"], df[f"{tick[0]}-lower"] = BB(df, days=DAYS_BB, col=tick[0])
        
    df.dropna(inplace=True)
    return df


def trade(data, col="BTC"):
    buys = []
    sells = []
    count = 0
    for i in range(len(data)):
        if 0<data[f"{col}-RSI"].iloc[i]<31 and data[f"{col}-low"].iloc[i]<data[f"{col}-lower"].iloc[i] and count!=1:
            buys.append(data[f"{col}-close"].iloc[i])
            sells.append(np.NaN)
            count = 1
        elif 70<data[f"{col}-RSI"].iloc[i]<99 and data[f"{col}-upper"].iloc[i]<data[f"{col}-high"].iloc[i] and count!=-1:
            buys.append(np.NaN)
            sells.append(data[f"{col}-close"].iloc[i])
            count = -1
        else:
            buys.append(np.NaN)
            sells.append(np.NaN)
    
    return buys, sells

ticker = split_tickers(SEQ=TICKERS_LENGHT)
df = get_data(ticker[INT_TICKER_TRADE])
df = get_Indicators(df)


for tick in ticker[INT_TICKER_TRADE]:
    df[f"{tick[0]}-Buy"], df[f"{tick[0]}-Sell"] = trade(df, col=tick[0])

showing = ShowEverything(ticker, INT_TICKER_TRADE)
showing.PlotEvery(df)

