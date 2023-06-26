from typing import Dict
import datetime
from classes.portfolio import Portfolio


class Strategy():
    type = ""

    def to_json(self):
        return {}

    @staticmethod
    def from_json(json):
        if json['type'] == "ALLIN":
            return StrategyALLIN(assets=json['assets'])
        elif json['type'] == "DCA":
            return StrategyDCA(assets=json['assets'], freq=json['freq'])
        else:
            return Strategy()



class StrategyALLIN(Strategy):
    type = "ALLIN"

    def __init__(self, assets: Dict[str, int] = {}):
        self.assets = assets

    def to_json(self):
        return {
            "type": self.type,
            "assets": self.assets
        }
    
    def apply(self, portfolio: Portfolio, start_date: datetime):
        for ticker, percent in self.assets.items():
            portfolio.buy(start_date, ticker, portfolio.cash*percent/100, description="buy ALLIN")






class StrategyDCA(Strategy):
    type = "DCA"

    def __init__(self, assets: Dict[str, int] = {}, freq="", inflow=0):
        self.assets = assets
        self.freq = freq
        self.inflow = inflow

    def to_json(self):
        return {
            "type": self.type,
            "assets": self.assets,
            "freq": self.freq,
            "inflow": self.inflow
        }
        
    def apply(self, portfolio: Portfolio):
        pass
        #     portfolio.deposit(date, self.inflow, description="deposit DCA")
        # for ticker, percent in self.assets.items():
        #     portfolio.buy(date, ticker, portfolio.cash*percent/100, description="buy DCA")

