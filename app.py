import pandas as pd
import streamlit as st
from typing import List
st.set_page_config(layout="wide", page_title="Portfolio Backtest")
import plotly.graph_objects as go

from classes.form import Form
import classes.form as form
import pages.form_page as form_page


portfolios = form.read_forms()

st.title("Backtest portfolio")

