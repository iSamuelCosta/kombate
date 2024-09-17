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

    bairro_visitas = conn.query(querry_bairro(data_filtro[0], data_filtro[1]), ttl=600)
    teste = pd.read_csv('lat_long_final - Sheet1 (1).csv')

    bairro_visitas = bairro_visitas.applymap(lambda x: str(x).upper() if isinstance(x, str) else x)
    teste = teste.applymap(lambda x: str(x).upper() if isinstance(x, str) else x)
    df_teste=bairro_visitas.merge(teste, left_on='bairro', right_on='bairro_nome')
    colunas_para_substituir = ['latitude', 'longitude']
    df_teste[colunas_para_substituir] = df_teste[colunas_para_substituir].applymap(lambda x: str(x).replace(',', '.'))
    df_teste['latitude'] = df_teste['latitude'].astype(float)
    df_teste['longitude'] = df_teste['longitude'].astype(float)

    difdata = data_filtro[1] - data_filtro[0]
    if difdata.days != 0:
        aux = 10 / difdata.days
        aux2 = 150 / difdata.days
    else:
        aux = 10
        aux2 = 150

    
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=df_teste,
        get_position='[longitude, latitude]',
        get_radius=f'numero_de_visitas * {aux}',  # Ajuste o multiplicador conforme necessário
        get_fill_color=[32, 252, 3],  # Cor vermelha para marcadores
        pickable=True
    )

    # Criar o mapa
    view_state = pdk.ViewState(latitude=-22.4269, longitude=-45.453, zoom=12.5)
    tooltip = {'html': 'Quantidade de Visitas: {numero_de_visitas} bairro: {bairro}'}

    map_ = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    )

    M_teve_larvida = conn.query(query_metric_teve_larvicida(data_filtro[0], data_filtro[1]), ttl=600)
    M_teve_larvida_7 = conn.query(query_metric_teve_larvicida_7_dias(), ttl=600)
    M_quantidade_visitas = conn.query(query_metric_quantidade_visitas(data_filtro[0], data_filtro[1]), ttl=600)
    M_quantidade_visitas_7 = conn.query(query_quantidade_visitas_7_dias(), ttl=600)
    qtd_visitas = M_quantidade_visitas['numero_de_linhas'].mean()
    qtd_larvicida = M_teve_larvida['numero_de_linhas'].mean()
    qtd_visitas_7_dias=M_quantidade_visitas_7['numero_de_linhas'].mean()
    qtd_larvicida_7_dias = M_teve_larvida_7['numero_de_linhas'].mean()

   

    
    fig_bairro = criar_grafico_horizontal(bairro_visitas,'numero_de_visitas', 'bairro', 'Grafico bairros')
   

    with st.container(height=600):
        st.markdown("<h4 style='text-align: center;'>Visitas por bairro</h4>", unsafe_allow_html=True)
        st.pydeck_chart(map_,use_container_width=True)


    with st.container(height=600):
        col11,coll2 = st.columns(2)
        with col11:
            st.metric("Quantidade de Visitas total", formata_numero(qtd_visitas))
            st.metric("Quantidade de larvecidas total", formata_numero(qtd_larvicida))
        with coll2:
            st.metric("Quantidade de Visitas ultimos 7 dias", formata_numero(qtd_visitas_7_dias))
            st.metric("Quantidade de larvecidas ultimos 7 dias", formata_numero(qtd_larvicida_7_dias))
        with st.container(height=395):
            st.altair_chart(fig_bairro, use_container_width=True)


   ##########################################################################################################
    bairro_tipo_imovel = conn.query(querry_bairro_tipo_imovel(data_filtro[0], data_filtro[1]), ttl=600)
    fig_bairro_tipo = criar_grafico_horizontal_segmento(bairro_tipo_imovel, 'sum(numero_de_visitas):Q','bairro',"Visitas por bairro", 'tipo:N', 'Resposta Origem' )
    with st.container(height=400):
        st.altair_chart(fig_bairro_tipo, use_container_width=True)
##################################################################################################################
    

    visitas_agente=conn.query(query_visitas_agente(data_filtro[0], data_filtro[1]), ttl=600)

    visitas_supervisores=conn.query(query_supervisores_agentes(data_filtro[0], data_filtro[1]), ttl=600)

    fig_agentes = criar_grafico_horizontal(visitas_agente,'numero_de_visitas','nome', 'Visitas por agente')

    fig_supervisores=cria_grafico_barras(visitas_supervisores, 'numero_de_visitas', 'nome', "Quantidade de visitas supervisores" )

    col3, col4 = st.columns (2)

    with col3:
            with st.container(height=400):
                st.altair_chart(fig_agentes, use_container_width=True)
    with col4:
            with st.container(height=400):
                st.altair_chart(fig_supervisores, use_container_width=True)

    st.divider()
    M_media_visitas_dia=conn.query(query_metric_media_visitas_diaria(data_filtro[0], data_filtro[1]), ttl=600)
    M_media_visitas_agente=conn.query(query_media_visitas_agente(data_filtro[0], data_filtro[1]), ttl=600)
    M_quantidade_focos=conn.query(query_quantidade_focos(data_filtro[0], data_filtro[1]), ttl=600)
    media_visitas = M_media_visitas_dia['media_numero_linhas'].mean()
    media_visitas_agente=M_media_visitas_agente['media_numero_linhas'].mean()
    qtd_focos= M_quantidade_focos['numero_de_linhas'].mean()

    porcentagem_larvicida=(qtd_larvicida/qtd_visitas)*100
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric("Média de visitas diarias", formata_metrica(media_visitas))

    with col6:
        st.metric("Média de visitas por agente", formata_metrica(media_visitas_agente))

    with col7:
        st.metric("Contagem de focos", formata_metrica(qtd_focos))

    with col8:
        st.metric("Porcentagem de larvicida", f"{porcentagem_larvicida:.2f}%")
    st.divider()
    #############################################################################################################
    visitas_por_mes=conn.query(query_visitas_mes(), ttl=600)
    fig_visitas_mes = criar_grafico_linhas(visitas_por_mes, 'mes_ano', 'numero_de_linhas', "Visitas por mês")
    with st.container():
     st.altair_chart(fig_visitas_mes, use_container_width=True)
    st.divider()
   

    #################################################################################################################
    visitas_por_dia=conn.query(query_visitas_dia(data_filtro[0], data_filtro[1]), ttl=600)
    visitas_por_dia = visitas_por_dia.tail(30)
    fig_visitas_dia = criar_grafico_linhas(visitas_por_dia, 'data', 'numero_de_linhas', "Visitas por dia")
    with st.container():
        st.altair_chart(fig_visitas_dia, use_container_width=True)
############################################################################################################################
    situacao_visita=conn.query(query_situacao_visita(data_filtro[0], data_filtro[1]), ttl=600)

    tipo_imovel_visita=conn.query(query_tipo_imovel_visita(data_filtro[0], data_filtro[1]), ttl=600)
    

    fig_situacao = alt.Chart(situacao_visita).mark_arc(innerRadius=50).encode(
        theta="quantidade",
        color="situacao:N",
    ).properties(
        title={
                "text": 'Visitas por situação',
                "anchor": 'middle'
            }
    )

    fig_tipo_residencia = criar_grafico_horizontal(tipo_imovel_visita, 'numero_de_visitas:Q', 'tipo:O', "Visitas por tipo de imovel", altura_personalizada=True)

    col9, col10 = st.columns (2)

    with col9:
            with st.container(height=400):
                st.altair_chart(fig_situacao, use_container_width=True)
    with col10:
            with st.container(height=400):
                st.altair_chart(fig_tipo_residencia, use_container_width=True)

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
    adiciona_tabela('Visitas por bairro', bairro_visitas.sort_values(by='numero_de_visitas', ascending=False))
    
    adiciona_tabela('Visitas por agente', visitas_agente.sort_values(by='numero_de_visitas', ascending=False))
    
    adiciona_tabela('Visitas por supervisor', visitas_supervisores.sort_values(by='numero_de_visitas', ascending=False))
    
    adiciona_tabela('Visitas por situação', situacao_visita.sort_values(by='quantidade', ascending=False))

    adiciona_tabela('Visitas por tipo de imovel', tipo_imovel_visita.sort_values(by='numero_de_visitas', ascending=False))
    st.text("Relatório Estatístico")
    pdf.output(f'relatorio_geral_{data_filtro[1]}.pdf', 'F')
    
    with open(f'relatorio_geral_{data_filtro[1]}.pdf', "rb") as file:
        file_bytes = file.read()
        btn = st.download_button(
            label="Baixar PDF",
            data=file_bytes,
            file_name=f'relatorio_geral_{data_filtro[1]}.pdf'
        )