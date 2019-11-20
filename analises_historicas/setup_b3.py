import pickle
import bs4 as bs
import requests
import os
import datetime as dt
import pandas as pd
import pandas_datareader.data as web


def save_b3_tags():
    resp = requests.get("http://www.investsite.com.br/selecao_acoes.php")
    soup = bs.BeautifulSoup(resp.text)
    table = soup.find('table', {"id": "tabela_selecao_acoes"})
    tags = []
    for row in table.findAll('tr')[1:]:
        tag = row.findAll('td')[0].text
        tags.append(tag)

        print(tags)

    with open("b3_tags.pickle", "wb") as f:
        pickle.dump(tags, f)

    return tags


def get_data_from_yahoo(reload_b3=False):
    if reload_b3:
        tags = save_b3_tags()
    else:
        with open("b3_tags.pickle", "rb") as f:
            tags = pickle.load(f)

    if not os.path.exists("acoes_dfs"):
        os.makedirs("acoes_dfs")

    start = dt.datetime(1999, 1, 1)
    end = dt.date.today()

    for tag in tags:
        if not os.path.exists("acoes_dfs/{}.csv".format(tag)):
            try:
                df = df = web.DataReader(
                    "{}.SA".format(tag), 'yahoo', start, end)
                df.to_csv("acoes_dfs/{}.csv".format(tag))
            except:
                print("Problema ao recuperar dados da Tag {}".format(tag))
        else:
            print("Ação {} já foi coletada".format(tag))


get_data_from_yahoo()
