import cryptocompare
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt 
from visulization import ShowEverything

INT_TICKER_TRADE = 1
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
        data_frame = cryptocompare.get_historical_price_day(name[0], currency='USDT', limit=100, 
                                                            exchange='CCCAGG')
        print(name)
        data_frame = pd.DataFrame(data_frame)
        data_frame.set_index("time", inplace=True) 
        #data_frame = data_frame[:-1]
        data_frame.rename(columns={"close":f"{name[0]}-close", "low":f"{name[0]}-low", 
                                  "high":f"{name[0]}-high"}, inplace=True)
        
        data_frame = data_frame[[f"{name[0]}-high", f"{name[0]}-low", f"{name[0]}-close"]]
        if len(main_df)==0:
            main_df = data_frame
        else:
            main_df = main_df.join(data_frame) 
            
    return main_df


def RSI(df, periods=14, ema=True):

    for tick in ticker[INT_TICKER_TRADE]:
        close_delta = df[f'{tick[0]}-close'].diff()

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
        df[f"{tick[0]}-RSI"] = rsi

    df.dropna(inplace=True)
    return df


def trade(data, col="BTC"):
    buys = []
    sells = []
    close = []
    for i in range(len(data)-4):
        if data[f"{col}-low"].iloc[i]>data[f"{col}-low"].iloc[i+1]>data[f"{col}-low"].iloc[i+2]<data[f"{col}-low"].iloc[i+3]<data[f"{col}-low"].iloc[i+4] and data[f"{col}-high"].iloc[i]>data[f"{col}-high"].iloc[i+1]>data[f"{col}-high"].iloc[i+2]<data[f"{col}-high"].iloc[i+3]<data[f"{col}-high"].iloc[i+4] and 31>data[f"{col}-RSI"].iloc[i+2]>0:
            buys.append(data[f"{col}-close"].iloc[i+4])
            sells.append(np.NaN)
            close.append(data[f"{col}-close"].iloc[i+4])
        elif data[f"{col}-high"].iloc[i]<data[f"{col}-high"].iloc[i+1]<data[f"{col}-high"].iloc[i+2]>data[f"{col}-high"].iloc[i+3]>data[f"{col}-high"].iloc[i+4] and data[f"{col}-low"].iloc[i]<data[f"{col}-low"].iloc[i+1]<data[f"{col}-low"].iloc[i+2]>data[f"{col}-low"].iloc[i+3]>data[f"{col}-low"].iloc[i+4] and 99>data[f"{col}-RSI"].iloc[i+2]>70:
            buys.append(np.NaN)
            sells.append(data[f"{col}-close"].iloc[i+4])
            close.append(data[f"{col}-close"].iloc[i+4])
        else:
            buys.append(np.NaN)
            sells.append(np.NaN) 
            close.append(data[f"{col}-close"].iloc[i+4])
     
    return buys, sells, close
    

ticker = split_tickers(SEQ=TICKERS_LENGHT)
df = get_data(ticker[INT_TICKER_TRADE])
df = RSI(df, periods=13, ema=True)
print(df.head())

main_df = pd.DataFrame()
for tick in ticker[INT_TICKER_TRADE]:
    main_df[f"{tick[0]}-Buy"], main_df[f"{tick[0]}-Sell"], main_df[f"{tick[0]}-close"] = trade(df, col=tick[0])

main_df.index = [i for i in range(len(main_df))]

showing = ShowEverything(ticker, INT_TICKER_TRADE)
showing.PlotEvery(main_df)



