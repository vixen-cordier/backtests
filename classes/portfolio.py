from typing import List
import pandas as pd
import numpy as np
from datetime import datetime

from classes.stockchart import StockChart


class Portfolio:
    def __init__(self, name: str, initial_cash: int, tickers: List[str]):
        """ Initialisation of portfolio """
        self.name = name
        self.cash = initial_cash
        self.operations = pd.DataFrame(columns=['Date', 'Ticker', 'Price', 'Quantity', 'Fees', 'Amount', 'Description'])
        self.charts = { ticker: StockChart(ticker) for ticker in tickers }


    def buy(self, date: datetime, ticker: str, amount: float, description = "buy"):
        fees = 0.0
        price = self.charts[ticker].get_price(date)
        quantity = (amount-fees)/price
        self.operations.loc[len(self.operations)] = [date, ticker, price, quantity, fees, amount, description]
        self.cash -= amount 
    
    def sell(self, date: datetime, ticker: str, amount: float, description = "sell"):
        self.buy(date, ticker, -amount, description=description)

    def deposit(self, date: datetime, additional_cash: int, description = "deposit"):
        fees = 0.0
        amount = additional_cash+fees
        self.operations.loc[len(self.operations)] = [date, "cash", 1, additional_cash, fees, amount, description]
        self.cash += additional_cash 
    
    def withdraw(self, date: datetime, reduction_cash: int, description = "withdraw"):
        self.deposit(self, date, -reduction_cash, description=description)

    def get_oldest_date(self) -> datetime:
        return max( chart.get_oldest_date() for chart in self.charts.values() )
    
    def get_youngest_date(self) -> datetime:
        return min( chart.get_youngest_date() for chart in self.charts.values() )

    def stats(self):
        return Statistics(self)
        

class Statistics:
    def __init__(self, portfolio: Portfolio):
        range_date = { 
            'start': portfolio.operations.sort_values(by='Date').iloc[0]['Date'].strftime('%Y-%m-%d'),
            'end': pd.to_datetime('now').strftime('%Y-%m-%d')
        }
        self._data = pd.DataFrame(
            index=pd.date_range(start=range_date['start'], end=range_date['end']), 
            columns=pd.MultiIndex(levels=[[],[]], codes=[[],[]], names=[u'ticker', u'metric'])
        )

        for ticker in np.unique(portfolio.operations['Ticker']):
            df_ticker = pd.DataFrame(index=self._data.index)
            df_operation = portfolio.operations[portfolio.operations['Ticker'] == ticker]
            
            position, invested = pd.Series(dtype=float), pd.Series(dtype=float)
            for date in df_ticker.index:
                position[date] = np.sum(df_operation[df_operation['Date'] <= date]['Quantity'])
                invested[date] = np.sum(df_operation[df_operation['Date'] <= date]['Amount'])
                
            df_ticker = pd.concat([df_ticker, pd.DataFrame({
                'Position': position,
                'Invested': invested,
            })], axis=1)
            
            df_ticker = df_ticker.join(portfolio.charts[ticker].data).ffill()
            df_ticker['Value'] = df_ticker['Close'] * df_ticker['Position']

            for column in df_ticker.columns:
                self._data[ticker, column] = df_ticker[column]  
        
                 
        self._build_chart()
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
        
        
    def _build_chart(self):
        self.chart: pd.Series = self._data.loc[:, pd.IndexSlice[:, 'Value']].sum(axis=1)
