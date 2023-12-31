import io
from docxtpl import DocxTemplate
import streamlit as st

# Function to create and render the Word document
def doc_file_creation(template_path, data):
    doc = DocxTemplate(template_path)
    doc.render(data)
    return doc

# Streamlit app
st.title("Document Generation and Download")

# Path to the Word document template
template_path = "declaracaotransferencia.docx"

# Data for rendering the template
chaves = ["responsavel", "cpf_responsavel", "nome_aluno", "RA", "serie"]
valores = ["Primeiro Pai", "000000", "Primeiro Aluno Dowload", "131313", "5"]
context = dict(zip(chaves, valores))

# Create and render the Word document
doc_download = doc_file_creation(template_path, context)

# Save the document to BytesIO
bio = io.BytesIO()
doc_download.save(bio)

# Display the download button
if doc_download:
    st.download_button(
        label="Click here to download",
        data=bio.getvalue(),
        file_name=(f"{context["nome_aluno"]}_saida.docx"),
        mime="docx"
    )
