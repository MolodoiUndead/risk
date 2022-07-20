import pandas as pd
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dash_table as dt
import dash_pivottable
import datetime
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

CONTENT_STYLE = {
    "margin-left": "11rem",
    "margin-right": "0rem",
    "padding": "1rem 0rem",
}

df = pd.DataFrame(np.array([['Risk1', 19, 1.3, 2.4, 'circle'],
                            ['Risk1', 20, 1.9, 2.6, 'circle'],
                            ['Risk1', 21, 1.0, 1.5, 'circle'],
                            ['Risk1', 22, 1.2, 1.9, 'circle'],
                            ['Risk2', 19, 2.8, 1.1, 'triangle-up'],
                            ['Risk2', 20, 2.8, 0.5, 'triangle-up'],
                            ['Risk2', 21, 2.7, 0.7, 'triangle-up'],
                            ['Risk2', 22, 2.2, 0.3, 'triangle-up'],
                            ['Risk3', 19, 4.4, 4.9, 'square'],
                            ['Risk3', 20, 4.0, 4.4, 'square'],
                            ['Risk3', 21, 3.5, 4.0, 'square'],
                            ['Risk3', 22, 3.1, 3.2, 'square']]),
                  columns=['Название', 'Дата', 'Вероятность','Последствия','Фигура'])

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

content = html.Div(id="page-content",
                   children=[dcc.Graph(id='x'),
                             dcc.Slider(int(df['Дата'].sort_values().unique()[0]),
                                        int(df['Дата'].sort_values().unique()[len(df['Дата'].sort_values().unique())-1]),
                                        1,
                                        id='s',
                                        value=int(df.loc[0,'Дата'])),
                             dcc.Dropdown(
                                 df['Название'].unique(),
                                 df['Название'].unique(),
                                 id='d',
                                 clearable=True,
                                 multi=True
                             )
                             ],
                   style=CONTENT_STYLE)

app.layout = dbc.Container(
    [
        content
    ]
)

@app.callback(Output('x', 'figure'),
              Input('s', 'value'),
              Input('d', 'value'),
              prevent_initial_call=False)

def update_g(s,d):

    dfs = df.copy()
    d_indexes = list(dfs[dfs['Название'].isin(d)].index)
    dfs = dfs.drop(list(set(set(list(dfs.index))).difference(d_indexes)))
    s_indexes = list(dfs[dfs['Дата'] == str(s)].index)
    p_indexes = list(dfs[dfs['Дата'] == str(int(s)-1)].index)
    dfp = dfs.drop(list(set(set(list(dfs.index))).difference(p_indexes)))
    dfs = dfs.drop(list(set(set(list(dfs.index))).difference(s_indexes)))


    x1=go.Heatmap(
        z=[[1,1,2,2,3,3],
           [1,2,2,3,3,4],
           [2,2,3,3,4,4],
           [2,3,3,4,4,5],
           [3,3,4,4,5,5]],
        x=[0, 1, 2, 3, 4, 5],
        y=[1, 2, 3, 4, 5],
        showscale = False,
        xgap=2,
        ygap=2,
        hovertemplate= 'z<extra></extra>',
        legendgroup="group",
        name="first legend group",
        type='heatmap',
        colorscale=[(0, "green"),(0.5, "yellow"), (1, "red")]
    )

    x = make_subplots(rows=1, cols=1,x_title = 'Последствия реализации события риска')

    def x_x(df,op):
        x_n= go.Scatter(
                    x = df['Последствия'],
                    y = df['Вероятность'],
                    text=df['Название'],
                    textposition="middle center",
                    mode='markers+text',
                    showlegend= False,
                    hovertemplate='Индекс вероятности: %{y} <Br>' +
                                  'Индекс последствий: %{x}<extra></extra>',
                    legendgroup="group2",
                    name="second legend group",
                    marker=dict(
                                size=[50, 50, 50, 50, 50, 50, 50, 50, 50],
                                opacity=op,
                                color=['#ff0000', 'rgba(135, 206, 250, 1)', 2],
                                symbol=df['Фигура'])
                    )
        return x_n

    x2 = x_x(dfs,1)
    x3 = x_x(dfp,0.3)


    x.append_trace(x1, row=1, col=1)
    x.append_trace(x2, row=1, col=1)
    x.append_trace(x3, row=1, col=1)
    x.update_layout(height=800,
                    width=1000,
                    #paper_bgcolor='black',
                    plot_bgcolor='black'
                    )

    x.update_xaxes(
        ticktext=['Пренебрежимо<Br>малые', 'Очень<Br>незначительные', 'Незначительные', 'Заметные', 'Большие', 'Катастрофические'],
        tickvals=[0, 1, 2, 3, 4, 5],
        showgrid=False,
        showline=False,
        zeroline = False

    )
    x.update_yaxes(
        ticktext=['Крайне<Br>маловероятный', 'Маловероятный', 'Возможный', 'Вероятный', 'Крайне<Br>вероятный'],
        tickvals=[1, 2, 3, 4, 5],
        showgrid=False,
        showline=False,
        showticklabels = True,
        zeroline = False

    )
    return x


if __name__ == "__main__":
    app.run_server(debug=True)