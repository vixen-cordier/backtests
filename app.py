from typing import List

import streamlit as st
st.set_page_config(layout="wide", page_title="Portfolio Backtest")
import pandas as pd
pd.options.plotting.backend = "plotly"

from classes.portfolio import Portfolio
import api

portfolios: List[Portfolio] = []

# if 'instantiated' not in st.session_state:
#     print('Initialization')
#     st.session_state.instantiated = True

    
with st.sidebar:
  st.write("Portfolios")
  portfolios = []
  for i, portfolio in enumerate(api.read_portfolios()):
    if st.checkbox(portfolio.name, key=f'{i}_checkbox'):
      portfolios.append(portfolio)
  print(len(portfolios), "portfolios")
  
  st.markdown("---")
  min_date, max_date = api.get_date_range(portfolios)
  date_min = st.date_input("Beginning date", value=min_date, min_value=min_date, max_value=max_date)
  date_max = st.date_input("Ending date", value=max_date, min_value=min_date, max_value=max_date)
  initial_cash = st.number_input("Initial cash", value = 10000)
  print("app.min_date", type(min_date), min_date)
  print("app.max_date", type(max_date), max_date)
  print("app.date_min", type(date_min), date_min)
  print("app.date_max", type(date_max), date_max)
            

for portfolio in portfolios:
  portfolio.deposit(date_min, initial_cash, description="initial deposit")
  portfolio.apply_strategies(date_min)
  portfolio.compute_stats(date_min, date_max)
    
st.dataframe(api.get_stats(portfolios))
# fig = go.Figure()
# for metric in rows:
#   fig.add_trace(go.Scatter(x=rows[metric].index, y=rows[metric].values, name=metric))
st.plotly_chart(api.get_charts(portfolios).plot.line(), use_container_width=True)




# if 'instantiated' not in st.session_state:
#     print("""
#     # ---------------
#     # -- Initilisation
#     # ---------------""")
#     st.session_state.portfolios: Dict[Portfolio, bool] = {}
#     for form in read_forms():
#         print("Portfolio", form.name)
#         st.session_state.portfolios[Portfolio(
#             name=form.name,
#             initial_cash=form.initial_cash,
#             tickers = [ ticker for _, strategy in form.strategies for ticker in strategy.assets ]
#         )] = False
#     st.session_state.instantiated = True
#     print(len(st.session_state.portfolios), "portfolios found")



# print("""
#     # ---------------
#     # -- Sidebar
#     # ---------------""")
# with st.sidebar:
#     st.title("Portfolios")
#     # st.write(" ")
#     # if st.button("Create new portfolio", type='primary'):
#     #     st.session_state.forms[Form.empty()] = True
#     st.write(" ")
#     for i, portfolio in enumerate(st.session_state.portfolios):
#         st.session_state.portfolios[portfolio] = st.checkbox(portfolio.name, key=f'{i}_checkbox')

#     print("Portfolio ckecked")
#     print({portfolio.name:checked for portfolio, checked in st.session_state.portfolios.items() if checked})


# print("""
#     # ---------------
#     # -- Result
#     # ---------------""")
# forms_checked: List[Form] = [form for form, checked in st.session_state.forms.items() if checked]
# print([form_checked.name for form_checked in forms_checked])
# if forms_checked:
#     start_date = max( chart.get_oldest_date() for form in forms_checked for chart in form.portfolio.charts.values() )
#     end_date = min( chart.get_youngest_date() for form in forms_checked for chart in form.portfolio.charts.values() )
#     date_range = st.slider("Date slider to filter data", format="YYYY-MM-DD", value=(
#         datetime.datetime(start_date.year, start_date.month, start_date.day),
#         datetime.datetime(end_date.year, end_date.month, end_date.day)
#     ))
    

#     fig = go.Figure()
#     for form in forms_checked:
#         form.portfolio.filter_by_dates(date_range[0], date_range[1])
#         for _, strategy in form.strategies:
#             strategy.apply(form.portfolio, start_date=date_range[0])
#         if not form.portfolio.operations.empty:
#             stats = form.portfolio.stats()
#             fig.add_trace(go.Scatter(x=stats.chart.index, y=stats.chart.values, name=form.name))
#     st.plotly_chart(fig)





# print("""
#     # ---------------
#     # -- Forms
#     # ---------------""")
# forms_checked: List[Form] = [{form for form, checked in st.session_state.forms.items() if checked}]
# print(forms_checked)
# form_cols = st.columns(len(forms_checked))
# for idx, data in enumerate(forms_checked):
#     form = st.form(f'{idx}_form')

#     with form_cols[idx]:
#         cols = st.columns([2, 1])
#         with cols[0]:
#             form.text_input("Portfolio name", value=data.name, key=f'{idx}_name')
#         with cols[1]:
#             form.number_input("Initial cash", value=data.initial_cash, key=f'{idx}_Initial_cash')

#         print("Strategy count:", len(data.strategies))
#         for i, (percent, strategy) in enumerate(data.strategies):
#             print(strategy.type)
#             strategy_cols = st.columns([1, 6, 3])
#             if strategy_cols[0].button("⊖", use_container_width=True, key=f'{idx}.{i}_strategy_delete'):
#                 data.strategies.pop(i)
#                 print("Strategy deleted: new count", len(form.strategies))
#             with strategy_cols[1]:
#                 form.selectbox(f"Strategy {i+1}", options=[type.name for type in StrategyType], index=StrategyType[strategy.type].value, label_visibility='collapsed', key=f'{idx}{i}_strategy_type')
#             with strategy_cols[2]:
#                 form.number_input("Percent", value=percent, label_visibility='collapsed', key=f'{idx}.{i}_strategy_percent')
            
#             print("Asset count:", len(strategy.assets))
#             for j, (ticker, percent) in enumerate(strategy.assets.items()):
#                 print(ticker)
#                 asset_cols = st.columns([1, 1, 6, 3])
#                 if asset_cols[1].button("⊖", use_container_width=True, key=f'{idx}.{i}.{j}_asset_delete'):
#                     strategy.assets.pop(ticker)
#                 with asset_cols[2]:
#                     form.text_input(f"Asset {j+1}", value=ticker, placeholder="ticker", label_visibility='collapsed', key=f'{idx}.{i}.{j}_asset_ticker')
#                 with asset_cols[3]:
#                     form.number_input("Percent", value=percent, label_visibility='collapsed', key=f'{idx}.{i}.{j}_asset_percent')
            
#             asset_cols = st.columns([1, 1, 6, 3])
#             asset_cols[1].button("⊕", type='primary', use_container_width=True, key=f'{idx}.{i}.{j+1}_asset_add')
#             asset_cols[2].text_input(f"Asset {j+1}", placeholder="ticker", label_visibility='collapsed', key=f'{idx}.{i}.{j+1}_asset_ticker')
#             asset_cols[3].number_input("Percent", value=0, label_visibility='collapsed', key=f'{idx}.{i}.{j+1}_asset_percent')
        
#         strategy_cols = st.columns([1, 6, 3])
#         strategy_cols[0].button("⊕", type='primary', use_container_width=True, key=f'{idx}.{i+1}_strategy_add')
#         strategy_cols[1].selectbox(f"Strategy {i+1}", options=[type.name for type in StrategyType], index=StrategyType.ALLIN.value, label_visibility='collapsed', key=f'{idx}{i+1}_strategy_type')
#         strategy_cols[2].number_input("Percent", value=0, label_visibility='collapsed', key=f'{idx}.{i+1}_strategy_percent')
        
#     # if form.form_submit_button():