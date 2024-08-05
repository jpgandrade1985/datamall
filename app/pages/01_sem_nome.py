import pandas as pd
#from sqlalchemy import create_engine
import mysql.connector
import streamlit as st

import os

# Everything is accessible via the st.secrets dict:
st.write("DB USER:", st.secrets["db_user"])
st.write("DB password:", st.secrets["db_password"])
st.write("My cool secrets:", st.secrets["my_cool_secrets"]["things_i_like"])

# And the root-level secrets are also accessible as environment variables:
st.write(
    "Has environment variables been set:",
    os.environ["db_user"] == st.secrets["db_user"],)

# Configurar a conexão com o MySQL
#engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
def load_data():
    connection = mysql.connector.connect(
        db_host,
        db_user,
        db_password,
        db_name)
    
# Consultar dados
    query = 'SELECT * FROM data_mall.indicadores'
    df = pd.read_sql(query, connection)
    return df

st.title('Meu Dashboard')

# Exibir os dados
st.write(df)
