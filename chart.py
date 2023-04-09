import yfinance as yf
import pandas as pd
import numpy as np


class Chart:
    def __init__(self):
        """ Initialisation of graphic """
        self.ticker: str
        self.data: pd.DataFrame


    def fetch_yf(self, ticker):
        """ Fetch daily data from yahoo finance API"""
        self.ticker = ticker
        self.data = yf.Ticker(self.ticker).history(period="max")[['Close']].reset_index()
        print(f"{self.ticker}:  {self.data.iloc[0]['Date'].strftime('%Y-%m-%d')} --> {self.data.iloc[-1]['Date'].strftime('%Y-%m-%d')}")


    def set_flag(self):
        """ Flags end of Week and end of Month """
        self.data['ClosureDaily'] = False
        self.data['ClosureWeekly'] = False
        self.data['ClosureMonthly'] = False
        for i in range(self.data.shape[0]-1):
            curr_date = self.data.index[i]
            next_date = self.data.index[i+1]
            if curr_date.day != next_date.day:
                self.data.at[curr_date, 'ClosureDaily'] = True 
            if curr_date.week != next_date.week:
                self.data.at[curr_date, 'ClosureWeekly'] = True 
            if curr_date.month != next_date.month:
                self.data.at[curr_date, 'ClosureMonthly'] = True 
        last_date = self.data.index[-1]
        self.data.at[last_date, 'ClosureDaily'] = True
        self.data.at[last_date, 'ClosureWeekly'] = True 
        self.data.at[last_date, 'ClosureMonthly'] = True 


    def add_mm(self, mm: int, time='Daily'):
        """ Add moving average to the graph data (Daily|Weekly|Monthly) """
        data_mm = self.data[self.data[f'Closure{time}'] == True][['Close']]
        data_mm[f'MM{mm}{time}'] = np.nan
        for i, date in enumerate(data_mm.index[mm-1:]):
            data_mm.at[date, f'MM{mm}{time}'] = np.mean(data_mm.iloc[i:i+mm]['Close'])
        self.data[f'MM{mm}{time}'] = pd.concat([
            self.data, 
            data_mm[[f'MM{mm}{time}']]
        ], axis=1).ffill()[f'MM{mm}{time}']


    def add_mom(self, mom: int, time='Daily'):
        """ Add momentum value to the graph data (Daily|Weekly|Monthly) """
        data_mom = self.data[self.data[f'Closure{time}'] == True][['Close']]
        data_mom[f'Mom{mom}{time}'] = ""
        for i, date in enumerate(data_mom.index[mom-1:]):
            data_mom.at[date, f'Mom{mom}{time}'] = data_mom.at[date, 'Close'] / data_mom.iloc[i-mom, 'Close'] - 1
        self.data = pd.merge(self.data, data_mom[['Date', f'Mom{mom}{time}']], on='Date', how='left').fillna(method='bfill')


    def add_rsi(self, rsi, time='Daily'):
        """ Add RSI index to the graph data (Daily|Weekly|Monthly) """
        data_rsi = self.data[self.data[f'Closure{time}'] == True].reset_index(drop=True)
        data_rsi[f'RSI{rsi}{time}'] = ""
        data_rsi['tmp_var'] = 0
        data_rsi['tmp_bull'] = 0
        data_rsi['tmp_bear'] = 0
        for idx in data_rsi.index[1:]:
            data_rsi.at[idx,'tmp_var'] = data_rsi.at[idx, 'Close'] / data_rsi.at[idx-1, 'Close'] -1
            if data_rsi.at[idx,'tmp_var'] > 0:
                data_rsi.at[idx,'tmp_bull'] = data_rsi.at[idx,'tmp_var']
            else:
                data_rsi.at[idx,'tmp_bear'] = data_rsi.at[idx,'tmp_var']
        for idx in data_rsi.index[rsi:]:
            data_rsi.at[idx, f'RSI{rsi}{time}'] = 100 - (100 / (1 + np.mean(data_rsi.loc[idx-rsi:idx]['tmp_bull']) / np.mean(data_rsi.loc[idx-rsi:idx]['tmp_bear'])))
        self.data = pd.merge(self.data, data_rsi[['Date', f'RSI{rsi}{time}']], on='Date', how='left').fillna(method='bfill') 



