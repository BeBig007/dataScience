import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy import stats


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


def remouve_outliers(data: pd.DataFrame) -> pd.DataFrame:
    """ Remove outliers from the dataset. """
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        print("Removing outliers from the dataset...\n")

        z_scores_purchases = stats.zscore(data['purchases'])
        z_scores_total_spent = stats.zscore(data['total_spent'])
        z_scores_views = stats.zscore(data['views'])
        z_scores_cart_adds = stats.zscore(data['cart_adds'])

        seuil = 3

        data = data[(z_scores_purchases < seuil) & (z_scores_purchases > -seuil) &
                    (z_scores_total_spent < seuil) & (z_scores_total_spent > -seuil) &
                    (z_scores_views < seuil) & (z_scores_views > -seuil) &
                    (z_scores_cart_adds < seuil) & (z_scores_cart_adds > -seuil)]
        return data

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")
    return None


def featuring_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Extracts features for each customer by aggregating the data."""
    try:
        assert isinstance(raw_data, pd.DataFrame), "Input must be a pandas DataFrame"
        print("Extracting features from the data...\n")

        raw_data['event_time'] = pd.to_datetime(raw_data['event_time'])
        recent_date = raw_data.groupby('user_id')['event_time'].max().reset_index()
        recent_date.columns = ['user_id', 'recent_event_time']
        raw_data = pd.merge(raw_data, recent_date, on='user_id', how='left')
        raw_data['recency'] = (raw_data['recent_event_time'] - raw_data['event_time']).dt.days
        print("Recency calculated.\n")

        total_purchases = raw_data[raw_data['event_type'] == 'purchase'].groupby('user_id')['event_type'].count()
        total_spent = raw_data[raw_data['event_type'] == 'purchase'].groupby('user_id')['price'].sum()
        average_spent = raw_data[raw_data['event_type'] == 'purchase'].groupby('user_id')['price'].mean()
        total_sessions = raw_data.groupby('user_id')['user_session'].nunique()
        recency = raw_data.groupby('user_id')['recency'].mean()

        customer_data = pd.DataFrame({
            'purchases': total_purchases,   # total purchases made by each customer
            'total_spent': total_spent,     # total amount spent by each customer
            'average_spent': average_spent, # average amount spent by each customer
            'sessions': total_sessions,     # total sessions made by each customer
            'recency': recency              # average recency of each customer
        }).fillna(0)

        print("Features extracted customer_data:")
        print(customer_data.head(50))
        print()

        # data = remouve_outliers(customer_data)
        # print("Outliers removed from the dataset.\n")

        # desc = data.describe()
        desc = customer_data.describe()
        print("Descriptive statistics of the data:")
        print(desc.to_string(formatters={'purchases': '{:.2f}'.format,
                                'total_spent': '{:.2f}'.format,
                                'sessions': '{:.2f}'.format,
                                'recency': '{:.2f}'.format}))
        print()

        data.to_csv("customer_data.csv")
        print("Dataset saved to 'customer_data.csv'.\n")
        return pd.DataFrame(data, columns=data.columns)

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")
    return None


if __name__ == '__main__':
    data = load("raw_data.csv")
    if data is not None:
        featuring_data(data)
