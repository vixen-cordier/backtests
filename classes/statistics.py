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
        self._data = pd.DataFrame(
            index=pd.date_range(start=min_date, end=max_date), 
            columns=pd.MultiIndex(levels=[[],[]], codes=[[],[]], names=[u'ticker', u'metric'])
        )
        tickers = np.unique(portfolio.operations['Ticker'])
        for ticker in tickers:
            # print(ticker)
            df_ticker = pd.DataFrame(index=self._data.index, columns=['Position', 'Invested'])
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
            self._data[ticker, 'Position'] = df_ticker['Position']  
            self._data[ticker, 'Invested'] = df_ticker['Invested']  
            self._data[ticker, 'Close'] = df_ticker['Close'] 
                
                
        for ticker in tickers:
            if ticker != 'CASH':
                self._data['CASH', 'Position'] -= self._data[ticker, 'Invested'] 
                self._data['CASH', 'Invested'] -= self._data[ticker, 'Invested'] 
        for ticker in tickers:
            self._data[ticker, 'Value'] = self._data[ticker, 'Close'] * self._data[ticker, 'Position'] 

        print(self._data) 
        
        
        self.invested: float = self._data.loc[pd.Timestamp(max_date), pd.IndexSlice[:, 'Invested']].sum()
        self.balance: float = self._data.loc[pd.Timestamp(max_date), pd.IndexSlice[:, 'Value']].sum()
        # self.fees: float
        self.cash: float = self._data.loc[pd.Timestamp(max_date),  pd.IndexSlice['CASH', 'Value']] / self.balance * 100
        self.total_return: float = self.balance / self.invested * 100
        self.annual_return: float = 0.0
        self.st_deviation: float = 0.0
        self.sharp_ratio: float = 0.0
        self.max_drawdown: float = 0.0
        self.max_drawdown_daterange: str = "2000/01/01 - 2003/01/01"
        self.best_year: str = "2000"
        self.best_year_return: float = 0.0
        self.worst_year: str = "2000"
        self.worst_year_return: float = 0.0
        self.chart: pd.Series = self._data.loc[:, pd.IndexSlice[:, 'Value']].sum(axis=1)
        
        
    def _build_chart(self) -> pd.Series:
        return self._data.loc[:, pd.IndexSlice[:, 'Value']].sum(axis=1)