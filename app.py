import threading
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
# import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel

from src.components.dash1 import *
from src.components.dash2 import generate_visualizations as generate_visualizations2
from src.components.dash3 import generate_visualizations as generate_visualizations3
from src.components.dash4 import generate_visualizations as generate_visualizations4

from flask import jsonify, make_response, request, Flask

import ujson

import json

from src.components.stat_cards import *

from src.layout import create_layout

# from src.data.source import get_data_base
# db_data = get_data_base()

from src.data.read_json import get_json_data

json_data = get_json_data()

server = Flask(__name__)

# Initialize the app
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP], title='Dashboard caixa Braslar')
# server = app.server

stat_cards = Stat_Cards(json_data)
dash1 = Dash1(json_data)

app.layout = create_layout(app, json_data, stat_cards)

def save_to_file(content, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            ujson.dump(content, f, ensure_ascii=False, indent=4)
        print(f"Gravação no arquivo {filename} foi bem-sucedida.")
        json_data = get_json_data()
        dash1.update_df(json_data)
    except Exception as e:
        print(f"Erro ao gravar no arquivo {filename}: {e}")

@server.route('/receber', methods=['POST'])
def getDataReceber():
    content = request.json
    threading.Thread(target=save_to_file, args=(content, './data-files/receber.json')).start()
    data = {'message': 'Done', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 201)

@server.route('/pagar', methods=['POST'])
def getDataPagar():
    content = request.json
    threading.Thread(target=save_to_file, args=(content, './data-files/pagar.json')).start()
    data = {'message': 'Done', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 201)

@server.route('/extrato', methods=['POST'])
def getDataExtrato():
    content = request.json
    threading.Thread(target=save_to_file, args=(content, './data-files/extrato.json')).start()
    data = {'message': 'Done', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 201)

@app.callback(
    Output('tabs-content', 'children'),
    # Input('graph-tabs', 'value'),
    Input('submit-button', 'n_clicks'),
    State('input-on-submit-text', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('radio-button', 'value')
)
def update_tab(clicks, text, start_date, end_date, radio_value):
    if clicks > 0 :
        fig1 = dash1.update_opening_balance(text, start_date, end_date, radio_value)
        return html.Div([
            html.Div([
                dcc.Graph(id='graph1', figure=fig1),
            ], style={'width': '100%', 'display': 'inline-block'}),
            ])
    else:
        # if tab == 'overview':
            # fig1, fig2, fig3, fig4 = generate_visualizations1(db_data)
            fig1 = dash1.generate_visualizations(start_date, end_date)
            return html.Div([
            html.Div([
                dcc.Graph(id='graph1', figure=fig1),
            ], style={'width': '100%', 'display': 'inline-block'}),
            # html.Div([
            #     dcc.Graph(id='graph2', figure=fig2),
            # ], style={'width': '100%', 'display': 'inline-block'}),
            # html.Div([
            #     dcc.Graph(id='graph3', figure=fig3),
            # ], style={'width': '100%', 'display': 'inline-block'}),
            # html.Div([
            #     dcc.Graph(id='graph4', figure=fig4),
            # ], style={'width': '50%', 'display': 'inline-block'})
        ])
        # elif tab == 'content_creators':
        #     fig1, fig2, fig3, fig4 = generate_visualizations2(json_data)
        #     return html.Div([
        #     html.Div([
        #         dcc.Graph(id='graph1', figure=fig1),
        #     ], style={'width': '50%', 'display': 'inline-block'}),
        #     html.Div([
        #         dcc.Graph(id='graph2', figure=fig2),
        #     ], style={'width': '50%', 'display': 'inline-block'}),
        #     html.Div([
        #         dcc.Graph(id='graph3', figure=fig3),
        #     ], style={'width': '50%', 'display': 'inline-block'}),
        #     html.Div([
        #         dcc.Graph(id='graph4', figure=fig4),
        #     ], style={'width': '50%', 'display': 'inline-block'})
        # ])
        # elif tab == 'parental':
        #     fig1, fig2 = generate_visualizations3(json_data)
        #     return html.Div([
        #     html.Div([
        #         dcc.Graph(id='graph1', figure=fig1),
        #     ], style={'width': '50%', 'display': 'inline-block'}),
        #     html.Div([
        #         dcc.Graph(id='graph2', figure=fig2),
        #     ], style={'width': '50%', 'display': 'inline-block'}),
        #     ])
        # elif tab == 'year':
        #     fig1, fig2 = generate_visualizations4(json_data)
        #     return html.Div([
        #     html.Div([
        #         dcc.Graph(id='graph1', figure=fig1),
        #     ], style={'width': '50%', 'display': 'inline-block'}),
        #     html.Div([
        #         dcc.Graph(id='graph2', figure=fig2),
        #     ], style={'width': '50%', 'display': 'inline-block'}),
        #     ])
        
@app.callback(
    Output('stats_card_values', 'children'),
    Input('submit-button', 'n_clicks'),
    State('input-on-submit-text', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('radio-button', 'value')
)
def update_stat_cards_values(clicks, text, start_date, end_date, radio_value):
    total_recebido, total_receber, total_pago, total_pagar, saldo_atual = stat_cards.get_constants(clicks, text, start_date, end_date, radio_value)

    return html.Div([
        dbc.Col(stat_cards.generate_stats_card("Pago", total_pago,"./assets/saldo-atual.png")),
        dbc.Col(stat_cards.generate_stats_card("Recebido", total_recebido,"./assets/recebidos.png")),
        dbc.Col(stat_cards.generate_stats_card("Pagar", total_pagar,"./assets/total-atrasado.png")),
        dbc.Col(stat_cards.generate_stats_card("Receber", total_receber,"./assets/pagos.png")),
        dbc.Col(stat_cards.generate_stats_card("Saldo Atual", saldo_atual,"./assets/saldo-final.png"))
    ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '10px'})

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=9082)