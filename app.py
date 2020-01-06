import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from datetime import datetime 
import plotly.graph_objs as go

# read the csv file
df = pd.read_csv("ibrd-statement-of-loans-historical-data.csv", low_memory = False, parse_dates=['End of Period'])

# remove columns we donot need to make data processing faster
df.drop(['Effective Date (Most Recent)', 'Closed Date (Most Recent)'], axis=1, inplace=True)

# Basic stats
def stats():
    return html.Div([
        html.Div("Number of records in the dataset: " + str(len(df))),
        html.Div("Number of features in the dataset: " + str(len(df.columns))),
))
])

# CLEANING AND PREPARING DATA
# Convert dates to datetime
df['End of Period'] = pd.to_datetime(df['End of Period']).dt.date.astype('datetime64[ns]')
df['First Repayment Date'] = pd.to_datetime(df['First Repayment Date']).dt.date.astype('datetime64[ns]')
df['Last Repayment Date'] = pd.to_datetime(df['Last Repayment Date']).dt.date.astype('datetime64[ns]')
df['Agreement Signing Date'] = pd.to_datetime(df['Agreement Signing Date']).dt.date.astype('datetime64[ns]')
df['Board Approval Date'] = pd.to_datetime(df['Board Approval Date']).dt.date.astype('datetime64[ns]')
df['Last Disbursement Date'] = pd.to_datetime(df['Last Disbursement Date']).dt.date.astype('datetime64[ns]')

# List all countries inorder to populate the dropdown

ctry_options = df["Country"].unique()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# initialize the dash application
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# access flask application instance for purposes of deployment
server = app.server
colors = {
    'background': '#e2ebf0',
    'text': '#273746',
}
# set up the layout of the application
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H3(
        children='Loans History Data - IBRD',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Service that consumes the monthly loans dataset', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div(
        [
            dcc.Dropdown(
                id="Country",
                options=[{
                    'label': i,
                    'value': i
                } for i in ctry_options],
                value='All Countries'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(
        id='funnel-graph'),
    
    html.H5(children='Basic Statistics'),
    stats()

])

# add interactivity to the application
# bind callback function to the html input field
@app.callback(
    Output('funnel-graph', 'figure'),
    [Input("Country", "value")]
)
def update_graph(Country):
    if Country == "All Countries":
        df_plot = df.copy()
    else:
        df_plot = df[df["Country"] == Country]
    
    # pivot table aggregates values by taking the sum
    pv = pd.pivot_table(df_plot,index=["Project Name "], values=["Due to IBRD"], fill_value=0)
    trace1 = go.Bar(x=pv.index, y=pv[('Due to IBRD')])

    return {
        'data': [trace1],
        'layout':
        go.Layout(
            title='Loan Status for {}'.format(Country),
            barmode='stack')
    }

if __name__ == '__main__':
    app.run_server(debug=True)


