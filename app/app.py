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

#sort by date
df = df.sort_values(by='mes', ascending=True)

# Get unique values for the shopping multiselect menu
shopping_options = df['shopping'].unique()

#Criar opções de mês e ano
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
years = list(range(df['mes'].dt.year.min(), df['mes'].dt.year.max() + 1))

with st.sidebar:

    # Create a multiselect menu for 'shopping'
    selected_shopping = st.multiselect('Select Shopping', shopping_options, default=shopping_options)

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

#Subtitle
st.subheader("Vendas")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("vendas totais")
    fig1 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="venda_total", color='shopping')
    fig1.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'Total de Vendas'}, margin=dict(l=0, r=0, t=0, b=2))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.write("vendas/m² total")
    fig2 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="venda_total_m2", color='shopping')
    fig2.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'Vendas / m² - área total'}, margin=dict(l=0, r=0, t=0, b=2))
    st.plotly_chart(fig2, use_container_width=True)


with col3:
    st.write("vendas/m² ocupado")
    fig3 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="venda_total_m2_ocupado", color='shopping')
    fig3.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'Vendas / m² - área ocupada'}, margin=dict(l=0, r=0, t=0, b=2))
    st.plotly_chart(fig3, use_container_width=True)

#Subtitle
st.subheader("NOI")

col4, col5, col6 = st.columns(3)

with col4:
    st.write("NOI Caixa")
    fig4 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="noi_caixa", color='shopping')
    fig4.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'NOI Caixa'}, margin=dict(l=0, r=0, t=0, b=2))
    st.plotly_chart(fig4, use_container_width=True)

with col5:
    st.write("NOI Caixa/m² total")
    fig5 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="noi_caixa_m2_abl_total", color='shopping')
    fig5.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'NOI Caixa / m² - área total'}, margin=dict(l=0, r=0, t=0, b=2))
    st.plotly_chart(fig5, use_container_width=True)


with col6:
    st.write("NOI Caixa/m² ocupado")
    fig6 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="noi_caixa_m2_abl_ocupado", color='shopping')
    fig6.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'NOI Caixa / m² ocupado'}, margin=dict(l=0, r=0, t=0, b=2))
    st.plotly_chart(fig6, use_container_width=True)

#Subtitle
st.subheader("Vacância e Inadimplência")

col7, col8, col9 = st.columns(3)

with col7:
    st.write("ABL vago")
    fig7 = px.bar(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="abl_vago", color='shopping', barmode='group')
    fig7.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'ABL Vago'}, margin=dict(l=0, r=0, t=0, b=2))
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    st.write("Lojas Vagas")
    fig8 = px.bar(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="lojas_vagas", color='shopping', barmode='group')
    fig8.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'Lojas Vagas'}, margin=dict(l=0, r=0, t=0, b=2))
    st.plotly_chart(fig8, use_container_width=True)


with col9:
    st.write("Vacância %")
    fig9 = px.bar(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="vacancia_pct", color='shopping', barmode='group')
    fig9.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'Vacância %'}, margin=dict(l=0, r=0, t=0, b=2))
    st.plotly_chart(fig9, use_container_width=True)



with st.expander("Tabela de Dados"):
    # Display the filtered DataFrame
    st.write(filtered_df)
