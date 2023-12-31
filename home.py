import streamlit as st
import pandas as pd
from pathlib import Path
from st_pages import Page, Section, add_page_title, show_pages

# Specify what pages should be shown in the sidebar, and what their titles 
# and icons should be
show_pages([
    Page("home.py", "Home"),
    Page("pages/listapiloto.py", "Lista Piloto"),
    Page("pages/editarLista.py", "Editar Lista Piloto"),
    Page("pages/aluno.py", "Ficha do Aluno"),
    Page("pages/matricularAluno.py", "Matricular Aluno"),
    Page("pages/ocorrencias.py", "Ocorrencias"),
])
# Função para obter dados simulados

ficha_do_aluno = pd.read_csv('datasets/fichadoaluno.csv',sep=';', dtype={'TEL1': str,'TEL2':str, 'TEL3': str,'RA':str})
df = pd.read_csv('datasets/listapiloto2024.csv',sep=';', dtype={'RA': str,'SERIE':str})
df['SERIE'] = df['SERIE'].astype(str)
df['SALA'] = df['SALA'].astype(str)
df['SALA'] = df['SERIE'] + df['SALA']
df['ENTRADA'] = pd.to_datetime(df['ENTRADA'], format='%d/%m/%Y')
df['SAIDA'] = pd.to_datetime(df['SAIDA'], format='%d/%m/%Y')
df['NASCIMENTO'] = pd.to_datetime(df['NASCIMENTO'], format='%d/%m/%Y')
# Criar uma nova coluna 'RA' concatenando 'RA', 'DIG_RA' e 'UF_RA'
#df['RA'] = df['RA'].astype(str) + df['DIG_RA'].astype(str) + df['UF_RA'].astype(str)

# Remover as colunas 'DIG_RA' e 'UF_RA' agora que 'RA' foi criada
#df = df.drop(['DIG_RA', 'UF_RA'], axis=1)
#DECLARANDO SEÇÕES
st.session_state['ficha_do_aluno'] = ficha_do_aluno
st.session_state['df'] = df
df["select"] = False
st.session_state['data'] = df
st.write("Seja Bem Vindo ao Projeto Alcantara")

# Contar o número de alunos na sala com saída vazia
matriculasTotais = df[df['SAIDA'].isnull()].groupby('SALA').size().reset_index(name='matriculasTotais')
# Contar o número de entradas em fevereiro
entradas_fevereiro = df[df['ENTRADA'].dt.month == 2].groupby('SALA').size().reset_index(name='Entradas_Fevereiro')
entradas_marco = df[df['ENTRADA'].dt.month == 3].groupby('SALA').size().reset_index(name='Entradas_Marco')




# Contar o número de saídas na sala
saida_fevereiro = df[df['SAIDA'].dt.month == 2].groupby('SALA').size().reset_index(name='Saida_Fevereiro')

dadosEscolares = matriculasTotais
dadosEscolares["EntradasFevereiro"] = entradas_fevereiro["Entradas_Fevereiro"]
dadosEscolares["SaidasFeveiro"] = saida_fevereiro["Saida_Fevereiro"]

# Substituir valores NaN por 0
dadosEscolares = dadosEscolares.fillna(0)
st.divider()
st.title("Dados Escolares Feveiro")
st.dataframe(dadosEscolares)