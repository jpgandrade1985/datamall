import pandas as pd
from sqlalchemy import create_engine
import datetime
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

# Convert 'mes' column to datetime if it's not already
df['mes'] = pd.to_datetime(df['mes'])

# Create a new column with formatted dates
df['mes_formatted'] = df['mes'].dt.strftime('%b-%y')

# Write page Title
st.title('Indicadores')
#st.write(df)

shopping_options = df['shopping'].unique()
mes_options = df['mes'].unique()

#insert filters
col1, col2 = st.columns(2)
with col1:
    selected_shopping = st.multiselect('Select Shopping', shopping_options, default=shopping_options)
with col2:
    start_date, end_date = st.date_input('Select Date Range', value=[df['mes'].min().date(), df['mes'].max().date()])

start_date = datetime.datetime.combine(start_date, datetime.datetime.min.time())
end_date = datetime.datetime.combine(end_date, datetime.datetime.max.time())

filtered_df = df[df['shopping'].isin(selected_shopping) & (df['mes'] >= start_date) & (df['mes'] <= end_date)]
filtered_df = filtered_df.drop(columns=['mes']).rename(columns={'mes_formatted': 'mes'})
st.write(filtered_df)

# Exibir os dados
#st.write(df)
