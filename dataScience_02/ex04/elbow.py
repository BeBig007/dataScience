import pandas as pd
import matplotlib.pyplot as plt
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

        wcss = []
        for i in range (1,11):
            kmeans = KMeans(n_clusters=i,init='k-means++', n_init=10 ,random_state=42)
            kmeans.fit(data)
            wcss.append(kmeans.inertia_)
        print("K-means clustering completed.\n")
        print("wcss: ", wcss)

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
    data = load("out.csv")
    customer_data = featuring_data(data)
    kmean_clustering(customer_data)


# docker cp postgres:elbow_chart.png ex04