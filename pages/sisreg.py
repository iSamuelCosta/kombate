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


def formata_metrica(valor):
     return f'{valor: .2f}'


conn = st.connection('mysql', type='sql')
conn2 = st.connection('mysql_2', type='sql')
conn3 = st.connection('mysql_3', type='sql')

df_data = conn.query(query_datas(), ttl=600)
caminho_imagem_kombate = "imagens/Logo_kombate.svg"
caminho_imagem_itajuba="imagens/logo_itajuba.svg"

left_co,a, cent_co,b,last_co = st.columns([2,1,3,1,2])

with left_co:
     st.image(caminho_imagem_itajuba, use_column_width=False)

with cent_co:
    st.image(caminho_imagem_kombate, use_column_width=True)


with last_co:
    
    data_filtro = st.date_input('Selecione um período', (df_data['menor_data'].min(), df_data['maior_data'].max()), format="DD/MM/YYYY")

if len(data_filtro) < 2:
    
    with st.spinner('Esperando uma segunda data...'):
        time.sleep(5)





df = conn3.query(query_sisreg(), ttl=600)
st.dataframe(df)
filtro_unidade = st.multiselect('Selecione a unidade de saúde', df['unidade_saude_solicitante'].unique())

df_filtrado = df[df['unidade_saude_solicitante'].isin(filtro_unidade)]

df_solicitacao_medico = df[['profissional', 'solicitacoes_pendentes']]

df_solicitacao_medico = df_solicitacao_medico.groupby('profissional').sum().reset_index()

fig_solicitacao_medico = criar_grafico_horizontal(df_solicitacao_medico, 'solicitacoes_pendentes', 'profissional', 'Solicitações Pendentes por Médico')
with st.container(height=500):
    st.altair_chart(fig_solicitacao_medico, use_container_width=True)