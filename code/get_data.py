from sqlalchemy import create_engine
import pandas as pd

# Configurar a conexão com o MySQL
db_user = 'data_mall'
db_password = 'Lgt#0701'
db_host = 'data_mall.mysql.dbaas.com.br'
db_port = '3306'  # Porta padrão do MySQL
db_name = 'data_mall'

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

query = 'SELECT * FROM data_mall.grupo_ativ_loja'
df = pd.read_sql(query, engine)

#faz o gráfico de sunburst de vendas, classificando por tipo > setor > loja
import plotly.express as px
df1 = df.loc[(df["data"] == "2023-08-01")] #deixar essa data como variável do dropdown
fig = px.sunburst(df1, path=['grupo', 'setor', 'nome_loja'], values='venda')
fig.show()

#faz o gráfico de sunburst de vendas/m², classificando por tipo > setor > loja
df1 = df.loc[(df["data"] == "2023-08-01")]
#df2 = df.loc[(df["data"] == "2023-09-01")]
fig = px.sunburst(df1, path=['grupo', 'setor', 'nome_loja'], values='venda_m2')
fig.show()
