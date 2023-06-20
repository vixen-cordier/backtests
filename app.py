import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from datetime import datetime 
import plotly.graph_objects as go
import pandas as pd

from utils.portfolio import Portfolio

    
# Layout construction
# =============================
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    dbc.Navbar(
        dbc.Collapse(
            dbc.Row([
                dbc.Col(dbc.Input(type="search", placeholder="Search")),
                dbc.Col(
                    dbc.Button("Search", color="primary", className="ms-2", n_clicks=0),
                    width="auto"
                )],
                className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                align="center",
            ),
            navbar=True,
            is_open=False,
        ),
        color="dark",
        dark=True,
    ),
    dash.page_container,
])


# # Callbacks definition
# # =============================
# @callback(
#     Output('portfolio-graph', '_'),
#     Input('ticker-input', 'ticker')
# )
# def edit_form(portfolio):
#     return None


# @callback(
#     Output('portfolio-graph', '_'),
#     Input('ticker-input', 'ticker')
# )
# def view_result(portfolio):
#     return None


# main
# =============================
if __name__ == '__main__':
    app.run_server(debug=True)