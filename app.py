import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# read the csv file
df = pd.read_csv("ibrd-statement-of-loans-historical-data.csv")

# List all countries inorder to populate the dropdown

ctry_options = df["Country"].unique()

def generate_summary(dataframe):
    return html.Table(
        # Body
        [html.Tr("Missing Values:"),
        html.Tr("Maximum value:"),
        html.Tr("Minimum value:")]
    )

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
        children='Loans History Data - Awamo',
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
    html.H5(children='Statistics on the quality of data supplied by field'),
    generate_summary(df)
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
    pv = pd.pivot_table(
        df_plot,
        index=["Region"],
        columns=["End of Period"],
        values=["Repaid to IBRD"])
        
    trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'Repaid')], name='Declined')

    return {
        'data': [trace1],
        'layout':
        go.Layout(
            title='Loan Status for {}'.format(Country),
            barmode='stack')
    }

if __name__ == '__main__':
    app.run_server(debug=True)