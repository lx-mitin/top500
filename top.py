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


df_country_ag = get_tflops_by_country('https://www.top500.org/list/2015/06/?page=')
df_country_inc = df_country.sub(df_country_ag, fill_value=0)
df_country_inc = df_country_inc.sort_values('rmax', ascending=False)

chart3 = print_chart(
    x=df_country_inc.index,
    y=df_country_inc['rmax'],
    palette="Greys_d",
    ylabel='TFlops change'
    )
plt.show()


df_hist = {}

for y in range(12, 20):
    path = 'https://www.top500.org/list/20' + str(y) + '/11/?page='
    df_hist.update({y: get_tflops_by_country(path)})

df_diff = pd.DataFrame(columns=['year', 'country', 'rmax'])

for y in range(13,20):
    df_diff_y = df_hist[y].sub(df_hist[y-1], fill_value=0)
    df_diff_y = df_diff_y.reset_index()
    df_diff_y.insert(0, 'year', '20'+str(y))
    df_diff = df_diff.append(df_diff_y, ignore_index=True)

df_diff['rmax'] = (df_diff['rmax']/1000).round(1)

groups = json.load(open('country_group.json'))
df_diff['group'] = df_diff['country'].map(groups)
df_diff_group = df_diff.groupby(['group', 'year']).agg({'rmax': 'sum'}).reset_index()

group_list = df_diff_group.groupby('group').agg({'rmax': 'sum'})
group_list = group_list.sort_values('rmax', ascending=False)

df_diff_group = df_diff_group.pivot(index='group', columns='year', values='rmax')
df_diff_group = df_diff_group.loc[group_list.index]

sns.set(font_scale=0.5)
chart4 = sns.heatmap(df_diff_group, cmap='Greens', annot=True)
plt.xlabel(None)
plt.ylabel(None)
bottom, top = chart4.get_ylim()
chart4.set_ylim(bottom + 0.5, top - 0.5)
chart4.set_yticklabels(chart4.get_yticklabels(), rotation=0)

plt.show()


df_diff_country = df_diff.pivot(index='country', columns='year', values='rmax')
df_diff_country.fillna(value=0, inplace=True)

country_list = df_diff.groupby('country').agg({'rmax': 'sum'})
country_list = country_list.sort_values('rmax', ascending=False)

df_diff_country = df_diff_country.loc[country_list.index]
df_diff_country = df_diff_country.reset_index()
df_diff_country['group'] = df_diff_country['country'].map(groups)

df_diff_eu = df_diff_country.loc[df_diff_country['group']=='European Union']
df_diff_eu = df_diff_eu.drop(columns='group')
df_diff_eu = df_diff_eu.set_index('country')

sns.set(font_scale=0.5)
chart5 = sns.heatmap(df_diff_eu, cmap='Greens', annot=True)
plt.xlabel(None)
plt.ylabel(None)
bottom, top = chart5.get_ylim()
chart5.set_ylim(bottom + 0.5, top - 0.5)
plt.show()


df_diff_common = df_diff_country.loc[df_diff_country['group']=='Commonwealth']
df_diff_common = df_diff_common.drop(columns='group')
df_diff_common = df_diff_common.set_index('country')

sns.set(font_scale=0.5)
chart6 = sns.heatmap(df_diff_common, cmap='Greens', annot=True)
plt.xlabel(None)
plt.ylabel(None)
bottom, top = chart6.get_ylim()
chart6.set_ylim(bottom + 0.5, top - 0.5)
plt.show()


df_diff_others = df_diff_country.loc[df_diff_country['group']=='Others']
df_diff_others = df_diff_others.drop(columns='group')
df_diff_others = df_diff_others.set_index('country')

sns.set(font_scale=0.5)
chart7 = sns.heatmap(df_diff_others, cmap='Greens', annot=True)
plt.xlabel(None)
plt.ylabel(None)
bottom, top = chart7.get_ylim()
chart7.set_ylim(bottom + 0.5, top - 0.5)
plt.show()
