import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def load(path: str) -> pd.DataFrame:
    """Load a dataset from a CSV file and print its content."""

    try:
        assert isinstance(path, str), "the input must be string"
        data = pd.read_csv(path)
        print(f"Loading {path}\n")
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
        print("Performing K-means clustering...\n")

        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        data_scaled = pd.DataFrame(data_scaled, columns=data.columns)

        wcss = []
        for i in range (1,11):
            kmeans = KMeans(n_clusters=i,init='k-means++', n_init=10 ,random_state=42)
            kmeans.fit(data_scaled)
            wcss.append(kmeans.inertia_)
        print("K-means clustering completed.\n")

        plt.figure(figsize=(10, 6))
        plt.plot(range(1, 11), wcss, marker = '+')
        plt.title('The Elbow Method')
        plt.xlabel('Number of Clusters')
        plt.tick_params(length=0)
        plt.savefig('elbow_chart.png')
        plt.show()
        print("Elbow plot generated.\n")

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


def groups_graph(data: pd.DataFrame):
    """ Generate a graph of the groups in the dataset. """
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"

        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        data_scaled = pd.DataFrame(data_scaled, columns=data.columns)

        kmeans = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
        data['cluster'] = kmeans.fit_predict(data_scaled)
        print("K-means clustering completed.\n")
        print(data.head())
        print()

        data_segm_kmean = data_scaled.copy()
        data_segm_kmean['Segment_K_means'] = kmeans.labels_

        data_segm_analysis = data_segm_kmean.groupby(['Segment_K_means']).mean()

        print("data_segm_analysis\n", data_segm_analysis)
        print()

        print("Mean:\n", data.mean())
        print()

        data_segm_kmean['Labels'] = data_segm_kmean['Segment_K_means'].map({
            0: 'Loyal customers Gold',
            1: 'Inactive',
            2: 'New customers',
            3: 'Loyal customers Platinum'
        })

        print(data_segm_kmean.head())
        print()

        data_segm_kmean['Customer_Type'] = data_segm_kmean['Labels'].map({
            'New customers': 'New customers',
            'Inactive': 'Inactive',
            'Loyal customers Platinum': 'Loyal customers',
            'Loyal customers Gold': 'Loyal customers'
        })

        customer_counts = data_segm_kmean['Customer_Type'].value_counts()
        customer_counts = customer_counts.sort_index()
        color_mapping = { 'Inactive': '#b6c5d8', 'Loyal customers': '#73c0a6', 'New customers': '#f5dcb7' }
        colors = [color_mapping[customer] for customer in customer_counts.index]

        plt.rcParams['axes.spines.right'] = False
        plt.rcParams['axes.spines.top'] = False
        plt.figure(figsize=(10, 8))
        plt.barh(customer_counts.index, customer_counts.values, color=colors)
        for index, value in enumerate(customer_counts.values):
            plt.text(value, index, str(value))
        plt.tick_params(left=False, bottom=False)
        plt.savefig('chart_bar.png')
        plt.show()
        print("chart_bar generated.\n")

        df_grouped = data.groupby('cluster').median(numeric_only=True).reset_index()
        df_grouped['Customer'] = df_grouped['cluster'].replace({
            0: 'Loyal customers',
            1: 'Inactive',
            2: 'New customers',
            3: 'Loyal customers'
        })
        df_grouped = df_grouped.groupby('Customer').median(numeric_only=True).reset_index()
        print(df_grouped)

        plt.figure(figsize=(10, 8))
        sns.scatterplot(x='recency', y='frequency',
                        data=df_grouped,
                        hue='cluster',
                        size='total_spent',
                        sizes=(200, 400),
                        palette=colors,
                        legend=False)
        for line in range(0,df_grouped.shape[0]):
            plt.text(
                df_grouped["recency"][line] + 0.1,
                df_grouped["frequency"][line],
                f"{round(df_grouped['total_spent'][line], 2):.2f} ₳",
                ha='left')
        plt.xlabel('Median Recency')
        plt.ylabel('Median Frequency')
        plt.show()
        plt.savefig('chart_median.png')

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    data = load("raw_data.csv")
    if data is not None:
        kmean_clustering(data)
        groups_graph(data)

# docker cp postgres:app/elbow_chart.png ex05 && docker cp postgres:app/chart_median.png ex05 && docker cp postgres:app/chart_bar.png ex05
