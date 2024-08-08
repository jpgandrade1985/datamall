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
