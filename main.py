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
import plotly.graph_objects as go

CONTENT_STYLE = {
    "margin-left": "11rem",
    "margin-right": "0rem",
    "padding": "1rem 0rem",
}

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

content = html.Div(id="page-content",
                   children=[dcc.Graph(id='x'),
                             dcc.Slider(-5,5,1,
                                             id='s',
                                             value=2),
                             dcc.Dropdown(
                                 ['риск1','риск2','риск3','риск4','риск5'],
                                 ['риск2','риск4','риск5'],
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
              prevent_initial_call=True)

def update_g(s,d):

    '''x=go.Figure(data=go.Heatmap(
        z=[[1,1,2,2,3,3],
           [1,2,2,3,3,4],
           [2,2,3,3,4,4],
           [2,3,3,4,4,5],
           [3,3,4,4,5,5]],
        x=['100','1000','5000','20000','1000000','1000000000'],
        y=['km','m','vz','v','kv'],
        color_continuous_scale=px.colors.sequential.Cividis_r))'''

    x = px.imshow([[3, 3, 4, 4, 5, 5],
                   [2, 3, 3, 4, 4, 5],
                   [2, 2, 3, 3, 4, 4],
                   [1, 2, 2, 3, 3, 4],
                   [1, 1, 2, 2, 3, 3]],
                    labels=dict(x="Последствия реализации события риска",
                                y="Вероятность реализации события риска",
                                color="Опасность"),
                    x=['Пренебрежимо<Br>малые','Очень<Br>незначительные','Незначительные','Заметные','Большие','Катострофические'],
                    y=['Крайне<Br>вероятный','Вероятный','Возможный','Маловероятный','Крайне<Br>маловероятный']
               )
    x.update_layout(height=850, width=1000)
    return x


if __name__ == "__main__":
    app.run_server(debug=True)