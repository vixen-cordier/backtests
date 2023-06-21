import dash
from dash import html, dcc, callback, Output, Input

dash.register_page(
    __name__, 
    name="Home", 
    path_template="/home"
)

def layout():
    return html.Div([
        html.H1(children="List of portfolio"),
        # dcc.Input(id="ticker-input", type="text", placeholder="ticker"),
	])