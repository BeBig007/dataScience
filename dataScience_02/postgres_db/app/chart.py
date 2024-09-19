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
        print("Performing K-means clustering...\n")

        # plt.figure(figsize=(15, 10))
        # plt.scatter(data['month_with_purchase_count'], data['first_purchase_month'])
        # plt.xlabel('month_with_purchase_count')
        # plt.ylabel('first_purchase_month')
        # y_ticks = [10, 11, 12, 13, 14]
        # y_ticks_labels = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb']
        # plt.yticks(ticks=y_ticks, labels=y_ticks_labels)
        # plt.savefig('purchases_tot_spent.png')
        # plt.show()
        # print('purchases_tot_spent.png created !\n')

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


def groups_graph(data: pd.DataFrame):
    """ Generate a graph of the groups in the dataset. """
    plt.style.use('ggplot')
    try:
        assert isinstance(data, pd.DataFrame), "arg must be a dataframe"
        print("Generating graph of the groups...\n")

        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        data_scaled = pd.DataFrame(data_scaled, columns=data.columns)
        print("Features generated and normalized.\n")

        kmeans = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
        kmeans.fit(data_scaled)
        print("K-means clustering completed.\n")

        data_segm_kmean = data_scaled.copy()
        data_segm_kmean = pd.DataFrame(data_scaled, columns=data_scaled.columns)
        data_segm_kmean['Segment_K_means'] = kmeans.labels_

        data_segm_analysis = data_segm_kmean.groupby(['Segment_K_means']).mean().round(2)
        user_count = data_segm_kmean.groupby(['Segment_K_means']).size()
        data_segm_analysis['User_Count'] = user_count
        
        data_segm_analysis.rename({0: 'New customers', 
                                1: 'Inactive', 
                                2: 'Loyal customers Platinum', 
                                3: 'Loyal customers Gold'}, inplace=True)
        
        print("data_segm_analysis\n", data_segm_analysis)
        print()

        print(data.describe())
        print()

        data_segm_kmean['Labels'] = data_segm_kmean['Segment_K_means'].map({0: 'New customers',
                                                                            1: 'Inactive',
                                                                            2: 'Loyal customers Platinum',
                                                                            3: 'Loyal customers Gold'})

        print(data_segm_kmean.head())
        print()

        groups = data_segm_kmean.groupby('Segment_K_means')
        plt.figure(figsize=(10, 8))
        for name, group in groups:
            label = data_segm_kmean.loc[data_segm_kmean['Segment_K_means'] == name, 'Labels'].iloc[0]
            plt.scatter(group['month_with_purchase_count'], group['first_purchase_month'], label=label)
        plt.xlabel('month_with_purchase_count')
        plt.ylabel('Total first_purchase_month')
        plt.title('Segmentation K-means')
        plt.legend()
        plt.savefig('chart_pop.png')
        plt.show()
        print("chart_pop generated.\n")

        data_segm_kmean['Customer_Type'] = data_segm_kmean['Labels'].map({
            'New customers': 'New customers',
            'Inactive': 'Inactive',
            'Loyal customers Platinum': 'Loyal customers',
            'Loyal customers Gold': 'Loyal customers'
        })

        customer_counts = data_segm_kmean['Customer_Type'].value_counts()
        plt.figure(figsize=(10, 8))
        plt.barh(customer_counts.index, customer_counts.values, color=['blue', 'red', 'green'])
        for index, value in enumerate(customer_counts.values):
            plt.text(value, index,str(value))
        plt.tick_params(length=0)
        plt.tight_layout()
        plt.savefig('chart_bar.png')
        plt.show()
        print("chart_bar generated.\n")

    except AssertionError as msg:
        print(f"AssertionError: {msg}")
    except Exception as error:
        print(f"Error: {error}")

if __name__ == '__main__':
    data = load("raw_data.csv")
    if data is not None:
        kmean_clustering(data)
        groups_graph(data)

# docker cp postgres:app/chart_pop.png ex05 && docker cp postgres:app/elbow_chart.png ex05 && docker cp postgres:app/chart_bar.png ex05

##################################################################################

        # plt.figure()
        # sns.heatmap(data.corr(numeric_only=True),annot=True,cmap='RdBu')
        # plt.title('Correlation Heatmap')
        # plt.yticks(rotation =0)
        # plt.savefig('corr_chart.png')
        # plt.show()

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

# SELECT DISTINCT
#     CASE
#         WHEN month_with_purchase_count = 5 THEN 'loyal platinum'
#         WHEN month_with_purchase_count = 4 THEN 'loyal gold'
#         WHEN month_with_purchase_count = 3 THEN 'loyal silver'
#         WHEN month_with_purchase_count = 2 THEN 'new customer'
#         WHEN month_with_purchase_count = 1 AND first_purchase_month NOT IN (1, 2)THEN 'inactive'
#         ELSE 'new customer'
#     END AS purchase_months_category,
#     COUNT(DISTINCT user_id) AS customer_count
# FROM (
#     SELECT
#         user_id,
#         COUNT(DISTINCT EXTRACT(MONTH FROM event_time)) AS month_with_purchase_count,
#         EXTRACT(MONTH FROM MIN(event_time)) AS first_purchase_month
#     FROM customers
#     WHERE event_type = 'purchase'
#     GROUP BY user_id
# ) AS purchase_counts
# GROUP BY purchase_months_category
# ORDER BY customer_count;
##################################################################################