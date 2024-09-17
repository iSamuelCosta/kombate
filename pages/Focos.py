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

with left_co:
     st.image(caminho_imagem_itajuba, use_column_width=False)

with cent_co:
    st.image(caminho_imagem_kombate, use_column_width=True)


with last_co:
    
    data_filtro = st.date_input('Selecione um período', (df_data['menor_data'].min(), df_data['maior_data'].max()), format="DD/MM/YYYY")


##################

if len(data_filtro) < 2:
    
    with st.spinner('Esperando uma segunda data...'):
        time.sleep(5)

else:

    difdata = data_filtro[1] - data_filtro[0]
    
    
    if difdata.days != 0:
        aux = 50 / difdata.days
        aux2 = 150 / difdata.days
    else:
        aux = 50
        aux2 = 150

    focos_geo=conn.query(query_geo_foco(data_filtro[0], data_filtro[1]), ttl=600)
    if not focos_geo.empty:
        focos_geo[['lat', 'long']] = focos_geo['geo'].str.split(', ', expand=True)

    # Converter as novas colunas para tipo float
        focos_geo['lat'] = focos_geo['lat'].astype(float)
        focos_geo['long'] = focos_geo['long'].astype(float)

        
        layer2 = pdk.Layer(
            'ScatterplotLayer',
            data=focos_geo,
            get_position='[long, lat]',
            get_radius=f'Quantidade * {aux2}',  # Ajuste o multiplicador conforme necessário
            get_fill_color=[32, 252, 3],  # Cor vermelha para marcadores
            pickable=True
        )

        # Estado inicial da visualização
        view_state2 = pdk.ViewState(
            latitude=-22.4269,  # Centralize no ponto desejado
            longitude=-45.453,
            zoom=12.5
        )
        tooltip = {'html': 'Quantidade de Focos: {Quantidade}'}
        # Criar o mapa com Deck.gl
        map_2 = pdk.Deck(
            layers=[layer2],
            initial_view_state=view_state2,
            tooltip=tooltip
        )

        with st.container(height=600):
            st.markdown("<h4 style='text-align: center;'>Mapa de calor aplicado Larvecida</h4>", unsafe_allow_html=True)
            
            st.pydeck_chart(map_2, use_container_width=True)
    else: 
        st.text("Não foram encontrados Focos")
    aplicados_larvicidas=conn.query(query_geo_larvicida(data_filtro[0], data_filtro[1]), ttl=600)

    if not aplicados_larvicidas.empty:

        aplicados_larvicidas[['lat', 'long']] = aplicados_larvicidas['geo'].str.split(', ', expand=True)

        COLOR_BREWER_BLUE_SCALE = [
        [240, 249, 232],
        [204, 235, 197],
        [168, 221, 181],
        [123, 204, 196],
        [67, 162, 202],
        [8, 104, 172],
        ]

        aplicados_larvicidas['lat'] = aplicados_larvicidas['lat'].astype(float)
        aplicados_larvicidas['long'] = aplicados_larvicidas['long'].astype(float)
    
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=aplicados_larvicidas,
            get_position='[long, lat]',
            get_radius=f'Quantidade * {aux}',  # Ajuste o multiplicador conforme necessário
            get_fill_color=[32, 252, 250],  # Cor vermelha para marcadores
            pickable=True
        )

        # Criar o mapa
        view_state = pdk.ViewState(latitude=-22.4269, longitude=-45.453, zoom=12.5)
        tooltip = {'html': 'Quantidade de Larvecidadas: {Quantidade}'}

        map_ = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip
        )


        # Exibir o mapa no Streamlit
        
        
        with st.container(height=600):
            st.markdown("<h4 style='text-align: center;'>Mapa de calor aplicado Larvecida</h4>", unsafe_allow_html=True)
            
            st.pydeck_chart(map_, use_container_width=True)
    else: 
        st.text('Ainda não foi aplicado larvecida')

    bairros_larvecidas=conn.query(query_bairro_larvecida(data_filtro[0], data_filtro[1]), ttl=600)
    
    fig_bairros_larvecidas = criar_grafico_horizontal(bairros_larvecidas, 'Quantidade', 'Bairro', "Bairros com mais aplicações de larvecidas")

    col3, col4 = st.columns(2)
    

    with col3:
        with st.container(height=700):
            st.altair_chart(fig_bairros_larvecidas, use_container_width=True)

    bairros_focos=conn.query(query_bairro_focos(data_filtro[0], data_filtro[1]), ttl=600)
    
    fig_bairros_focos = criar_grafico_horizontal(bairros_focos, 'Quantidade', 'Bairro', "Bairros com mais focos")
    with col4:
        with st.container(height=700):
            st.altair_chart(fig_bairros_focos, use_container_width=True)
    def adiciona_tabela(titulo, data):
            pdf.add_page()
            pdf.set_font('Times', 'B', 12)
            pdf.alias_nb_pages()
            pdf.cell(0, 10, f'{titulo}', 0, 0, 'C')
            pdf.ln(10)
            pdf.create_table(data)
            



    dt_in = pd.to_datetime(data_filtro[0], format='%d/%m/%Y')
    dt_in=dt_in.strftime('%d/%m/%Y')
    dt_fin = pd.to_datetime(data_filtro[1], format='%d/%m/%Y')
    dt_fin=dt_fin.strftime('%d/%m/%Y')
    pdf = PDF(dt_in, dt_fin)  # Passando dt_in e dt_fin ao criar uma instância da classe PDF
    
    pdf.set_font('Times', '', 12)
    pdf.alias_nb_pages()

    # Chamar o método header sem passar dt_in e dt_fin
    adiciona_tabela('Visitas por bairro', bairros_larvecidas)
    
    adiciona_tabela('Visitas por agente', bairros_focos)
    
    
    st.text("Relatório Estatístico")
    pdf.output(f'relatorio_geral_{data_filtro[1]}.pdf', 'F')
    
    with open(f'relatorio_geral_{data_filtro[1]}.pdf', "rb") as file:
        file_bytes = file.read()
        btn = st.download_button(
            label="Baixar PDF",
            data=file_bytes,
            file_name=f'relatorio_geral_{data_filtro[1]}.pdf'
        )