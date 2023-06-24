from typing import List
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime


class StockChart:
    def __init__(self, ticker='SPY'):
        """ Initialisation of graphic by fetching daily data from yahoo finance API"""
        self.data: pd.DataFrame = yf.Ticker(ticker).history(period='max')[['Close']].tz_localize(None)
        print(f"{ticker}:  {self.data.index[0].strftime('%Y-%m-%d')} --> {self.data.index[-1].strftime('%Y-%m-%d')}")

    def get_oldest_date(self) -> datetime:
        return self.data.index[0]
    
    def get_youngest_date(self) -> datetime:
        return self.data.index[-1]
    
    def get_price(self, date: datetime) -> float:
        return self.data[self.data.index == date]['Close'].values[0]
    

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
        data_mm[col_mm] = 0
        for i, date in enumerate(data_mm.index[mm-1:]):
            # print(data_mm.iloc[i:i+mm]['Close'])
            data_mm.at[date, col_mm] = np.mean(data_mm.iloc[i:i+mm]['Close'])
        self.data[col_mm] = pd.concat([self.data, data_mm[[col_mm]]], axis=1).bfill()[col_mm]


    def add_mom(self, moms: List[int], time='Daily'):
        """ Add momentum value to the graph data (Daily|Weekly|Monthly) """
        data_mom = self.data[self.data[f'Closure_{time}'] == True][['Close']]
        for mom in moms:
            data_mom[str(mom)] = 0
            for i, date in enumerate(data_mom.index[mom:]):
                # print(f"i={i}, i+mom={i+mom}, date={date}, data_mom.index[i]={data_mom.index[i]}, data_mom.index[i+mom]={data_mom.index[i+mom]}")
                data_mom.at[date, str(mom)] = data_mom.iloc[i+mom]['Close'] - data_mom.iloc[i]['Close']# - 1) * 100
        col_mom = f"MoM_{time}_{'-'.join([str(mom) for mom in moms])}"
        data_mom[col_mom] = data_mom[[str(mom) for mom in moms]].mean(axis=1)
        self.data[col_mom] = pd.concat([self.data, data_mom[[col_mom]]], axis=1).bfill()[col_mom]


    def add_rsi(self, rsi, time='Daily'):
        """ Add RSI index to the graph data (Daily|Weekly|Monthly) """
        data_rsi = self.data[self.data[f'Closure_{time}'] == True][['Close']]
        col_rsi = f'RSI_{time}_{rsi}'
        data_rsi[col_rsi] = 0
        data_rsi['tmp_var'] = 0
        data_rsi['tmp_bull'] = 0
        data_rsi['tmp_bear'] = 0
        # print("build temp columns")
        for i, date in enumerate(data_rsi.index[1:]):
            data_rsi.at[date,'tmp_var'] = data_rsi.iloc[i+1]['Close'] - data_rsi.iloc[i]['Close']
            if i == 0:
                print(f"date={date}, data_rsi.index[i]={data_rsi.index[i]}, data_rsi.index[i+1]={data_rsi.index[i+1]}, data_rsi.at[date,'tmp_var']={data_rsi.at[date,'tmp_var']}")
            if data_rsi.at[date,'tmp_var'] > 0:
                data_rsi.at[date,'tmp_bull'] = data_rsi.at[date,'tmp_var']
            else:
                data_rsi.at[date,'tmp_bear'] = -data_rsi.at[date,'tmp_var']
        # print("build RSI")
        for i, date in enumerate(data_rsi.index[rsi:]):
            data_rsi.at[date, col_rsi] = 100 - (100 / (1 + np.sum(data_rsi.iloc[i+1:i+rsi+1]['tmp_bull']) / np.sum(data_rsi.iloc[i+1:i+rsi+1]['tmp_bear'])))
            if i in range (0, 10):
                print(i)
                print(f"date={date}, data_rsi.index[i+1]={data_rsi.index[i+1]}, data_rsi.index[i+rsi]={data_rsi.index[i+rsi]}")
                print(f"date={date}, np.sum(data_rsi.iloc[i+1:i+rsi+1]['tmp_bull'])={np.sum(data_rsi.iloc[i+1:i+rsi+1]['tmp_bull'])}, np.sum(data_rsi.iloc[i+1:i+rsi+1]['tmp_bear'])={np.sum(data_rsi.iloc[i+1:i+rsi+1]['tmp_bear'])}")
                print(f"date={date}, data_rsi.at[date, col_rsi]={data_rsi.at[date, col_rsi]}")
        self.data[col_rsi] = pd.concat([self.data, data_rsi[[col_rsi]]], axis=1).bfill()[col_rsi]
        # print(data_rsi.tail(60))


