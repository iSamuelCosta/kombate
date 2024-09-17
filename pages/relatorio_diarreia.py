

#Importando as bibliotecas necessarias
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import secrets
import altair as alt
from querrys import *
import pydeck as pdk
import MySQLdb
from cria_imagens import *
import folium
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import time
from gerar_pdf import *

from folium.plugins import HeatMap

import mysql.connector

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

def enviar_email(destinatario, assunto, corpo, anexo_path):
    # Configurações do servidor de e-mail (exemplo com Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    remetente_email = "itajubadigitaldac@gmail.com"  # Substitua pelo seu e-mail
    remetente_senha = "qnve siib qdla ybso"  # Substitua pela sua senha

    # Criando a mensagem
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente_email
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto

    # Adicionando o corpo do e-mail
    mensagem.attach(MIMEText(corpo, 'plain'))

    # Adicionando o anexo
    with open(anexo_path, "rb") as arquivo:
        parte = MIMEApplication(arquivo.read(), Name=os.path.basename(anexo_path))
    parte['Content-Disposition'] = f'attachment; filename="{os.path.basename(anexo_path)}"'
    mensagem.attach(parte)

    # Enviando o e-mail
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(remetente_email, remetente_senha)
            server.send_message(mensagem)
        return True
    except Exception as e:
        st.text(f"Erro ao enviar e-mail: {e}")
        return False


st.set_page_config(layout='wide', page_title="Nota de Avaliação dos Serviços da Prefeitura")
@st.cache_data
def formata_numero(valor, prefixo=''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            if valor.is_integer():  # Verifica se o valor é um número inteiro
                return f'{prefixo} {int(valor)} {unidade}'
            else:
                return f'{prefixo} {valor: .1f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor: .1f} milhões'

  
conn2 = st.connection('mysql_2', type='sql')   
col1, col2, col3 = st.columns([4,1,1])

with col1:
    st.title('Monitorização das doenças diarreicas agudas')

ano_diarreia = conn2.query(query_ano_diarreia(), ttl=60)

with col2:
    ano_selecionando = st.selectbox('Selecione o ano', ano_diarreia['ano'].unique())
    semana_diarreia = conn2.query(query_diarreia_semana_epidemiologica(ano_selecionando), ttl=60)

with col3:
    semana_selecionando = st.selectbox('Selecione a semana epidêmica', semana_diarreia['semana'].unique())

unidade_saude='7782934'

nome_ubs = conn2.query(query_pega_nome_ubs(unidade_saude), ttl=60)
nome_ubs = nome_ubs.iloc[0, 0]
st.subheader(f'{nome_ubs} - Semana Epidêmica {semana_selecionando} do Ano {ano_selecionando}')
faixa_etaria = conn2.query(query_faixa_etaria_diarreia_ubs(ano_selecionando, semana_selecionando, unidade_saude), ttl=60)


faixa_etaria_sangue = conn2.query(query_faixa_etaria_diarreia(ano_selecionando, semana_selecionando), ttl=60)

plano_tratamento = conn2.query(query_plano_diarreia(ano_selecionando, semana_selecionando), ttl=60)
semana_selecionando = int(semana_selecionando)
ano_selecionando = int(ano_selecionando)


with st.container(border=True):
    col4, col5, col6 = st.columns([2,2,2])
    with col4:
        st.dataframe(faixa_etaria, hide_index=True, use_container_width=True)

    with col5:
        st.dataframe(faixa_etaria_sangue, hide_index=True, use_container_width=True)

    with col6:
        st.dataframe(plano_tratamento, hide_index=True, use_container_width=True)

procedencia = conn2.query(query_procedencia_diarreia(ano_selecionando, semana_selecionando), ttl=60)


try:
    analise_casos = conn2.query(query_analise_casos_ubs(semana_selecionando, ano_selecionando, unidade_saude), ttl=60)
except:
    analise_casos = pd.DataFrame()

if not analise_casos.empty:
    aumento = analise_casos.iloc[0, 3]
    texto_aumento = analise_casos.iloc[0, 4]
    mudanca_faixa_etaria = analise_casos.iloc[0, 5]
    texto_mudanca_faixa_etaria = analise_casos.iloc[0, 6]
    texto_mudanca_faixa_etaria2 = analise_casos.iloc[0, 7]
    casos_concentrados = analise_casos.iloc[0, 8]
    texto_casos_concentrados = analise_casos.iloc[0, 9]
    plano_aux = analise_casos.iloc[0, 10]
    texto_plano_tratamento_mais_usado = analise_casos.iloc[0, 11]
    houve_mudancas = analise_casos.iloc[0, 12]
    houve_surtos = analise_casos.iloc[0, 13]
    texto_surtos = analise_casos.iloc[0, 14]
    texto_surtos2 = analise_casos.iloc[0, 15]
    colheu_material = analise_casos.iloc[0, 16]
    texto_colheu_material = analise_casos.iloc[0, 17]
else:
    aumento = ''
    texto_aumento = ''
    mudanca_faixa_etaria = ''
    texto_mudanca_faixa_etaria = ''
    texto_mudanca_faixa_etaria2 = ''
    casos_concentrados = ''
    texto_casos_concentrados = ''
    plano_aux = ''
    texto_plano_tratamento_mais_usado = ''  
    houve_mudancas = ''
    houve_surtos = ''
    texto_surtos = ''
    texto_surtos2 = ''
    colheu_material = ''
    texto_colheu_material = ''



with st.container(border=True):
    col7, col8 = st.columns([2,2])
    with col7:
        st.dataframe(procedencia, hide_index=True, use_container_width=True)

    with col8:
        st.subheader('Análise')
        aumento = st.radio('Houve aumento de casos?', ['Sim', 'Não'], index=0 if aumento == 'Sim' else 1, horizontal=True)
        if aumento == 'Sim':
            texto_aumento = st.text_input('Se sim, que fatores contribuíram para o aumento de casos?', value=texto_aumento)
        else:
            texto_aumento = ''
        mudanca_faixa_etaria = st.radio('Houve mudança na faixa etária?', ['Sim', 'Não'], index=0 if mudanca_faixa_etaria == 'Sim' else 1, horizontal=True)
        if mudanca_faixa_etaria == 'Sim':
            texto_mudanca_faixa_etaria = st.text_input('Se sim, para qual?', value=texto_mudanca_faixa_etaria)
            texto_mudanca_faixa_etaria2 = st.text_input('O que sugere essa mudança?', value=texto_mudanca_faixa_etaria2)
        else:
            texto_mudanca_faixa_etaria = ''
            texto_mudanca_faixa_etaria2 = ''
            
        casos_concentrados = st.radio('Houve casos concentrados em alguma localidade?', ['Sim', 'Não'], index=0 if casos_concentrados == 'Sim' else 1, horizontal=True)
        if casos_concentrados == 'Sim':
            texto_casos_concentrados = st.text_input('Se sim, em quais e qual a explicação?', value=texto_casos_concentrados)
        else:
            texto_casos_concentrados = ''
        plano_aux = plano_tratamento.iloc[0, 0]
        st.write(f'O plano de tratamento mais usado foi: {plano_aux}')
        
        if plano_aux == 'C':
            texto_plano_tratamento_mais_usado = st.text_input('O que sugere esse plano de tratamento ser o mais usado?', value=texto_plano_tratamento_mais_usado)
        else:
            texto_plano_tratamento_mais_usado = ''
        houve_mudancas = st.text_input('Houve mudança no comportamento usual das diarreias, quais as medidas tomadas?', value=houve_mudancas)

        houve_surtos = st.radio('Houve surtos?', ['Sim', 'Não'], index=0 if houve_surtos == 'Sim' else 1, horizontal=True)
        if houve_surtos == 'Sim':
            texto_surtos = st.text_input('Qual o total de surtos?', value=texto_surtos)
            texto_surtos2 = st.text_input('Nº surtos investigados?', value=texto_surtos2)
        else:
            texto_surtos = ''
            texto_surtos2 = ''
        
        colheu_material = st.radio('Houve colheita de material?', ['Sim', 'Não'], index=0 if colheu_material == 'Sim' else 1, horizontal=True)
        if colheu_material == 'Sim':
            texto_colheu_material = st.text_input('Qual o material colhido?', value=texto_colheu_material)
        else:
            texto_colheu_material = ''

            
            


col10, col11, col12 = st.columns([2,2,2])
with col10:
    if st.button("Enviar E-mail"):
        destinatario = 'isamucosta@gmail.com'
        pdf_path = f'relatorio_diarreia_{semana_selecionando}_{ano_selecionando}_{nome_ubs}.pdf'
        assunto = f"Relatório de Diarreia - Semana {semana_selecionando}, Ano {ano_selecionando}"
        corpo = f"Segue em anexo o relatório de diarreia para {nome_ubs}."

        if enviar_email(destinatario, assunto, corpo, pdf_path):
            st.success("E-mail enviado com sucesso!")
        else:
            st.error("Falha ao enviar e-mail. Verifique o console para mais detalhes.")

with col11:

    def get_db_connection():
        return mysql.connector.connect(
            host='prod-dev.myscriptcase.com',
            user='proddevm_samuel',
            password='Gayzao123',
            database='proddevm_sinan_notifica'
    )

    if st.button('Salvar Dados'):
        connection = get_db_connection()
        cursor = connection.cursor()

        # Verificar se já existe um registro para esta semana e ano
        check_query = """
        SELECT * FROM analise_casos 
        WHERE semana_selecionando = %s AND ano_selecionando = %s and ubs = %s
        """
        cursor.execute(check_query, (semana_selecionando, ano_selecionando, unidade_saude))
        existing_record = cursor.fetchone()

        if existing_record:
            # Se o registro existe, fazer um UPDATE
            update_query = """
            UPDATE analise_casos SET
                houve_aumento_casos = %s, fatores_aumento = %s,
                houve_mudanca_faixa_etaria = %s, faixa_etaria_mudanca = %s, sugestao_mudanca_faixa_etaria = %s,
                houve_casos_concentrados = %s, localidade_casos_concentrados = %s, plano_tratamento_mais_usado = %s,
                sugestao_plano_tratamento_mais_usado = %s, houve_mudancas_comportamento = %s, houve_surtos = %s,
                total_surtos = %s, surtos_investigados = %s, houve_colheita_material = %s, material_colhido = %s
            WHERE semana_selecionando = %s AND ano_selecionando = %s and ubs = %s
            """
            data = (
                aumento, texto_aumento,
                mudanca_faixa_etaria, texto_mudanca_faixa_etaria, texto_mudanca_faixa_etaria2,
                casos_concentrados, texto_casos_concentrados, plano_aux,
                texto_plano_tratamento_mais_usado, houve_mudancas, houve_surtos,
                texto_surtos, texto_surtos2, colheu_material, texto_colheu_material,
                semana_selecionando, ano_selecionando, unidade_saude
            )
            cursor.execute(update_query, data)
            st.success('Dados atualizados com sucesso!')
        else:
            # Se o registro não existe, fazer um INSERT
            insert_query = """
            INSERT INTO analise_casos (
                semana_selecionando, ano_selecionando, houve_aumento_casos, fatores_aumento,
                houve_mudanca_faixa_etaria, faixa_etaria_mudanca, sugestao_mudanca_faixa_etaria,
                houve_casos_concentrados, localidade_casos_concentrados, plano_tratamento_mais_usado,
                sugestao_plano_tratamento_mais_usado, houve_mudancas_comportamento, houve_surtos,
                total_surtos, surtos_investigados, houve_colheita_material, material_colhido, ubs
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                semana_selecionando, ano_selecionando, aumento, texto_aumento,
                mudanca_faixa_etaria, texto_mudanca_faixa_etaria, texto_mudanca_faixa_etaria2,
                casos_concentrados, texto_casos_concentrados, plano_aux,
                texto_plano_tratamento_mais_usado, houve_mudancas, houve_surtos,
                texto_surtos, texto_surtos2, colheu_material, texto_colheu_material, unidade_saude
            )
            cursor.execute(insert_query, data)
            st.success('Novos dados salvos com sucesso!')

        connection.commit()
        cursor.close()
        connection.close()
with col12:
    
    pdf = PDF3(semana_selecionando, ano_selecionando)  # Passando dt_in e dt_fin ao criar uma instância da classe PDF



    pdf.set_font('Times', '', 12)
    pdf.alias_nb_pages()

    pdf.add_page()
    eixo_y = 35
    eixo_x = 7.5
    pdf.create_table(faixa_etaria, eixo_x, eixo_y, 60)
    pdf.create_table(faixa_etaria_sangue, x=eixo_x+60+7.5, y=eixo_y, width=60)
    pdf.create_table(plano_tratamento, x=eixo_x+120+15, y=eixo_y, width=60)

    pdf.create_table(procedencia, eixo_x, eixo_y+75, 93.75)
    eixo_ynovo = eixo_y+75+5
    #Crianddo a parte textual

    eixo_x_novo = eixo_x+93.75+7.5


    pdf.set_font('Times', '', 12)
    largura_celula = 93.75  # Ajuste conforme necessário

    pdf.set_xy(eixo_x_novo, eixo_ynovo)
    pdf.multi_cell(largura_celula, 5, f'Houve aumento de casos? {aumento}')
    if aumento == 'Sim':
        pdf.set_font('Times', '', 8)
        pdf.set_xy(eixo_x_novo, pdf.get_y())
        pdf.multi_cell(largura_celula, 5, f'Os fatores que contribuíram para o aumento de casos foram: {texto_aumento}')
        pdf.set_font('Times', '', 12)

    pdf.set_xy(eixo_x_novo, pdf.get_y() + 3)
    pdf.multi_cell(largura_celula, 5, f'Houve mudança na faixa etária? {mudanca_faixa_etaria}')
    if mudanca_faixa_etaria == 'Sim':
        pdf.set_font('Times', '', 8)
        pdf.set_xy(eixo_x_novo, pdf.get_y())
        pdf.multi_cell(largura_celula, 5, f'A mudança na faixa etária foi para: {texto_mudanca_faixa_etaria}')
        pdf.set_xy(eixo_x_novo, pdf.get_y())
        pdf.multi_cell(largura_celula, 5, f'O que sugere essa mudança? {texto_mudanca_faixa_etaria2}')

        pdf.set_font('Times', '', 12)

    pdf.set_xy(eixo_x_novo, pdf.get_y() + 3)
    pdf.multi_cell(largura_celula, 5, f'Houve casos concentrados em alguma localidade? {casos_concentrados}')
    if casos_concentrados == 'Sim':
        pdf.set_font('Times', '', 8)
        pdf.set_xy(eixo_x_novo, pdf.get_y())
        pdf.multi_cell(largura_celula, 5, f'Os casos concentrados estão localizados em: {texto_casos_concentrados}')
        pdf.set_font('Times', '', 12)

    pdf.set_xy(eixo_x_novo, pdf.get_y() + 3)
    pdf.multi_cell(largura_celula, 5, f'O plano de tratamento mais usado foi: {plano_aux}')
    if plano_aux == 'C':
        pdf.set_font('Times', '', 8)
        pdf.set_xy(eixo_x_novo, pdf.get_y())
        pdf.multi_cell(largura_celula, 5, f'O que sugere esse plano de tratamento ser o mais usado? {texto_plano_tratamento_mais_usado}')
        pdf.set_font('Times', '', 12)

    pdf.set_xy(eixo_x_novo, pdf.get_y() + 3)
    pdf.multi_cell(largura_celula, 5, 'Houve mudança no comportamento usual das diarreias, quais as medidas tomadas?')
    if houve_mudancas != '':
        pdf.set_font('Times', '', 8)
        pdf.set_xy(eixo_x_novo, pdf.get_y())
        pdf.multi_cell(largura_celula, 5, f'As medidas tomadas foram: {houve_mudancas}')
        pdf.set_font('Times', '', 12)

    pdf.set_xy(eixo_x_novo, pdf.get_y() + 3)
    pdf.multi_cell(largura_celula, 5, f'Houve surtos? {houve_surtos}')
    if houve_surtos == 'Sim':
        pdf.set_font('Times', '', 8)
        pdf.set_xy(eixo_x_novo, pdf.get_y())
        pdf.multi_cell(largura_celula, 5, f'O total de surtos foi: {texto_surtos}')
        pdf.set_xy(eixo_x_novo, pdf.get_y())
        pdf.multi_cell(largura_celula, 5, f'O total de surtos invetigados foi: {texto_surtos2}')
        pdf.set_font('Times', '', 12)

    pdf.set_xy(eixo_x_novo, pdf.get_y() + 3)
    pdf.multi_cell(largura_celula, 5, f'Houve colheita de material? {colheu_material}')
    if colheu_material == 'Sim':
        pdf.set_font('Times', '', 8)
        pdf.set_xy(eixo_x_novo, pdf.get_y())
        pdf.multi_cell(largura_celula, 5, f'O material colhido foi: {texto_colheu_material}')
        pdf.set_font('Times', '', 12)
    pdf.output(f'relatorio_diarreia_{semana_selecionando}_{ano_selecionando}_{nome_ubs}.pdf', 'F')

    with open(f'relatorio_diarreia_{semana_selecionando}_{ano_selecionando}_{nome_ubs}.pdf', "rb") as file:
            file_bytes = file.read()
            btn = st.download_button(
                label="Baixar PDF",
                data=file_bytes,
                file_name=f'relatorio_diarreia_{semana_selecionando}_{ano_selecionando}_{nome_ubs}.pdf'
            )