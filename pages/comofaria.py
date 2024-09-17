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
conn2 = st.connection('mysql_2', type='sql')


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




focos_geo = conn.query(query_geo_foco(data_filtro[0], data_filtro[1]), ttl=600)

focos_geo[['lat', 'long']] = focos_geo['geo'].str.split(', ', expand=True)
    # Converter as novas colunas para tipo float
focos_geo['lat'] = focos_geo['lat'].astype(float)
focos_geo['long'] = focos_geo['long'].astype(float)


aplicados_larvicidas=conn.query(query_geo_larvicida(data_filtro[0], data_filtro[1]), ttl=600)
aplicados_larvicidas[['lat', 'long']] = aplicados_larvicidas['geo'].str.split(', ', expand=True)
    # Converter as novas colunas para tipo float
aplicados_larvicidas['lat'] = aplicados_larvicidas['lat'].astype(float)
aplicados_larvicidas['long'] = aplicados_larvicidas['long'].astype(float)


imoveis_fechados = conn.query(query_imoveis_fechados(data_filtro[0], data_filtro[1]), ttl=600)
imoveis_fechados[['lat', 'long']] = imoveis_fechados['geo'].str.split(', ', expand=True)
    # Converter as novas colunas para tipo float
imoveis_fechados['lat'] = imoveis_fechados['lat'].astype(float)
imoveis_fechados['long'] = imoveis_fechados['long'].astype(float)
imoveis_fechados = imoveis_fechados.drop(imoveis_fechados.index[0])


casos_confirmados_bairro = conn2.query(query_bairros_confirmados(data_filtro[0], data_filtro[1]), ttl=600)


teste = pd.read_csv('lat_long_final - Sheet1 (1).csv')

bairro_visitas = casos_confirmados_bairro.applymap(lambda x: str(x).upper() if isinstance(x, str) else x)
teste = teste.applymap(lambda x: str(x).upper() if isinstance(x, str) else x)
df_teste=bairro_visitas.merge(teste, left_on='nome_bairro', right_on='bairro_nome')
colunas_para_substituir = ['latitude', 'longitude']
df_teste[colunas_para_substituir] = df_teste[colunas_para_substituir].applymap(lambda x: str(x).replace(',', '.'))
df_teste['latitude'] = df_teste['latitude'].astype(float)
df_teste['longitude'] = df_teste['longitude'].astype(float)

difdata = data_filtro[1] - data_filtro[0]
if difdata.days != 0:
    aux = 100 / difdata.days
    aux2 = 250 / difdata.days
else:
    aux = 10
    aux2 = 150

COLOR_BREWER_BLUE_SCALE = [
    [240, 249, 232],
    [204, 235, 197],
    [168, 221, 181],
    [123, 204, 196],
    [67, 162, 202],
    [8, 104, 172],
]

layer = pdk.Layer(
    'ScatterplotLayer',
    data=df_teste,
    get_position='[longitude, latitude]',
    get_radius=f'Quantidade * {aux}',  # Ajuste o multiplicador conforme necessário
    get_fill_color=[32, 252, 3],  # Cor vermelha para marcadores
    pickable=True
)

layer2 = pdk.Layer(
        'ScatterplotLayer',
        data=imoveis_fechados,
        get_position='[long, lat]',
        get_radius=f'Quantidade * {aux2}',  # Ajuste o multiplicador conforme necessário
        get_fill_color=[32, 252, 255],
        opacity=0.4,  # Cor vermelha para marcadores
        pickable=True
    )

focos = pdk.Layer(
    "HeatmapLayer",
    data=focos_geo,
    opacity=0.9,
    get_position=["long", "lat"],
    aggregation=pdk.types.String("MEAN"),
    
    threshold=1,
    get_weight="Quantidade",
    pickable=True,
)

larvecidas = pdk.Layer(
    "HeatmapLayer",
    data=aplicados_larvicidas,
    opacity=0.9,
    get_position=["long", "lat"],
    aggregation=pdk.types.String("MEAN"),
    color_range=COLOR_BREWER_BLUE_SCALE,
    threshold=1,
    get_weight="Quantidade",
    pickable=True,
)




# Criar o mapa
view_state = pdk.ViewState(latitude=-22.4269, longitude=-45.453, zoom=12.5)
tooltip = {'html': 'Quantidade de Casos confirmados: {Quantidade} bairro: {nome_bairro}'}

map_ = pdk.Deck(
    layers=[layer2,layer,larvecidas,focos ],
    initial_view_state=view_state,
    tooltip=tooltip
)

with st.container(height=600):
    st.markdown("<h4 style='text-align: center;'>Visitas por bairro</h4>", unsafe_allow_html=True)
    st.pydeck_chart(map_,use_container_width=True)

st.data_editor(imoveis_fechados)