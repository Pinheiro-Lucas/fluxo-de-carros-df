import os


# Opens estradas.txt and collects all name values
def rotas(path="estradas.txt"):
    result = {}
    with open(fr"{os.path.dirname(__file__).replace('/src', '')}/{path}", 'r') as cod_estradas:
        e = list(cod_estradas)[4:]
        for i in e:
            cod_estradas, desc = i.split(maxsplit=1)
            result[cod_estradas] = desc[:-1]

    return result


if __name__ == '__main__':
    print(rotas())
