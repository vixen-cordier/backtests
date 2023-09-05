from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from classes.portfolio import Portfolio

from typing import Dict
import  enum
import datetime

class StrategyType(enum.Enum):
   BUYANDHOLD = 0
   MOVINGAVERAGE = 1


class Strategy():
  type = ""

  @staticmethod
  def from_json(json):
    if json['type'] == StrategyType.BUYANDHOLD.name:
      return StrategyBH(assets=json['assets'])
    elif json['type'] == StrategyType.MOVINGAVERAGE.name:
      return StrategyMA(assets=json['assets'], ma=json['ma'])
    else:
      return Strategy()
    
  # def apply():
  #   pass
  def to_json(self):
    return {}



class StrategyBH(Strategy):
  type = StrategyType.BUYANDHOLD.name

  def __init__(self, assets: Dict[str, int] = {}):
    self.assets = assets

  def to_json(self):
    return {
      "type": self.type,
      "assets": self.assets
    }
  
  # def apply(self, portfolio, percent_global: int, start_date: datetime):
  def apply(self, portfolio: Portfolio, percent_global: int, start_date: datetime):
    for ticker, percent_local in self.assets.items():
      percent = percent_global/100*percent_local/100
      portfolio.buy(start_date, ticker, portfolio.assets['CASH']['quantity']*percent, description="buy BUYANDHOLD")




class StrategyMA(Strategy):
  type = StrategyType.MOVINGAVERAGE.name

  def __init__(self, assets: Dict[str, int] = {}, ma: int = 10):
    self.assets = assets
    self.ma = ma

  def to_json(self):
    return {
      "type": self.type,
      "ma": self.ma,
      "assets": self.assets
    }
    
  def apply(self, portfolio, start_date: datetime):
    pass
    #   portfolio.deposit(date, self.inflow, description="deposit MOVINGAVERAGE")
    # for ticker, percent in self.assets.items():
    #   portfolio.buy(date, ticker, portfolio.cash*percent/100, description="buy MOVINGAVERAGE")

