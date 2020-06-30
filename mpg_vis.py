# %%
import pandas as pd
import datetime as dt
import pandas as pd
import numpy as np
import math
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import plotly.io as pio
from plotly.colors import n_colors
import plotly.express as px
import plotly.figure_factory as ff
import chart_studio
# api_key = f = open("plotly_keys.txt", "r").readline()
# chart_studio.tools.set_credentials_file(username='ethanfuerst', api_key=api_key)
import datetime as dt
from datetime import date, timedelta, datetime
from mpg_refresh import mpg_data_creator, insight_creator
df = pd.read_csv('car_mpg_data.csv')
# - returns the correct data types
df = mpg_data_creator(df)

def money_format(x):
    return '${:.2f}'.format(x)

show_all = False

# %%
# todo Change line colors
X = df['date']
Y = df['gal_cost']

# - format for finding tick vals
Y_t = Y * 10
range(math.floor(Y_t.min()), math.ceil(Y_t.max()), 2)

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['date'],
                                y=df['gal_cost'],
                                mode='lines',
                                hovertemplate=df['gal_cost'].apply(money_format) + ' on ' + df['date'].dt.strftime('%b %d %Y'),
                                name='Gallon cost',
                                line=dict(color="#1A4D94")
))
fig.add_trace(go.Scatter(x=df['date'],
                                y=df['gal_cost'].rolling(window=5).mean(),
                                mode='lines',
                                hovertemplate='$' + round(df['gal_cost'].rolling(window=5).mean(),2).apply(lambda x: '{:.2f}'.format(x)) + ' on ' + df['date'].dt.strftime('%b %d %Y'),
                                name='Moving average',
                                line=dict(color="#5C7DAA")
))

fig.update_layout(
    showlegend=False,
    width=1000,
    height=500,
    updatemenus=[
        dict(
            type = "buttons",
            buttons=list([
                dict(
                    args=[dict(visible=[True, False]),
                            dict(title='Gallon Cost')],
                    label="Gallon cost",
                    method="restyle"
                ),
                dict(
                    args=[dict(visible=[False, True]),
                            dict(title='Moving average')],
                    label="Moving average",
                    method="restyle"
                ),
                dict(
                    args = [dict(visible=[True, True])],
                    label="Both",
                    method="restyle"
                )
            ]),
            direction='down',
            showactive=True,
            x=1.05,
            xanchor="left",
            yanchor="top"
        ),
    ],
    plot_bgcolor='#cccccc',
    title=dict(
        text='Cost of a gallon of gas over time',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Date',
        ticktext=pd.date_range(df['date'].min(),df['date'].max(),freq='MS').strftime("%b '%y").tolist(),
        tickvals=pd.date_range(df['date'].min(),df['date'].max(),freq='MS'),
        range=[df['date'].min() - dt.timedelta(days=5), df['date'].max() + dt.timedelta(days=5)]
    ),
    yaxis=dict(
        title='Cost',
        tickvals=[i/10 for i in range(math.floor(Y_t.min()), math.ceil(Y_t.max()) + 2, 2)],
        range=[df['gal_cost'].min() - .2, df['gal_cost'].max() + .2],
        ticktext=[money_format(i) for i in [i/10 for i in range(math.floor(Y_t.min()), math.ceil(Y_t.max()) + 2, 2)]]
    )
)

if show_all:
    fig.show()



# %%
# todo Change line colors
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['date'],
                                y=df['mpg'],
                                mode='lines',
                                hovertemplate=df['mpg'].astype(str)+ ' on ' + df['date'].dt.strftime('%b %d %Y'),
                                name='MPG',
                                line=dict(color="#1A4D94")
))
fig.add_trace(go.Scatter(x=df['date'],
                                y=df['mpg'].rolling(window=5).mean(),
                                mode='lines',
                                hovertemplate=round(df['mpg'].rolling(window=5).mean(),2).astype(str) + ' on ' + df['date'].dt.strftime('%b %d %Y'),
                                name='Moving average',
                                line=dict(color="#5C7DAA")
))

fig.update_layout(
    showlegend=False,
    plot_bgcolor='#cccccc',
    width=1000,
    height=500,
    updatemenus=[
        dict(
            type = "buttons",
            buttons=list([
                dict(
                    args=[dict(visible=[True, False]),
                            dict(title='MPG')],
                    label="MPG",
                    method="restyle"
                ),
                dict(
                    args=[dict(visible=[False, True]),
                            dict(title='Moving average')],
                    label="Moving average",
                    method="restyle"
                ),
                dict(
                    args = [dict(visible=[True, True])],
                    label="Both",
                    method="restyle"
                )
            ]),
            direction='down',
            showactive=True,
            x=1.05,
            xanchor="left",
            yanchor="top"
        ),
    ],
    title=dict(
        text='Miles per gallon over time',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Date',
        ticktext=pd.date_range(df['date'].min(),df['date'].max(),freq='MS').strftime("%b '%y").tolist(),
        tickvals=pd.date_range(df['date'].min(),df['date'].max(),freq='MS'),
        range=[df['date'].min() - dt.timedelta(days=5), df['date'].max() + dt.timedelta(days=5)]
    ),
    yaxis=dict(
        title='MPG',
        range=[df['mpg'].min() - 1, df['mpg'].max() + 1],
        tickvals=[i for i in range(math.floor(df['mpg'].min()),math.ceil(df['mpg'].max()))]
    )
)

if show_all:
    fig.show()


# %%
# - mpg vs. miles driven scatter plot
# todo color by date

X = df['miles']
Y = df['mpg']

slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
linreg = slope * X + intercept
r_2 = round(r_value ** 2, 2)

fig = go.Figure(data=[go.Scatter(x=X,
                                y=Y,
                                mode='markers',
                                name='Data',
                                hovertemplate='<b>Miles driven: </b>' + X.astype(str)+
                                '<br><b>Miles per gallon: </b>' + Y.astype(str)+
                                '<br>'+df['date'].dt.strftime('%b %d %Y')+
                                '<extra></extra>'
                                ),
                        go.Scatter(
                                x=X,
                                y=linreg,
                                mode='lines',
                                name='Linear Regression' +
                                '<br>y = {0}x + {1}'.format(round(slope, 3), round(intercept, 2)) + 
                                '<br>r^2 = {}'.format(r_2),
                                hovertemplate='<b>Miles driven: </b>' + X.astype(str)+
                                '<br><b>Predicted miles per gallon: </b>' + Y.astype(str)+
                                '<extra></extra>'
                                )]
                )
fig.update_layout(
    plot_bgcolor='#cccccc',
    title=dict(
        text='Miles per gallon vs. miles driven',
        font=dict(
            size=24,
            color='black'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Miles driven',
        range=[X.min() - 2, X.max() + 2]
    ),
    yaxis=dict(
        title='Miles per gallon',
        range=[Y.min() - .5, Y.max() + .5],
        tickvals=[i for i in range(math.floor(Y.min()),math.ceil(Y.max()))]
    ),
    width=900,
    height=800
)

if show_all:
    fig.show()


# %%
# - $ per mile vs. miles scatter plot
# todo color by date
# todo Add average cost per mile as text

X = df['miles']
# - Cents per mile
Y = round(df['dollars per mile'] * 100, 2)

slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
linreg = slope * X + intercept
r_2 = round(r_value ** 2, 2)

fig = go.Figure(data=[go.Scatter(x=X,
                                y=Y,
                                mode='markers',
                                name='Data',
                                hovertemplate='<b>Miles driven: </b>' + X.astype(str)+
                                '<br><b>Cents per mile: </b>' + Y.astype(str)+
                                '<br>'+df['date'].dt.strftime('%b %d %Y')+
                                '<extra></extra>'
                                ),
                        go.Scatter(
                                x=X,
                                y=linreg,
                                mode='lines',
                                name='Linear Regression' +
                                '<br>y = {0}x + {1}'.format(round(slope, 3), round(intercept, 2)) + 
                                '<br>r^2 = {}'.format(r_2),
                                hovertemplate='<b>Miles driven: </b>' + X.astype(str)+
                                '<br><b>Predicted dollars per mile: </b>' + Y.astype(str)+
                                '<extra></extra>'
                                )]
                )
fig.update_layout(
    plot_bgcolor='#cccccc',
    title=dict(
        text='Cost per mile vs. miles driven',
        font=dict(
            size=24,
            color='black'
        ),
        x=.5
    ),
    xaxis=dict(
        title='Miles driven',
        range=[X.min() - 5, X.max() + 5]
    ),
    yaxis=dict(
        title='Cost to drive one mile',
        range=[math.floor(Y.min()), math.ceil(Y.max())],
        tickvals=[i for i in range(math.floor(Y.min()), math.ceil(Y.max()) + 1)],
        ticktext=[money_format(i) for i in [i/100 for i in range(math.floor(Y.min()), math.ceil(Y.max()) + 1)]]
    ),
    width=900,
    height=800
)

if show_all:
    fig.show()


# %%
# todo Predict mpg based on miles driven and date


# %%
# todo High/low temp over a year with mpg

