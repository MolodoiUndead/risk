import pandas as pd
import dash
#import math as m
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
#from dash import dash_table as dt
#import datetime
#import plotly.express as px
import numpy as np
#import ipywidgets
#from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
#import pyautogui
#from selenium import webdriver


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

df['Незначительный'] = (df['Вероятность'].astype(float) < 0.4) & (df['Последствия'].astype(float) < 32000)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

g_v = df['Название'].unique()
g_df = df.copy()
content = html.Div(id = "page-content",
                   children = [dbc.Row([
                       dbc.Col([html.Br(),
                                dcc.Graph(id='x',
                                          config={'displayModeBar': False}),
                                dcc.Graph(id='y',
                                          config={'displayModeBar': False})]),
                       dbc.Col([
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                dbc.Card([ html.H4('Первичная сортировка',style={'text-align':"center"}),
                                            html.Br(),
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
                                        dcc.Checklist([' Незначительные риски'],
                                                      [' Незначительные риски'],
                                                      id='o',
                                                      style={'width': 250, 'margin-left': 10, 'font-size': 20}),
                                        html.Br(),
                                        html.A("Дата",style={'text-align':"center"}),
                                        dcc.RangeSlider(int(df['Дата'].sort_values().unique()[0]),
                                                  int(df['Дата'].sort_values().unique()[
                                                          len(df['Дата'].sort_values().unique()) - 1]),
                                                  1,
                                                  value = [int(df['Дата'].sort_values().unique()[0]),
                                                  int(df['Дата'].sort_values().unique()[
                                                          len(df['Дата'].sort_values().unique()) - 1])],
                                                  id='s',
                                                  #value=int(df.loc[0, 'Дата']),
                                                  #tooltip={"placement":"right"}
                                                   ),
                                        html.Br(),

                                ],
                                    style={'width': 270}),
                       html.Br(),
                       dbc.Card([html.H4('Ручная сортировка',style={'text-align':"center"}),
                                 html.Br(),
                                 html.A("Отслеживать активы:",style={'text-align':"center"}),
                                 dcc.Dropdown(
                                             options=[],
                                             value=[],
                                             id='r',
                                             multi=True,
                                             style={'width': 250, 'margin-left': 5}
                                            ),
                                 html.Br(),
                                 html.Button('Применить', id='button-example-1',style={'width': 200,'text-align':"center", 'margin-left': 35}),
                                 html.Br(),
                                 html.Button('Сбросить', id='button-example-2',style={'width': 200,'text-align':"center", 'margin-left': 35}),
                                 html.Br(),
                                 html.Div(id='hidden-div', style={'display':'none'}),
                                 html.Div(id='hidden-div-1', style={'display':'none'}),
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

@app.callback(Output('hidden-div', 'children'),
              Input('button-example-1', 'n_clicks'),
              State('r','value'),
              prevent_initial_call=True)
def update_set_button(n,v):

    global df
    global g_df
    global g_v
    if v != []:
        n_indexes = list(g_df[g_df['Название'].isin(v)].index)
        df = g_df.drop(list(set(set(list(g_df.index))).difference(n_indexes)))
    g_v = v
    return ' '

@app.callback(Output('hidden-div-1', 'children'),
              Input('button-example-2', 'n_clicks'),
              prevent_initial_call=True)
def update_reset_button(n):
    global df
    global g_df
    global g_v
    df = g_df
    g_v = g_df['Название'].unique()
    '''pyautogui.hotkey('f5')
    try:
        driver = webdriver.Safari()
        driver.get("http://127.0.0.1:8050/")
        driver.refresh()
    except:
        return ' '''

    return ' '

@app.callback(Output('d', 'value'),
              Input('button-example-2', 'n_clicks'),
              Input('button-example-1', 'n_clicks'),
              State('t', 'value'),
              State('r', 'value'),
              prevent_initial_call=True)
def update_reset_button_2(n,n1,t,v):
    global g_v

    t_indexes = list(df[df['Тип'].isin(t)].index)
    dft = g_df.drop(list(set(set(list(g_df.index))).difference(t_indexes)))
    do = dft['Название'].unique()

    if v != []:
        return g_v
    return do

@app.callback(Output('r','options'),
              Output('r','value'),
              Input('x', 'clickData'),
              Input('r','options'),
              State('r','value'),
              #Input('button-example-1', 'n_clicks'),
              prevent_initial_call=True)
def update_clicks(click,o,v):
    o.append(str(click['points'][0]['text']))
    v.append(str(click['points'][0]['text']))
    return list(set(o)), list(set(v)),


@app.callback(Output('x', 'figure'),
              Output('y', 'figure'),
              Output('d', 'options'),
              Input('s', 'value'),
              Input('d', 'value'),
              Input('t', 'value'),
              Input('o', 'value'),
              State('r','value'),
              Input('button-example-1', 'n_clicks'),
              Input('button-example-2', 'n_clicks'),
              prevent_initial_call=False)

def update_g(s,d,t,o,v,n,n1):
    global g_v
    dfs = df.copy()

    #Нанесение точек на график
    def x_x(df,op):
        d = df.reset_index(drop=True)['Дата'].get(0)
        x_n= go.Scatter(
                    x = df['Последствия'],
                    y = df['Вероятность'],
                    text = df['Название'],
                    textposition="middle center",
                    textfont=dict(color='white'),
                    mode='markers+text',
                    showlegend= False,
                    hovertemplate='Индекс вероятности: %{y} <Br>' +
                                  'Индекс последствий: %{x}<Br>'+
                                  'Год: {}<extra></extra>'.format(d),
                    legendgroup="group2",
                    name="second legend group",
                    marker=dict(
                                size=[55] * len(df),
                                opacity=op,
                                color=df["Цвет"],
                                symbol=df['Фигура']),
                    xaxis='x2',
                    yaxis='y2'
                    )
        return x_n

    def c(x,df):
        df.reset_index(drop=True, inplace=True)
        for i in range(len(df)):
            x4 = go.Scatter(x=df['Последствия'],
                            y=df['Вероятность'],
                            line=dict(color='white',
                                      width=3,
                                      dash='dash'),
                            xaxis='x2',
                            yaxis='y2',
                            hoverinfo='skip',
                            showlegend=False)
            x.add_trace(x4)
        return x

    def at(x,s,d,t,o,df):
        xe = []
        if o == []:
            mv_indexes = list(df[df['Незначительный'] == False].index)
            dfs = df.drop(list(set(set(list(df.index))).difference(mv_indexes)))
            ov_indexes = list(df[df['Незначительный'] == True].index)
            dfo = df.drop(list(set(set(list(df.index))).difference(ov_indexes)))
            o_indexes = list(dfo[dfo['Дата'] == str(s[1])].index)
            dfk = dfo.drop(list(set(set(list(dfo.index))).difference(o_indexes)))
            f_indexes = list(df[df['Название'].isin(dfk['Название'].unique())].index)
            df = df.drop(list(set(set(list(df.index))).intersection(f_indexes)))
        for i in range(s[0],s[1]+1,1):
            dfs = df.copy()
            if i == s[1]:
                op = 1
            else:
                op = 0.5
            t_indexes = list(dfs[dfs['Тип'].isin(t)].index)
            dft = dfs.drop(list(set(set(list(dfs.index))).difference(t_indexes)))
            d_indexes = list(dfs[dfs['Название'].isin(d)].index)
            dfd = dft.drop(list(set(set(list(dft.index))).difference(d_indexes)))
            s_indexes = list(dfd[dfd['Дата'] == str(i)].index)
            dfs = dfd.drop(list(set(set(list(dfd.index))).difference(s_indexes)))
            x2 = x_x(dfs,op)
            xe.append(x2)
            if i == s[0]:
                dfz = dfs.copy()
            else:
                dfz = pd.concat([dfs,dfz])

        for j in dfz['Название'].unique():
            dfx = dfz.copy()
            d_indexes = list(dfx[dfx['Название'] == j].index)
            dfd = dfx.drop(list(set(set(list(dfx.index))).difference(d_indexes)))
            x = c(x, dfd)
        x.add_traces(xe)
        return x


    '''t_indexes = list(dfs[dfs['Тип'].isin(t)].index)
    dft = dfs.drop(list(set(set(list(dfs.index))).difference(t_indexes)))
    d_indexes = list(dfs[dfs['Название'].isin(d)].index)
    dfd = dft.drop(list(set(set(list(dft.index))).difference(d_indexes)))
    s_indexes = list(dfd[dfd['Дата'] == str(s[1])].index)
    p_indexes = list(dfd[dfd['Дата'] == str(int(s[1])-1)].index)

    dfp = dfd.drop(list(set(set(list(dfd.index))).difference(p_indexes)))
    dfs = dfd.drop(list(set(set(list(dfd.index))).difference(s_indexes)))

    if o == []:
        mv_indexes = list(dfs[dfs['Незначительный'] == False].index)
        mp_indexes = list(dfs[dfs['Незначительный'] == True].index)
        mp_indexes = [*map(lambda x: x - 1, mp_indexes)]
        dfs = dfs.drop(list(set(set(list(dfs.index))).difference(mv_indexes)))
        dfp = dfp.drop(list(set(set(list(dfp.index))).intersection(mp_indexes)))'''

    table_data = [
                    ['</b>Крайне<Br>вероятный', '</b>1'],
                    ['Вероятный', '0.8'],
                    ['Возможный', '0.6'],
                    ['Мало-<Br>вероятный', '0.4'],
                    ['Крайне<Br>мало-<Br>вероятный', '</b>0.2']]
    table_data_2 = [['</b>Пренебрежимо<Br>малые', '</b>Очень<Br>незначительные', '</b>Незначительные', '</b>Заметные', '</b>Большие', '</b>Катастрофические'],
                    ['<100$', '<1000$', '<32000$', '<1000000$', '<32000000$', '<1000000000$']]

    x = ff.create_table(table_data,colorscale=['White','White','White'],font_colors=['Black'])
    y = ff.create_table(table_data_2,colorscale=['White','White','White'],font_colors=['Black'])


    z =go.Scatter(#x= np.sqrt((-2*zy) +0.8),
                  #y=zy,
                  x= [0,32000,32000],
                  y= [0.4,0.4,0],
                  line =dict(color='FireBrick',width=5),
                  xaxis='x2',
                  yaxis='y2',
                  showlegend= False,
                  hoverinfo='skip')

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
        x=[1, 32, 1000, 32000, 1000000, 32000000, 1000000000],
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


    #x2 = x_x(dfs,1)
    #x3 = x_x(dfp,0.3)

    x.add_trace(x1)
    #if int(s[1]) != int(df['Дата'].sort_values().unique()[0]): x = c(x,dfs,dfp)
    #x.add_trace(x2)
    #x.add_trace(x3)
    x = at(x,s,d,t,o,df)
    x.add_trace(z)


    x.update_layout(height=700,
                    width=1000,
                    #paper_bgcolor='black',
                    plot_bgcolor='black',
                    #clickmode = 'event+select'
                    )
    if o == []:
        x.add_shape(type="rect",
                      xref="x2", yref="y2",
                      fillcolor="PaleTurquoise",
                      x0=0, y0=0, x1=32000, y1=0.4,
                      line_color="LightSeaGreen",
                      opacity=0.5)

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
                            'showticklabels': False
                            })

    x.layout.yaxis2.update({'anchor': 'x2',
                            'range': [0, 1],
                            'showgrid': False,
                            'showline': False,
                            "autorange": False,
                            'zeroline': False,
                            'showticklabels': False
                            })
    x.layout.yaxis.update({'title': 'Вероятность реализации события риска',
                           'showticklabels': False
                           })

    x.layout.margin.update({'t': 50, 'b': 0,'l': 0})
    for i in range(len(x.layout.annotations)):
        x.layout.annotations[i].font.size = 12

    t_indexes = list(df[df['Тип'].isin(t)].index)
    dft = df.drop(list(set(set(list(df.index))).difference(t_indexes)))

    do = dft['Название'].unique()

    if v != []:
        do = [*do, *v]
    return x, y, do




if __name__ == "__main__":
    app.run_server(debug=True)