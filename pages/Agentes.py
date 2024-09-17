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
    df_agentes = conn.query(query_agentes_unicos(), ttl=600)
    
    nome_funcionario = st.selectbox("Escolha o funcionário", df_agentes['nome'])

    filtro_nome_funcionario = df_agentes[df_agentes['nome']==nome_funcionario]
    id_funcionario = filtro_nome_funcionario['id'].iloc[0]
    
    df_visitas_bairro = conn.query(query_visitas_agentes_bairro(data_filtro[0], data_filtro[1], id_funcionario), ttl=600)
    fig_bairro = criar_grafico_horizontal(df_visitas_bairro,"Quantidade de Visitas", 'Bairro', 'Grafico bairros')


    col1, col2 = st.columns(2)
    with col1:
        with st.container(height=350):
            st.altair_chart(fig_bairro, use_container_width=True)
   
    df_visitas_tipo = conn.query(query_visitas_agentes_tipo_imovel(data_filtro[0], data_filtro[1], id_funcionario), ttl=600)
    fig_tipo = criar_grafico_horizontal(df_visitas_tipo,"Quantidade de Visitas", 'Tipo', 'Grafico tipos de imovel')

    with col2:
        with st.container(height=350):
            st.altair_chart(fig_tipo, use_container_width=True)
    st.divider()
    df_visitas_mes = conn.query(query_visitas_mes_agente(id_funcionario), ttl=600)
    
    fig_visitas_mes = criar_grafico_varias_linhas(df_visitas_mes, 'Mês', 'Quantidade', "Visitas por mês",400, 'situacao')
    with st.container():
        st.altair_chart(fig_visitas_mes, use_container_width=True)
    st.divider()

    df_visitas_dia = conn.query(query_visitas_dia_agente(data_filtro[0], data_filtro[1], id_funcionario), ttl=600)
    visitas_por_dia = df_visitas_dia.tail(30)
    st.divider()
    fig_visitas_dia = criar_grafico_linhas(visitas_por_dia, 'Dia', 'Quantidade', "Visitas por dia")
    with st.container():
        st.altair_chart(fig_visitas_dia, use_container_width=True)
    st.divider()

    def adiciona_tabela(titulo, data):
            pdf.add_page()
            pdf.cell(0, 5, f'Relátorio sobre {nome_funcionario}', 0, 1, 'C')
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
    adiciona_tabela('Visitas por bairro', df_visitas_bairro)
    
    adiciona_tabela('Visitas por tipo', df_visitas_tipo)
    adiciona_tabela('Visitas por mês', df_visitas_mes)
    adiciona_tabela('Visitas por dia', visitas_por_dia)
    
    
    st.text("Relatório Estatístico")
    pdf.output(f'relatorio_geral_{data_filtro[1]}.pdf', 'F')
    
    with open(f'relatorio_geral_{data_filtro[1]}.pdf', "rb") as file:
        file_bytes = file.read()
        btn = st.download_button(
            label="Baixar PDF",
            data=file_bytes,
            file_name=f'relatorio_geral_{data_filtro[1]}.pdf'
        )