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


def featuring_data(data: pd.DataFrame) -> pd.DataFrame:
    """Extracts features for each customer by aggregating the data."""
    try:
        assert isinstance(data, pd.DataFrame), "Input must be a pandas DataFrame"

        total_purchases = data[data['event_type'] == 'purchase'].groupby('user_id')['event_type'].count()
        total_views = data[data['event_type'] == 'view'].groupby('user_id')['event_type'].count()
        total_cart_adds = data[data['event_type'] == 'cart'].groupby('user_id')['event_type'].count()
        total_spent = data[data['event_type'] == 'purchase'].groupby('user_id')['price'].sum()
        total_sessions = data.groupby('user_id')['user_session'].nunique()

        customer_data = pd.DataFrame({
            'purchases': total_purchases,   # total purchases made by each customer
            'views': total_views,           # total views made by each customer
            'cart_adds': total_cart_adds,   # total cart additions made by each customer
            'total_spent': total_spent,     # total amount spent by each customer
            'sessions': total_sessions      # total sessions made by each customer
        }).fillna(0)
        print("Features extracted customer_data:")
        print(customer_data.head())
        print()
        customer_data.describe()
        print()

        scaler = StandardScaler()
        customer_data_scaled = scaler.fit_transform(customer_data)
        print("Features generated and normalized.\n")
        return pd.DataFrame(customer_data_scaled, columns=customer_data.columns)

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

        # plt.figure()
        # sns.heatmap(data.corr(numeric_only=True),annot=True,cmap='RdBu')
        # plt.title('Correlation Heatmap')
        # plt.yticks(rotation =0)
        # plt.savefig('corr_chart.png')
        # plt.show()

        kmeans = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
        kmeans.fit(data)
        print("K-means clustering completed.\n")

        data_segm_kmean = data.copy()
        data_segm_kmean = pd.DataFrame(data, columns=data.columns)
        data_segm_kmean['Segment_K_means'] = kmeans.labels_
        print("data_segm_kmean\n", data_segm_kmean.head())
        print()

        data_segm_analysis = data_segm_kmean.groupby(['Segment_K_means']).mean()
        print("data_segm_analysis\n", data_segm_analysis)
        print()

        filtered_data = data_segm_kmean[(data_segm_kmean['purchases'] < 40)]
        x_axis = filtered_data['purchases']
        y_axis = filtered_data['total_spent']
        plt.figure()
        plt.scatter(x_axis, y_axis, c=filtered_data['Segment_K_means'], cmap='hsv')
        plt.xlabel('Purchases')
        plt.ylabel('Total Spent')
        plt.title('Segmentation K-means')
        plt.savefig('chart_purch_spent.png')
        plt.show()
        print("chart_purch_spent generated.\n")

        filtered_data = data_segm_kmean[(data_segm_kmean['sessions'] < 40) & (data_segm_kmean['views'] < 100)]
        x_axis = filtered_data['sessions']
        y_axis = filtered_data['views']
        plt.figure()
        plt.scatter(x_axis, y_axis, c=filtered_data['Segment_K_means'], cmap='hsv')
        plt.xlabel('Sessions made')
        plt.ylabel('Views')
        plt.title('Segmentation K-means')
        plt.savefig('chart_session_views.png')
        plt.show()
        print("chart_session_views generated.\n")

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    data = load("out.csv")
    customer_data = featuring_data(data)
    kmean_clustering(customer_data)


# docker cp postgres:corr_chart.png ex05 && docker cp postgres:chart_purch_spent.png ex05 && docker cp postgres:chart_session_views.png ex05
# docker cp postgres:chart_purch_spent.png ex05 && docker cp postgres:chart_session_views.png ex05