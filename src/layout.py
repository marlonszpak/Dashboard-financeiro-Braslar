from dash import Dash, html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from src.styles.colors import *
from src.components.stat_cards import *
import pandas as pd
# import dash_core_components as dcc
from datetime import date
import ipywidgets as widgets

tab_style = {
    'idle':{
        'borderRadius': '10px',
        'padding': '0px',
        'marginInline': '5px',
        'display':'flex',
        'alignItems':'center',
        'justifyContent':'center',
        'fontWeight': 'bold',
        'backgroundColor': principal_color,
        'border':'none'
    },
    'active':{
        'borderRadius': '10px',
        'padding': '0px',
        'marginInline': '5px',
        'display':'flex',
        'alignItems':'center',
        'justifyContent':'center',
        'fontWeight': 'bold',
        'border':'none',
        'textDecoration': 'underline',
        'backgroundColor': principal_color
    }
}

def create_layout(app: Dash, source: pd.DataFrame, stat_cards: Stat_Cards)-> html.Div:
    return html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dcc.Tabs(id='graph-tabs', value='overview', children=[
                ], style={'width':'600px','height':'10px'})
            ,width=6),
        ]),
        dbc.Row([       
            dbc.Col(stat_cards.generate_stats_card("Pago", '0',"./assets/pagos.png")),
            dbc.Col(stat_cards.generate_stats_card("Recebido",'0',"./assets/recebidos.png")),
            dbc.Col(stat_cards.generate_stats_card("Pagar",'0',"./assets/saldo-atual.png")),
            dbc.Col(stat_cards.generate_stats_card("Receber",'0',"./assets/total-atrasado.png")),
            dbc.Col(stat_cards.generate_stats_card("Saldo Atual",'0',"./assets/saldo-final.png"))
        ],id="stats_card_values", style={'maxWidth': '100vw'}),
        html.Div([
            dcc.DatePickerRange(
                id='my-date-picker-range',
                display_format='DD/MM/YYYY',
                start_date_placeholder_text='DD/MM/YYYY',
                end_date_placeholder_text='DD/MM/YYYY',
                min_date_allowed=date(2022, 1, 1),
                max_date_allowed=date(2030, 12, 31),
                initial_visible_month=date.today(),
                start_date=date.today(),
                end_date=date.today(),
                style={'height': '50px'}
            ),
            dcc.Input(id='input-on-submit-text', type='number', placeholder='Digite o saldo inicial', style={'border': '1px solid #007bff', 'border-radius': '5px', 'width': '250px', 'height': '48px'}),
            dcc.RadioItems(id='radio-button',
            options=[{'label': 'Previsto', 'value': '1'},
                     {'label': 'Efetivo', 'value': '2'},],value='1', style={'color': 'white'}),
            html.Button('Calcular', id='submit-button', n_clicks=0, style={'background-color': '#007bff', 'color': 'white', 'height': '48px', 'border': 'none', 'border-radius': '5px','cursor': 'pointer', 'width': '250px'})
        ],style={'display': 'flex', 'width': '80vw', 'height': '7vh','margin': '10px 0px', 'gap': '10px'}),
        # dbc.Row([
        #     dcc.DatePickerRange(
        #         id='my-date-picker-range',
        #         min_date_allowed=date(2022, 1, 1),
        #         max_date_allowed=date(2030, 12, 31),
        #         initial_visible_month=date.today(),
        #         start_date=date.today(),
        #         end_date=date.today()
        #     )
        # ]),
        dbc.Row([
            dcc.Loading([
                html.Div(id='tabs-content')
            ],type='default',color=principal_color)
        ])
    ], style={'padding': '0px'})
],style={'backgroundColor': 'black', 'minHeight': '100vh'})
