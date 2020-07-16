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
api_key = f = open("plotly_key.txt", "r").readline()
chart_studio.tools.set_credentials_file(username='ethanfuerst', api_key=api_key)
import datetime as dt
from datetime import date, timedelta, datetime
from mpg_refresh import get_data, insight_creator
df = get_data()
df_i = insight_creator(df)

def money_format(x):
    return '${:.2f}'.format(x)

show_all = False

# todo create dict of figs and names then iterate over and update plotly server

# %%
X = df['date']
Y = df['gal_cost']

# - format for finding tick vals
Y_t = Y * 10
range(math.floor(Y_t.min()), math.ceil(Y_t.max()), 2)
date_range = pd.date_range(df['date'].min(),df['date'].max(),freq='MS')

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
    width=700,
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
        ticktext=date_range.strftime("%b '%y").tolist(),
        tickvals=date_range,
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

chart_studio.plotly.plot(fig, filename='Cost of a gallon of gas over time', auto_open=False)

# %%
date_range = pd.date_range(df['date'].min(),df['date'].max(),freq='MS')

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['date'],
                                y=df['mpg'],
                                mode='lines',
                                hovertemplate=df['mpg'].astype(str)+ ' on ' + df['date'].dt.strftime('%b %d %Y'),
                                name='MPG',
                                line=dict(color="#CB4F0A")
))
fig.add_trace(go.Scatter(x=df['date'],
                                y=df['mpg'].rolling(window=5).mean(),
                                mode='lines',
                                hovertemplate=round(df['mpg'].rolling(window=5).mean(),2).astype(str) + ' on ' + df['date'].dt.strftime('%b %d %Y'),
                                name='Moving average',
                                line=dict(color="#F58426")
))

fig.update_layout(
    showlegend=False,
    plot_bgcolor='#cccccc',
    width=700,
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
        ticktext=date_range.strftime("%b '%y").tolist(),
        tickvals=date_range,
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

chart_studio.plotly.plot(fig, filename='Miles per gallon over time', auto_open=False)


# %%
# - mpg vs. miles driven scatter plot

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
    width=700,
    height=700,
    annotations=[
        dict(
            x=0.5,
            y=1.04,
            showarrow=False,
            text="On average, I get " + (round(df_i['MPG'].iloc[-1], 2)).astype(str) + " miles per gallon",
            xref="paper",
            yref="paper",
            font=dict(
                color="black",
                size=12
            )
        )]
)

if show_all:
    fig.show()

chart_studio.plotly.plot(fig, filename='Miles per gallon vs. miles driven', auto_open=False)


# %%
# - $ per mile vs. miles scatter plot

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
    width=700,
    height=700,
    annotations=[
        dict(
            x=0.5,
            y=1.04,
            showarrow=False,
            text="On average, it costs $" + (round(df_i['Cost to go one mile (in cents)'].iloc[-1]/100, 3)).astype(str) + " to drive one mile",
            xref="paper",
            yref="paper",
            font=dict(
                color="black",
                size=12
            )
        )]
)

if show_all:
    fig.show()


chart_studio.plotly.plot(fig, filename='Cost per mile vs. miles driven', auto_open=False)


#%%
alt_greys = ['#cccccc', '#e4e4e4'] * len(df_i)
fig = go.Figure(data=[go.Table(
    header=dict(values=['Time period', 'Miles', 'Dollars', 'Gallons', 'MPG', 'Avg gallon cost',
       'Cost to go one mile'],
                fill_color='#5C7DAA',
                font_color='white',
                align='left'),
    cells=dict(values=[df_i['Time period'], 
                        df_i['Miles'].apply(lambda x: "{:,}".format(x)),
                        df_i['Dollars'].apply(lambda x: "${:,.2f}".format(x)), 
                        df_i['Gallons'].apply(lambda x: "{:,.2f}".format(x)), 
                        round(df_i['MPG'], 2),
                        df_i['Avg gallon cost'].apply(lambda x: '$' + str(x) + '0' if len(str(x)) < 4 else '$' + str(x)),
                        '$' + (round(df_i['Cost to go one mile (in cents)']/100, 2)).astype(str).apply(lambda x: str(x) + '0' if len(str(x)) < 4 else str(x))],
                fill_color=[alt_greys[:len(df_i)]]*3,
                font_color='black',
                align='left'))])

fig.update_layout(
    title=dict(
        text='Gas Insights',
        font=dict(
            size=24,
            color='#000000'
        ),
        x=.5
    ),
    width=700,
    height=500
)

if show_all:
    fig.show()

chart_studio.plotly.plot(fig, filename='Gas insights', auto_open=False)

# %%
# todo Predict mpg based on miles driven and date


# %%
# todo High/low temp over a year with mpg

#%%
def vis_creator():
    