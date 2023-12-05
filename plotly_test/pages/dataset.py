import pandas as pd
import dash
from dash import html, dash_table, dcc
import plotly.graph_objects as go

dash.register_page(__name__, path='/dataset', name='Dataset')

######## LOAD DATASET ######
titanic_df = pd.read_csv('titanic.csv')

layout = html.Div(children=[
    html.Br(),
    dash_table.DataTable(data=titanic_df.to_dict('records'),
                         page_size=20,
                         )
])