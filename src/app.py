#import google
#from google.cloud import bigquery
#from google.oauth2 import service_account
import pandas_gbq
import pydata_google_auth
from sklearn.preprocessing import StandardScaler # data normalization
from sklearn.cluster import KMeans # K-means algorithm
import matplotlib
from sklearn.preprocessing import StandardScaler

matplotlib.use('agg')
import matplotlib.pyplot as plt




# Explicitly create a credentials object. This allows you to use the same
# credentials for both the BigQuery and BigQuery Storage clients, avoiding
# unnecessary API calls to fetch duplicate authentication tokens.
def get_data():
    SCOPES = [
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/drive',
    ]

    credentials = pydata_google_auth.get_user_credentials(
        SCOPES,
        # Set auth_local_webserver to True to have a slightly more convienient
        # authorization flow. Note, this doesn't work if you're running from a
        # notebook on a remote sever, such as over SSH or with Google Colab.
        auth_local_webserver=True,
    )

    query = """
            SELECT user_id, count(distinct order_id) as orders, CAST(avg(basket) as INT64) as total_basket, 
            max(case when cuisine_parent='Breakfast' then 1 else 0 end) as has_ordered_breakfast, 
            sum(case when cuisine_parent='Breakfast' then 1 else 0 end) as breakfast_orders
            FROM `bi-2019-test.ad_hoc.orders_jan2021` 
            group by 1
            """
    df = pandas_gbq.read_gbq(
        query,
        project_id='bi-2019-test',
        credentials=credentials,
    )
    return df


def optimal_k(points, kmax):
    sse = []

    for i in range(1, kmax):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=12, random_state=100)
        kmeans.fit(points)
        sse.append(kmeans.inertia_)
    plt.plot(range(1, kmax), sse, 'bx-')
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('SSE')
    plt.savefig('Files/Elbow.png')
    return sse

def segmentation():
    customer_data = get_data()
    clusters = 5

    attributes = customer_data[['orders','total_basket']].values
    scaler = StandardScaler().fit(attributes)

    X = scaler.transform(attributes)
    optimal_k(X, 10)
    model = KMeans(init='k-means++',
                   n_clusters=clusters,
                   n_init=12,
                   random_state=100)
    model.fit(X)

    labels = model.labels_
    customer_data['cluster_num'] = labels
    customer_data.to_csv('Files/clustering.csv' ,index=False)
    print(customer_data.head())

if __name__=='__main__':
    segmentation()