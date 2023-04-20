from chart import Chart
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np


class TestChart:
    def __init__(self):
        self.err_cnt = 0
        self.err_lib = ""
        self.chart = Chart()
        self.chart.data = pd.read_excel('data3.csv.xlsx', sheet_name='data', parse_dates=['Date']).set_index('Date')
        # self.chart.data = pd.read_csv('dataSPY.csv', sep=',', parse_dates=['Date']).set_index('Date')
        # self.chart.data = pd.read_csv('data.csv', sep=';', parse_dates=['Date']).set_index('Date')
# data.csv is copy of https://docs.google.com/spreadsheets/d/1k7zAJ9K7mB9W1A-8Mu7o1YBiS_AAIs8JJYhXx7C37tU/edit

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
        for date, (expected, value) in self.chart.data[[f'{col}_exp', col]].iterrows():
            if not np.isclose(value, expected, atol=1e-4, equal_nan=True):
                err = err + 1
                print(f"{msg} ERR on {date} -> expected:{expected}, value:{value}.")

        self.err_lib += f"{msg} {'OK' if err == 0 else f'{err} errors'}\n"
        self.err_cnt += err



if __name__ == '__main__':
    test = TestChart()

    test.chart.set_flag()
    # test.equal_bool('Closure_Daily')
    # test.equal_bool('Closure_Weekly')
    # test.equal_bool('Closure_Monthly')

    test.chart.add_mm(20)
    test.chart.add_mm(20, time='Weekly')
    test.chart.add_mm(20, time='Monthly')
    test.equal_float('MM_Daily_20')
    test.equal_float('MM_Weekly_20')
    test.equal_float('MM_Monthly_20')

    # test.chart.add_mom([10])
    # test.chart.add_mom([10], time='Weekly')
    # test.chart.add_mom([10], time='Monthly')
    # # test.chart.add_mom([1,5,10], time='Monthly')
    # test.equal_float('MoM_Daily_10')
    # test.equal_float('MoM_Weekly_10')
    # test.equal_float('MoM_Monthly_10')
    # # test.equal_float('MoM_Monthly_1-5-10')

    # test.chart.add_rsi(21)
    # test.chart.add_rsi(21, time='Weekly')
    # test.chart.add_rsi(21, time='Monthly')
    # test.equal_float('RSI_Daily_21')
    # test.equal_float('RSI_Weekly_21')
    # test.equal_float('RSI_Monthly_21')

    print(f"\n{test.err_lib}\n{test.err_cnt} error(s)") 
    print(test.chart.data.columns)
    test.chart.data.to_csv('dataResult.csv')


