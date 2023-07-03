import streamlit as st
import datetime
from typing import List, Dict
import plotly.graph_objects as go
st.set_page_config(layout="wide", page_title="Portfolio Backtest")

from classes.form import Form, read_forms, save_forms
from classes.strategies import StrategyType


if 'instantiated' not in st.session_state:
    print("""
    # ---------------
    # -- Initilisation
    # ---------------""")
    st.session_state.forms: Dict[Form, bool] = {}
    for form in read_forms():
        st.session_state.forms[form] = False
    st.session_state.instantiated = True

print("""
    # ---------------
    # -- Sidebar
    # ---------------""")
with st.sidebar:
    st.title("Portfolios")
    st.write(" ")
    if st.button("Create new portfolio", type='primary'):
        st.session_state.forms[Form.empty()] = True
    st.write(" ")
    for i, form in enumerate(st.session_state.forms):
        st.session_state.forms[form] = st.checkbox(form.name, key=f'{i}_checkbox')

print("Form ckecked")
print({form.name:checked for form,checked in st.session_state.forms.items()})

 

print("""
    # ---------------
    # -- Forms
    # ---------------""")
forms_checked: List[Form] = [{form for form, checked in st.session_state.forms.items() if checked}]
form_cols = st.columns(len(forms_checked))
for idx, data in enumerate(forms_checked):
    form = st.form(f'{idx}_form')
    # data = form_checked
    print(data.name)
    
    with form_cols[idx]:
        cols = st.columns([2, 1])
        with cols[0]:
            form.text_input("Portfolio name", value=data.name, key=f'{idx}_name')
        with cols[1]:
            form.number_input("Initial cash", value=data.initial_cash, key=f'{idx}_Initial_cash')

        print("Strategy count:", len(data.strategies))
        for i, (percent, strategy) in enumerate(data.strategies):
            print(strategy.type)
            strategy_cols = st.columns([1, 6, 3])
            if strategy_cols[0].button("⊖", use_container_width=True, key=f'{idx}.{i}_strategy_delete'):
                data.strategies.pop(i)
                print("Strategy deleted: new count", len(form.strategies))
            with strategy_cols[1]:
                form.selectbox(f"Strategy {i+1}", options=[type.name for type in StrategyType], index=StrategyType[strategy.type].value, label_visibility='collapsed', key=f'{idx}{i}_strategy_type')
            with strategy_cols[2]:
                form.number_input("Percent", value=percent, label_visibility='collapsed', key=f'{idx}.{i}_strategy_percent')
            
            print("Asset count:", len(strategy.assets))
            for j, (ticker, percent) in enumerate(strategy.assets.items()):
                print(ticker)
                asset_cols = st.columns([1, 1, 6, 3])
                if asset_cols[1].button("⊖", use_container_width=True, key=f'{idx}.{i}.{j}_asset_delete'):
                    strategy.assets.pop(ticker)
                with asset_cols[2]:
                    form.text_input(f"Asset {j+1}", value=ticker, placeholder="ticker", label_visibility='collapsed', key=f'{idx}.{i}.{j}_asset_ticker')
                with asset_cols[3]:
                    form.number_input("Percent", value=percent, label_visibility='collapsed', key=f'{idx}.{i}.{j}_asset_percent')
            
            asset_cols = st.columns([1, 1, 6, 3])
            asset_cols[1].button("⊕", type='primary', use_container_width=True, key=f'{idx}.{i}.{j+1}_asset_add')
            asset_cols[2].text_input(f"Asset {j+1}", placeholder="ticker", label_visibility='collapsed', key=f'{idx}.{i}.{j+1}_asset_ticker')
            asset_cols[3].number_input("Percent", value=0, label_visibility='collapsed', key=f'{idx}.{i}.{j+1}_asset_percent')
        
        strategy_cols = st.columns([1, 6, 3])
        strategy_cols[0].button("⊕", type='primary', use_container_width=True, key=f'{idx}.{i+1}_strategy_add')
        strategy_cols[1].selectbox(f"Strategy {i+1}", options=[type.name for type in StrategyType], index=StrategyType.ALLIN.value, label_visibility='collapsed', key=f'{idx}{i+1}_strategy_type')
        strategy_cols[2].number_input("Percent", value=0, label_visibility='collapsed', key=f'{idx}.{i+1}_strategy_percent')
        
    if form.form_submit_button():
        






st.markdown('---')
print("""
    # ---------------
    # -- Result
    # ---------------""")
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