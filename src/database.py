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

