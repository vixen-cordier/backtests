import os
import json
import datetime as dt
from typing import List

from classes.portfolio import Portfolio
from classes.strategies import Strategy, StrategyDCA, StrategyALLIN 

CURDIR = os.getcwd()


class Form():
    def __init__(self, name, initial_cash,
                 date=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                 strategies: List[tuple[int, Strategy | StrategyDCA | StrategyALLIN]] = []):
        self.name = name
        self.date = date
        self.initial_cash = initial_cash
        self.strategies = strategies
        self.portfolio = Portfolio(
            name, initial_cash, 
            tickers = [ ticker for _, strategy in strategies for ticker in strategy.assets ]
        )


    
    
    def to_json(self) -> dict:
        return {
            "name": self.name,
            "date": self.date,
            "strategies": [ {
                "percent": percent,
                "strategy": strategy.to_json()
            } for percent, strategy in self.strategies ]
        }


    @staticmethod
    def from_json(json: dict):
        return Form(json['name'], json['date'], strategies = [
            (
                strategy_json['percent'],
                Strategy.from_json(strategy_json['strategy'])
            ) for strategy_json in json['strategies'] ]
        )



def read_forms() -> List[Form]:
    forms: List[Form] = []
    try:
        with open(f"{CURDIR}/forms.json", 'r') as file:
            forms = [ Form.from_json(json) for json in json.loads(file.read()) ]
    except Exception as error:
        print(error)
    return forms


def save_forms(forms: List[Form], backup=False):
    try:
        if os.path.isfile(f"{CURDIR}/forms.json") and backup:
            os.rename(f"{CURDIR}/forms.json", 
                    f"{CURDIR}/.old/forms/forms.{dt.datetime.now().strftime('%Y-%m-%d.%H:%M:%S')}.json")
        with open(f"{CURDIR}/forms.json", 'w') as file:
            file.write(json.dumps([ form.to_json() for form in forms ]))
    except Exception as error:
        print(error)

