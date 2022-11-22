import streamlit as st

import pandas as pd
import time
import os

import requests

from bs4 import BeautifulSoup


def select_db():
    dataset = "https://dados.gov.br/dataset/volume-medio-diario-de-trafego"

    req = requests.get(dataset)
    soup = BeautifulSoup(req.content, features="html5lib").find(id="dataset-resources")

    result = soup.find_all("a", class_="heading")

    return {i["title"]: "https://dados.gov.br" + i["href"] for i in result}


def download_db(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, features="html5lib")

    url = soup.find("p", class_="muted ellipsis").a["href"]

    return pd.read_csv(url, encoding='latin-1')


@st.cache
def fluxo_carros(data, tipo="Total"):
    # Performance counter
    inicial = time.time()

    # Creating the dataframe
    df = pd.DataFrame(data, columns=["Trecho", "Sentido", "Dia", "Intervalo", "Porte", "Fluxo"])

    # Filtering all
    data = df[df.Porte == tipo]

    # Just some car information
    carros = sum(map(int, df.Fluxo))

    # Ends the performance counter
    final = time.time()

    return df, data, carros, final-inicial

