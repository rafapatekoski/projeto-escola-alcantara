import streamlit as st
from datetime import date
import pandas as pd
import random
import numpy as np
from time import sleep
from streamlit_extras.switch_page_button import switch_page
from pathlib import Path

pasta_datasets = Path(__file__).parent.parent / 'datasets/'

if "df" not in st.session_state:
    st.success('Espere o carregamento dos dados')
    sleep(1)
    switch_page('home')
@st.cache_data
def get_data():
    df = st.session_state['df']
    # Excluir colunas 'B' e 'D' usando o método drop
    return df
colunas = list(get_data().columns)
# Verifica se os dados estão na sessão, caso contrário, carrega dados
if "data" not in st.session_state:
    df = get_data()
    df["select"] = False
    st.session_state["data"] = df
else:
    print("data esta em session state")
# Gera uma chave única para o editor de dados
if "editor_key" not in st.session_state:
    st.session_state["editor_key"] = random.randint(0, 100000)

# Inicializa a última linha selecionada como nula
if "last_selected_row" not in st.session_state:
    st.session_state["last_selected_row"] = None

# Função para obter a última linha selecionada e limpar a seleção
def get_row_and_clear_selection():
    key = st.session_state["editor_key"]
    df = st.session_state["data"]
    selected_rows = st.session_state[key]["edited_rows"]
    selected_rows = [int(row) for row in selected_rows if selected_rows[row]["select"]]
    try:
        last_row = selected_rows[-1]
    except IndexError:
        return
    df["select"] = False
    st.session_state["data"] = df
    st.session_state["editor_key"] = random.randint(0, 100000)
    st.session_state["last_selected_row"] = df.iloc[last_row]

# Utiliza o editor de dados do Streamlit com a função de callback
salas = list(st.session_state['df']['SALA'].unique())
valor_filtro = st.selectbox('Filtrar por sala:', salas)
col1, col2 = st.columns(2)
status_filtrar = col1.button('Filtrar')
status_limpar = col2.button('Limpar')
if status_filtrar:
    data = st.session_state["df"]
    df_filtrado = data.loc[data['SALA'] == valor_filtro]
    df_filtrado["select"] = False
    st.session_state["data"] = df_filtrado
elif status_limpar:
    df = st.session_state["df"]
    df["select"] = False
    st.session_state["data"] = df
try:
    edited_rows = st.session_state[key]["edited_rows"]
    st.write(edited_rows)
except Exception as e:
    st.write("")
dataEditor = st.data_editor(
    st.session_state["data"],
    width=300,
    height=600,
    key=st.session_state["editor_key"],
    on_change=get_row_and_clear_selection,
    use_container_width=True,
    num_rows="dynamic",
    hide_index=True,
    column_config={
        "NASCIMENTO": st.column_config.DateColumn(
            "NASCIMENTO",
            min_value=date(1900, 1, 1),
            max_value=date(2005, 1, 1),
            format="DD/MM/YYYY",
            step=1,
        ),
         "ENTRADA": st.column_config.DateColumn(
            "ENTRADA",
            min_value=date(1900, 1, 1),
            max_value=date(2005, 1, 1),
            format="DD/MM/YYYY",
            step=1,
        ),
          "SAIDA": st.column_config.DateColumn(
            "SAIDA",
            min_value=date(1900, 1, 1),
            max_value=date(2005, 1, 1),
            format="DD/MM/YYYY",
            step=1,
        ),
    },
)

# Obtém a última linha selecionada e exibe informações
last_row = st.session_state["last_selected_row"]

if last_row is not None:
    print(type(last_row))
    switch_page("Ficha do Aluno")
    
#FUNÇÃO EDITAR
