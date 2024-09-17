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

conn = st.connection('mysql', type='sql') 
conn2 = st.connection('mysql_2', type='sql')   
col1, col2, col3 = st.columns([4,1,1])

with col1:
    st.title('Relátorio semanal dos agentes')

ano_diarreia = conn2.query(query_ano_diarreia(), ttl=60)

with col2:
    ano_selecionando = st.selectbox('Selecione o ano', ano_diarreia['ano'].unique())
    semana_diarreia = conn2.query(query_diarreia_semana_epidemiologica(ano_selecionando), ttl=60)

with col3:
    semana_selecionando = st.selectbox('Selecione a semana epidêmica', semana_diarreia['semana'].unique())

df_agentes = conn.query(query_agentes_unicos(), ttl=600)
df_datas = conn2.query(datas_semana_epidemiologica(ano_selecionando, semana_selecionando), ttl=600)
data_inicial = df_datas['data_inicio'].iloc[0]
data_final = df_datas['data_fim'].iloc[0]

nome_funcionario = st.selectbox("Escolha o funcionário", df_agentes['nome'])

filtro_nome_funcionario = df_agentes[df_agentes['nome']==nome_funcionario]
id_funcionario = filtro_nome_funcionario['id'].iloc[0]

st.subheader(f'{nome_funcionario} - Semana Epidêmica {semana_selecionando} do Ano {ano_selecionando}')

df_producao = conn.query(query_resumo_producao_semanal(data_inicial, data_final, id_funcionario), ttl=600)


df_visitas_bairro = conn.query(query_visitas_agentes_bairro(data_inicial, data_final, id_funcionario), ttl=600)
fig_bairro = criar_grafico_horizontal(df_visitas_bairro,"Quantidade de Visitas", 'Bairro', 'Grafico bairros')


col1, col2 = st.columns(2)
with col1:
    with st.container(height=350):
        st.altair_chart(fig_bairro, use_container_width=True)

df_visitas_tipo = conn.query(query_visitas_agentes_tipo_imovel(data_inicial, data_final, id_funcionario), ttl=600)
fig_tipo = criar_grafico_horizontal(df_visitas_tipo,"Quantidade de Visitas", 'Tipo', 'Grafico tipos de imovel')

with col2:
    with st.container(height=350):
        st.altair_chart(fig_tipo, use_container_width=True)
st.divider()

df_visitas_dia = conn.query(query_visitas_dia_agente(data_inicial, data_final, id_funcionario), ttl=600)
visitas_por_dia = df_visitas_dia.tail(30)
st.divider()
fig_visitas_dia = criar_grafico_linhas(visitas_por_dia, 'Dia', 'Quantidade', "Visitas por dia")
with st.container():
    st.altair_chart(fig_visitas_dia, use_container_width=True)
st.divider()

df_visitas_horario = conn.query(query_visitas_horario(data_inicial, data_final, id_funcionario), ttl=600)
fig_visitas_horario = criar_grafico_linhas(df_visitas_horario, 'Hora', 'Numero de Visitas', "Visitas por hora")
with st.container():
    st.altair_chart(fig_visitas_horario, use_container_width=True)
st.divider()

dt_in = pd.to_datetime(data_inicial, format='%d/%m/%Y')
dt_in=dt_in.strftime('%d/%m/%Y')
dt_fin = pd.to_datetime(data_final, format='%d/%m/%Y')
dt_fin=dt_fin.strftime('%d/%m/%Y')
pdf = PDF(dt_in, dt_fin)  # Passando dt_in e dt_fin ao criar uma instância da classe PDF

pdf.set_font('Times', '', 12)
pdf.add_page()
pdf.image('imagens/fundo_certo.png',0,0,210,297)
municipio = 'Itajubá'
pdf.text(20.24,51.0, municipio)
pdf.text(94,51.0, nome_funcionario)
pdf.text(85,62.3, dt_in)
pdf.text(118,62.3, dt_fin)

semana_selecionando_str = str(semana_selecionando)
pdf.text(172,62.3, semana_selecionando_str)
ano_selecionando_str = str(ano_selecionando)
pdf.text(185,62.3, ano_selecionando_str)

pdf.text(32.15, 102, str(df_producao.iloc[0, 6]))
pdf.text(48, 102, str(df_producao.iloc[0, 7]))
pdf.text(64, 102, str(df_producao.iloc[0, 8]))
pdf.text(80, 102, str(df_producao.iloc[0, 10]))
pdf.text(96, 102, str(df_producao.iloc[0, 9]))
pdf.text(105, 102, str(df_producao.iloc[0, 2]))

pdf.text(113, 102, str(df_producao.iloc[0, 13]))

pdf.text(126, 102, str(df_producao.iloc[0, 12]))

pdf.text(165, 102, str(df_producao.iloc[0, 5]))
pdf.text(176, 102, str(df_producao.iloc[0, 4]))

pdf.text(189, 102, str(df_producao.iloc[0, 3]))

pdf.output(f'relatorio_geral_{nome_funcionario}_{ano_selecionando}_{semana_selecionando}.pdf', 'F')

with open(f'relatorio_geral_{nome_funcionario}_{ano_selecionando}_{semana_selecionando}.pdf', "rb") as file:
        file_bytes = file.read()
        btn = st.download_button(
            label="Baixar PDF",
            data=file_bytes,
            file_name=f'relatorio_geral_{nome_funcionario}_{ano_selecionando}_{semana_selecionando}.pdf'
        )