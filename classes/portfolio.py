from typing import List
import pandas as pd
import numpy as np
import datetime as dt
from classes.stockchart import StockChart


class Portfolio:
    def __init__(self, name: str, initial_cash: int, tickers: List[str]):
        """ Initialisation of portfolio """
        self.name = name
        self.cash = initial_cash
        self.operations = pd.DataFrame(columns=['Date', 'Ticker', 'Price', 'Quantity', 'Fees', 'Amount', 'Description'])
        self.charts = { ticker: StockChart(ticker) for ticker in tickers }


    def buy(self, date: dt.datetime, ticker: str, amount: float, description = "buy"):
        fees = 0.0
        price = self.charts[ticker].get_price(date)
        quantity = (amount-fees)/price
        self.operations.loc[len(self.operations)] = [date, ticker, price, quantity, fees, amount, description]
        self.cash -= amount 
    
    def sell(self, date: dt.datetime, ticker: str, amount: float, description = "sell"):
        self.buy(date, ticker, -amount, description=description)

    def deposit(self, date: dt.datetime, additional_cash: int, description = "deposit"):
        fees = 0.0
        amount = additional_cash+fees
        self.operations.loc[len(self.operations)] = [date, "cash", 1, additional_cash, fees, amount, description]
        self.cash += additional_cash 
    
    def withdraw(self, date: dt.datetime, reduction_cash: int, description = "withdraw"):
        self.deposit(self, date, -reduction_cash, description=description)

    def get_min_date(self) -> dt.datetime:
        return max( chart.get_min_date() for chart in self.charts.values() )
    
    def get_max_date(self) -> dt.datetime:
        return min( chart.get_max_date() for chart in self.charts.values() )

    def filter_by_dates(self, start_date: dt.datetime, end_date: dt.datetime):
        self.operations = self.operations[(self.operations['Date'] >= start_date) & (self.operations['Date'] <= end_date)]
    
    def stats(self, min_date: dt.datetime, max_date: dt.datetime):
        return Statistics(self, min_date, max_date)
        

class Statistics:
    def __init__(self, portfolio: Portfolio, min_date: dt.datetime, max_date: dt.datetime):
        # range_date = { 
        #     'start': portfolio.operations.sort_values(by='Date').iloc[0]['Date'].strftime('%Y-%m-%d'),
        #     'end': pd.to_datetime('now', utc=True).strftime('%Y-%m-%d')
        # }
        self._data = pd.DataFrame(
            index=pd.date_range(start=min_date, end=max_date), 
            columns=pd.MultiIndex(levels=[[],[]], codes=[[],[]], names=[u'ticker', u'metric'])
        )

        for ticker in np.unique(portfolio.operations['Ticker']):
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
            
            df_ticker = df_ticker.join(portfolio.charts[ticker].data).ffill()
            df_ticker['Value'] = df_ticker['Close'] * df_ticker['Position']

            for column in df_ticker.columns:
                self._data[ticker, column] = df_ticker[column]  
        
        
        # self.deposit: float
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
        self.chart: self._build_chart()
        
        
    def _build_chart(self):
        self.chart: pd.Series = self._data.loc[:, pd.IndexSlice[:, 'Value']].sum(axis=1)
