import streamlit as st
import pandas as pd
import sys

from src.database import select_db, download_db, fluxo_carros
from src.routes import rotas

# Relative imports
sys.path.append("/src")

st.set_page_config(page_title="Tráfego de carros DF",
                   page_icon="📊",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={
                       'Get Help': 'https://github.com/Pinheiro-Lucas/fluxo-de-carros-df',
                       'Report a bug': "https://github.com/Pinheiro-Lucas/fluxo-de-carros-df",
                       'About': "Alo"
                   })

for i in ("db", "option"):
    if i not in st.session_state:
        st.session_state[i] = None

if "estradas" not in st.session_state:
    st.session_state.estradas = rotas()

if st.session_state.db is not None:
    fluxo_all, _, qtd_carros, tempo_total = fluxo_carros(st.session_state.db)

    # Streamlit visualization
    st.title(f"{st.session_state.option} (Brasília-DF)")
    st.header(f"{qtd_carros:,} carros carregados em {tempo_total:.2f}s")

    # Type input
    tipos = dict.fromkeys(fluxo_all.Porte.tolist())
    # Start in "Total"
    start = list(tipos.keys()).index("Total")
    tipo_veiculo = st.selectbox("Tipo de carro", tipos, index=start)
    # Updates everything with vehicle type
    fluxo_all, fluxo, qtd_carros, tempo_total = fluxo_carros(st.session_state.db, tipo_veiculo)

    # Local input
    locais = dict.fromkeys(fluxo.Trecho.tolist())
    # Setting all the saved names
    for estrada in st.session_state.estradas.keys():
        locais[estrada] = st.session_state.estradas[estrada]

    # If the database name equals to None, put ID instead (UI)
    for cod, nome in locais.items():
        if nome is None:
            locais[cod] = cod

    # It's easier to find with name value in streamlit
    nomes_locais = {y: x for x, y in locais.items()}
    local = st.selectbox("Selecione a região",
                         nomes_locais)
    fluxo_local = fluxo[fluxo.Trecho == nomes_locais[local]]

    # Rendering both graphs
    crescente = fluxo_local[fluxo_local.Sentido == "crescente"]
    decrescente = fluxo_local[fluxo_local.Sentido == "decrescente"]

    # Check if data is not null to render
    if sum(crescente.Fluxo) != 0:
        st.header("Crescente")
        st.bar_chart(data=crescente.groupby(['Trecho', 'Intervalo', 'Porte']).sum(numeric_only=True).reset_index(),
                     x="Intervalo",
                     y="Fluxo")
    if sum(decrescente.Fluxo) != 0:
        st.header("Decrescente")
        st.bar_chart(data=decrescente.groupby(['Trecho', 'Intervalo', 'Porte']).sum(numeric_only=True).reset_index(),
                     x="Intervalo",
                     y="Fluxo")

    # Raw data
    with st.expander("Amostra dos dados brutos"):
        st.dataframe(fluxo_local)
else:
    st.info("Antes de visualizar o gráfico, selecione um banco de dados")
