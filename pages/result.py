import dash
from dash import html, dcc, callback, Output, Input

dash.register_page(
    __name__, 
    name="Result", 
    top_nav=True,
    path_template="/result/<portfolio_id>"
)

def layout(portfolio_id=None, **other_unknown_query_strings):
    return html.Div([
        html.H1(children=f'Backtest of {portfolio_id}'),
        # dcc.Graph(id='portfolio-graph')
	])