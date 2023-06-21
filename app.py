from dash import dash, Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from datetime import datetime 
import plotly.graph_objects as go
import pandas as pd

from utils.portfolio import Portfolio

    
# Layout construction
# =============================
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
    dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src='assets/C.png', height="30px")),
                    dbc.Col(dbc.NavbarBrand("Portfolio Backtest", className="ms-2")),
                ]),
                href="/home",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        ]),
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