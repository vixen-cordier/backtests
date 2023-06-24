import os
import json
import datetime as dt
from typing import List

from classes.strategies import Strategy, StrategyDCA, StrategyALLIN 

CURDIR = os.getcwd()


class Form():
    def __init__(self, name, 
                 date=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                 strategies: List[tuple[int, Strategy | StrategyDCA | StrategyALLIN]] = []):
        self.name = name
        self.date = date
        self.strategies = strategies
    
    
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
        return Form(json['name'], json['date'], strategies=
            [(
                strategy_json['percent'],
                Strategy.from_json(strategy_json['strategy'])
            ) for strategy_json in json['strategies']]
        )



def to_json_list(forms: List[Form]) -> List[dict]:
    return [ form.to_json() for form in forms ]


def from_json_list(json_list: List[dict]) -> List[Form]:
    return [ Form.from_json(json) for json in json_list ]


def read_forms() -> List[Form]:
    forms: List[Form] = []
    try:
        with open(f"{CURDIR}/forms.json", 'r') as file:
            forms = from_json_list(json.loads(file.read()))
    except Exception as error:
        print(error)
    return forms


def save_forms(forms: List[Form], backup=False):
    try:
        if os.path.isfile(f"{CURDIR}/forms.json") and backup:
            os.rename(f"{CURDIR}/forms.json", 
                    f"{CURDIR}/.old/forms/forms.{dt.datetime.now().strftime('%Y-%m-%d.%H:%M:%S')}.json")
        with open(f"{CURDIR}/forms.json", 'w') as file:
            file.write(json.dumps(to_json_list(forms)))
    except Exception as error:
        print(error)

