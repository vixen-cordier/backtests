from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.portfolio import Portfolio

import datetime as dt
import pandas as pd
import numpy as np


class Statistics:
    def __init__(self, portfolio: Portfolio, min_date: dt.date, max_date: dt.date):
        # range_date = { 
        #     'start': portfolio.operations.sort_values(by='Date').iloc[0]['Date'].strftime('%Y-%m-%d'),
        #     'end': pd.to_datetime('now', utc=True).strftime('%Y-%m-%d')
        # }
        self.data = pd.DataFrame(
            index=pd.date_range(start=min_date, end=max_date), 
            columns=pd.MultiIndex(levels=[[],[]], codes=[[],[]], names=[u'ticker', u'metric'])
        )
        tickers = np.unique(portfolio.operations['Ticker'])
        for ticker in tickers:
            # print(ticker)
            df_ticker = pd.DataFrame(index=self.data.index, columns=['Position', 'Invested'])
            df_ope: pd.DataFrame = portfolio.operations[portfolio.operations['Ticker'] == ticker]
            df_ope = df_ope.groupby('Date').agg({'Quantity': 'sum', 'Amount': 'sum'})
            df_ope.index = df_ope.index.astype('datetime64[ns]')
            
            for idx in df_ope.index:
                df_ticker.loc[idx, 'Position'] = np.sum(df_ope.loc[:idx, 'Quantity'])
                df_ticker.loc[idx, 'Invested'] = np.sum(df_ope.loc[:idx, 'Amount'])

            if ticker == 'CASH':
                df_ticker['Close'] = 1
            else:
                df_ticker = df_ticker.join(portfolio.assets[ticker]['chart'].data)

            df_ticker = df_ticker.ffill()
            self.data[ticker, 'Position'] = df_ticker['Position']  
            self.data[ticker, 'Invested'] = df_ticker['Invested']  
            self.data[ticker, 'Close'] = df_ticker['Close'] 
                
                
        for ticker in tickers:
            if ticker != 'CASH':
                self.data['CASH', 'Position'] -= self.data[ticker, 'Invested'] 
                self.data['CASH', 'Invested'] -= self.data[ticker, 'Invested'] 
        for ticker in tickers:
            self.data[ticker, 'Value'] = self.data[ticker, 'Close'] * self.data[ticker, 'Position'] 

        # print(self.data) 
        self.chart: pd.Series = self.data.loc[:, pd.IndexSlice[:, 'Value']].sum(axis=1)
        self.invested: float = self.data.loc[pd.Timestamp(max_date), pd.IndexSlice[:, 'Invested']].sum()
        self.balance: float = self.data.loc[pd.Timestamp(max_date), pd.IndexSlice[:, 'Value']].sum()
        # self.fees: float
        self.cash: float = self.data.loc[pd.Timestamp(max_date),  pd.IndexSlice['CASH', 'Value']] / self.balance
        self.total_return: float = (self.balance - self.invested) / self.invested
        self.annual_return: float = (1+self.total_return)**(365/(max_date-min_date).days) - 1
        self.annual_stdev: float = self.chart.pct_change().std()*np.sqrt(260)
        self.sharp_ratio: float = self.annual_return / self.annual_stdev
        self.max_drawdown: float = 0.0
        self.max_drawdown_daterange: str = "2000/01/01 - 2003/01/01"
        self.best_year: str = "2000"
        self.best_year_return: float = 0.0
        self.worst_year: str = "2000"
        self.worst_year_return: float = 0.0
        
        
    def get_timeframe(self, time) -> pd.DataFrame:
        chart_tf = pd.Series(self.chart[-1], index=[self.chart.index[-1]])
        for i in range(self.chart.shape[0]-1):
            curr_date: dt.date = self.chart.index[i]
            next_date: dt.date = self.chart.index[i+1]
            if time == 'Daily' and curr_date.day != next_date.day       \
            or time == 'Weekly' and curr_date.week != next_date.week    \
            or time == 'Monthly' and curr_date.month != next_date.month \
            or time == 'Annually' and curr_date.year != next_date.year:
            # print(curr_date, next_date)
                chart_tf = pd.concat((chart_tf, pd.Series(self.chart[i], index=[self.chart.index[i]])))
        return chart_tf.sort_index()
    