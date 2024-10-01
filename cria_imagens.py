import altair as alt
import streamlit as st
def criar_grafico_horizontal(data, x, y, titulo, altura_personalizada=False):
    # Criar o gráfico
    base = alt.Chart(data).encode(
        x=x,
        y=alt.Y(y).sort('-x'),
        text=x
    )

    # Adicionar o título centralizado usando properties
    base = base.properties(
        title={
            "text": titulo,
            "anchor": 'middle'  # Centralizar o título
        }
    )

    fig=base.mark_bar(cornerRadiusTopRight=10, cornerRadiusBottomRight=10) + base.mark_text(align='left', dx=2)

    if altura_personalizada:
        # Atribuir a propriedade height diretamente ao objeto de gráfico
        fig = fig.properties(height=400)

    return fig

    

import altair as alt
def criar_grafico_horizontal_segmento(data, x, y, titulo, segmento, titulosegmento):
    # Criar o gráfico
    base = alt.Chart(data).encode(
        x=alt.X(x),
        y=alt.Y(y).sort('-x'),
        text=x,
        color=alt.Color(segmento, title=titulosegmento)
    )

    # Adicionar o título centralizado usando properties
    base = base.properties(
        title={
            "text": titulo,
            "anchor": 'middle'  # Centralizar o título
        }
    )

    fig=base.mark_bar(cornerRadiusTopRight=10, cornerRadiusBottomRight=10) + base.mark_text(align='center', dx=2, color='black')

    return fig

def criar_grafico_linhas(data, x, y, titulo):
    # Criar o gráfico
    grafico = alt.Chart(data).mark_line().encode(
        x=x,
        y=y
    )

    # Adicionar o título centralizado usando properties
    grafico = grafico.properties(
        title={
            "text": titulo,
            "anchor": 'middle'  # Centralizar o título
        }
    )

    # Retornar o gráfico
    return grafico

def cria_grafico_barras(dados, eixox, eixoy, titulo):
    grafico = alt.Chart(dados).mark_bar(cornerRadiusTopRight=10, cornerRadiusBottomRight=10).encode(
        y=alt.Y(f'{eixox}:Q', title=''),
        x=alt.X(f'{eixoy}:O', title='').sort('-y')
    )

    grafico = grafico.properties(
        title={
            "text": titulo,
            "anchor": 'middle'
        }
    )

    return grafico

def centralizar_imagem(imagem_path):
    st.markdown(
        f'<style>div.Widget.stImage img {{display: block;margin-left: auto;margin-right: auto;}}</style>',
        unsafe_allow_html=True,
    )
    st.image(imagem_path, width=500)

def criar_grafico_varias_linhas(data, x, y, titulo, tamanho, color):
    # Criar o gráfico
    grafico = alt.Chart(data).mark_line(point=True).encode(
        x=x,
        y=y,
        color=alt.Color(color)
    )

    # Adicionar o título centralizado usando properties
    grafico = grafico.properties(
        title={
            "text": titulo,
            "anchor": 'middle'  # Centralizar o título
        }
    )
    text = grafico.mark_text(align='center', baseline='middle', dy=-10).encode(
        text=y
    )
    grafico = grafico + text
    grafico=grafico.properties(height=tamanho, width = tamanho * 3)
    grafico=grafico.configure(background="transparent")
    return grafico

def cria_grafico_pizza(dados, valor, legenda, titulo, rad, orient):
    base = alt.Chart(dados).mark_arc(innerRadius=rad).encode(
        theta=valor,
        color=alt.Color(legenda)
    )

    base = base.properties(
         title={
            "text": titulo,
            "anchor": orient  # Centralizar o título
        }
    )
    base = base.properties(height=400)
    base = base.configure(background="transparent")  # Corrected the property name
    return base