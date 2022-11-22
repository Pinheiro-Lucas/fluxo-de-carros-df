import pandas as pd


def rotas():
    db_estradas = "https://dados.gov.br/dataset/3cb44f4a-576c-45b8-8f13-ae94a6623277/resource" \
                  "/2bd0f48e-d3a1-47c6-bd12-83aed24e9461/download/2022-08-18-scr.csv"

    # Download CSV file
    estradas = pd.read_csv(db_estradas, delimiter=';')

    # Easier to read
    estradas["TRECHO"] = estradas['INÍCIO'] + " <-> " + estradas['FIM']

    # Filtered table
    estradas = dict(zip(estradas["COD. TRECHO"], estradas["TRECHO"]))

    return estradas


if __name__ == '__main__':
    print(rotas())
