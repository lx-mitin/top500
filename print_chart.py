import matplotlib.pyplot as plt
import seaborn as sns


def print_chart(x, y, palette, ylabel):
    chart = sns.barplot(
        x=x,
        y=y,
        palette=palette
        )
    chart.set_xticklabels(
        chart.get_xticklabels(),
        rotation=90
        )
    chart.set_xlabel('')
    chart.set_ylabel(ylabel=ylabel)

    return chart
