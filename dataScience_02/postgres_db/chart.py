import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def load(path: str) -> pd.DataFrame:
    """Load a dataset from a CSV file and print its content."""

    try:
        assert isinstance(path, str), "the input must be string"
        data = pd.read_csv(path)
        print(f"Loading {path} dataset of type:\n{data.dtypes}\n")
        return data

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")
    return None


def chart_box_plot(data: pd.DataFrame):
    """ Create a chart from the data """
    plt.style.use('ggplot')
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        print(data)
        plt.figure()
        box = plt.boxplot(data, vert=False, patch_artist=True, boxprops=dict(facecolor='lightgreen'))
        plt.xlabel('price')
        plt.yticks([])
        plt.margins(x=0.05,y=-0.4)
        plt.savefig('box_plot_chart.png')

        stats = {}
        stats['count'] = data['price'].count()
        stats['mean'] = data['price'].mean()
        stats['std'] = data['price'].std()
        stats['min'] = data['price'].min()
        stats['25%'] = data['price'].quantile(0.25)
        stats['50%'] = data['price'].quantile(0.50)
        stats['75%'] = data['price'].quantile(0.75)
        stats['max'] = data['price'].max()
        
        print()
        print(f"count\t {stats['count']:.6f}")
        print(f"mean\t {stats['mean']:.6f}")
        print(f"std\t {stats['std']:.6f}")
        print(f"min\t {stats['min']:.6f}")
        print(f"25%\t {stats['25%']:.6f}")
        print(f"50%\t {stats['50%']:.6f}")
        print(f"75%\t {stats['75%']:.6f}")
        print(f"max\t {stats['max']:.6f}")
        print()
        print('Box plot created !\n')

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


def chart_box_no_outlier_plot(data: pd.DataFrame):
    """ Create a chart from the data """
    plt.style.use('ggplot')
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        # print(data)
        plt.figure()
        box = plt.boxplot(data, sym='', vert=False, patch_artist=True, boxprops=dict(facecolor='lightgreen'))
        plt.xlabel('price')
        plt.yticks([])
        plt.margins(x=0.05,y=-0.4)
        plt.savefig('chart_box_no_outlier_plot.png')
        print('Box plot without outliers created !\n')

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


def chart_box_plot_av_basket(data: pd.DataFrame):
    """ Create a chart from the data """
    plt.style.use('ggplot')
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        print(data)
        plt.figure()
        box = plt.boxplot(data, vert=False, patch_artist=True, boxprops=dict(facecolor='lightblue'))
        plt.xlabel('price')
        plt.yticks([])
        plt.margins(x=0.05,y=-0.45)
        plt.savefig('average_basket_chart.png')
        print('Box plot average basket created !\n')

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    data = load("out_price.csv")
    chart_box_plot(data)
    chart_box_no_outlier_plot(data)
    
    average_basket = load("out_average_price.csv")
    chart_box_plot_av_basket(average_basket)


# psql -U bebigel -d piscineds -h localhost

# docker cp postgres:box_plot_chart.png ex02 && docker cp postgres:chart_box_no_outlier_plot.png ex02 && docker cp postgres:average_basket_chart.png ex02
