import streamlit as st
from time import sleep
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import io
from docxtpl import DocxTemplate
from pathlib import Path
from datetime import datetime
pasta_datasets = Path(__file__).parent.parent / 'datasets/'
pasta_documentos = Path(__file__).parent.parent / 'documentos/'
template_path = str(pasta_documentos)+"\\declaracaotransferencia.docx"
# Path to the Word document template
#construir download aqui
    #funcoes transferencia
def doc_file_creation(template_path, data):
    doc = DocxTemplate(template_path)
    doc.render(data)
    return doc
if "voltarHome" not in st.session_state:
    print("continue daqui")
else:
    switch_page("Home")
if "transferencia" not in st.session_state:
    print("algo")
else:
    st.warning('Aluno transferido', icon="⚠️")
    sleep(3)
    st.error("Selecione um aluno que ainda está matriculado")
    del st.session_state["transferencia"]
    
ocorrencia = st.button("Ocorrencia")
if ocorrencia:
    if "ocorrencia" not in st.session_state:
        print('')
    else:
        switch_page("Ocorrencias")
if "alunoSelecionado" not in st.session_state:
    #df_alunos.loc[df_alunos[col_filtro] == valor_filtro, colunas_selecionadas]
    if "last_selected_row" not in st.session_state:
        st.error("Você precisa selecionar um aluno na lista piloto")
        sleep(2)
        switch_page("Lista Piloto")
    elif st.session_state["last_selected_row"] is None:
        st.success('Selecione um aluno na Lista Piloto')
    else:
        st.session_state["alunoSelecionado"] = st.session_state["last_selected_row"]
else:
    if "last_selected_row" not in st.session_state:
        print(...)
    elif st.session_state["last_selected_row"] is None:
        st.error("Selecione um aluno na Lista Piloto")
        sleep(2)
        switch_page("Lista Piloto")
    else:
        st.session_state["alunoSelecionado"] = st.session_state["last_selected_row"]
infoAluno = st.session_state["alunoSelecionado"]
ficha_do_aluno = st.session_state["ficha_do_aluno"]
ficha_do_aluno = ficha_do_aluno.loc[ficha_do_aluno["RA"]==infoAluno["RA"]]
ficha_do_aluno = ficha_do_aluno.squeeze()
st.session_state["alunoSelecionado"] = infoAluno
st.write(f"Nome: {infoAluno["NOME"]} -  Sala: {infoAluno["SALA"]} - Nascimento: {infoAluno["NASCIMENTO"].strftime("%d/%m/%Y")} - {infoAluno["LAUDO"]}")
st.write(f"Contatos: {ficha_do_aluno["TEL1"]} - {ficha_do_aluno["TEL2"]} - {ficha_do_aluno["TEL3"]}")
st.write(f"Endereço: {ficha_do_aluno["ENDERECO"]} - ROTA: {ficha_do_aluno["ROTA"]}")
st.write(f"Observações: {ficha_do_aluno["OBSERVACOES"]}")
st.session_state["ocorrencia"] = True
    
sala = str(infoAluno["SALA"])
sala = sala[0]
chaves = ["responsavel", "cpf_responsavel", "nome_aluno", "RA", "serie"]
valores = ["Primeiro Pai", "000000", infoAluno["NOME"], infoAluno["RA"], ]
context = dict(zip(chaves, valores))
        
        # Create and render the Word document

def transferencia():
    st.session_state["transferencia"] = True
    #alterar data de saida
    df = pd.read_csv('datasets/listapiloto2024.csv',sep=';', dtype={'RA': str,'SERIE':str})
    hoje = datetime.today().date()
    hoje = hoje.strftime("%d/%m/%Y")
    hoje = str(hoje)
    df.loc[df['RA'] == infoAluno["RA"], 'SAIDA'] = hoje
    df.to_csv(str(pasta_datasets) + '\\listapiloto2024.csv', decimal=',', sep=';', index=False)
    st.session_state["voltarHome"] = True
        # Display the download button
#se o aluno foi transferido
if pd.isna(infoAluno["SAIDA"]):
    doc_download = doc_file_creation(template_path, context)
    bio = io.BytesIO()
    doc_download.save(bio)
    if doc_download:
        btn_baixar = st.download_button(
            label="Emitir Transferência",
            data=bio.getvalue(),
            file_name=(f"{context["nome_aluno"]}_saida.docx"),
            mime="docx",
            on_click=transferencia
        )
else:
    st.error(f"Aluno transferido no dia: {str(infoAluno["SAIDA"].strftime("%d/%m/%y"))}")
        # Save the document to BytesIO

del st.session_state['last_selected_row'] 