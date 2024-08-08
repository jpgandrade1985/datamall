import pandas as pd
from sqlalchemy import create_engine
import datetime
import streamlit as st
import os
import plotly.express as px

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

# Get unique values for the shopping multiselect menu
shopping_options = df['shopping'].unique()

#Page title
st.subheader("Geral")

# Create a multiselect menu for 'shopping'
selected_shopping = st.multiselect('Select Shopping', shopping_options, default=shopping_options)

# Create lists of months and years
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
years = list(range(df['mes'].dt.year.min(), df['mes'].dt.year.max() + 1))

# Create select boxes for start and end month/year
start_month = st.selectbox('Select Start Month', months, index=0)
start_year = st.selectbox('Select Start Year', years, index=0)
end_month = st.selectbox('Select End Month', months, index=len(months) - 1)
end_year = st.selectbox('Select End Year', years, index=len(years) - 1)

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

# Display the filtered DataFrame
st.write(filtered_df)

col1, col2, col3 = st.columns(3)

with col1:
    st.write("vendas totais")
    fig1 = px.line(filtered_df, x="mes", y="venda_total", color='shopping')
    fig.update_layout(xaxis_visible=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.write("vendas/m² total")
    fig2 = px.line(filtered_df, x="mes", y="venda_total_m2", color='shopping')
    fig.update_layout(xaxis={'visible': False})
    st.plotly_chart(fig2, use_container_width=True)


with col3:
    st.write("vendas/m² ocupado")
    fig3 = px.line(filtered_df, x="mes", y="venda_total_m2_ocupado", color='shopping')
    fig.update_layout(xaxis_visible=False)
    st.plotly_chart(fig3, use_container_width=True)
