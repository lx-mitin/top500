import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_table_records(page, table_class):

    p = requests.get(page)
    page = BeautifulSoup(p.text, 'html5lib').body
    table = page.find('table', table_class)
    records = table.find('tbody').find_all('tr')


    return records


def get_tflops_by_country(pages):

    top500 = []
    table_class ='table table-condensed table-striped'

    for page in pages:

        records = get_table_records(page, table_class)

        for record in records:
            cells = record.find_all('td')
            
            country = [s for s in cells[1].strings][-1]
            rmax = round(float(re.sub(r'[^0-9.]','',cells[4].get_text())))

            top500.append((country, rmax))


    df = pd.DataFrame(top500, columns=['country','rmax'])
    df_country = df.groupby('country').agg('sum')
    df_country = df_country.sort_values('rmax', ascending=False)


    return df_country

