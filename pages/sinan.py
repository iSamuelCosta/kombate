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

else:
    m = folium.Map(location=[-22.4269, -45.453], zoom_start=12)

    focos_geo = conn.query(query_geo_foco_data(data_filtro[0], data_filtro[1]), ttl=600)

    aplicados_larvicidas=conn.query(query_geo_larvicida_data(data_filtro[0], data_filtro[1]), ttl=600)
    imoveis_fechados = conn.query(query_imoveis_fechados_data(data_filtro[0], data_filtro[1]), ttl=600)
    imoveis_visitados = conn.query(query_imoveis_visitados_data(data_filtro[0], data_filtro[1]), ttl=600)
    imoveis_recuperados = conn.query(query_imoveis_recuperados_data(data_filtro[0], data_filtro[1]), ttl=600)
    from folium import CustomIcon

    from folium.plugins import MarkerCluster


    icon_create_function = """\
    function(cluster) {
        return L.divIcon({
            html: '<div style="background-color: #800080; color: white; border-radius: 50%; padding: 5px; text-align: center; font-size: 12px;">' +
                '<b>' + cluster.getChildCount() + '</b>' +
                '</div>',
            className: 'marker-cluster',
            iconSize: new L.Point(40, 40)
        });
    }"""

    icon_create_function2 = """\
    function(cluster) {
        return L.divIcon({
            html: '<div style="background-color: #ff0000; color: white; border-radius: 50%; padding: 5px; text-align: center; font-size: 12px;">' +
                '<b>' + cluster.getChildCount() + '</b>' +
                '</div>',
            className: 'marker-cluster',
            iconSize: new L.Point(40, 40)
        });
    }"""

    icon_create_function3 = """\
    function(cluster) {
        return L.divIcon({
            html: '<div style="background-color: #05313d; color: white; border-radius: 50%; padding: 5px; text-align: center; font-size: 12px;">' +
                '<b>' + cluster.getChildCount() + '</b>' +
                '</div>',
            className: 'marker-cluster',
            iconSize: new L.Point(40, 40)
        });
    }"""

    icon_create_function4 = """\
    function(cluster) {
        return L.divIcon({
            html: '<div style="background-color: #008000; color: white; border-radius: 50%; padding: 5px; text-align: center; font-size: 12px;">' +
                '<b>' + cluster.getChildCount() + '</b>' +
                '</div>',
            className: 'marker-cluster',
            iconSize: new L.Point(40, 40)
        });
    }"""

    icon_create_function5 = """\
    function(cluster) {
        return L.divIcon({
            html: '<div style="background-color: #808080; color: white; border-radius: 50%; padding: 5px; text-align: center; font-size: 12px;">' +
                '<b>' + cluster.getChildCount() + '</b>' +
                '</div>',
            className: 'marker-cluster',
            iconSize: new L.Point(40, 40)
        });
    }"""



    # Exemplo com aplicados_larvicidas
    

    # Exemplo com focos_geo
    

    
    casos_confirmados_bairro = conn2.query(query_bairros_confirmados(data_filtro[0], data_filtro[1]), ttl=600)


    
    
    sele1, sele2, sele3 = st.columns(3)
    with sele1:
        Larvi = st.toggle("Ativar a aplicação de larvicidas")
    if Larvi:
        if not aplicados_larvicidas.empty:
            aplicados_larvicidas[['lat', 'long']] = aplicados_larvicidas['geo'].str.split(', ', expand=True)
            aplicados_larvicidas['lat'] = aplicados_larvicidas['lat'].astype(float)
            aplicados_larvicidas['long'] = aplicados_larvicidas['long'].astype(float)

            marker_cluster = MarkerCluster(icon_create_function=icon_create_function).add_to(m)

            for index, row in aplicados_larvicidas.iterrows():
                
                folium.Marker(
                    location=[row['lat'], row['long']], 
                    popup="Larvicida aplicado", 
                    tooltip=f'Larvicida aplicado na data de: <br> {row["Data"]} <br> Pelo agente: {row["nome"]}',
                    icon=folium.Icon(color='purple', icon="info-sign")
                ).add_to(marker_cluster)

    with sele2:
        focos = st.toggle("Ativar os focos")
    if focos:
        if not focos_geo.empty:
            focos_geo[['lat', 'long']] = focos_geo['geo'].str.split(', ', expand=True)
            focos_geo['lat'] = focos_geo['lat'].astype(float)
            focos_geo['long'] = focos_geo['long'].astype(float)

            marker_cluster = MarkerCluster(icon_create_function=icon_create_function2).add_to(m)

            for index, row in focos_geo.iterrows():
                
                folium.Marker(
                    location=[row['lat'], row['long']], 
                    popup="Foco dengue", 
                    tooltip=f'Foco encontrado na data: <br> {row["Data"]} <br> Pelo agente: {row["nome"]}',
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(marker_cluster)
    with sele3:
        fechados = st.toggle("Ativar os fechados")
    if fechados:
        if not imoveis_fechados.empty:
            imoveis_fechados[['lat', 'long']] = imoveis_fechados['geo'].str.split(', ', expand=True)
            # Converter as novas colunas para tipo float
            imoveis_fechados['lat'] = imoveis_fechados['lat'].astype(float)
            imoveis_fechados['long'] = imoveis_fechados['long'].astype(float)
            imoveis_fechados = imoveis_fechados.drop(imoveis_fechados.index[0])

            marker_cluster = MarkerCluster(icon_create_function=icon_create_function3).add_to(m)

            for index, row in imoveis_fechados.iterrows():
                
                folium.Marker(
                    location=[row['lat'], row['long']], 
                    popup="Foco dengue", 
                    tooltip=f'Imovel fechado na data: <br> {row["Data"]} <br> Pelo agente: {row["nome"]}',
                    icon=folium.Icon(color="black", icon="info-sign")
                ).add_to(marker_cluster)

    sele4, sele5, sele6 = st.columns(3)
    with sele4:
        confirmados = st.toggle("Ativar os casos confirmados")
    if confirmados:
        teste = pd.read_csv('lat_long_final - Sheet1 (1).csv')

        bairro_visitas = casos_confirmados_bairro.applymap(lambda x: str(x).upper() if isinstance(x, str) else x)
        teste = teste.applymap(lambda x: str(x).upper() if isinstance(x, str) else x)
        df_teste=bairro_visitas.merge(teste, left_on='nome_bairro', right_on='bairro_nome')
        colunas_para_substituir = ['latitude', 'longitude']
        df_teste[colunas_para_substituir] = df_teste[colunas_para_substituir].applymap(lambda x: str(x).replace(',', '.'))
        df_teste['latitude'] = df_teste['latitude'].astype(float)
        df_teste['longitude'] = df_teste['longitude'].astype(float)

        data = (
            np.random.normal(size=(100, 3)) * np.array([[1, 1, 1]]) + np.array([[48, 5, 1]])
        ).tolist()

        df_aux = df_teste[['Quantidade', 'latitude', 'longitude']]
        heat_data = df_aux[['latitude', 'longitude', 'Quantidade']].values.tolist()
        HeatMap(heat_data, opacity=0.2).add_to(m)

    with sele5:
        visitados = st.toggle("Ativar os visitados")
    if visitados:
        if not imoveis_visitados.empty:
            imoveis_visitados[['lat', 'long']] = imoveis_visitados['geo'].str.split(', ', expand=True)
            # Converter as novas colunas para tipo float
            imoveis_visitados['lat'] = imoveis_visitados['lat'].astype(float)
            imoveis_visitados['long'] = imoveis_visitados['long'].astype(float)
            imoveis_visitados = imoveis_visitados.drop(imoveis_visitados.index[0])

            marker_cluster = MarkerCluster(icon_create_function=icon_create_function4).add_to(m)

            for index, row in imoveis_visitados.iterrows():
                
                folium.Marker(
                    location=[row['lat'], row['long']], 
                    popup="Foco dengue", 
                    tooltip=f'Imovel visitado na data: <br> {row["Data"]} <br> Pelo agente: {row["nome"]}',
                    icon=folium.Icon(color="green", icon="info-sign")
                ).add_to(marker_cluster)

    with sele6:
        recuperados = st.toggle("Ativar os recuperados")
    if recuperados:
        if not imoveis_recuperados.empty:
            imoveis_recuperados[['lat', 'long']] = imoveis_recuperados['geo'].str.split(', ', expand=True)
            # Converter as novas colunas para tipo float
            imoveis_recuperados['lat'] = imoveis_recuperados['lat'].astype(float)
            imoveis_recuperados['long'] = imoveis_recuperados['long'].astype(float)
            imoveis_recuperados = imoveis_recuperados.drop(imoveis_recuperados.index[0])

            marker_cluster = MarkerCluster(icon_create_function=icon_create_function5).add_to(m)

            for index, row in imoveis_recuperados.iterrows():
                
                folium.Marker(
                    location=[row['lat'], row['long']], 
                    popup="Foco dengue", 
                    tooltip=f'Imovel recuperado na data: <br> {row["Data"]} <br> Pelo agente: {row["nome"]}',
                    icon=folium.Icon(color="gray", icon="info-sign")
                ).add_to(marker_cluster)


        
    col1, col2 = st.columns([5,1])

    with col1:
        folium_static(m, width=None, height=800)
    with col2:
        if Larvi:
            st.write("Está aparecendo no mapa as aplicações de larvicidas na cor Roxa" )
        if focos:
            st.write("Está aparecendo no mapa as aplicações de larvicidas na cor Vermelha" )
        if fechados:
            st.write("Está aparecendo no mapa as aplicações de larvicidas na cor Preta" )
        if confirmados:
            st.write("Está aparecendo um mapa de calor dos casos confirmados de dengue" )
        if visitados:
            st.write("Está aparecendo no mapa as visitas na cor Verde" )
        if recuperados:
            st.write("Está aparecendo no mapa os imóveis recuperados na cor Cinza" )



