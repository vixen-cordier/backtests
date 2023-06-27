import plotly.graph_objects as go
import streamlit as st
import datetime
from typing import List

from classes.form import Form


def layout(forms: List[Form]):
    if forms:
        st.title(" vs ".join(form.name for form in forms))
        start_date = max( chart.get_oldest_date() for form in forms for chart in form.portfolio.charts.values() )
        end_date = min( chart.get_youngest_date() for form in forms for chart in form.portfolio.charts.values() )
        date_range = st.slider("Date slider to filter data", format="YYYY-MM-DD", value=(
            datetime.datetime(start_date.year, start_date.month, start_date.day),
            datetime.datetime(end_date.year, end_date.month, end_date.day)
        ))
        

        fig = go.Figure()
        for form in forms:
            form.portfolio.filter_by_dates(date_range[0], date_range[1])
            for _, strategy in form.strategies:
                strategy.apply(form.portfolio, start_date=date_range[0])
            if not form.portfolio.operations.empty:
                stats = form.portfolio.stats()
                fig.add_trace(go.Scatter(x=stats.chart.index, y=stats.chart.values, name=form.name))
        st.plotly_chart(fig)