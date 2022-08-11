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
#import numpy as np
#import ipywidgets
#from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
#import pyautogui
#from selenium import webdriver
import tkinter as tk


root = tk.Tk()
screen_height = root.winfo_screenheight()

#F7FBF5
#0079c2
#8a8d8f

SIDEBAR_STYLE = {
    'position':'fixed',
    "top":0,
    "left":0,
    "bottom":0,
    "width":'17%',
    "padding": "1% 1%",
    "background-color": "PowderBlue",
    'overflowY': 'scroll',
    'text-align':"center"}

R_SIDEBAR_STYLE = {
    'position':'fixed',
    "top":0,
    #"right":0,
    'left':'79.5%',
    "bottom":0,
    "width":'20.5%',
    "padding": "1%",
    "background-color": "PowderBlue",
    'overflowY': 'scroll',
    #'text-align':"center"
}

CONTENT_STYLE = {
    'position':'fixed',
    #"margin-left": 310,
    #"padding": "1rem 1rem",
    "left":'17%',
    'width':'62.5%',
    'height':'100%',
    #'height':'75em',
    #"right":400,
    "background-color":'#f3ecc2',
    "margin-right": "0rem",
    "padding": "1% 1%",
    'overflowY': 'scroll',
}
#style = {'color' : '#f3ecc2'}

v = 0.4
p = 4.5

df = pd.read_excel('risk.xlsx', engine='openpyxl')
df = df.sort_values(by = 'Дата')
df['Дата'] = df['Дата'].dt.round('1D')
#print(type(df['Дата'].dt.year[0]))
'''df = pd.DataFrame(np.array([['Risk1', 19, 0.3, 2222,"IT", 'circle',"Indigo"],
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
                  columns=['Название', 'Дата', 'Вероятность','Последствия',"Тип",'Фигура',"Цвет"])'''

df['Незначительный'] = (df['Вероятность'].astype(float) < v) & (df['Последствия'].astype(float) < 10**p)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True
                )
g_v = df['Название'].unique()
g_df = df.copy()
sidebar = html.Div(id = "sidebar",
                   children =[
                            dbc.Card([html.H5('Первичная сортировка',style={'text-align':"center"}),
                                html.A("Выбор актива:",style={'text-align':"center"}),
                                dcc.Dropdown(
                                 options = df['Название'].unique(),
                                 value = df['Название'].unique(),
                                 id='d',
                                 multi=True,
                                 style={'margin-left': '2.5%', 'width': '95%','height':'50%',#'overflowY': 'scroll'
                                        }
                            ),
                            html.Br(),
                            html.A("Выбор подразделения:",style={'text-align':"center"}),
                            dcc.Dropdown(
                                 df['Тип'].unique(),
                                 df['Тип'].unique(),
                                 id='t',
                                 multi=True,
                                 style={'margin-left': '2.5%', 'width': '95%'}
                                ),
                            html.Br(),
                            dcc.Checklist([' Незначительные риски',' Показывать историю'],
                                          [' Незначительные риски',' Показывать историю'],
                                          id='o',
                                          style={'margin-left': '2.5%', 'width': '95%','margin-bottom':'5%'}
                                          )]),
                            html.Br(),
                            dbc.Card([html.H5('Ручная сортировка',style={'text-align':"center"}),
                            html.A("Отслеживать активы:",style={'text-align':"center"}),
                            dcc.Dropdown(
                                 options=[],
                                 value=[],
                                 id='r',
                                 multi=True,
                                 style={'margin-left': '2.5%', 'width': '95%'}
                                ),
                             html.Br(),
                             html.Button('Применить', id='button-example-1',style={'margin-left': '5%', 'width': '90%'}
                                        ),
                             html.Br(),
                             html.Button('Сбросить', id='button-example-2',style={'margin-left': '5%', 'width': '90%','margin-bottom':'5%'}
                                                                                  )]),
                             html.Br(),
                             html.Div(id='hidden-div', style={'display':'none'}),
                             html.Div(id='hidden-div-1', style={'display':'none'}),

                             dbc.Card([html.H5('Настройка уровня значимости',style={'text-align':"center"}),
                             html.A("Шкала вероятности:",style={'text-align':"center"}),
                             dcc.RangeSlider(0,1,
                                   value=[v],
                                   id='v',
                                   tooltip={"placement": "bottom", "always_visible": True},
                                   included = True,
                                    marks = {
                                    0: {'label': '0', 'style': {'color': '#77b0b1'}},
                                    0.2: {'label': '0.2'},
                                    0.4: {'label': '0.4'},
                                    0.6: {'label': '0.6'},
                                    0.8: {'label': '0.8'},
                                    1: {'label': '1', 'style': {'color': '#f50'}}},
                                   # value=int(df.loc[0, 'Дата']),
                                   # tooltip={"placement":"right"}
                                   ),
                             html.Br(),
                             html.A("Шкала последствий (степень 10):", style={'text-align': "center"}),
                             dcc.RangeSlider(1,9,
                                           #marks={i: '{}'.format(10 ** i) for i in [0,1.5,3,4.5,6,7.5,9]},
                                           value=[p],
                                           id='p',
                                           tooltip={"placement": "bottom", "always_visible": True},
                                           included = True,
                                           marks = {
                                            1: {'label': '1', 'style': {'color': '#77b0b1'}},
                                            3: {'label': '3'},
                                            6: {'label': '6'},
                                            9: {'label': '9', 'style': {'color': '#f50'}}}
                                           # value=int(df.loc[0, 'Дата']),
                                           # tooltip={"placement":"right"}
                                           )]),
                             html.Div(id='hidden-div-2', style={'display':'none'})],
                                style=SIDEBAR_STYLE,
                               #style={'width': 300,'text-align':"center"}
                   )

rsidebar = html.Div([dbc.Card([html.H5('Выбор временного промежутка',style={'text-align':"center"}),
                    dbc.Row([ dbc.Col([
                    html.A("Год",style={'text-align':"center"}),
                    dcc.RangeSlider(int(df['Дата'].dt.year.min()),
                              int(df['Дата'].dt.year.max()),
                              1,
                              value = [int(df['Дата'].dt.year.min()),
                              int(df['Дата'].dt.year.max())],
                              id='s',
                                    vertical= True,
                                verticalHeight =screen_height*0.5,
                              #value=int(df.loc[0, 'Дата']),
                              #tooltip={"placement":"right"}
                                marks={i: '{}'.format(str(i)) for i in range(int(df['Дата'].dt.year.min()),int(df['Дата'].dt.year.max())+1)}
                               )],style={'margin-left':'10%'}),
                    dbc.Col([html.A("Месяц",style={'text-align':"center"}),
                       dcc.RangeSlider(1,12,1,
                                       value=[1,12],
                                       id='j',
                                        vertical= True,
                                        verticalHeight =screen_height*0.5,
                                        marks={i: '{}'.format(str(i)) for i in range(13)}
                                       # value=int(df.loc[0, 'Дата']),
                                       # tooltip={"placement":"right"}
                                       )],style={'margin-left':'7%'}),
                    dbc.Col([html.A("День",style={'text-align':"center"}),
                       dcc.RangeSlider(1,31,1,
                                       value=[1,31],
                                       id='g',
                                        vertical= True,
                                        verticalHeight =screen_height*0.5,
                                        marks={i: '{}'.format(str(i)) for i in range(32)}
                                       # value=int(df.loc[0, 'Дата']),
                                       # tooltip={"placement":"right"}
                                       )],style={'margin-left':'7%'})])])],
                        style=R_SIDEBAR_STYLE)
content = html.Div(id = "page-content",
                   children = [dbc.Row([
                                dbc.Col([
                                html.H2("Система контроля рисков",style={'height':'3%','text-align':"center"}),
                                dcc.Graph(id='x',
                                          config={'displayModeBar': False,'showAxisDragHandles':False,'showAxisRangeEntryBoxes':False}),
                                dcc.Graph(id='y',
                                          config={'displayModeBar': False,'showAxisDragHandles':False,'showAxisRangeEntryBoxes':False})],
                           #width={"size": 8,"order": "last", "offset": 1 },
                           #lg = 8
                                )
                   ],
                       style={'width': '100%','text-align':"center"},
                       justify="start",
                       #className="g-0"

                   )],
                   style=CONTENT_STYLE
          )

app.layout = dbc.Container(
    [
        sidebar,
        rsidebar,
        content,
    ], style ={"background-color": '#f3ecc2'},
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
    o.append(str(click['points'][0]['text']).split('<')[:-1][0])
    v.append(str(click['points'][0]['text']).split('<')[:-1][0])
    return list(set(o)), list(set(v)),


@app.callback(Output('x', 'figure'),
              Output('y', 'figure'),
              Output('d', 'options'),
              Input('s', 'value'),
              Input('j', 'value'),
              Input('g', 'value'),
              Input('d', 'value'),
              Input('t', 'value'),
              Input('o', 'value'),
              State('r','value'),
              Input('v', 'value'),
              Input('p','value'),
              Input('button-example-1', 'n_clicks'),
              Input('button-example-2', 'n_clicks'),
              prevent_initial_call=False)

def update_g(s,j,g,d,t,o,l,u,k,n,n1):
    global g_v
    global p
    global v
    global df
    #dfs = df.copy()

    #Нанесение точек на график
    def x_x(df,op):
        x_n= go.Scatter(
                    x = df['Последствия'],
                    y = df['Вероятность'],
                    text = df['Название']+'<Br>'+df['Дата'].astype(str),
                    textposition="middle center",
                    textfont=dict(color='RebeccaPurple'),
                    #mode='markers+text',
                    mode='markers',
                    showlegend= False,
                    hovertemplate='Индекс вероятности: %{y} <Br>' +
                                  'Индекс последствий: %{x}<Br>'+
                                  '%{text}<extra></extra>',
                                  #'Дата: {}.{}.{}<extra></extra>'.format(d),
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

    def x_x2(df,op):
        x_n= go.Scatter(
                    x = [df['Последствия']],
                    y = [df['Вероятность']],
                    text = [df['Название']+'<Br>'+str(df['Дата'].year)+'-'+str(df['Дата'].month)+'-'+str(df['Дата'].day)],
                    textposition="middle center",
                    textfont=dict(color='purple'),
                    mode='markers+text',
                    #mode='markers',
                    showlegend= False,
                    hovertemplate='Индекс вероятности: %{y} <Br>' +
                                  'Индекс последствий: %{x}<Br>'+
                                  '%{text}<extra></extra>',
                                  #'Дата: {}.{}.{}<extra></extra>'.format(d),
                    legendgroup="group2",
                    name="second legend group",
                    marker=dict(line=dict(width=2,color='white'),
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


    def at(x, s, j, g, d, t, o, df):
        dfs = df.copy()
        t_indexes = list(dfs[dfs['Тип'].isin(t)].index)
        dft = dfs.drop(list(set(set(list(dfs.index))).difference(t_indexes)))
        d_indexes = list(dfs[dfs['Название'].isin(d)].index)
        dfd = dft.drop(list(set(set(list(dft.index))).difference(d_indexes)))
        s_indexes = list(dfd[(dfd['Дата'].dt.year >= int(s[0])) & (dfd['Дата'].dt.year <= int(s[1]))].index)
        dfj = dfd.drop(list(set(set(list(dfd.index))).difference(s_indexes)))
        j_indexes = list(dfj[(dfj['Дата'].dt.month >= int(j[0])) & (dfj['Дата'].dt.month <= int(j[1]))].index)
        dfg = dfj.drop(list(set(set(list(dfj.index))).difference(j_indexes)))
        g_indexes = list(dfg[(dfg['Дата'].dt.day >= int(g[0])) & (dfg['Дата'].dt.day <= int(g[1]))].index)
        dfs = dfg.drop(list(set(set(list(dfg.index))).difference(g_indexes)))
        for h in dfs['Название'].unique():
            dfx = dfs.copy()
            d_indexes = list(dfx[dfx['Название'] == h].index)
            dfd = dfx.drop(list(set(set(list(dfx.index))).difference(d_indexes)))
            dfd = dfd.reset_index(drop=True)
            if o == [' Показывать историю']:
                if (dfd.loc[len(dfd) - 1]['Незначительный'] == False):
                    x = c(x, dfd)
                    x.add_traces(x_x(dfd.loc[:len(dfd)-2],0.5))
                    x.add_traces(x_x2(dfd.loc[len(dfd)-1], 1))
            elif o == [' Незначительные риски']:
                x.add_traces(x_x2(dfd.loc[len(dfd) - 1], 1))
            elif o == []:
                if (dfd.loc[len(dfd) - 1]['Незначительный'] == False):
                    x.add_traces(x_x2(dfd.loc[len(dfd) - 1], 1))
            else:
                x = c(x, dfd)
                x.add_traces(x_x(dfd.loc[:len(dfd) - 2], 0.5))
                x.add_traces(x_x2(dfd.loc[len(dfd) - 1], 1))

        return x , dfd

    table_data = [
                    ['</b>Крайне<Br>вероятный', '</b><1'],
                    ['Вероятный', '<0.8'],
                    ['Возможный', '<0.6'],
                    ['Мало-<Br>вероятный', '<0.4'],
                    ['Крайне<Br>мало-<Br>вероятный', '</b><0.2']]
    table_data_2 = [['</b>Пренебрежимо<Br>малые', '</b>Очень<Br>незначительные', '</b>Незначительные', '</b>Заметные', '</b>Большие', '</b>Катастрофические'],
                    ['<100$', '<1000$', '<32000$', '<1000000$', '<32000000$', '<1000000000$']]

    x = ff.create_table(table_data,colorscale=['White','White','White'],font_colors=['Black'])
    y = ff.create_table(table_data_2,colorscale=['White','White','White'],font_colors=['Black'])


    z =go.Scatter(#x= np.sqrt((-2*zy) +0.8),
                  #y=zy,
                  x= [0,10**p,10**p],
                  y= [v,v,0],
                  line =dict(color='FireBrick',width=5),
                  xaxis='x2',
                  yaxis='y2',
                  showlegend= False,
                  hoverinfo='skip')

    y.update_layout(height=screen_height*0.15,
                    #width=1050,
                    paper_bgcolor='#f3ecc2',
                    #paper_bgcolor='green',
                    plot_bgcolor='black',
                    )

    y.layout.xaxis.update({'domain': [.2, 1],
                           'title': 'Последствия реализации события риска',
                           #'showgrid': False,
                           #'showline': False,
                           #"autorange": False,
                           'zeroline': False,
                           'showticklabels': False
                           })

    y.layout.margin.update({'t': 0, 'b': 40, 'l': 25,'r':25})
    y.layout.yaxis.update({#'showgrid': False,
                            #'showline': False,
                            #"autorange": False,
                            'zeroline': False,
                            'showticklabels': False,
                            'title': '',
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
        colorscale=[(0, "#14b1ab"),(0.5, "#f9d56e"), (1, "#e8505b")],
        xaxis = 'x2',
        yaxis = 'y2'
    )

    x.add_trace(x1)
    x, dfd = at(x,s,j,g,d,t,o,df)
    x.add_trace(z)

    '''x.add_annotation(text="Absolutely-positioned annotation",
                       xref="x2", yref="y2",
                       x=3, y=0.3, showarrow=True,
                     )'''

    x.update_layout(height=screen_height*0.65,
                    #width=1050,
                    paper_bgcolor='#f3ecc2',
                    plot_bgcolor='black',
                    #clickmode = 'event+select'
                    )
    if o == [] or o == [' Показывать историю']:
        x.add_shape(type="rect",
                      xref="x2", yref="y2",
                      fillcolor="PaleTurquoise",
                      x0=0, y0=0, x1=10**p, y1=v,
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

    x.layout.margin.update({'t': 5, 'b': 0,'l': 0,'r':25})
    for i in range(len(x.layout.annotations)):
        x.layout.annotations[i].font.size = 12

    t_indexes = list(df[df['Тип'].isin(t)].index)
    dft = df.drop(list(set(set(list(df.index))).difference(t_indexes)))

    do = dft['Название'].unique()

    if l != []:
        do = [*do, *l]
    return x, y, do

@app.callback(Output('hidden-div-2','children'),
              Input('v', 'value'),
              Input('p','value'),
              prevent_initial_call=True)
def update_ax(a,b):
    global p
    global v
    global df

    v = a[0]
    p = b[0]

    df['Незначительный'] = (df['Вероятность'].astype(float) < v) & (df['Последствия'].astype(float) < 10 ** p)
    g_df['Незначительный'] = (df['Вероятность'].astype(float) < v) & (df['Последствия'].astype(float) < 10 ** p)
    return ''

if __name__ == "__main__":
    app.run_server(debug=True)