import pandas as pd

def get_json_data() -> pd.DataFrame: 
    df = pd.read_json("data-files/pagar.json")
    data = df['ListaContasPagar']
    dff = pd.json_normalize(data)

    pago_mes = dff[(dff.Status == "P")]
    pago_mes.loc[:, 'Valor'] = pago_mes['Valor'].astype(float)
    pago_mes = pago_mes.groupby('Pagamento')['Valor'].sum().to_frame().reset_index()
    pago_mes = pago_mes.rename(columns={"Pagamento":"Data","Valor":"Pago"})

    pagar_mes = dff[(dff.Status == "A")]
    pagar_mes.loc[:, 'Valor'] = pagar_mes['Valor'].astype(float)
    pagar_mes = pagar_mes.groupby('Vencimento')['Valor'].sum().to_frame().reset_index()
    pagar_mes = pagar_mes.rename(columns={"Vencimento":"Data", "Valor":"Pagar"})

    df2 = pd.read_json("data-files/receber.json")
    data2 = df2['ListaContasReceber']
    dff2 = pd.json_normalize(data2)

    recebido_mes = dff2[(dff2.Status == "R")]
    recebido_mes.loc[:, 'Valor'] = recebido_mes['Valor'].astype(float)
    recebido_mes = recebido_mes.groupby('Recebimento')['Valor'].sum().to_frame().reset_index()
    recebido_mes = recebido_mes.rename(columns={"Recebimento":"Data","Valor":"Recebido"})

    receber_mes = dff2[(dff2.Status.isin(["A","C","H"]))]
    receber_mes.loc[:, 'Valor'] = receber_mes['Valor'].astype(float)
    receber_mes = receber_mes.groupby('Vencimento')['Valor'].sum().to_frame().reset_index()
    receber_mes = receber_mes.rename(columns={"Vencimento":"Data", "Valor":"Receber"})

    realizado = pd.merge(pago_mes, recebido_mes, on="Data", how="outer")
    projetado = pd.merge(pagar_mes, receber_mes, on="Data", how="outer")
    

    # pd.set_option('future.no_silent_downcasting', True)
    if(~projetado.empty & ~realizado.empty):
        return pd.merge(realizado, projetado, on="Data", how="outer").fillna(0)

    if(projetado.empty & ~realizado.empty):
        return realizado.fillna(0)

    if(realizado.empty & ~projetado.empty):
        return projetado.fillna(0)

    return pd.DataFrame()