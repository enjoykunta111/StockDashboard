import dash
from dash import html

dash.register_page(__name__, path='/', name='Introduction ')

layout = html.Div(children=[
    html.Div(children=[
        html.H2("Titanic Dataset Overview"),
        "The sinking of the Titanic is one of the most infamous shipwrecks in history"
    ])
])