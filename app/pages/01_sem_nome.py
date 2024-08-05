import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

# Configurar a conexão com o MySQL
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Consultar dados
query = 'SELECT * FROM data_mall.indicadores'
df = pd.read_sql(query, engine)

st.title('Meu Dashboard')

# Exibir os dados
st.write(df)
