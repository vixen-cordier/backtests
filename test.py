from chart import Chart
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np


class TestChart:
    def __init__(self):
        self.err = 0
        self.chart = Chart()
        self.chart.data = pd.read_csv('data2.csv', sep=';', parse_dates=['Date']).set_index('Date')


    def equal_bool(self, col):
        err = 0
        msg = f"Equality test on {col} ... "
        for idx, equal in self.chart.data.apply(lambda x: x[f'{col}_exp'] == x[f'{col}'], axis = 1).items():
            if not equal:
                err = err + 1
                print(f"{msg} ERR on index {idx} -> expected:{self.chart.data.iloc[idx][f'{col}_exp']}, value:{self.chart.data.iloc[idx][f'{col}']}.")
        if err == 0:
            print(f"{msg} OK")
        self.err = self.err + err


    def equal_float(self, col):
        err = 0
        msg = f"Equality test on {col} ... "
        for date, equal in self.chart.data.apply(lambda x: np.isclose(x[f'{col}_exp'], x[f'{col}'], equal_nan=True), axis = 1).items():
            if not equal:
                err = err + 1
                print(f"{msg} ERR on {date} -> expected:{self.chart.data.at[date, f'{col}_exp']}, value:{self.chart.data.at[date, f'{col}']}.")
        if err == 0:
            print(f"{msg} OK")
        self.err = self.err + err



if __name__ == '__main__':
    test = TestChart()

    test.chart.set_flag()
    test.equal_bool('ClosureDaily')
    test.equal_bool('ClosureWeekly')
    test.equal_bool('ClosureMonthly')

    test.chart.add_mm(20)
    test.chart.add_mm(20, time='Weekly')
    test.chart.add_mm(20, time='Monthly')
    test.equal_float('MM20Daily')
    test.equal_float('MM20Weekly')
    test.equal_float('MM20Monthly')

    print(f"\n{test.err} error(s)") 


