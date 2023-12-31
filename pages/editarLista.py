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
    df['NASCIMENTO'] = pd.to_datetime(df['NASCIMENTO'], format='%d/%m/%Y')
    return df
colunas = list(get_data().columns)
# Verifica se os dados estão na sessão, caso contrário, carrega dados
st.session_state["data"] = st.session_state["df"]
# Gera uma chave única para o editor de dados

# Utiliza o editor de dados do Streamlit com a função de callback

try:
    edited_rows = st.session_state[key]["edited_rows"]
    st.write(edited_rows)
except Exception as e:
    st.write("")
dataEditor = st.data_editor(
    st.session_state["data"],
    width=300,
    height=600,
    use_container_width=True,
    hide_index=True,
    column_config={
        "NASCIMENTO": st.column_config.DateColumn(
            "NASCIMENTO",
            min_value=date(2011, 1, 1),
            max_value=date(2022, 1, 1),
            format="DD/MM/YYYY",
            step=1,
            disabled=True
        ),
        "ENTRADA": st.column_config.DateColumn(
            "ENTRADA",
            min_value=date(2024, 1, 1),
            max_value=date(2025, 1, 1),
            format="DD/MM/YYYY",
            step=1,
        ),
        "SAIDA": st.column_config.DateColumn(
            "SAIDA",
            min_value=date(2024, 1, 1),
            max_value=date(2025, 1, 1),
            format="DD/MM/YYYY",
            step=1,
        ),
        "SALA": st.column_config.SelectboxColumn(
            "SALA",
             width="medium",
            options=[
            "1A",
            "1B",
            "1C",
            "1D",
            "2A",
            "2B",
            "2C",
            "3A",
            "3B",
            "3C",
            "4A",
            "4B",
            "4C",
            "5A",
            "5B",
            "5C",
            "5D"
            ],
            required=True,
        ),
        "CHAMADA": st.column_config.NumberColumn(
            "CHAMADA",
            min_value=1,
            max_value=40,
            step=1,
            disabled=True,
        ),
        "SERIE": st.column_config.NumberColumn(
        "SERIE",
            min_value=1,
            max_value=40,
            step=1,
            disabled=True,
        ),
        "RA": st.column_config.TextColumn(
        "RA",
            disabled=True,
        ),
          
    },
)


#FUNÇÃO EDITAR


def click_editar():
        # Split the "SALA" column into "SERIE" and "SALA"
    
    dataEditor[['SERIE', 'SALA']] = dataEditor['SALA'].str.extract('(\d+)([A-Za-z]+)')
    df = dataEditor
    # Reorder the columns
    df = df[['SERIE', 'SALA', 'CHAMADA', 'NOME', 'RA', 'NASCIMENTO', 'LAUDO' ,'ENTRADA', 'SAIDA']]
    df['ENTRADA'] = pd.to_datetime(df['ENTRADA']).dt.strftime('%d/%m/%Y')
    df['SAIDA'] = pd.to_datetime(df['SAIDA']).dt.strftime('%d/%m/%Y')
    df['NASCIMENTO'] = pd.to_datetime(df['NASCIMENTO']).dt.strftime('%d/%m/%Y')
    df["CHAMADA"] = df["CHAMADA"].astype(str)
    df['CHAMADA'] = df['CHAMADA'].str.replace(',', '.').astype(float).astype('Int64')
    df = df.sort_values(by=['SERIE','SALA','CHAMADA'])
    df.to_csv(str(pasta_datasets) + '\\listapiloto2024.csv', decimal=',', sep=';', index=False)
    sleep(2)
    st.success("Edição concluida com sucesso, o App vai recarregar a lista") 
    st.session_state["editou"] = True
st.button("Editar",on_click=click_editar)
if "editou" not in st.session_state:
    print("----")
else:
    print('sjksfknfkksfnks')
    del st.session_state["data"]
    print("datapagado")
    del st.session_state["editou"]
    switch_page("Home")