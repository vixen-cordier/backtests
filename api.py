import datetime as dt
import pandas as pd
from typing import List

from classes.portfolio import Portfolio


def get_date_range(portfolios: List[Portfolio]) -> (dt.datetime, dt.datetime):
  if len(portfolios) > 0:
    min_date = max( ptf.get_min_date() for ptf in portfolios )
    max_date = min( ptf.get_max_date() for ptf in portfolios )
  else:
    min_date = dt.datetime(1900, 1, 1)
    max_date = dt.datetime.now()
  return min_date, max_date


def get_portfolios_stats(portfolios: List[Portfolio], min_date: dt.datetime, max_date: dt.datetime) -> pd.DataFrame:
  ptfs_stats = pd.DataFrame(columns=['Total return', 'Annual return', 'St deviation', 'Sharp ratio', 'Max drawdown', 
                                     'Max drawdown daterange', 'Best year', 'Best year return', 'Worst year', 'Worst year return'])
  for portfolio in portfolios:
    stats = portfolio.stats(min_date, max_date)
    print(portfolio.name, stats)
    ptfs_stats.loc[portfolio.name] = {
      'Total return': stats.total_return,
      'Annual return': stats.annual_return,
      'St deviation': stats.st_deviation,
      'Sharp ratio': stats.sharp_ratio,
      'Max drawdown': stats.max_drawdown,
      'Max drawdown daterange': stats.max_drawdown_daterange,
      'Best year': stats.best_year,
      'Best year return': stats.best_year_return,
      'Worst year': stats.worst_year,
      'Worst year return': stats.worst_year_return,
    }

  return ptfs_stats

