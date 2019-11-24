import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_table_records(page, class_):

    p = requests.get(page)
    page = BeautifulSoup(p.text, 'html5lib').body
    table = page.find('table', class_)
    records = table.find('tbody').find_all('tr')

    return records


def get_tflops_by_country(page):

    top500 = []

    for i in range(1,5):
        records = get_table_records(
            page=page+str(i),
            class_='table table-condensed table-striped'
            )

        for record in records:
            cells = record.find_all('td')
            country = [s for s in cells[1].strings][1]
            rmax = round(float(re.sub(r'[^0-9.]','',cells[4].get_text())))
            top500.append((country, rmax))

    df = pd.DataFrame(top500, columns=['country','rmax'])
    df_country = df.groupby('country').agg('sum')
    df_country = df_country.sort_values('rmax', ascending=False)

    return df_country


def get_gdp_by_country(page, class_):
    gdp_nom = {}
    p = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)')
    page = BeautifulSoup(p.text, 'html5lib').body
    table = page.find('table', class_='wikitable sortable')
    records = table.find('tbody').find_all('tr')

    for r in range(2, len(records)):
        record = records[r]
        cells = record.find_all('td')
        country = [s for s in cells[1].strings][1]
        gdp = round(float(re.sub(r'[^0-9.]','',cells[2].get_text()))/1000)
        gdp_nom.update({country: gdp})

    return gdp_nom
