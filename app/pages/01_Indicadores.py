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

# Create lists of months and years
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
years = list(range(df['mes'].dt.year.min(), df['mes'].dt.year.max() + 1))

#insert filters
col1, col2 = st.columns(2)
with col1:
    selected_shopping = st.multiselect('Select Shopping', shopping_options, default=shopping_options)
with col2:
    start_month = st.selectbox('Select Start Month', months, index=0)
    start_year = st.selectbox('Select Start Year', years, index=0)
    end_month = st.selectbox('Select End Month', months, index=len(months) - 1)
    end_year = st.selectbox('Select End Year', years, index=len(years) - 1)

start_date = datetime.datetime.strptime(f"{start_year}-{start_month}-01", "%Y-%b-%d")
end_date = datetime.datetime.strptime(f"{end_year}-{end_month}-01", "%Y-%b-%d")
end_date = end_date + pd.offsets.MonthEnd(1)  # Get the last day of the end month

# Filter the DataFrame based on selected values
filtered_df = df[df['shopping'].isin(selected_shopping) & (df['mes'] >= start_date) & (df['mes'] <= end_date)]

# Drop the original 'mes' column and rename the formatted column for display
filtered_df = filtered_df.drop(columns=['mes']).rename(columns={'mes_formatted': 'mes'})

st.write(filtered_df)

# Exibir os dados
#st.write(df)
