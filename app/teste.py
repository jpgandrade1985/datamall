


# Função para executar o conteúdo de um arquivo Python
def run_script(path):
    with open(path, "r") as file:
        script = file.read()
        exec(script)

# Criando as abas
tab1, tab2, tab3 = st.tabs(["Geral", "Vendas", "Contratos"])

# Executando o script correspondente em cada aba
with tab1:
    run_script("app.py")

with tab2:
    run_script("vendas.py")

with tab3:
    run_script("contratos.py")
