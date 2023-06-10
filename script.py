from src.portfolio import Portfolio
from datetime import datetime


if __name__ == '__main__':
    zen = Portfolio("ZEN")
    zen.buy(datetime(2023, 6, 1), 'SPY', 1)
    stats = zen.stats()
    # print(stats.balance)
