import pandas as pd
import streamlit as st
from typing import List
st.set_page_config(layout="wide", page_title="Portfolio Backtest")
import plotly.graph_objects as go

import form


portfolios = form.read_forms()

st.title("Backtest portfolio")