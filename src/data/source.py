import pandas as pd
import mysql.connector as connection

def get_data_base():
    try:
        mydb = connection.connect(host="10.1.1.103", database = 'financeiro',user="root", passwd="3GgSFHpeZDj3d7",use_pure=True)
        query = "Select * from contas_receber;"
        result_dataFrame = pd.read_sql(query,mydb)
        mydb.close() #close the connection
    except Exception as e:
        mydb.close()
        print(str(e))


    # Incorporate data
    df = result_dataFrame
    return df