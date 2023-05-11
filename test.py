from chart import Chart
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from datetime import datetime


class TestChart:
    def __init__(self):
        self.err_cnt = 0
        self.err_lib = ""
        self.chart = Chart()
        # self.chart.data = pd.read_csv('dataTradingView.csv', sep=';', parse_dates=['Date'], date_parser=lambda x: datetime.strptime(x, '%d/%m/%Y')).set_index('Date')
        self.chart.data = pd.read_csv('dataTradingView.csv', sep=';')#.astype({'Date': 'datetime64[ns]'}).sort_values('Date').set_index('Date')
        self.chart.data['Date'] = pd.to_datetime(self.chart.data['Date'], format='%d/%m/%Y')
        self.chart.data.set_index('Date', inplace=True)
        print('index:', self.chart.data.index)
        print('columns:', self.chart.data.columns)

    def equal_bool(self, col):
        err = 0
        msg = f"Equality test on {col} ... "
        for date, (expected, value) in self.chart.data[[f'{col}_exp', col]].iterrows():
            if expected != value:
                err = err + 1
                # print(f"{msg} ERR on index {idx} -> \t expected:{self.chart.data.iloc[idx][f'{col}_exp']} \t value:{self.chart.data.iloc[idx][f'{col}']}.")
                print(f"{msg} ERR on {date.strftime('%m/%d/%Y')} -> expected:{expected}, value:{value}.")
        
        self.err_lib += f"{msg} {'OK' if err == 0 else f'{err} errors'}\n"
        self.err_cnt += err


    def equal_float(self, col):
        err = 0
        msg = f"Equality test on {col} ... "
        for date, (expected, value) in self.chart.data[[f'{col}_exp', col]].iterrows():
            if not np.isclose(value, expected, atol=1e-4, equal_nan=True):
                err = err + 1
                print(f"{msg} ERR on {date.strftime('%m/%d/%Y')} -> expected:{expected}, value:{value}.")

        self.err_lib += f"{msg} {'OK' if err == 0 else f'{err} errors'}\n"
        self.err_cnt += err



if __name__ == '__main__':
    test = TestChart()

    test.chart.set_flag()
    # test.equal_bool('Closure_Daily')
    # test.equal_bool('Closure_Weekly')
    # test.equal_bool('Closure_Monthly')
    print(test.chart.data.tail(50))

    test.chart.add_mm(20)
    test.chart.add_mm(20, time='Weekly')
    test.chart.add_mm(20, time='Monthly')

    test.chart.add_mom([10])
    test.chart.add_mom([10], time='Weekly')
    test.chart.add_mom([10], time='Monthly')
    test.chart.add_mom([1,5,10], time='Monthly')

    # test.chart.add_rsi(21)
    # test.chart.add_rsi(21, time='Weekly')
    # test.chart.add_rsi(21, time='Monthly')


    test.chart.data.replace(0, np.nan, inplace=True)
    test.equal_float('MM_Daily_20')
    test.equal_float('MM_Weekly_20')
    test.equal_float('MM_Monthly_20')
    test.equal_float('MoM_Daily_10')
    test.equal_float('MoM_Weekly_10')
    test.equal_float('MoM_Monthly_10')
    # test.equal_float('MoM_Monthly_1-5-10')
    # test.equal_float('RSI_Daily_21')
    # test.equal_float('RSI_Weekly_21')
    # test.equal_float('RSI_Monthly_21')

    print(f"\n{test.err_lib}\n{test.err_cnt} error(s)") 
    print(test.chart.data.columns)
    print(test.chart.data.tail(50))
    test.chart.data.to_csv('dataResult.csv', sep=';')



