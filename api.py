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


def get_date_range(portfolios: List[Portfolio]) -> (dt.date, dt.date):
  if len(portfolios) > 0:
    min_date = max( ptf.get_min_date() for ptf in portfolios )
    max_date = min( ptf.get_max_date() for ptf in portfolios )
  else:
    min_date = dt.date(1900, 1, 1)
    max_date = dt.datetime.now().date()
  return min_date, max_date



def get_stats(portfolios: List[Portfolio]) -> pd.DataFrame:
  ptfs_stats = pd.DataFrame(columns=['Portfolio', 'Invested', 'Balance', 'Annual return', 'St deviation', 'Sharp ratio', 'Max drawdown', 
                                     'Max drawdown daterange', 'Best year', 'Best year return', 'Worst year', 'Worst year return'])
  for i, portfolio in enumerate(portfolios):
    ptfs_stats.loc[i] = {
      'Portfolio': portfolio.name,
      'Invested': "{:.0f} €".format(portfolio.stats.invested),
      'Balance': "{:.0f} €".format(portfolio.stats.balance),
      # 'Cash': "{:.2f} %".format(portfolio.stats.cash*100),
      # 'Total return': "{:.2f} %".format(portfolio.stats.total_return*100),
      'Annual return': "{:.2f} %".format(portfolio.stats.annualized_return*100),
      'St deviation': "{:.2f} %".format(portfolio.stats.annualized_stdev*100),
      'Sharp ratio': "{:.2f}".format(portfolio.stats.sharp_ratio),
      'Max drawdown': "{:.2f} %".format(portfolio.stats.max_drawdown*100),
      'Max drawdown daterange': portfolio.stats.max_drawdown_daterange,
      'Best year return': "{:.2f} %".format(portfolio.stats.best_year_return*100),
      'Best year': portfolio.stats.best_year,
      'Worst year return': "{:.2f} %".format(portfolio.stats.worst_year_return*100),
      'Worst year': portfolio.stats.worst_year,
    }
  return ptfs_stats



def get_charts(portfolios: List[Portfolio]) -> pd.DataFrame:
  ptfs_charts = pd.DataFrame()
  for portfolio in portfolios:
    ptfs_charts[portfolio.name] = portfolio.stats.chart
  # print(ptfs_charts)
  return ptfs_charts


def get_ticker_charts(portfolios: List[Portfolio], same_axis=True) -> pd.DataFrame:
  tickers_charts = pd.DataFrame()
  min_dates, max_dates = [], []
  if len(portfolios) != 0:
    for portfolio in portfolios:
      # print(portfolio)
      for ticker in portfolio.assets.keys():
        # print(ticker)
        if ticker not in ["CASH", *tickers_charts.columns]:
          tickerchart = portfolio.assets[ticker]['chart']
          min_dates.append(tickerchart.get_min_date())
          max_dates.append(tickerchart.get_max_date())
          tickers_charts[ticker] = tickerchart.data
    if same_axis:
      tickers_charts: pd.DataFrame = tickers_charts[
        (tickers_charts.index > pd.Timestamp(max(min_dates))) &
        (tickers_charts.index < pd.Timestamp(min(max_dates)))
      ]
      for ticker in tickers_charts:
        ref_value = tickers_charts.iloc[0][ticker]
        tickers_charts[f"{ticker}%"] = tickers_charts[ticker].apply(lambda cur_value: (cur_value - ref_value)/ref_value*100)
      tickers_charts = tickers_charts[[ ticker for ticker in tickers_charts.columns if '%' in ticker ]]
  # print(tickers_charts)
  return tickers_charts



def get_annual_returns(portfolios: List[Portfolio]) -> pd.DataFrame:
  ptfs_returns = pd.DataFrame()
  for portfolio in portfolios:
    ptfs_returns[portfolio.name] = portfolio.stats.annual_returns
  # print(ptfs_charts)
  return ptfs_returns


def get_ticker_annual_returns(portfolios: List[Portfolio]) -> pd.DataFrame:
  tickers_returns = pd.DataFrame()
  min_dates, max_dates = [], []
  if len(portfolios) != 0:
    for portfolio in portfolios:
      # print(portfolio)
      for ticker in portfolio.assets.keys():
        # print(ticker)
        if ticker not in ["CASH", *tickers_returns.columns]:
          tickerchart = portfolio.assets[ticker]['chart']
          min_dates.append(tickerchart.get_min_date())
          max_dates.append(tickerchart.get_max_date())
          tickers_returns[f"{ticker}%"] = tickerchart.get_timeframe(time='Annually').pct_change().fillna(0)
    tickers_returns: pd.DataFrame = tickers_returns[
      (tickers_returns.index > pd.Timestamp(max(min_dates))) &
      (tickers_returns.index < pd.Timestamp(min(max_dates)))
    ]
    # for ticker in tickers_returns:
    #   ref_value = tickers_returns.iloc[0][ticker]
    #   tickers_returns[f"{ticker}%"] = tickers_returns[ticker].apply(lambda cur_value: (cur_value - ref_value)/ref_value*100)
    # tickers_returns = tickers_returns[[ ticker for ticker in tickers_returns.columns if '%' in ticker ]]
  # print(tickers_charts)
  return tickers_returns



def get_porfolios_operations(portfolios: List[Portfolio]) -> pd.DataFrame:
  if len(portfolios) != 0:
    operations = pd.concat([portfolio.operations for portfolio in portfolios]).sort_values(by='Date')
    # print(operations)
    return operations
  return None