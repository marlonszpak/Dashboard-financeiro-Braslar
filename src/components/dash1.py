import plotly.express as px
from dash import Patch
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import date, timedelta

class Dash1:
    def __init__(self, df):
        self.df = df

    def update_df(self, df):
        self.df = df

    def format_large_number(number):
        if number >= 1_000_000:
            return f"{number / 1_000_000:.2f}M"
        elif number >= 1_000:
            return f"{number / 1_000:.2f}K"
        else:
            return str(number)
    
    def calcular_saldo(self, opening_balance, start_date_object, end_date_object, radio_value) -> pd.DataFrame:        
        start_date_string = start_date_object.strftime('%Y%m%d')
        end_date_string = end_date_object.strftime('%Y%m%d')
    
        self.df['Data'] = pd.to_datetime(self.df['Data'], format='%Y%m%d')
    
        dff = self.df[(self.df.Data >= start_date_string) & (self.df.Data <= end_date_string)]

        if opening_balance is None:
            opening_balance = 0

        saldos = np.array([[start_date_object - timedelta(days=1),opening_balance]])
        saldo_atual = opening_balance
    
        for index, row in dff.iterrows():
            saldo_atual += (row['Recebido'] - row['Pago'])
            if radio_value == '1':
                saldo_atual += (row['Receber'] - row['Pagar'])
            array_saldo_atual = np.array([[row['Data'], saldo_atual]])
            saldos = np.append(saldos, array_saldo_atual, axis=0)

        dataset = pd.DataFrame(saldos, columns=['Data', 'Saldo'])

        return dataset

    def generate_visualizations(self, start_date, end_date):
        start_date = str(start_date)
        end_date = str(end_date)
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%Y%m%d')
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%Y%m%d')

        dff = self.df[(self.df.Data >= start_date_string) & (self.df.Data <= end_date_string)]

        fig = go.Figure()

        # Adiciona o primeiro traço de barras
        fig.add_trace(
            go.Bar(name='Pago', x=pd.to_datetime(dff.Data).dt.strftime('%d/%m/%y'), y=dff.Pago, texttemplate='R$%{y:,s}', textposition='outside', marker=dict(color='#FF3333'))
        )

        # Adiciona o segundo traço de barras
        fig.add_trace(
            go.Bar(name='Recebido', x=pd.to_datetime(dff.Data).dt.strftime('%d/%m/%y'), y=dff.Recebido, texttemplate='R$%{y:,s}', textposition='outside', marker=dict(color='#00CC00'))
        )

         # Adiciona o primeiro traço de barras
        fig.add_trace(
            go.Bar(name='Pagar', x=pd.to_datetime(dff.Data).dt.strftime('%d/%m/%y'), y=dff.Pagar, texttemplate='R$%{y:,s}', textposition='outside', marker=dict(color='#CC6600'))
        )

        # Adiciona o segundo traço de barras
        fig.add_trace(
            go.Bar(name='Receber', x=pd.to_datetime(dff.Data).dt.strftime('%d/%m/%y'), y=dff.Receber, texttemplate='R$%{y:,s}', textposition='outside', marker=dict(color='#3333FF'))
        )

        # Adiciona o traço de linha
        # fig.add_trace(
        #     go.Scatter(name='Receber_linha', x=pd.to_datetime(self.df.Data).dt.strftime('%d/%m/%y'), y=self.df.Receber, texttemplate='R$%{y:.2f}', marker=dict(color='#33FF33')) 
        # )

        fig.update_layout(barmode='group')
        fig.update_layout(yaxis_title='Financeiro')
        fig.update_layout(yaxis=dict(categoryorder='total ascending'))
        fig.update_layout(xaxis=dict(tickfont=dict(size=10)))
        fig.update_layout(template='plotly_dark', font=dict(color='white'))

        return fig
    

    def update_opening_balance(self, opening_balance, start_date, end_date, radio_value):
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%Y%m%d')
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%Y%m%d')

        dff = self.df[(self.df.Data >= start_date_string) & (self.df.Data <= end_date_string)]

        saldos = self.calcular_saldo(opening_balance, start_date_object, end_date_object, radio_value)

        fig = go.Figure()

        # Adiciona o traço de linha
        fig.add_trace(
            go.Scatter(name='Saldo', x=pd.to_datetime(saldos.Data).dt.strftime('%d/%m/%y'), y=saldos.Saldo, texttemplate='R$%{y:,s}', marker=dict(color='#FFFF00'), mode='lines+markers') 
        )

        # Adiciona o primeiro traço de barras
        fig.add_trace(
            go.Bar(name='Pago', x=pd.to_datetime(dff.Data).dt.strftime('%d/%m/%y'), y=dff.Pago, texttemplate='R$%{y:,s}', textposition='outside', marker=dict(color='#FF3333'))
        )

        # Adiciona o segundo traço de barras
        fig.add_trace(
            go.Bar(name='Recebido', x=pd.to_datetime(dff.Data).dt.strftime('%d/%m/%y'), y=dff.Recebido, texttemplate='R$%{y:,s}', textposition='outside', marker=dict(color='#00CC00'))
        )

         # Adiciona o primeiro traço de barras
        fig.add_trace(
            go.Bar(name='Pagar', x=pd.to_datetime(dff.Data).dt.strftime('%d/%m/%y'), y=dff.Pagar, texttemplate='R$%{y:,s}', textposition='outside', marker=dict(color='#CC6600'))
        )

        # Adiciona o segundo traço de barras
        fig.add_trace(
            go.Bar(name='Receber', x=pd.to_datetime(dff.Data).dt.strftime('%d/%m/%y'), y=dff.Receber, texttemplate='R$%{y:,s}', textposition='outside', marker=dict(color='#3333FF'))
        )

            
        fig.update_layout(barmode='group')
        fig.update_layout(yaxis_title='Financeiro')
        fig.update_layout(yaxis=dict(categoryorder='total ascending'))
        fig.update_layout(xaxis=dict(tickfont=dict(size=10)))
        fig.update_layout(template='plotly_dark', font=dict(color='white'))

        return fig


# def update_opening_balance(opening_balace):
#     patched_fig = Patch()
#     # patched_fig["Extrato"][0]["y"] = opening_balace
#     print(opening_balace)
#     patched_fig["data"][2]["y"] = 0
#     return patched_fig

# def generate_visualizations(df):
#     # recebidos = df[(df.status=='R') & (df.data_recebimento > '20240617')]
#     # agrupados = recebidos.groupby(['data_recebimento','banco'])['valor'].sum().reset_index()

#     # top_values_country = recebidos["data_recebimento"].value_counts().head(15).reset_index(name='count')
#     # total_count_country = top_values_country['count'].sum()
#     # top_values_country['percentage'] = (top_values_country['count'] / total_count_country) * 100
#     # fig_bar_country = px.bar(df, x='Data', y='Recebido',
#     #                          color='Recebido', text='Recebido',
#     #                          title='Top Productions Company',
#     #                         #  labels={'count': 'Count', 'index': 'Production Company', 'percentage': 'Percentage'}
#     #                          )
#     # fig_bar_country.update_traces(texttemplate='%{text:.2f}', textposition='outside')
#     # fig_bar_country.update_layout(yaxis_title='Production Company')
#     # fig_bar_country.update_layout(yaxis=dict(categoryorder='total ascending'))
#     # fig_bar_country.update_layout(template='plotly_dark', font=dict(color='yellow'))

#     # top_five_genres = df_atrasos["razao_cliente"].value_counts().head(15).reset_index(name='count')
#     # fig_treemap = px.treemap(top_five_genres, 
#     #                          path=['razao_cliente'],  
#     #                          values='count', 
#     #                          title='Top clientes',
#     #                          color='count',color_continuous_scale='viridis')
#     # fig_treemap.update_layout(template='plotly_dark', font=dict(color='yellow'))

#     # top_values_language = df["razao_cliente"].value_counts().head(10).reset_index(name='count')
#     # total_count_language = top_values_language['count'].sum()
#     # top_values_language['percentage'] = (top_values_language['count'] / total_count_language) * 100
#     # fig_bar_language = px.bar(top_values_language, x='count', y="razao_cliente", orientation='h',
#     #                           color='count', text='percentage',
#     #                           title='Top genres',
#     #                           labels={'count': 'Count', 'index': 'razao_cliente', 'percentage': 'Percentage'},
#     #                           color_continuous_scale='Viridis')
#     # fig_bar_language.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
#     # fig_bar_language.update_layout(yaxis=dict(categoryorder='total ascending'))
#     # fig_bar_language.update_layout(template='plotly_dark', font=dict(color='yellow'))
    
#     # # Generate box plot for ratings
#     # fig_boxplot = px.box(df, x="valor", title='Ratings Distribution')
#     # fig_boxplot.update_traces(marker=dict(color='yellow'))
#     # fig_boxplot.update_layout(template='plotly_dark', font=dict(color='yellow'))


#     # return fig_treemap, fig_bar_language, fig_choropleth, fig_boxplot

#     # fig = go.Figure(data=[
#     #     go.Bar(name='Recebido', x=df.Data, y=df.Recebido, text='Recebido'),
#     #     go.Bar(name='Pago', x=df.Data, y=df.Pago, text="Pago"),
#     # ])
#     # # Change the bar mode

#     # fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
#     # fig.update_layout(barmode='group')
#     # fig.update_layout(yaxis_title='Financeiro')
#     # fig.update_layout(yaxis=dict(categoryorder='total ascending'))
#     # fig.update_layout(template='plotly_dark', font=dict(color='yellow'))

#     fig = go.Figure()

#     # Adiciona o primeiro traço de barras
#     fig.add_trace(
#         go.Bar(name='Pagar', x=pd.to_datetime(df.Data).dt.strftime('%d/%m/%Y'), y=df.Pagar, texttemplate='R$%{y:.2f}', textposition='outside', marker=dict(color='#FF3333'))
#     )

#     # Adiciona o segundo traço de barras
#     fig.add_trace(
#         go.Bar(name='Receber', x=pd.to_datetime(df.Data).dt.strftime('%d/%m/%Y'), y=df.Receber, texttemplate='R$%{y:.2f}', textposition='outside', marker=dict(color='#0066CC'))
#     )

#     # Adiciona o traço de linha
#     fig.add_trace(
#         go.Scatter(name='Receber', x=pd.to_datetime(df.Data).dt.strftime('%d/%m/%Y'), y=df.Receber, texttemplate='R$%{y:.2f}', marker=dict(color='#33FF33')) 
#     )

#     # # Adiciona o primeiro traço de barras
#     # fig.add_trace(
#     #     go.Bar(name='Pago', x=pd.to_datetime(df.Data).dt.strftime('%d/%m/%Y'), y=df.Pago, texttemplate='R$%{y:.2f}', textposition='outside', marker=dict(color='#FF3333'))
#     # )

#     # # Adiciona o segundo traço de barras
#     # fig.add_trace(
#     #     go.Bar(name='Recebido', x=pd.to_datetime(df.Data).dt.strftime('%d/%m/%Y'), y=df.Recebido, texttemplate='R$%{y:.2f}', textposition='outside', marker=dict(color='#0066CC'))
#     # )

#     # # Adiciona o traço de linha
#     # fig.add_trace(
#     #     go.Scatter(name='Recebido', x=pd.to_datetime(df.Data).dt.strftime('%d/%m/%Y'), y=df.Recebido, texttemplate='R$%{y:.2f}', marker=dict(color='#33FF33')) 
#     # )

#     # Configura o layout
#     # fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
#     fig.update_layout(barmode='group')
#     fig.update_layout(yaxis_title='Financeiro')
#     fig.update_layout(yaxis=dict(categoryorder='total ascending'))
#     fig.update_layout(template='plotly_dark', font=dict(color='white'))

#     return fig
