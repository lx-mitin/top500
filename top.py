import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from get_data import get_tflops_by_country
from get_data import get_gdp_by_country
from print_chart import print_chart


df_country = get_tflops_by_country('https://www.top500.org/lists/top500/list/2020/06/?page=')

chart1 = print_chart(
    x=df_country.index,
    y=df_country['rmax'],
    palette="Blues_d",
    ylabel='TFlops'
    )
plt.show()


gdp_nom = get_gdp_by_country(
    page='https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)',
    class_='wikitable sortable'
    )

df_country['gdp_bio'] = df_country.index.map(gdp_nom)
df_country['tflops_per_bio'] = round(df_country['rmax']/df_country['gdp_bio'], 1)
df_country_tb = df_country.sort_values('tflops_per_bio', ascending=False)

chart2 = print_chart(
    x=df_country_tb.index,
    y=df_country_tb['tflops_per_bio'],
    palette="Greens_d",
    ylabel='TFlops per GDP bio'
    )
plt.show()

