import os, json
import datetime as dt
import pandas as pd
from typing import List

from classes.portfolio import Portfolio

CURDIR = os.getcwd()


def read_portfolios() -> List[Portfolio]:
  portfolios: List[Portfolio] = []
  try:
    with open(f"{CURDIR}/portfolios.json", 'r') as file:
      portfolios = [ Portfolio.from_json(json) for json in json.loads(file.read()) ]
  except Exception as error:
    print(error)
  return portfolios


def save_portfolios(portfolios: List[Portfolio], backup=False):
  try:
    if os.path.isfile(f"{CURDIR}/portfolios.json") and backup:
      os.rename(f"{CURDIR}/portfolios.json", 
                f"{CURDIR}/.old/portfolios.{dt.datetime.now().strftime('%Y-%m-%d.%H:%M:%S')}.json")
    with open(f"{CURDIR}/portfolios.json", 'w') as file:
      file.write(json.dumps([ portfolio.to_json() for portfolio in portfolios ]))
  except Exception as error:
    print(error)


def get_date_range(portfolios: List[Portfolio]) -> (dt.datetime, dt.datetime):
  if len(portfolios) > 0:
    min_date = max( ptf.get_min_date() for ptf in portfolios )
    max_date = min( ptf.get_max_date() for ptf in portfolios )
  else:
    min_date = dt.datetime(1900, 1, 1)
    max_date = dt.datetime.now()
  return min_date, max_date


def get_stats(portfolios: List[Portfolio]) -> pd.DataFrame:
  ptfs_stats = pd.DataFrame(columns=['Invested', 'Balance', 'Total return', 'Annual return', 'St deviation', 'Sharp ratio', 'Max drawdown', 
                                     'Max drawdown daterange', 'Best year', 'Best year return', 'Worst year', 'Worst year return'])
  for portfolio in portfolios:
    ptfs_stats.loc[portfolio.name] = {
      'Invested': portfolio.stats.invested,
      'Balance': portfolio.stats.balance,
      'Total return': portfolio.stats.total_return,
      'Annual return': portfolio.stats.annual_return,
      'St deviation': portfolio.stats.st_deviation,
      'Sharp ratio': portfolio.stats.sharp_ratio,
      'Max drawdown': portfolio.stats.max_drawdown,
      'Max drawdown daterange': portfolio.stats.max_drawdown_daterange,
      'Best year': portfolio.stats.best_year,
      'Best year return': portfolio.stats.best_year_return,
      'Worst year': portfolio.stats.worst_year,
      'Worst year return': portfolio.stats.worst_year_return,
    }

  return ptfs_stats

def get_charts(portfolios: List[Portfolio]) -> pd.DataFrame:
  ptfs_charts = pd.DataFrame()
  for portfolio in portfolios:
    ptfs_charts[portfolio.name] = portfolio.stats.chart
  # print(ptfs_charts)
  return ptfs_charts