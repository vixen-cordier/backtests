from typing import List
import pandas as pd
import datetime as dt
from classes.tickerchart import TickerChart
from classes.strategies import Strategy, StrategyBH, StrategyMA 
from classes.statistics import Statistics


class Portfolio:
  CASH = "EUREUR=X"
  
  def __init__(self, name: str, tickers: List[str],
         strategies: List[tuple[int, Strategy | StrategyBH | StrategyMA]] = []):
    """ Initialisation of portfolio """
    self.name = name
    self.assets: dict[str, dict[str, float | TickerChart]] = { "CASH" : {'quantity': 0, 'chart': None} }
    self.strategies = strategies
    self.operations = pd.DataFrame(columns=['Date', 'Ticker', 'Price', 'Quantity', 'Fees', 'Amount', 'Description'])
    self.stats: Statistics = None
    
    # for ticker in [Portfolio.CASH, *tickers]:
    for ticker in tickers:
      self.assets[ticker] = { 
        'quantity': 0, 
        'chart': TickerChart(ticker) 
      }
      

  @staticmethod
  def from_json(json: dict):
    return Portfolio(
      json['name'], 
      json['tickers'], 
      strategies = [
      (
        strategy_json['percent'],
        Strategy.from_json(strategy_json['strategy'])
      ) for strategy_json in json['strategies'] ]
    )
    
    
  def to_json(self) -> dict:
    return {
      "name": self.name,
      "tickers": [ ticker for ticker in self.assets.keys() if ticker != "CASH" ],
      "strategies": [ {
        "percent": percent,
        "strategy": strategy.to_json()
      } for percent, strategy in self.strategies ]
    }
    
    
  def buy(self, date: dt.datetime, ticker: str, amount: float, description = "buy"):
    fees = 0.0
    price = self.assets[ticker]['chart'].get_price(date)
    quantity = (amount-fees)/price
    self.operations.loc[len(self.operations)] = [date, ticker, price, quantity, fees, amount, description]
    self.assets[Portfolio.CASH]['quantity'] -= amount
    self.assets[ticker]['quantity'] += quantity
  
  
  def sell(self, date: dt.datetime, ticker: str, amount: float, description = "sell"):
    self.buy(date, ticker, -amount, description=description)


  def deposit(self, date: dt.datetime, additional_cash: int, description = "deposit"):
    fees = 0.0
    amount = additional_cash+fees
    self.operations.loc[len(self.operations)] = [date, "cash", 1, additional_cash, fees, amount, description]
    self.assets[Portfolio.CASH]['quantity'] += additional_cash
  
  
  def withdraw(self, date: dt.datetime, reduction_cash: int, description = "withdraw"):
    self.deposit(self, date, -reduction_cash, description=description)


  def filter_by_dates(self, start_date: dt.datetime, end_date: dt.datetime):
    self.operations = self.operations[(self.operations['Date'] >= start_date) & (self.operations['Date'] <= end_date)]
  
  
  def compute_stats(self, min_date: dt.datetime, max_date: dt.datetime):
    self.stats = Statistics(self, min_date, max_date)


  def apply_strategies(self, min_date: dt.datetime):
    for percent, strategy in self.strategies:
      strategy.apply(self, percent, min_date)
      

  def get_min_date(self) -> dt.datetime:
    return max( self.assets[ticker]['chart'].get_min_date() for ticker in self.assets )
  
  
  def get_max_date(self) -> dt.datetime:
    return min( self.assets[ticker]['chart'].get_max_date() for ticker in self.assets )
    

