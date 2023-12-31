import streamlit as st
import pandas as pd
from datetime import datetime,timedelta
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page
from time import sleep
pasta_datasets = Path(__file__).parent.parent / 'datasets/'
nome = st.text_input("Nome Do Aluno")
sala = st.selectbox("Sala",list(st.session_state['df']['SALA'].unique()))
ra = st.text_input("RA do Aluno")
nascimento = st.date_input("Nascimento", format='DD/MM/YYYY')
nascimento = nascimento.strftime("%d/%m/%Y")
nascimento = str(nascimento)
serie = sala[0]
quantidade_alunos = st.session_state['df'].groupby('SALA').size()
chamada = quantidade_alunos[sala] + 1
chamada = str(chamada)
entrada = st.date_input("Data da Matricula",min_value=datetime.today().date() - timedelta(days=7),max_value=datetime.today().date(),format='DD/MM/YYYY')
entrada = entrada.strftime("%d/%m/%Y")
entrada = str(entrada)
sala = sala[1]
laudo = st.text_input("LAUDO")
novo_aluno = {"SERIE":serie,"SALA":sala,"CHAMADA":chamada,"NOME":nome, "LAUDO":laudo, "RA":ra,"NASCIMENTO":nascimento,"ENTRADA":entrada,"SAIDA":None}


#parte da ficha do aluno
#RA;TEL1;TEL2;TEL3;ENDERECO;ROTA;OBSERVACOES
tel1 = st.text_input("Contato 1")
tel2 = st.text_input("Contato 2")
tel3 = st.text_input("Contato 3")
endereco = st.text_input("Endereço")
rota = st.selectbox("Sala", {
    "Santa Rita",
    "Barro Branco",
    "Centro",
    "Vila Adriana",
    "Não Utiliza"
    })
observacoes = st.text_area("Observações")
novo_aluno_ficha = {"RA":ra,"TEL1":tel1,"TEL2":tel2,"TEL3":tel3,"ENDERECO":endereco,"ROTA":rota,"OBSERVACOES":observacoes}
btn_matricular = st.button("Matricular Aluno")

if btn_matricular:
    ficha_do_aluno = pd.read_csv('datasets/fichadoaluno.csv',sep=';', dtype={'TEL1': str,'TEL2':str, 'TEL3': str,'RA':str})
    df = pd.read_csv('datasets/listapiloto2024.csv',sep=';', dtype={'RA': str,'SERIE':str})
    df['SERIE'] = df['SERIE'].astype(str)
    df['SALA'] = df['SALA'].astype(str)
    novo_aluno = pd.DataFrame([novo_aluno])
    novo_aluno_ficha =pd.DataFrame([novo_aluno_ficha])
    novalistapiloto = pd.concat([df, novo_aluno], ignore_index=True)
    novafichadoaluno = st.session_state["ficha_do_aluno"]
    novafichadoaluno = pd.concat([ficha_do_aluno, novo_aluno_ficha], ignore_index=True)
    novalistapiloto = novalistapiloto.sort_values(by=['SERIE','SALA','CHAMADA'])
    novalistapiloto.to_csv(str(pasta_datasets) + '\\listapiloto2024.csv', decimal=',', sep=';', index=False)
    novafichadoaluno.to_csv(str(pasta_datasets) + '\\fichadoaluno.csv', decimal=',', sep=';', index=False)
# Aplicando strftime individualmente a cada elemento da coluna 'NASCIMENTO'


# Convertendo a coluna 'NASCIMENTO' para string (se for realmente necessário)
    sleep(2)
    switch_page("Home")