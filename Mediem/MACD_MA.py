import cryptocompare
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from visulization import ShowEverything

INT_TICKER_TRADE = 0
DAYS_MA = 205
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
        data_frame = cryptocompare.get_historical_price_day(name[0], currency='USDT', limit=350, 
                                                            exchange='CCCAGG')

        data_frame = pd.DataFrame(data_frame) 
        print(name)      
        data_frame.set_index("time", inplace=True) 
        data_frame.rename(columns={"close":f"{name[0]}-close"}, inplace=True)
        data_frame = data_frame[[f"{name[0]}-close"]]
        if len(main_df)==0:
            main_df = data_frame
        else:
            main_df = main_df.join(data_frame)

    return main_df


def MACD(data, EMA1=12, EMA2=26, col="BTC"):
    data[f"{col}-EMA{EMA1}"] = data[f"{col}-close"].ewm(span=EMA1).mean()
    data[f"{col}-EMA{EMA2}"] = data[f"{col}-close"].ewm(span=EMA2).mean()
    data[f"{col}-MACD"] = data[f"{col}-EMA{EMA1}"] - data[f"{col}-EMA{EMA2}"]
    macd = data[f"{col}-MACD"]
    signal = data[f"{col}-MACD"].ewm(span=9).mean()
    return macd, signal


def get_Indicators(df, days_MA=200, simple_MA=True):
    for tick in ticker[INT_TICKER_TRADE]:
        df[f"{tick[0]}-MACD"], df[f"{tick[0]}-signal"] = MACD(df, EMA1=12, EMA2=26, col=tick[0])

    for tick in ticker[INT_TICKER_TRADE]:
        if simple_MA==True:
            df[f"MA{days_MA}-{tick[0]}"] = df[f"{tick[0]}-close"].rolling(window=days_MA).mean()
        else:
            df[f"MA{days_MA}-{tick[0]}"] = df[f"{tick[0]}-close"].ewm(com=days_MA-1, adjust=True, 
                                                                    min_periods=days_MA).mean()     
    df.dropna(inplace=True)
    return df


def trade(data, col="BTC"):
    buys = []
    sells = []
    count = 0
    for i in range(len(data)):
        if data[f"{col}-MACD"].iloc[i]>data[f"{col}-signal"].iloc[i] and count!=1:
            buys.append(data[f"{col}-close"].iloc[i])
            sells.append(np.NaN)
            count = 1
        elif data[f"{col}-MACD"].iloc[i]<data[f"{col}-signal"].iloc[i] and count!=-1: 
            buys.append(np.NaN)
            sells.append(data[f"{col}-close"].iloc[i])
            count = -1                     
        else:
            buys.append(np.NaN)
            sells.append(np.NaN)
    
    return buys, sells


ticker = split_tickers(SEQ=TICKERS_LENGHT)
df = get_data(ticker[INT_TICKER_TRADE])
df = get_Indicators(df, days_MA=DAYS_MA, simple_MA=True)

for tick in ticker[INT_TICKER_TRADE]:
	df[f"{tick[0]}-Buy"], df[f"{tick[0]}-Sell"] = trade(df, col=tick[0])
            
showing = ShowEverything(ticker, INT_TICKER_TRADE)
showing.PlotEvery(df)
