import streamlit as st
from time import sleep
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
ocorrencia = st.button("Ocorrencia")
if ocorrencia:
    if "ocorrencia" not in st.session_state:
        print('')
    else:
        switch_page("Ocorrencias")
if "last_selected_row" not in st.session_state:
    st.success('Selecione um aluno na Lista Piloto')
elif  st.session_state["last_selected_row"] is None:
    st.success('Selecione um aluno na Lista Piloto')
else:
    #df_alunos.loc[df_alunos[col_filtro] == valor_filtro, colunas_selecionadas]
    infoAluno = st.session_state["last_selected_row"]
    ficha_do_aluno = st.session_state["ficha_do_aluno"]
    ficha_do_aluno = ficha_do_aluno.loc[ficha_do_aluno["RA"]==infoAluno["RA"]]
    ficha_do_aluno = ficha_do_aluno.squeeze()
    st.write(f"Nome: {infoAluno["NOME"]} -  Sala: {infoAluno["SALA"]} - Nascimento: {infoAluno["NASCIMENTO"]}")
    st.write(f"Contatos: {ficha_do_aluno["TEL1"]} - {ficha_do_aluno["TEL2"]} - {ficha_do_aluno["TEL3"]}")
    st.write(f"Endereço: {ficha_do_aluno["ENDERECO"]} - ROTA: {ficha_do_aluno["ROTA"]}")
    st.session_state["ocorrencia"] = True
    del st.session_state['last_selected_row'] 
    
