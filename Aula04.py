# Passo a passo do projeto
# Passo 0: LER a tabela de vendas em uma variável dentro do PYTHON
# Passo 1: Criar a tela do sistema
# Passo 2: Criar o formulário de cadastro
# Passo 3: Salvar a venda na base de dados
# Passo 4: Mostrar a base de dados na tela
# Passo 5: Criar o dashboard com os gráficos

# pip install streamlit pandas plotly

import streamlit as st
import pandas as pd
import plotly.express as px
import time
# import pyautogui as pag
from datetime import date # Usado para validar e formatar datas (acrescentei por conta própria)
# import locale --> Isso é para forçar o interpretador do Python a adotar as regras numéricas do Brasil MAS NÃO DEU CERTO !
# locale.setlocale(locale.LC_ALL, "pt_BR.utf8") --> Isso garante que qualquer função localizada use ponto no milhar e vírgula no decimal MAS NÃO DEU CERTO !

# -----------------------------------------------
st.set_page_config(
    page_title="R&J Sitemas - VENDAS e DASHBOARD", # <-- Altera o nome na Aba do Navegador
    page_icon="📊")

if "sistema_iniciado" not in st.session_state:
    n_a = 0
    st.session_state["sistema_iniciado"] = True
else:
    n_a=1
# -----------------------------------------------

# Passo 0 - Lendo a tabela de vendas
tabela = pd.read_csv("Vendas.csv")
tabela["data"] = pd.to_datetime(tabela["data"]).dt.date # Garante que o Pandas entenda essa coluna como Data (Datetime) e o '.dt.date' no final ignora horas e minutos - por conta própria

# Passo 1 - Criando a tela do sistema
st.write("# Sistema de Vendas")

# Passo 2 - Criando o formulário de cadastro na SIDEBAR // Adicionados os argumentos 'key' para controlar a memória dos campos E ISSO NÃO FUNCIONOU
st.sidebar.write("## Cadastrar VENDA")
data = st.sidebar.date_input("Data", value=date.today(), max_value=date.today(), format="DD/MM/YYYY") # No imput já inicia com a data de HOJE, só permite inserir datas de HOJE pra trás e formata de acordo com BRASIL
vendedor = st.sidebar.selectbox("Vendedor", ["", "Ana", "Bruno", "Carla", "Junior", "Paloma", "Rita"], index=0, placeholder="Selecione o VENDEDOR")
produto = st.sidebar.selectbox("Produto", ["", "Celular", "Fone", "Notebook", "PS4", "Tablet"], index=0, placeholder="Selecione o PRODUTO")
qtde = st.sidebar.number_input("Quantidade", min_value=0, value=0 , step=1)
valor = st.sidebar.number_input("Valor do ITEM R$", min_value=0.00, value=0.00)    
st.sidebar.write(f"### Valor total da VENDA = R$ {qtde * valor:,.2f}")
botao = st.sidebar.button("Cadastrar a VENDA")

# Passo 3 - Salvando a venda na "base de dados"
if botao:    
    if vendedor == "" or produto == "" or qtde <= 0 or valor <= 0: # Validação simples: impede o cadastro se o vendedor ou produto estiverem vazios, ou valores zerados
        st.sidebar.error("Por favor, preencha todos os campos antes de cadastrar!") # Retorna o ERRO e força o preenchimento
    else:
        nova_venda = [data, vendedor, produto, qtde, valor, (qtde * valor)] # "Guardando" os dados digitados na variável nova_venda
        tabela.loc[len(tabela)] = nova_venda # Adiciona a nova venda na próxima linha disponível da tabela. O len(tabela) retorna o número de linhas existentes, que é o índice da posição onde a nova linha deve entrar.
        tabela.to_csv("Vendas.csv", index=False) # Salva toda a tabela atualizada de volta no arquivo Vendas.csv. O index=False evita que o Pandas adicione uma coluna extra de numeração no início de cada linha.
        # time.sleep(1.5)
        # pag.click(x=385, y=129)
        # time.sleep(2.5)        
        # pag.scroll(10000)
        # time.sleep(2.5)
        st.success("Venda cadastrada com sucesso!") # --> RETIRADO do código original do professor, para encaixar minhas demandas com o novo abaixo (MAS VOLTOU, rsrsrs):
        st.toast("Venda cadastrada com sucesso! 🎉")
        time.sleep(3) # PAUSA para visualização da mensagem de sucesso !        
        # st.rerun() # Força o Streamlit a reiniciar o script. Ao reiniciar, todos os inputs voltam ao padrão vazio/zerado!
        st.components.v1.html("<script>parent.window.location.reload();</script>", height=0)        

# Passo 4 - Mostrando na tela, toda a base de dados (tabela) atualizada
st.write("## Vendas Cadastradas")
st.dataframe(tabela, column_config={"data": st.column_config.DateColumn("Data da Venda", format="DD/MM/YYYY"),
                                    "valor": st.column_config.NumberColumn("Valor do ITEM", format="R$ %,.2f"),
                                    "total_venda": st.column_config.NumberColumn("Total da VENDA", format="R$ %,.2f")
                                    }, hide_index=True) # Exibe a tabela formatando apenas a exibição visual da coluna E Formatação do Preço/Valor em Real (R$) - por conta própria

# Passo 5 - Criando o DASBOARD com os Gráficos (FINAL)
st.write('## Dashboard')
soma = tabela['total_venda'].sum()
st.metric('Faturamento TOTAL', f'R${soma:,.2f}')

grafico = px.bar(tabela, x='vendedor', y='total_venda', color='produto')
st.plotly_chart(grafico)

grafico2 = px.pie(tabela, names='produto', values='total_venda')
st.plotly_chart(grafico2)

tabela["mes_nome"] = pd.to_datetime(tabela["data"]).dt.month_name()
grafico3 = px.bar(tabela, x='mes_nome', y='total_venda', color='vendedor', title="Evolução de Vendas por Mês")
st.plotly_chart(grafico3)

# if n_a == 0:
    # time.sleep(1)
    # pag.click(x=225, y=695)
    # time.sleep(0.5)
    # pag.scroll(-100)
    # time.sleep(0.5)
    # pag.click(x=1359, y=714)
    # time.sleep(0.5)
    # pag.click(x=603, y=325)
    # time.sleep(0.5)
    #pag.click(x=535, y=425)
