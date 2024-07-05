from dash import html
import dash_bootstrap_components as dbc
import numpy as np
from src.styles.colors import *
import pandas as pd
from datetime import date, timedelta

class Stat_Cards:
    def __init__(self, df):
        self.df = df

    def calcular_saldo(self, opening_balance, start_date, end_date, radio_value) -> pd.DataFrame:        
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%Y%m%d')
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%Y%m%d')
        
        self.df['Data'] = pd.to_datetime(self.df['Data'], format='%Y%m%d')
        
        dff = self.df[(self.df.Data >= start_date_string) & (self.df.Data <= end_date_string)]

        saldos = np.array([[start_date_object - timedelta(days=1),opening_balance]])
        if(opening_balance is None):
            saldo_atual = 0
        else:
            saldo_atual = opening_balance

        for index, row in dff.iterrows():
            saldo_atual += (row['Recebido'] - row['Pago'])
            if radio_value == '1':
                saldo_atual += (row['Receber'] - row['Pagar'])
            array_saldo_atual = np.array([[row['Data'], saldo_atual]])
            saldos = np.append(saldos, array_saldo_atual, axis=0)

        dataset = pd.DataFrame(saldos, columns=['Data', 'Saldo'])

        return dataset

    # def generate_stats_card (title, value, image_path, start_date, end_date):
    def generate_stats_card(self, title, value, image_path):
        return html.Div(
            dbc.Card([
                dbc.CardImg(src=image_path, top=True, style={'width': '50px','alignSelf': 'center'}),
                dbc.CardBody([
                    html.P(value, className="card-value", style={'margin': '0px','fontSize': '22px','fontWeight': 'bold'}),
                    html.H4(title, className="card-title", style={'margin': '0px','fontSize': '18px','fontWeight': 'bold'})
                ], style={'textAlign': 'center'}),
            ], style={'paddingBlock':'10px',"backgroundColor": principal_color,'border':'none','borderRadius':'10px'})
        )
    

    
    def get_constants(self, clicks, opening_balance, start_date, end_date, radio_value):
        # df = pd.DataFrame(source)

        saldo = self.calcular_saldo(opening_balance, start_date, end_date, radio_value)

        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%Y%m%d')
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%Y%m%d')

        dff = self.df[(self.df.Data >= start_date_string) & (self.df.Data <= end_date_string)]

        total_recebido = dff["Recebido"].sum()
        total_recebido = f'R$ {total_recebido:_.2f}'

        total_receber = dff["Receber"].sum()
        total_receber = f'R$ {total_receber:_.2f}'
    
        total_pago = dff["Pago"].sum()
        total_pago = f'R$ {total_pago:_.2f}'

        total_pagar = dff["Pagar"].sum()
        total_pagar = f'R$ {total_pagar:_.2f}'

        saldo_atual = saldo["Saldo"].iloc[-1]
        saldo_atual = f'R$ {saldo_atual:_.2f}'

        # total_faturado = df["Pagar"].sum()
        # total_faturado = f'R$ {total_faturado:.2f}'
        data_atual = date.today().strftime('%Y%m%d')
        dff2 = self.df[(self.df.Data < data_atual)]

        # total_atrasado = dff2["Receber"].sum()
        # total_atrasado = f'R$ {total_atrasado:_.2f}'

        total_recebido = total_recebido.replace('.',',').replace('_','.')
        total_receber = total_receber.replace('.',',').replace('_','.')
        total_pago = total_pago.replace('.',',').replace('_','.')
        total_pagar = total_pagar.replace('.',',').replace('_','.')
        saldo_atual = saldo_atual.replace('.',',').replace('_','.')
        # total_atrasado = total_atrasado.replace('.',',').replace('_','.')

        return total_recebido, total_receber, total_pago, total_pagar, saldo_atual