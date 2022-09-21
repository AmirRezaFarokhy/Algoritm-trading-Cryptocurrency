import cryptocompare
import pandas as pd
import numpy as np
from datetime import datetime

import matplotlib.pyplot as plt
from visulization import ShowEverything

INT_TICKER_TRADE = 1
DAYS_MA = 200
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
		data_frame = cryptocompare.get_historical_price_day(name[0], currency='USDT', limit=300, 
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


def get_Indicators(data, days_MA=200, simple_MA=True):
	for tick in ticker[INT_TICKER_TRADE]:
		df[f"{tick[0]}-RSI"] = RSI(df, periods=13, ema=True, col=f"{tick[0]}")
	
	for tick in ticker[INT_TICKER_TRADE]:
		if simple_MA==True:
			df[f"MA{days_MA}-{tick[0]}"] = df[f"{tick[0]}-close"].rolling(window=days_MA).mean()
		else:
			df[f"MA{days_MA}-{tick[0]}"] = df[f"{tick[0]}-close"].ewm(com=days_MA-1, adjust=True, 
																	min_periods=days_MA).mean()     
	
	data.dropna(inplace=True)
	return data


def trade(df, col="BTC"):
	buys = []
	sells= []
	for i in range(len(df)):
		if 70<df[f"{col}-RSI"].iloc[i]<99 and df[f"MA{DAYS_MA}-{col}"].iloc[i]>df[f"{col}-close"].iloc[i]:
			buys.append(np.NaN)
			sells.append(df[f"{col}-close"].iloc[i])
		elif 0>df[f"{col}-RSI"].iloc[i]>30 and df[f"MA{DAYS_MA}-{col}"].iloc[i]<df[f"{col}-close"].iloc[i]:
			buys.append(df[f"{col}-close"].iloc[i])
			sells.append(np.NaN)
		else:
			buys.append(np.NaN)
			sells.append(np.NaN)
			
	return buys, sells

	
ticker = split_tickers(SEQ=TICKERS_LENGHT)
df = get_data(ticker[INT_TICKER_TRADE])
df = get_Indicators(df, days_MA=DAYS_MA, simple_MA=True)
print(df.head())

for tick in ticker[INT_TICKER_TRADE]:
	df[f"{tick[0]}-Buy"], df[f"{tick[0]}-Sell"] = trade(df, col=tick[0])

showing = ShowEverything(ticker, INT_TICKER_TRADE)
showing.PlotEvery(df)



