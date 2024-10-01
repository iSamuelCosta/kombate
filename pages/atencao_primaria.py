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
st.set_page_config(layout='wide', page_title="Nota de Avaliação dos Serviços da Prefeitura")
import time
from gerar_pdf import *



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


conn = st.connection('mysql_9', type='sql')




caminho_imagem_kombate = "imagens/Logo_kombate.svg"
caminho_imagem_itajuba="imagens/logo_itajuba.svg"

left_co,a, cent_co,b,last_co = st.columns([2,1,3,1,2])



with cent_co:
    st.image(caminho_imagem_itajuba, use_column_width=True)

df=conn.query("""WITH RankedVendas AS (
    SELECT 
        ROW_NUMBER() OVER (PARTITION BY cns_cidadao ORDER BY dataatendimento desc) AS row_num,
        hipertensao_new.*
    FROM 
        hipertensao_new
)
SELECT 
    *
FROM 
    RankedVendas
WHERE 
    row_num = 1
""", ttl=600)
st.title("Atenção Primária Hipertensão")
df['dataatendimento'] = pd.to_datetime(df['dataatendimento'])


df['dif_meses'] = (pd.Timestamp.now().year - df['dataatendimento'].dt.year) * 12 + (pd.Timestamp.now().month - df['dataatendimento'].dt.month)

#Calculando a porcentagem com atendimento no ultimo 6 meses
df['atendimento_6_meses'] = df['dif_meses'] <= 6
atendimentos_6_meses_count = df['atendimento_6_meses'].sum()
st.write(f"Total de atendimentos nos últimos 6 meses: {atendimentos_6_meses_count}")
atendimentos_total = df.shape[0]
st.write(f"Total de atendimentos: {atendimentos_total}")
porcentagem_hiper = atendimentos_6_meses_count / atendimentos_total
st.write(f"Porcentagem de atendimentos nos últimos 6 meses: {porcentagem_hiper:.2%}")
df_criar_grafico_hipertensao = pd.DataFrame({
    'Atendimentos': [atendimentos_6_meses_count, atendimentos_total - atendimentos_6_meses_count],
    'Legenda': ['Atendimentos nos últimos 6 meses', 'Pessoas']
})

fig_hiper = cria_grafico_pizza(df_criar_grafico_hipertensao,'Atendimentos',"Legenda","Atendimentos Hipertensão",0.5, 'middle')
st.altair_chart(fig_hiper, use_container_width=True)

df2=conn.query("""WITH RankedVendas AS (
    SELECT 
        ROW_NUMBER() OVER (PARTITION BY cns_cidadao ORDER BY dataatendimento desc) AS row_num,
        diabetes_novo.*
    FROM 
        diabetes_novo
)
SELECT 
    *
FROM 
    RankedVendas
WHERE 
    row_num = 1
""", ttl=600)

df['dataatendimento'] = pd.to_datetime(df['dataatendimento'])

st.title("Atenção Primária Diabetes")
df2['dataatendimento'] = pd.to_datetime(df2['dataatendimento'])
df2['dif_meses'] = (pd.Timestamp.now().year - df2['dataatendimento'].dt.year) * 12 + (pd.Timestamp.now().month - df2['dataatendimento'].dt.month)
df2['atendimento_6_meses'] = df2['dif_meses'] <= 6
atendimentos_6_meses_count = df2['atendimento_6_meses'].sum()
st.write(f"Total de atendimentos nos últimos 6 meses: {atendimentos_6_meses_count}")
atendimentos_total = df2.shape[0]
st.write(f"Total de atendimentos: {atendimentos_total}")
porcentagem_diabetes = atendimentos_6_meses_count / atendimentos_total
st.write(f"Porcentagem de atendimentos nos últimos 6 meses: {porcentagem_diabetes:.2%}")
df_criar_grafico_diabetes = pd.DataFrame({
    'Atendimentos': [atendimentos_6_meses_count, atendimentos_total - atendimentos_6_meses_count],
    'Legenda': ['Atendimentos nos últimos 6 meses', 'Pessoas']
})
st.altair_chart(cria_grafico_pizza(df_criar_grafico_diabetes,'Atendimentos',"Legenda","Atendimentos Diabetes",0.5, 'middle'), use_container_width=True)