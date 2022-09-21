import cryptocompare
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from visulization import ShowEverything

INT_TICKER_TRADE = 2
DAYS_BB = 30
DAYS_D = 3
DAYS_k = 14
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
        data_frame.rename(columns={"close":f"{name[0]}-close", "low":f"{name[0]}-low", 
                                  "high":f"{name[0]}-high"}, inplace=True)
        
        data_frame = data_frame[[f"{name[0]}-high", f"{name[0]}-low", f"{name[0]}-close"]]
        if len(main_df)==0:
            main_df = data_frame
        else:
            main_df = main_df.join(data_frame)

    return main_df


def BB(data, days=20, col="BTC"):
    data["MA"] = data[f"{col}-close"].rolling(window=days).mean()
    data["STD"] = data[f"{col}-close"].rolling(window=days).std()
    data["Upper"] = data["MA"] + 2*df["STD"]
    data["Lower"] = data["MA"] - 2*df["STD"]
    data.dropna(inplace=True)
    Upper = data["Upper"]
    Lower = data["Lower"]
    return Upper, Lower


def stocastic(df ,k_period=14, d_period=3, col="BTC"):
    df['n_high'] = df[f'{col}-high'].rolling(k_period).max()
    df['n_low'] = df[f'{col}-low'].rolling(k_period).min()
    df['%K'] = (df[f'{col}-close'] - df['n_low']) * 100 / (df['n_high'] - df['n_low'])
    Dstoc = df['%K'].rolling(d_period).mean()
    Kstoc = df['%K']
    return Kstoc, Dstoc

def get_Indicators(df):
    for tick in ticker[INT_TICKER_TRADE]:
        df[f"{tick[0]}-upper"], df[f"{tick[0]}-lower"] = BB(df, days=DAYS_BB, col=tick[0])
        df[f"{tick[0]}-%K"], df[f"{tick[0]}-%D"] = stocastic(df, k_period=DAYS_k, d_period=DAYS_D, col=tick[0])
    
    df.dropna(inplace=True)
    return df


def trade(df, col="BTC"):
    buys = []
    sells = []
    for i in range(len(df)):
        if df[f"{col}-close"].iloc[i]>df[f"{col}-upper"].iloc[i] and df[f"{col}-%K"].iloc[i]<df[f"{col}-%D"].iloc[i]:
            buys.append(np.NaN)
            sells.append(df[f"{col}-close"].iloc[i])
        elif df[f"{col}-close"].iloc[i]<df[f"{col}-lower"].iloc[i] and df[f"{col}-%K"].iloc[i]>df[f"{col}-%D"].iloc[i]:
            buys.append(df[f"{col}-close"].iloc[i])
            sells.append(np.NaN)
        else:
            buys.append(np.NaN)
            sells.append(np.NaN)
            
    return buys, sells

ticker = split_tickers(SEQ=TICKERS_LENGHT)
df = get_data(ticker[INT_TICKER_TRADE])
df = get_Indicators(df)
print(df.head())

for tick in ticker[INT_TICKER_TRADE]:
    df[f"{tick[0]}-Buy"], df[f"{tick[0]}-Sell"] = trade(df, col=tick[0]) 

showing = ShowEverything(ticker, INT_TICKER_TRADE)
showing.PlotEvery(df)


