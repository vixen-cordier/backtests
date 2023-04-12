from typing import List
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
        self.data['Closure_Daily'] = False
        self.data['Closure_Weekly'] = False
        self.data['Closure_Monthly'] = False
        for i in range(self.data.shape[0]-1):
            curr_date = self.data.index[i]
            next_date = self.data.index[i+1]
            if curr_date.day != next_date.day:
                self.data.at[curr_date, 'Closure_Daily'] = True 
            if curr_date.week != next_date.week:
                self.data.at[curr_date, 'Closure_Weekly'] = True 
            if curr_date.month != next_date.month:
                self.data.at[curr_date, 'Closure_Monthly'] = True 
        last_date = self.data.index[-1]
        self.data.at[last_date, 'Closure_Daily'] = True
        self.data.at[last_date, 'Closure_Weekly'] = True 
        self.data.at[last_date, 'Closure_Monthly'] = True 


    def add_mm(self, mm: int, time='Daily'):
        """ Add moving average to the graph data (Daily|Weekly|Monthly) """
        data_mm = self.data[self.data[f'Closure_{time}'] == True][['Close']]
        col_mm = f"MM_{time}_{mm}"
        data_mm[col_mm] = np.nan
        for i, date in enumerate(data_mm.index[mm-1:]):
            data_mm.at[date, col_mm] = np.mean(data_mm.iloc[i:i+mm]['Close'])
        self.data[col_mm] = pd.concat([self.data, data_mm[[col_mm]]], axis=1).ffill()[col_mm]


    def add_mom(self, moms: List[int], time='Daily'):
        """ Add momentum value to the graph data (Daily|Weekly|Monthly) """
        data_mom = self.data[self.data[f'Closure_{time}'] == True][['Close']]
        for mom in moms:
            data_mom[str(mom)] = np.nan
            for i, date in enumerate(data_mom.index[mom:]):
                data_mom.at[date, str(mom)] = (data_mom.iloc[i+mom]['Close'] / data_mom.iloc[i]['Close'] - 1) * 100
        col_mom = f"MoM_{time}_{'-'.join([str(mom) for mom in moms])}"
        data_mom[col_mom] = data_mom[[str(mom) for mom in moms]].mean(axis=1)
        self.data[col_mom] = pd.concat([self.data, data_mom[[col_mom]]], axis=1).ffill()[col_mom]


    def add_rsi(self, rsi, time='Daily'):
        """ Add RSI index to the graph data (Daily|Weekly|Monthly) """
        data_rsi = self.data[self.data[f'Closure_{time}'] == True][['Close']]
        col_rsi = f'RSI_{time}_{rsi}'
        data_rsi[col_rsi] = np.nan
        data_rsi['tmp_var'] = 0
        data_rsi['tmp_bull'] = 0
        data_rsi['tmp_bear'] = 0
        # print("build temp columns")
        for i, date in enumerate(data_rsi.index[1:]):
            # print(f"i={i}", f"date={date}", f"data_rsi.iloc[i+1]['Close']={data_rsi.iloc[i+1]['Close']}", f"data_rsi.iloc[i]['Close']={data_rsi.iloc[i]['Close']}")
            data_rsi.at[date,'tmp_var'] = data_rsi.iloc[i+1]['Close'] - data_rsi.iloc[i]['Close']
            if data_rsi.at[date,'tmp_var'] > 0:
                data_rsi.at[date,'tmp_bull'] = data_rsi.at[date,'tmp_var']
            else:
                data_rsi.at[date,'tmp_bear'] = -data_rsi.at[date,'tmp_var']
        # print("build RSI")
        for i, date in enumerate(data_rsi.index[rsi-1:]):
            data_rsi.at[date, col_rsi] = 100 - (100 / (1 + np.sum(data_rsi.iloc[i:i+rsi]['tmp_bull']) / np.sum(data_rsi.iloc[i:i+rsi]['tmp_bear'])))
        self.data[col_rsi] = pd.concat([self.data, data_rsi[[col_rsi]]], axis=1).ffill()[col_rsi]
        # print(data_rsi.tail(60))


