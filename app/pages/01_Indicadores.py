import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import os

# Configurar a conexão com o MySQL
db_user = st.secrets["db_user"]
db_password = st.secrets["db_password"]
db_host = st.secrets["db_host"]
db_port = st.secrets["db_port"]
db_name = st.secrets["db_name"]
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
query = 'SELECT * FROM data_mall.indicadores'
df = pd.read_sql(query, engine)

st.title('Indicadores')
#st.write(df)

shopping_options = df['shopping'].unique()
mes_options = df['mes'].unique()

col1, col2 = st.columns(2)
with col1:
    selected_shopping = st.multiselect('Shopping', shopping_options)
with col2:
    selected_mes = st.multiselect('Mês', mes_options)

filtered_df = df[(df['shopping'] == selected_shopping) & (df['mes'] == selected_mes)]
st.write(filtered_df)

# Exibir os dados
#st.write(df)
