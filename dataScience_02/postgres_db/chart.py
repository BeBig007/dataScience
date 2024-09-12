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


def chart_bar_frequency(data: pd.DataFrame):
    """ Create a chart from the data """
    plt.style.use('ggplot')
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        print(data)
        plt.figure()
        plt.boxplot(data)
        plt.xlabel('price')
        plt.yticks([])
        plt.margins(x=0.05,y=-0.4)
        plt.savefig('frequency_chart.png')
        print('Box plot created !\n')

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


def chart_bar_monetary(data: pd.DataFrame):
    """ Create a chart from the data """
    plt.style.use('ggplot')
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        plt.figure()
        plt.boxplot(data)
        plt.xlabel('price')
        plt.yticks([])
        plt.margins(x=0.05,y=-0.4)
        plt.savefig('monetary_value_chart.png')
        print('Box plot without outliers created !\n')

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    data = load("out_freq.csv")
    chart_bar_frequency(data)

    monetary_value = load("out_monetary.csv")
    chart_bar_monetary(monetary_value)


# psql -U bebigel -d piscineds -h localhost

# docker cp postgres:frequency_chart.png ex03 && docker cp postgres:monetary_value_chart.png ex03