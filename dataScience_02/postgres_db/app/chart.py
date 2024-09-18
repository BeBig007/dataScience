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
    plt.style.use('ggplot')
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"

        plt.figure(figsize=(15, 10))
        sns.heatmap(data.corr(numeric_only=True),annot=True,cmap='RdBu')
        plt.title('Correlation Heatmap')
        plt.yticks(rotation =0)
        plt.savefig('corr_chart.png')
        plt.show()

        plt.figure(figsize=(15, 10))
        plt.scatter(data['purchases'], data['total_spent'], c='blue', s=10, marker='.')
        plt.savefig('purchases_tot_spent.png')
        plt.show()
        print('purchases_tot_spent.png created !\n')

        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        data_scaled = pd.DataFrame(data_scaled, columns=data.columns)
        print("Features generated and normalized.\n")

        wcss = []
        for i in range (1,11):
            kmeans = KMeans(n_clusters=i,init='k-means++', n_init=10 ,random_state=42)
            kmeans.fit(data_scaled)
            wcss.append(kmeans.inertia_)
        print("K-means clustering completed.\n")
        print("wcss: ", wcss)

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


if __name__ == '__main__':
    data = load("customer_data.csv")
    if data is not None:
        kmean_clustering(data)

# docker cp postgres:app/purchases_tot_spent.png ex05 && docker cp postgres:app/corr_chart.png ex05 && docker cp postgres:app/elbow_chart.png ex05

##################################################################################

        # plt.figure()
        # sns.heatmap(data.corr(numeric_only=True),annot=True,cmap='RdBu')
        # plt.title('Correlation Heatmap')
        # plt.yticks(rotation =0)
        # plt.savefig('corr_chart.png')
        # plt.show()

        # filtered_data = data_segm_kmean[(data_segm_kmean['sessions'] < 40) & (data_segm_kmean['views'] < 100)]
        # x_axis = filtered_data['sessions']
        # y_axis = filtered_data['views']
        # plt.figure()
        # plt.scatter(x_axis, y_axis, c=filtered_data['Segment_K_means'], cmap='hsv')
        # plt.xlabel('Sessions made')
        # plt.ylabel('Views')
        # plt.title('Segmentation K-means')
        # plt.savefig('chart_session_views.png')
        # plt.show()
        # print("chart_session_views generated.\n")
        
        # kmeans = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
        # kmeans.fit(data)
        # print("K-means clustering completed.\n")

        # data_segm_kmean = data.copy()
        # data_segm_kmean = pd.DataFrame(data, columns=data.columns)
        # data_segm_kmean['Segment_K_means'] = kmeans.labels_
        # print("data_segm_kmean\n", data_segm_kmean.head())
        # print()

        # data_segm_analysis = data_segm_kmean.groupby(['Segment_K_means']).mean().round(2)
        # user_count = data_segm_kmean.groupby(['Segment_K_means']).size()
        # data_segm_analysis['User_Count'] = user_count

        # print("data_segm_analysis\n", data_segm_analysis)
        # print()

        # filtered_data = data_segm_kmean[(data_segm_kmean['Segment_K_means'] == 1)]
        # x_axis = filtered_data['purchases']
        # y_axis = filtered_data['total_spent']
        # plt.figure(figsize=(10, 6))
        # plt.scatter(x_axis, y_axis, c=filtered_data['Segment_K_means'], cmap='brg', s=10)
        # plt.xlabel('Purchases')
        # plt.ylabel('Total Spent')
        # plt.title('Segmentation K-means')
        # plt.colorbar()
        # plt.savefig('chart_purch_spent.png')
        # plt.show()
        # print("chart_purch_spent generated.\n")

##################################################################################