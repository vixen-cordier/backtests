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
        self.chart.data = pd.read_csv('dataTradingView.csv', sep=';')
        self.chart.data['Date'] = pd.to_datetime(self.chart.data['Date'], format='%d/%m/%Y')
        self.chart.data.set_index('Date', inplace=True)
        print('index:', self.chart.data.index)
        print('columns:', self.chart.data.columns)

    def equal(self, col, type: type):
        err = 0
        msg = f"Equality test on {col} ... "
        for date, (expected, value) in self.chart.data[[f'{col}_exp', col]].iterrows():
            if type is bool and expected == value:
                continue
            elif type is float and np.isclose(value, expected, atol=1e-4, equal_nan=True):
                continue
            else:
                err = err + 1
                print(f"{msg} \t {type} \t ERR on {date.strftime('%m/%d/%Y')} -> expected:{expected}, value:{value}.")
        
        self.err_lib += f"{msg} {'OK' if err == 0 else f'{err} errors'}\n"
        self.err_cnt += err



if __name__ == '__main__':
    test = TestChart()

    test.chart.set_flag()
    # test.equal('Closure_Daily', bool)
    # test.equal('Closure_Weekly', bool)
    # test.equal('Closure_Monthly', bool)

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
    test.equal('MM_Daily_20', float)
    test.equal('MM_Weekly_20', float)
    test.equal('MM_Monthly_20', float)
    test.equal('MoM_Daily_10', float)
    test.equal('MoM_Weekly_10', float)
    test.equal('MoM_Monthly_10', float)
    # test.equal('MoM_Monthly_1-5-10', float)
    # test.equal('RSI_Daily_21', float)
    # test.equal('RSI_Weekly_21', float)
    # test.equal('RSI_Monthly_21', float)

    print(f"\n{test.err_lib}\n{test.err_cnt} error(s)") 
    print(test.chart.data.columns)
    print(test.chart.data.tail(50))
    test.chart.data.to_csv('dataResult.csv', sep=';')



