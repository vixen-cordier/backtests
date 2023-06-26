import streamlit as st
import datetime
import pandas as pd
from typing import List
st.set_page_config(layout="wide", page_title="Portfolio Backtest")
import plotly.graph_objects as go

from classes.form import Form, read_forms, save_forms
# import layouts.form_page as form_p



forms = read_forms()
forms_checked: List[Form] = []


def form_page(form=None):
    print("Go to Form Page:", form.name if form is not None else "New!")

# st.write("""
# <style>
# div[data-testid="stMarkdownContainer"] > p {
#     font-size: 24px;
# }
# </style>
# """, unsafe_allow_html=True)


with st.sidebar:
    st.title("Portfolios")
    st.write(" ")

    new_form_button = st.button("Create new portfolio", type="primary")#, use_container_width=True)
    st.write(" ")
    if new_form_button:
        st.write("Go to Form Page !")

    for form in forms:
        if st.checkbox(form.name, key=f'{form.name}_checkbox'):
            forms_checked.append(form)
        # buttons = st.columns(3)
        # if buttons[0].button("🛈", key=f'{form.name}_info'):
        #     print("Get Info:", form.name)
        #     st.write("Some information")
        # if buttons[1].button("🖍", key=f'{form.name}_upd'):
        #     print("Update:", form.name)
        # if buttons[2].button("🗙", key=f'{form.name}_del'):
        #     print("Delete:", form.name)


if forms_checked:
    st.title(" vs ".join(form.name for form in forms_checked))
    start_date = max( chart.get_oldest_date() for form in forms_checked for chart in form.portfolio.charts.values())
    end_date = min( chart.get_youngest_date() for form in forms_checked for chart in form.portfolio.charts.values())
    date_range = st.slider("Date slider to filter data", format="YYYY-MM-DD", value=(
        datetime.datetime(start_date.year, start_date.month, start_date.day),
        datetime.datetime(end_date.year, end_date.month, end_date.day)
    ))
    

    fig = go.Figure()
    for form in forms_checked:
        form.portfolio.filter_by_dates(date_range[0], date_range[1])
        for _, strategy in form.strategies:
            strategy.apply(form.portfolio, start_date=date_range[0])
        if not form.portfolio.operations.empty:
            stats = form.portfolio.stats()
            fig.add_trace(go.Scatter(x=stats.chart.index, y=stats.chart.values, name=form.name))
    st.plotly_chart(fig)