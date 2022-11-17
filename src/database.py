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

    dbs = {}

    for i in result:
        dbs[i["title"]] = "https://dados.gov.br" + i["href"]

    return dbs


def download_db(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, features="html5lib")

    url = soup.find("p", class_="muted ellipsis").a["href"]

    local_filename = url.split('/')[-1]

    # Stream needs to be true
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


@st.cache
def fluxo_carros(tipo: str):
    # Performance counter
    inicial = time.time()

    # Importing data from dados.gov.br
    data = pd.read_csv(fr"{os.path.dirname(__file__).replace('/src', '')}/fluxo-trecho-dados-abertos-divulgacao-10-2022.csv",
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

