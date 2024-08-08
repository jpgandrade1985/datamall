import pandas as pd
from sqlalchemy import create_engine
import datetime
import streamlit as st
import os
import plotly.express as px

import app_teste
import app

st.set_page_config(page_title="Legatus Data Mall", layout="wide")

# Configurar a conexão com o MySQL
db_user = st.secrets["db_user"]
db_password = st.secrets["db_password"]
db_host = st.secrets["db_host"]
db_port = st.secrets["db_port"]
db_name = st.secrets["db_name"]
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
query = 'SELECT * FROM data_mall.indicadores'
df = pd.read_sql(query, engine)

# Convert 'mes' column to datetime with the correct format and handle errors
df['mes'] = pd.to_datetime(df['mes'], format='%m-%d-%Y', errors='coerce') ### DA ERRO AQUI!
#df['mes'] = pd.to_datetime(df['mes'])

# Remove rows with NaN dates
df = df.dropna(subset=['mes'])

# Create a new column with formatted dates
df['mes_formatted'] = df['mes'].dt.strftime('%b-%y')

#sort by date
df = df.sort_values(by='mes', ascending=True)

# Get unique values for the shopping multiselect menu
shopping_options = df['shopping'].unique()

#Criar opções de mês e ano
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
years = list(range(df['mes'].dt.year.min(), df['mes'].dt.year.max() + 1))

with st.sidebar:

    # Create a multiselect menu for 'shopping'
    selected_shopping = st.multiselect('Selecionar Shopping', shopping_options, default=shopping_options)

    # Create select boxes for start and end month/year
    start_month = st.selectbox('Mês Inicial', months, index=0)
    start_year = st.selectbox('Ano Inicial', years, index=0)
    end_month = st.selectbox('Mês Final', months, index=len(months) - 1)
    end_year = st.selectbox('Ano Final', years, index=len(years) - 1)

# Convert selected month/year to datetime
try:
    start_date = datetime.datetime.strptime(f"01-{start_month}-{start_year}", "%d-%b-%Y")
    end_date = datetime.datetime.strptime(f"01-{end_month}-{end_year}", "%d-%b-%Y")
    end_date = end_date + pd.DateOffset(months=1) - pd.DateOffset(days=1)  # Get the last day of the end month
except ValueError:
    st.error("Invalid date format")
    st.stop()

# Ensure the selected date range is valid
if start_date < df['mes'].min():
    start_date = df['mes'].min()
if end_date > df['mes'].max():
    end_date = df['mes'].max()

# Filter the DataFrame based on selected values
filtered_df = df[df['shopping'].isin(selected_shopping) & (df['mes'] >= start_date) & (df['mes'] <= end_date)]

# Drop the original 'mes' column and rename the formatted column for display
filtered_df = filtered_df.drop(columns=['mes']).rename(columns={'mes_formatted': 'mes'})

# Função para executar o conteúdo de um arquivo Python

def run_script(path):
    if os.path.exists(path):
        with open(path, "w", encoding="utf-8") as file:
            script = file.read()
            exec(script, globals()


# Criando as abas
tab1 = st.tabs(["Geral"])

# Executando o script correspondente em cada aba
with tab1:
    run_script("app_teste.py")
