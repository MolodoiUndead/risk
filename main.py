import pandas as pd
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dash_table as dt
import datetime
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff

CONTENT_STYLE = {
    "margin-left": "11rem",
    "margin-right": "0rem",
    "padding": "1rem 0rem",
}

df = pd.DataFrame(np.array([['Risk1', 19, 0.3, 2222,"IT", 'circle',"Indigo"],
                            ['Risk1', 20, 0.9, 1050,"IT", 'circle',"Indigo"],
                            ['Risk1', 21, 0.1, 3460,"IT", 'circle',"Indigo"],
                            ['Risk1', 22, 0.2, 5290,"IT", 'circle',"Indigo"],
                            ['Risk2', 19, 0.8, 123123,"Бухгалтерия", 'triangle-up',"Black"],
                            ['Risk2', 20, 0.8, 231233,"Бухгалтерия", 'triangle-up',"Black"],
                            ['Risk2', 21, 0.7, 124441,"Бухгалтерия", 'triangle-up',"Black"],
                            ['Risk2', 22, 0.2, 14412,"Бухгалтерия", 'triangle-up',"Black"],
                            ['Risk3', 19, 0.4, 12312312,"IT", 'square',"DarkBlue"],
                            ['Risk3', 20, 0.3, 9123414,"IT", 'square',"DarkBlue"],
                            ['Risk3', 21, 0.5, 14234091,"IT", 'square',"DarkBlue"],
                            ['Risk3', 22, 0.1, 100342340,"IT", 'square',"DarkBlue"]]),
                  columns=['Название', 'Дата', 'Вероятность','Последствия',"Тип",'Фигура',"Цвет"])

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
content = html.Div(id = "page-content",
                   children = [dbc.Row([
                       dbc.Col([html.Br(),
                                dcc.Graph(id='x',
                                          config={'displayModeBar': True}),
                                dcc.Graph(id='y',
                                          config={'displayModeBar': False})]),
                       dbc.Col([
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                dbc.Card([  html.Br(),
                                            html.A("Выбор актива",style={'text-align':"center"}),
                                            dcc.Dropdown(
                                             options = df['Название'].unique(),
                                             value = df['Название'].unique(),
                                             id='d',
                                             multi=True,
                                             style={'width': 250, 'margin-left': 5}
                                        ),
                                        html.Br(),
                                        html.A("Выбор подразделения",style={'text-align':"center"}),
                                        dcc.Dropdown(
                                             df['Тип'].unique(),
                                             df['Тип'].unique(),
                                             id='t',
                                             multi=True,
                                             style={'width': 250, 'margin-left': 5}
                                            ),
                                        html.Br(),
                                        html.A("Дата",style={'text-align':"center"}),
                                        dcc.Slider(int(df['Дата'].sort_values().unique()[0]),
                                                  int(df['Дата'].sort_values().unique()[
                                                          len(df['Дата'].sort_values().unique()) - 1]),
                                                  1,
                                                  id='s',
                                                  value=int(df.loc[0, 'Дата']),
                                                  #tooltip={"placement":"right"}
                                                   )
                                ],
                                    style={'width': 270})

                       ],style={'width': 300})]
                   )],
                   #style=CONTENT_STYLE
          )

app.layout = dbc.Container(
    [
        content
    ]
)

@app.callback(Output('x', 'figure'),
              Output('y', 'figure'),
              Output('d', 'options'),
              Input('s', 'value'),
              Input('d', 'value'),
              Input('t', 'value'),
              prevent_initial_call=False)

def update_g(s,d,t):

    dfs = df.copy()
    t_indexes = list(dfs[dfs['Тип'].isin(t)].index)
    dft = dfs.drop(list(set(set(list(dfs.index))).difference(t_indexes)))
    d_indexes = list(dfs[dfs['Название'].isin(d)].index)
    dfd = dft.drop(list(set(set(list(dft.index))).difference(d_indexes)))
    s_indexes = list(dfd[dfd['Дата'] == str(s)].index)
    p_indexes = list(dfd[dfd['Дата'] == str(int(s)-1)].index)
    dfp = dfd.drop(list(set(set(list(dfd.index))).difference(p_indexes)))
    dfs = dfd.drop(list(set(set(list(dfd.index))).difference(s_indexes)))
    #['Крайне<Br>маловероятный', 'Маловероятный', 'Возможный', 'Вероятный', 'Крайне<Br>вероятный']
    table_data = [['</b>Крайне<Br>мало-<Br>вероятный', '</b>0.2'],
                  ['Мало-<Br>вероятный', '0.4'],
                  ['Возможный', '0.6'],
                  ['Вероятный', '0.8'],
                  ['Крайне<Br>вероятный', '1']]
    table_data_2 = [['</b>Пренебрежимо<Br>малые', '</b>Очень<Br>незначительные', '</b>Незначительные', '</b>Заметные', '</b>Большие', '</b>Катастрофические'],
                    ['<100$', '<1000$', '<5000$', '<20000$', '<1000000$', '<1000000000$']]

    x = ff.create_table(table_data,colorscale=['White','White','White'],font_colors=['Black'])
    y = ff.create_table(table_data_2,colorscale=['White','White','White'],font_colors=['Black'])
    y.update_layout(height=100,
                    width=1000,
                    #paper_bgcolor='green',
                    plot_bgcolor='black',
                    )
    y.layout.xaxis.update({
                           'title': 'Последствия реализации события риска',
                           'showticklabels': False
                           })
    y.layout.margin.update({'t': 0, 'b': 0, 'l': 220})
    y.layout.yaxis.update({'showticklabels': False
                           })

    x1=go.Heatmap(
        z=[[1,1,2,2,3,3],
           [1,2,2,3,3,4],
           [2,2,3,3,4,4],
           [2,3,3,4,4,5],
           [3,3,4,4,5,5]],
        y=[0,0.2, 0.4, 0.6, 0.8, 1],
        x=[1, 33.7, 1090, 36008, 1188500, 39264493, 1000000000],
        showscale = False,
        showlegend= False,
        xgap=2,
        ygap=2,
        #hovertemplate= 'z<extra></extra>',
        legendgroup="group",
        hoverinfo='skip',
        name="first legend group",
        #type='heatmap',
        colorscale=[(0, "green"),(0.5, "yellow"), (1, "red")],
        xaxis = 'x2',
        yaxis = 'y2'
    )

    #x = make_subplots(rows=1, cols=1,x_title = 'Последствия реализации события риска')

    def x_x(df,op):
        x_n= go.Scatter(
                    x = df['Последствия'],
                    y = df['Вероятность'],
                    text=df['Название'],
                    textposition="middle center",
                    textfont=dict(color='white'),
                    mode='markers+text',
                    showlegend= False,
                    hovertemplate='Индекс вероятности: %{y} <Br>' +
                                  'Индекс последствий: %{x}<extra></extra>',
                    legendgroup="group2",
                    name="second legend group",
                    marker=dict(
                                size=[50, 50, 50, 50, 50, 50, 50, 50, 50],
                                opacity=op,
                                color=df["Цвет"],
                                symbol=df['Фигура']),
                    xaxis='x2',
                    yaxis='y2'
                    )
        return x_n

    x2 = x_x(dfs,1)
    x3 = x_x(dfp,0.3)

    def c(x,dfs,dfp):
        dfs.reset_index(drop=True, inplace=True)
        dfp.reset_index(drop=True, inplace=True)
        for i in range(len(dfs)):
            x4 = go.Scatter(x=[dfs.loc[i,'Последствия'],dfp.loc[i,'Последствия']],
                            y=[dfs.loc[i,'Вероятность'],dfp.loc[i,'Вероятность']],
                            line=dict(color='white',
                                      width=4,
                                      dash='dash'),
                            xaxis='x2',
                            yaxis='y2',
                            hoverinfo='skip',
                            showlegend=False)
            x.add_trace(x4)
        return x

    x.add_trace(x1)
    if s != int(df['Дата'].sort_values().unique()[0]):
        x = c(x,dfs,dfp)
    x.add_trace(x2)
    x.add_trace(x3)

    x.update_layout(height=700,
                    width=1000,
                    #paper_bgcolor='black',
                    plot_bgcolor='black',
                    )

    '''x.update_xaxes(
        #ticktext=['Пренебрежимо<Br>малые', 'Очень<Br>незначительные', 'Незначительные', 'Заметные', 'Большие', 'Катастрофические'],
        #tickvals=[0, 1, 2, 3, 4, 5],
        showgrid=False,
        showline=False,
        zeroline = False,
        showticklabels = False,

        )
    x.update_yaxes(
        #ticktext=['Крайне<Br>маловероятный', 'Маловероятный', 'Возможный', 'Вероятный', 'Крайне<Br>вероятный'],
        #tickvals=[1, 2, 3, 4, 5],
        showgrid=False,
        showline=False,
        showticklabels = False,
        zeroline = False
        )'''

    x['layout']['xaxis2'] = {}
    x['layout']['yaxis2'] = {}
    x['layout']['xaxis3'] = {}
    x['layout']['yaxis3'] = {}

    # Edit layout for subplots
    x.layout.xaxis.update({'domain': [0, .2],
                           'showticklabels': False
                           })
    x.layout.xaxis2.update({'domain': [0.2, 1.],
                            'showgrid': False,
                            'range': [0, 9],
                            "type": "log",
                            'showline': False,
                            "autorange":False,
                            'zeroline': False,
                            #'showticklabels': False
                            })

    x.layout.yaxis2.update({'anchor': 'x2',
                            'showgrid': False,
                            'showline': False,
                            'zeroline': False,
                            'showticklabels': False
                            })
    x.layout.yaxis.update({'title': 'Вероятность реализации события риска',
                           'showticklabels': False
                           })

    x.layout.margin.update({'t': 50, 'b': 0,'l': 0})
    for i in range(len(x.layout.annotations)):
        x.layout.annotations[i].font.size = 12

    do = dft['Название'].unique()
    return x, y, do


if __name__ == "__main__":
    app.run_server(debug=True)