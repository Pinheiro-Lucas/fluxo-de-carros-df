import streamlit as st
import pandas as pd
import time
import os

from src.database import select_db, download_db
from src.select_db import select_db_page

# Todo: Dark mode
st.set_page_config(page_title="Tráfego de carros DF", layout="wide")


# Opens estradas.txt and collects all name values
def rotas(path="estradas.txt"):
    result = {}
    with open(fr"{os.path.dirname(__file__)}/{path}", 'r') as cod_estradas:
        e = [i for i in cod_estradas][4:]  # Remove instructions from the file
        for i in e:
            cod_estradas, desc = i.split(maxsplit=1)
            result[cod_estradas] = desc[:-1]

    return result


@st.cache
def fluxo_carros(tipo: str):
    # Performance counter
    inicial = time.time()

    # Importing data from dados.gov.br
    data = pd.read_csv(fr"{os.path.dirname(__file__)}/fluxo-trecho-dados-abertos-divulgacao-10-2022.csv",
                       encoding='latin-1')

    # Creating the dataframe
    df = pd.DataFrame(data, columns=["Trecho", "Sentido", "Dia", "Intervalo", "Porte", "Fluxo"])

    # Filtering all
    data = df[df.Porte == tipo]

    # Just some car information
    carros = sum(map(int, df.Fluxo))

    # Ends the performance counter
    final = time.time()

    return df, data, carros, final-inicial


estradas = rotas()
fluxo_all, _, qtd_carros, tempo_total = fluxo_carros(tipo="Total")

# Streamlit visualization
st.title(f"{qtd_carros:,} carros carregados em {tempo_total:.2f}s")

# Type input
tipos = dict.fromkeys(fluxo_all.Porte.tolist())
tipo_veiculo = st.selectbox("Tipo de carro", tipos, index=5)
fluxo_all, fluxo, qtd_carros, tempo_total = fluxo_carros(tipo_veiculo)

# Local input
locais = dict.fromkeys(fluxo.Trecho.tolist())
# Setting all the saved names
for estrada in estradas.keys():
    locais[estrada] = estradas[estrada]

# If the database name equals to None, put ID instead (UI)
for cod, nome in locais.items():
    if nome is None:
        locais[cod] = cod

# It's easier to find with name value in streamlit
nomes_locais = {y: x for x, y in locais.items()}
local = st.selectbox("Selecione a região",
                     nomes_locais,
                     help="Algumas estradas necessitam ser identificadas em estradas.txt")
fluxo_local = fluxo[fluxo.Trecho == nomes_locais[local]]

# Rendering both graphs
crescente = fluxo_local[fluxo_local.Sentido == "crescente"]
decrescente = fluxo_local[fluxo_local.Sentido == "decrescente"]

# Check if data is not null to render
if sum(crescente.Fluxo) != 0:
    st.header("Crescente")
    st.bar_chart(data=crescente, x="Intervalo", y="Fluxo")
if sum(decrescente.Fluxo) != 0:
    st.header("Decrescente")
    st.bar_chart(data=decrescente, x="Intervalo", y="Fluxo")
