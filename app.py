import pandas as pd
import numpy as np
import datetime as dt
import dash_table
import random
import math
import os
import urllib.request, json, time, sys
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc 
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from mpg_data import get_data, insight_creator, last_10_creator, money_format, lin_reg

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

df = get_data()
df['date'] = pd.to_datetime(df['date'].astype(str))
df_i = insight_creator(df)
df_insights = df_i.copy()
df_insights['Miles'] = df_insights['Miles'].apply(lambda x: "{:,}".format(x))
df_insights['Dollars'] = df_insights['Dollars'].apply(lambda x: "${:,.2f}".format(x))
df_insights['Gallons'] = df_insights['Gallons'].apply(lambda x: "{:,.2f}".format(x))
df_insights['MPG'] = round(df_insights['MPG'], 2)
df_insights['Avg gallon cost'] = df_insights['Avg gallon cost'].apply(lambda x: '$' + str(x) + '0' if len(str(x)) < 4 else '$' + str(x))
df_insights['Cost to go one mile'] = '$' + (round(df_insights['Cost to go one mile (in cents)']/100, 2)).astype(str).apply(lambda x: str(x) + '0' if len(str(x)) < 4 else str(x))

last_10 = last_10_creator(df)

date_range = pd.date_range(df['date'].min(),df['date'].max(),freq='MS')

scatter1_options = [{'label':str(i),'value':i} for i in [
    'Miles Per Gallon', 
    'Gallon Cost'
]]
scatter1_radio_options = [
    {'label': 'Values', 'value': 'values'},
    {'label': 'Moving Average (n=5)', 'value': 'mov_avg'}
]
scatter2_options = [{'label':str(i),'value':i} for i in [
    'Miles Per Gallon', 
    'Cost To Drive One Mile'
]]

app.layout = html.Div([
    dbc.Row(
        html.H1(
            children='MPG Dashboard',
            style={'textAlign': 'center'})
    ),

    html.Center(
        [dcc.Graph(id='scatter1')]
    ),

    html.Div([
        dcc.Dropdown(
            id='scatter1-kind', 
            options=scatter1_options, 
            value='Miles Per Gallon'
        ),
        dcc.RadioItems(
            id='scatter1-radio', 
            options=scatter1_radio_options, 
            value='mov_avg'
        )
    ],
    style={
        'width': '50%', 
        'align-items': 'center', 
        'display': 'inline-block', 
        'justify-content': 'center'
    }),

    html.Center(
        [dcc.Graph(id='scatter2')]
    ),

    html.Div([
        dcc.Dropdown(
            id='scatter2-kind', 
            options=scatter2_options, 
            value='Cost To Drive One Mile'
        )
    ],
    style={
        'width': '50%', 
        'align-items': 'center', 
        'display': 'inline-block', 
        'justify-content': 'center'
    }),

    dbc.Row(
        html.H2(
            children='Gas Insights',
            style={'textAlign': 'center'}
        )
    ),

    html.Center([
        html.Div([
            dash_table.DataTable(
                id='insight_table',
                columns=[{"name": i, "id": i} for i in [
                    'Time period', 
                    'Miles', 
                    'Dollars', 
                    'Gallons', 
                    'MPG', 
                    'Avg gallon cost',
                    'Cost to go one mile', 
                    'Average miles per day'
                ]],
                data=df_insights.to_dict('records'),
                style_header = {
                    'backgroundColor': '#5C7DAA',
                    'fontWeight': 'bold',
                    'border': '1px solid black',
                    'whiteSpace': 'normal',
                    'color': 'white',
                    'textAlign': 'left'
                },
                style_cell = {
                    'font-family':'sans-serif',
                    'backgroundColor': '#D3D3D3',
                    'textAlign': 'left',
                    'border': '1px solid grey',
                    'color': 'black'
                },
                style_table = {
                    'overflowX': 'scroll',
                    'maxWidth': '80%',
                    'minWidth': '40%'
                }
            ),
        ])
    ]),

    dbc.Row(
        html.H2(
            children='Last 10 Fillups',
            style={'textAlign': 'center'}
        )
    ),

    html.Center([
        html.Div([
            dash_table.DataTable(
                id='last10_table',
                columns=[{"name": i, "id": j} for i,j in zip([
                            'Date', 
                            'Miles', 
                            'Dollars', 
                            'Gallons', 
                            'MPG', 
                            'Gallon cost',
                            'Tank % Used', 
                            'Cost to go one mile', 
                            'Average miles per day'
                ], last_10.columns
                )
                ],
                data=last_10.to_dict('records'),
                style_header = {
                    'backgroundColor': '#5C7DAA',
                    'fontWeight': 'bold',
                    'border': '1px solid black',
                    'whiteSpace': 'normal',
                    'color': 'white',
                    'textAlign': 'left'
                },
                style_cell = {
                    'font-family':'sans-serif',
                    'backgroundColor': '#D3D3D3',
                    'textAlign': 'left',
                    'border': '1px solid grey',
                    'color': 'black'
                },
                style_table = {
                    'overflowX': 'scroll',
                    'maxWidth': '80%',
                    'minWidth': '40%'
                }
            ),
        ])
    ]),

])

@app.callback(Output('scatter1', 'figure'),
              [Input('scatter1-kind', 'value'),
              Input('scatter1-radio', 'value')])
def update_scatter1(graph_option, radio_option):
    if graph_option.startswith('Miles Per Gallon'):
        if radio_option == 'values':
            y = df['mpg']
            line_color = "#CB4F0A"
        else:
            y = round(df['mpg'].rolling(window=5).mean(),2)
            line_color = "#F58426"
        htemp = y.astype(str) + ' on ' + df['date'].dt.strftime('%b %-d, %Y')
        yrange = [df['mpg'].min() - 1, df['mpg'].max() + 1]
        ytick = [i for i in range(math.floor(df['mpg'].min()),math.ceil(df['mpg'].max()))]
        tick_text = [i  if i % 2 == 0 else '' for i in ytick]

    else:
        if radio_option == 'values':
            y = df['gal_cost']
            htemp = df['gal_cost'].apply(money_format) + ' on ' + df['date'].dt.strftime('%b %-d, %Y') + '<extra></extra>'
            line_color = "#1A4D94"
        else:
            y = df['gal_cost'].rolling(window=5).mean()
            htemp = '$' + round(df['gal_cost'].rolling(window=5).mean(),2).apply(lambda x: '{:.2f}'.format(x)) + ' on ' + \
                    df['date'].dt.strftime('%b %-d, %Y') + '<extra></extra>'
            line_color = "#5C7DAA"
        Y_t = y * 10
        yrange = [df['gal_cost'].min() - .2, df['gal_cost'].max() + .2]
        ytick = [i/10 for i in range(math.floor(Y_t.min()), math.ceil(Y_t.max()) + 2, 2)]
        tick_text = [money_format(i) for i in [i/10 for i in range(math.floor(Y_t.min()), math.ceil(Y_t.max()) + 2, 2)]]

    if radio_option == 'mov_avg':
        graph_option += ' Moving Average (n=5)'

    return {
        'data': [
            go.Scatter(
                x=df['date'],
                y=y,
                mode='lines',
                hovertemplate=htemp,
                name=graph_option,
                line=dict(
                    color=line_color
                )
            )
        ],
        'layout': go.Layout(
            showlegend=False,
            plot_bgcolor='#cccccc',
            title=dict(
                text='{} over time'.format(graph_option),
                font=dict(
                    size=24,
                    color='#000000'
                ),
                x=.5
            ),
            xaxis=dict(
                title='Date',
                ticktext=[i.strftime("%b '%y") for i in date_range],
                tickvals=date_range,
                range=[
                    df['date'].min() - dt.timedelta(days=5), 
                    df['date'].max() + dt.timedelta(days=5)
                ]
            ),
            yaxis=dict(
                title=graph_option,
                range=yrange,
                tickvals=ytick,
                ticktext=tick_text
            )
        )
    }

@app.callback(Output('scatter2', 'figure'),
              [Input('scatter2-kind', 'value')])
def update_scatter2(graph_option):
    x = df['miles']
    if graph_option.startswith('Miles'):
        y = df['mpg']
        htemp = '<b>Miles Driven: </b>' + x.astype(str)+ \
                '<br><b>Miles Per Gallon: </b>' + y.astype(str)+ \
                '<br>'+df['date'].dt.strftime('%b %-d, %Y') \
                +'<extra></extra>'
        yrange = [y.min() - .5, y.max() + .5]
        ytick = [i for i in range(math.floor(y.min()), math.ceil(y.max()))]
        tick_text = [i  if i % 2 == 0 else '' for i in ytick]
        annotation = "On average, I get " + (round(df_i['MPG'].iloc[-1], 2)).astype(str) + " miles per gallon"

    else:
        y = round(df['dollars per mile'] * 100, 2)
        htemp = '<b>Miles Driven: </b>' + x.astype(str)+ \
                '<br><b>Cost To Drive One Mile (in cents): </b>' + y.astype(str)+ \
                '<br>'+df['date'].dt.strftime('%b %-d, %Y') \
                +'<extra></extra>'
        yrange = [math.floor(y.min()), math.ceil(y.max())]
        ytick = [i for i in range(math.floor(y.min()), math.ceil(y.max()) + 1)]
        tick_text = [money_format(i) for i in [i/100 for i in range(math.floor(y.min()), math.ceil(y.max()) + 1)]]
        annotation = "On average, it costs " + (round(df_i['Cost to go one mile (in cents)'].iloc[-1], 2)).astype(str) + \
                    " cents to drive one mile"
                    
    if graph_option == 'Cost To Drive One Mile':
        graph_option += ' (in cents)'

    slope, intercept, preds, rmse, r_2 = lin_reg(x, y)

    return {
        'data': [
            go.Scatter(
                x=x,
                y=y,
                mode='markers',
                hovertemplate=htemp,
                name='Data'
            ),
            go.Scatter(
                x=x,
                y=preds,
                mode='lines',
                name='Linear Regression' + \
                    '<br>y = {0}x + {1}'.format(round(slope, 3), round(intercept, 2)) + \
                    '<br>r^2 = {}'.format(r_2) + \
                    '<br>RMSE = {}'.format(rmse),
                hovertemplate='<b>Miles Driven: </b>' + x.astype(str)+ \
                    '<br><b>Predicted {}: </b>'.format(graph_option) + round(preds, 2).astype(str)+ \
                    '<extra></extra>'
            )
        ],
        'layout': go.Layout(
            showlegend=True,
            plot_bgcolor='#cccccc',
            title=dict(
                text='Miles Driven vs. {}'.format(graph_option),
                font=dict(
                    size=24,
                    color='#000000'
                ),
                x=.5
            ),
            xaxis=dict(
                title='Miles Driven',
                range=[
                    x.min() - 2, 
                    x.max() + 2
                ]
            ),
            yaxis=dict(
                title=graph_option,
                range=yrange,
                tickvals=ytick,
                ticktext=tick_text
            ),
            annotations=[
                dict(
                    x=0.5,
                    y=1.075,
                    showarrow=False,
                    text=annotation,
                    xref="paper",
                    yref="paper",
                    font=dict(
                        color="black",
                        size=12
                    )
                )
            ]
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
