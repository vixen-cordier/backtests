from typing import Dict
import pandas as pd
import numpy as np
from datetime import datetime

from src.stockchart import StockChart



class Portfolio:
    def __init__(self, name):
        """ Initialisation of portfolio """
        self.name: str = name
        self.operations = pd.DataFrame(columns=['Date', 'Ticker', 'Price', 'Quantity', 'Fees', 'Operation'])
        self.charts: Dict[str, StockChart] = {}

    def buy(self, date: datetime, ticker: str, quantity: float):
        """ Add operation in operations Dataframe """
        if ticker not in self.charts.keys():
            self.charts[ticker] = StockChart(ticker)
        fees = 0
        price = self.charts[ticker].getPrice(date)
        operation = price*quantity+fees
        self.operations.loc[len(self.operations)] = [date, ticker, price, quantity, fees, operation] 

    def stats(self):
        return _Statistics(self)
        

class _Statistics:
    def __init__(self, portfolio: Portfolio):
        range_date = { 
            'start': portfolio.operations.sort_values(by='Date').iloc[0]['Date'].strftime('%Y-%m-%d'),
            'end': pd.to_datetime('now').strftime('%Y-%m-%d')
        }
        self._data = pd.DataFrame(
            index=pd.date_range(start=range_date['start'], end=range_date['end']), 
            columns=pd.MultiIndex(levels=[[],[]], codes=[[],[]], names=[u'ticker', u'metric'])
        )
        print(self._data)
        for ticker in np.unique(portfolio.operations['Ticker']):
            print(ticker)
            self._data[ticker, 'Close'] = portfolio.charts[ticker].data.loc[range_date['start']:range_date['end']]
            
            position, invested = pd.Series(dtype=float), pd.Series(dtype=float)
            for date in self._data.index:
                position[date] = np.sum(portfolio.operations[portfolio.operations['Date'] <= datetime(date.year, date.month, date.day)]['Quantity'])
                invested[date] = np.sum(portfolio.operations[portfolio.operations['Date'] <= datetime(date.year, date.month, date.day)]['Operation'])
                
            self._data = pd.concat([self._data, pd.DataFrame({
                (ticker, 'Position'): position,
                (ticker, 'Invested'): position,
            })], axis=1)
            
            self._data[ticker, 'Value'] = self._data[ticker, 'Close'] * self._data[ticker, 'Position']
            
        # self._buildChart()
        # self._setBalance()
        # self.deposit: float
        # self.fees: float
        # self.chart: pd.DataFrame
        # self.annual_return: float
        # self.yield_to_date: float
        # self.best_year: str
        # self.best_year_return: float
        # self.worst_year: str
        # self.worst_year_return: float
        # self.st_deviation: float
        # self.sharp_ratio: float
        # self.max_drawdown: float
        # self.max_drawdown_daterange: str
        
        
    def _buildChart(self):
        self.chart = pd.DataFrame(index=pd.date_range(start=self._range_date['start'], end=self._range_date['end']))
        for ticker in self._data.keys():
            self.chart = pd.concat(self.chart, self._data[ticker])
