import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def load(path: str) -> pd.DataFrame:
    """Load a dataset from a CSV file and print its content."""

    try:
        assert isinstance(path, str), "the input must be string"
        data = pd.read_csv(path)
        print(f"Loading {path}\n")
        # data.describe()
        # print("data.info()\n")
        # data.info()
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
        plt.figure(figsize=(12,9))
        sns.heatmap(data.corr(numeric_only=True),annot=True,cmap='RdBu')
        plt.title('Correlation Heatmap',fontsize=14)
        plt.yticks(rotation =0)
        plt.savefig('corr_chart.png')
        plt.show()
        
        # scaler = StandardScaler()
        # data_scaled = scaler.fit_transform(data)
        # data_scaled = pd.DataFrame(data_scaled, columns=data.columns)
        
        # wcss = []
        # for i in range (1,11):
        #     kmeans = KMeans(n_clusters=i,init='k-means++',random_state=42)
        #     kmeans.fit(data_scaled)
        #     wcss.append(kmeans.inertia_)
        # plt.figure(figsize = (10,8))
        # plt.plot(range(1, 11), wcss, marker = 'o', linestyle = '-.',color='red')
        # plt.xlabel('Number of Clusters')
        # plt.ylabel('WCSS')
        # plt.title('K-means Clustering')
        # plt.savefig('elbow_chart.png')
        # plt.show()

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    data = load("out.csv")
    kmean_clustering(data)


# docker cp postgres:elbow_chart.png ex04 && docker cp postgres:corr_chart.png ex04
