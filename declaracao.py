from docxtpl import DocxTemplate

doc = DocxTemplate("declaracaotransferencia.docx")
chaves = ["responsavel","cpf_responsavel","nome_aluno","RA","serie"]
valores = ["Seu Pai","293891389","David Henrique","131313","5"]
context = dict(zip(chaves, valores))
doc.render(context)
doc.save("declaracaogerada.docx")