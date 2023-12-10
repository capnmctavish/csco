import pandas as pd
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Load CSV data
balance_sheet_df = pd.read_csv('Cisco_data/balancesheet.csv')
balance_sheet_df = balance_sheet_df.set_index("Names").T
balance_sheet_df.index = pd.to_datetime(balance_sheet_df.index)
# balance_sheet_df = pd.read_csv('Cisco_data/balancesheet.csv', index_col=0)
cash_flow_df = pd.read_csv('Cisco_data/cashflow.csv', index_col=0)
cash_flow_df = cash_flow_df.transpose() 
stocks_history_df = pd.read_csv('Cisco_data/history.csv', index_col=0, parse_dates=True)
income_statement_df = pd.read_csv('Cisco_data/income_stmt.csv', index_col=0)

shareholder_data = pd.read_csv('Cisco_data/major_holders.csv')
shareholder_data['%'] = shareholder_data['%'].str.rstrip(' %').astype('float')
# shareholder_data['Equities'] = pd.to_numeric(shareholder_data['Equities'].str.replace(',', ''), errors='coerce')
# shareholder_data['%'] = pd.to_numeric(shareholder_data['%'].str.replace('%', ''), errors='coerce')


region_sales_df = pd.read_csv('Cisco_data/region.csv')
px.defaults.template = "ggplot2"

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]
# Create Dash app
app = dash.Dash(__name__, external_stylesheets=external_css)
server = app.server  # Added in for Cloud Run compatibility

# Define app layout
app.layout = html.Div(className='text-dark text-center fw-bold fs-1', children=[
    html.H1(children='CISCO Financial Performance Dashboard'),

    html.Div(className='container-fluid', children=[
        # First Row
        html.Div(className='row', children=[
            # First Column
            html.Div(className='col-md-4', children=[
                dcc.Graph(
                    id='total-assets-plot',
                    figure=px.line(balance_sheet_df, x=balance_sheet_df.index, y='Total Assets', title='Total Assets Over Time')
                )
            ]),
            # Second Column
            html.Div(className='col-md-4', children=[
                dcc.Graph(
                    id='debt-analysis-plot',
                    figure=go.Figure(data=[
                        go.Bar(x=balance_sheet_df.index, y=balance_sheet_df['Total Debt'], name='Total Debt'),
                        go.Bar(x=balance_sheet_df.index, y=balance_sheet_df['Net Debt'], name='Net Debt')
                    ], layout={'barmode': 'group', 'title': 'Debt Analysis'})
                )
            ]),
            # Third Column
            html.Div(className='col-md-4', children=[
                dcc.Graph(
                    id='cash-investments-plot',
                    figure=go.Figure(data=[
                        go.Bar(x=balance_sheet_df.index, y=balance_sheet_df['Cash Cash Equivalents And Short Term Investments'], name='Cash Cash Equivalents And Short Term Investments')
                    ], layout={'barmode': 'group', 'title': 'Cash and Short-Term Investments'})
                )
            ]),
        ]),
        
        # Second Row
        html.Div(className='row', children=[
            # First Column
            html.Div(className='col-md-4', children=[
                dcc.Graph(
                    id='free-cash-flow-plot',
                    figure=px.line(cash_flow_df, x=cash_flow_df.index, y='FreeCashFlow', title='Free Cash Flow Over Time')
                )
            ]),
            # Second Column
            html.Div(className='col-md-4', children=[
                dcc.Graph(
                    id='cash-flow-components-plot',
                    figure=px.bar(cash_flow_df, x=cash_flow_df.index, y=cash_flow_df.columns, barmode='group', title='Cash Flow Components Over Time')
                )
            ]),
            # Third Column
            html.Div(className='col-md-4', children=[
                dcc.Graph(
                    id='operating-cash-flow-breakdown-plot',
                    figure=px.bar(cash_flow_df, x=cash_flow_df.index, y=cash_flow_df.columns, barmode='stack', title='Operating Cash Flow Breakdown')
                )
            ]),
        ]),
        
        # Third Row
        html.Div(className='row', children=[
            # First Column
            html.Div(className='col-md-4', children=[
                dcc.Graph(
                    id='stocks-history-plot',
                    figure=go.Figure(data=[go.Candlestick(x=stocks_history_df.index,
                                                          open=stocks_history_df['Open'],
                                                          high=stocks_history_df['High'],
                                                          low=stocks_history_df['Low'],
                                                          close=stocks_history_df['Close'])],
                                    layout={'title': 'Stocks History'})
                )
            ]),
            html.Div(className='col-md-4', children=[

                dcc.Graph(
                    id='region-pie-chart',
                    figure=px.pie(region_sales_df, names='Region', values='2022', title='Region Sales Distribution (2022)')
                ),
            ]),
            html.Div(className='col-md-4', children=[
                dcc.Graph(
                id='shareholder-pie-chart',
                figure=px.pie(shareholder_data, names='Name', values='%', title='Shareholder Equities')
             ),
            ]),
        ]),
    ]),
])
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=int(os.environ.get('PORT', 8080)))