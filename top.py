import matplotlib.pyplot as plt
from get_data import get_tflops_by_country
from print_chart import print_chart


df_country = get_tflops_by_country('https://www.top500.org/lists/top500/list/2020/11/?page=')

chart1 = print_chart(
    x=df_country.index,
    y=df_country['rmax'],
    palette="Blues_d",
    ylabel='TFlops'
    )
plt.show()

