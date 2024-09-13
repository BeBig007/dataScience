import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans


def load(path: str) -> pd.DataFrame:
    """Load a dataset from a CSV file and print its content."""

    try:
        assert isinstance(path, str), "the input must be string"
        data = pd.read_csv(path)
        print(f"Loading {path}\n")
        data.describe()
        print()
        data.info()
        print()
        return data

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")
    return None


def kmean_clustering(data: pd.DataFrame):
    """ Perform K-means clustering on the dataset and print the results. """
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        print("data.head()\n", data.head())

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    data = load("out.csv")
    kmean_clustering(data)


# docker cp postgres:frequency_chart.png ex03 && docker cp postgres:monetary_value_chart.png ex03
