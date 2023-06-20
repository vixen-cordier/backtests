import dash
from dash import html, dcc, callback, Output, Input

dash.register_page(
    __name__, 
    name="Form", 
    top_nav=True,
    path_template="/form/<portfolio_id>"
)

def layout(portfolio_id=None, **other_unknown_query_strings):
    return html.Div([
        html.H1(children=f'Input data of {portfolio_id}'),
        # dcc.Input(id="ticker-input", type="text", placeholder="ticker"),
	])