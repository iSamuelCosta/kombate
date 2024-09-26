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
import mysql.connector
from cria_imagens import *

import time
from gerar_pdf import *
st.set_page_config(layout='wide', page_title="Nota de Avaliação dos Serviços da Prefeitura")

def formata_numero(valor, prefixo=''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            if valor.is_integer():  # Verifica se o valor é um número inteiro
                return f'{prefixo} {int(valor)} {unidade}'
            else:
                return f'{prefixo} {valor: .1f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor: .1f} milhões'


def formata_metrica(valor):
     return f'{valor: .2f}'


conn = st.connection('mysql', type='sql')


df_data = conn.query(query_datas(), ttl=600)

caminho_imagem_kombate = "imagens/Logo_kombate.svg"
caminho_imagem_itajuba="imagens/logo_itajuba.svg"

left_co,a, cent_co,b,last_co = st.columns([2,1,3,1,2])



with cent_co:
    st.image(caminho_imagem_itajuba, use_column_width=True)

M_teve_larvida = conn.query(query_metric_teve_larvicida('2020-01-01', '2025-01-01'), ttl=600)
M_teve_larvida_7 = conn.query(query_metric_teve_larvicida_7_dias(), ttl=600)
M_quantidade_visitas = conn.query(query_metric_quantidade_visitas('2020-01-01', '2025-01-01'), ttl=600)
M_quantidade_visitas_7 = conn.query(query_quantidade_visitas_7_dias(), ttl=600)
qtd_visitas = M_quantidade_visitas['numero_de_linhas'].mean()
qtd_larvicida = M_teve_larvida['numero_de_linhas'].mean()
qtd_visitas_7_dias=M_quantidade_visitas_7['numero_de_linhas'].mean()
qtd_larvicida_7_dias = M_teve_larvida_7['numero_de_linhas'].mean()

with st.container(border=True):
    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown("<h2 style='text-align: center;'>Resumo Kombate</h2>", unsafe_allow_html=True)
    with col2:
        dt_mais_recente = conn.query("SELECT max(date_time) as max_date from visita", ttl=600)
        dt_mais_recente = pd.to_datetime(dt_mais_recente['max_date'].iloc[0]).strftime('%d/%m/%Y')
        st.markdown(f"<h2 style='text-align: center;'>Data mais recente: {dt_mais_recente}</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3,1])
    with col2:
        with st.container(height=450):
            
            
            st.metric("Quantidade de Visitas total", formata_numero(qtd_visitas))
            st.metric("Quantidade de larvecidas total", formata_numero(qtd_larvicida))
        
            st.metric("Quantidade de Visitas ultimos 7 dias", formata_numero(qtd_visitas_7_dias))
            st.metric("Quantidade de larvecidas ultimos 7 dias", formata_numero(qtd_larvicida_7_dias))
        

    visitas_por_mes=conn.query(query_visitas_mes(), ttl=600)
    fig_visitas_mes = criar_grafico_linhas(visitas_por_mes, 'mes_ano', 'numero_de_linhas', "Visitas por mês")
    with col1:
        with st.container(height=450):
            st.altair_chart(fig_visitas_mes, use_container_width=True)

conn2 = st.connection('mysql_2', type='sql')

df_quantidade_notificacoes = conn2.query("select count(id) as Contagem from sinan_dengue", ttl=600)
df_quantidade_notificacoes_estagio_12 = conn2.query("select count(id) as Contagem from sinan_dengue where status_id in (1,2)", ttl=600)
df_notificacoes_mes = conn2.query("select count(id) as Contagem, DATE_FORMAT(data_notificacao, '%m/%y') as mes_ano from sinan_dengue group by mes_ano", ttl=600)

with st.container(border=True):
    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown("<h2 style='text-align: center;'>Resumo Epidemio</h2>", unsafe_allow_html=True)
    with col2:
        dt_mais_recente = conn2.query("SELECT max(data_notificacao) as max_date from sinan_dengue", ttl=600)
        dt_mais_recente = pd.to_datetime(dt_mais_recente['max_date'].iloc[0]).strftime('%d/%m/%Y')
        st.markdown(f"<h2 style='text-align: center;'>Data mais recente: {dt_mais_recente}</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3,1])
    with col2:
        with st.container(height=450):
            st.metric("Quantidade de Notificações", formata_numero(df_quantidade_notificacoes['Contagem'].iloc[0]))
            st.metric("Quantidade de Notificações em Estágio 1 e 2", formata_numero(df_quantidade_notificacoes_estagio_12['Contagem'].iloc[0]))
        
    fig_notificacoes_mes = criar_grafico_linhas(df_notificacoes_mes, 'mes_ano', 'Contagem', "Notificações por mês")
    with col1:
        with st.container(height=450):  
            st.altair_chart(fig_notificacoes_mes, use_container_width=True)

conn3 = st.connection('mysql_5', type='sql')
df_quantidade_ordens = conn3.query("select count(id) as Contagem from service_order", ttl=600)
df_quantidade_inspessoes = conn3.query("select count(id) as Contagem from inspection", ttl=600)
df_ordens_mes = conn3.query("select count(id) as Contagem, DATE_FORMAT(created_at, '%m/%y') as mes_ano from service_order group by mes_ano", ttl=600)

with st.container(border=True):
    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown("<h2 style='text-align: center;'>Resumo Fiscalização</h2>", unsafe_allow_html=True)
    with col2:
        dt_mais_recente = conn3.query("SELECT max(created_at) as max_date from service_order", ttl=600)
        dt_mais_recente = pd.to_datetime(dt_mais_recente['max_date'].iloc[0]).strftime('%d/%m/%Y')
        st.markdown(f"<h2 style='text-align: center;'>Data mais recente: {dt_mais_recente}</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3,1])
    with col2:
        with st.container(height=450):
            st.metric("Quantidade de Ordens de Serviço", formata_numero(df_quantidade_ordens['Contagem'].iloc[0]))
            st.metric("Quantidade de Inspeções", formata_numero(df_quantidade_inspessoes['Contagem'].iloc[0]))
    with col1:
        fig_ordens_mes = criar_grafico_linhas(df_ordens_mes, 'mes_ano', 'Contagem', "Ordens de Serviço por mês")
        with st.container(height=450):
            st.altair_chart(fig_ordens_mes, use_container_width=True)
            

conn4 = st.connection('mysql_4', type='sql')
df_quantidade_arquivos = conn4.query("select count(id) as Contagem from arquivo", ttl=600)
df_quantidade_arquivos_mes = conn4.query("select count(id) as Contagem, DATE_FORMAT(created_at, '%m/%y') as mes_ano from arquivo group by mes_ano", ttl=600)

with st.container(border=True):
    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown("<h2 style='text-align: center;'>Resumo GED</h2>", unsafe_allow_html=True)
    with col2:
        dt_mais_recente = conn4.query("SELECT max(created_at) as max_date from arquivo", ttl=600)
        dt_mais_recente = pd.to_datetime(dt_mais_recente['max_date'].iloc[0]).strftime('%d/%m/%Y')
        st.markdown(f"<h2 style='text-align: center;'>Data mais recente: {dt_mais_recente}</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3,1])
    with col2:
        with st.container(height=450):
            st.metric("Quantidade de Arquivos", formata_numero(df_quantidade_arquivos['Contagem'].iloc[0]))
    with col1:
        fig_arquivos_mes = criar_grafico_linhas(df_quantidade_arquivos_mes, 'mes_ano', 'Contagem', "Arquivos por mês")
        with st.container(height=450):
            st.altair_chart(fig_arquivos_mes, use_container_width=True)
            
        