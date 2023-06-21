import os
import json
import datetime as dt
from typing import List

CURDIR = os.getcwd()


class Form():
    def __init__(self, name, date_maj=dt.datetime.now().strftime('%Y-%m-%d.%H:%M:%S')):
        self.name = name
        self.date_maj = date_maj
    
    
    def to_json(self):
        return {
            'name': self.name,
            'date_maj': self.date_maj
        }



def to_json_list(portfolios: List[Form]):
    json_list = []
    for portfolio in portfolios:
        json_list.append(portfolio.to_json())
    return json_list


def from_json(json) -> Form:
    return Form(
        json['name'],
        date_maj = json['date_maj']
    )


def from_json_list(json_list) -> List[Form]:
    portfolios: List[Form] = []
    for json in json_list:
        portfolios.append(from_json(json))
    return portfolios


def read_forms() -> List[Form]:
    portfolios: List[Form] = []
    try:
        with open(f"{CURDIR}/data.json", 'r') as file:
            portfolios = from_json_list(json.loads(file.read()))
    except Exception as error:
        print(error)
    return portfolios


def save_forms(portfolios: List[Form], backup=False):
    try:
        if os.path.isfile(f"{CURDIR}/data.json") and backup:
            os.rename(f"{CURDIR}/data.json", 
                      f"{CURDIR}/.old/data/data.{dt.datetime.now().strftime('%Y-%m-%d.%H:%M:%S')}.json")
        with open(f"{CURDIR}/data.json", 'w') as file:
            file.write(json.dumps(to_json_list(portfolios)))
    except Exception as error:
        print(error)

