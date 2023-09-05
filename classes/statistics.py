from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.portfolio import Portfolio

import datetime as dt
import pandas as pd
import numpy as np



class Statistics:
    # def __init__(self, portfolio, min_date: dt.datetime, max_date: dt.datetime):
    def __init__(self, portfolio: Portfolio, min_date: dt.datetime, max_date: dt.datetime):
        # range_date = { 
        #     'start': portfolio.operations.sort_values(by='Date').iloc[0]['Date'].strftime('%Y-%m-%d'),
        #     'end': pd.to_datetime('now', utc=True).strftime('%Y-%m-%d')
        # }
        self._data = pd.DataFrame(
            index=pd.date_range(start=min_date, end=max_date), 
            columns=pd.MultiIndex(levels=[[],[]], codes=[[],[]], names=[u'ticker', u'metric'])
        )
        print(portfolio.name, portfolio.assets.keys())
        for ticker in np.unique(portfolio.operations['Ticker']):
            print(" ", ticker)
            df_ticker = pd.DataFrame(index=self._data.index)
            df_operation: pd.DataFrame = portfolio.operations[portfolio.operations['Ticker'] == ticker]
            
            quantity = df_operation['Quantity'].to_numpy()
            amount = df_operation['Amount'].to_numpy()
            position, invested = [], []
            for idx in range(df_ticker.shape[0]):
                position.append(np.sum(quantity[:idx+1]))
                invested.append(np.sum(amount[:idx+1]))
            
            df_ticker['Position'] = position
            df_ticker['Invested'] = invested
            
            if ticker == 'CASH':
                df_ticker['Close'] = 1
            else:
                df_ticker = df_ticker.join(portfolio.assets[ticker]['chart'].data).ffill()
                
            df_ticker['Value'] = df_ticker['Close'] * df_ticker['Position']

            for column in df_ticker.columns:
                self._data[ticker, column] = df_ticker[column]  
        
        print(self._data.shape)
        print(self._data.columns)
        
        
        self.invested: float = 0.0
        self.balance: float = 0.0
        # self.fees: float
        self.total_return: float = 0.0
        self.annual_return: float = 0.0
        self.st_deviation: float = 0.0
        self.sharp_ratio: float = 0.0
        self.max_drawdown: float = 0.0
        self.max_drawdown_daterange: str = "2000/01/01 - 2003/01/01"
        self.best_year: str = "2000"
        self.best_year_return: float = 0.0
        self.worst_year: str = "2000"
        self.worst_year_return: float = 0.0
        self.chart = self._build_chart()
        
        
    def _build_chart(self) -> pd.Series:
        return self._data.loc[:, pd.IndexSlice[:, 'Value']].sum(axis=1)