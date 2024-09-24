import psycopg2
from configparser import ConfigParser


def load_config(filename='database.ini', section='postgresql'):
    """ Load the configuration from the .ini file """
    parser = ConfigParser()
    parser.read(filename)
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return config


def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.\n')
            return conn

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def export_to_csv():
    """ Export the sum_event_type table to a CSV file """
    command = """
    COPY (
        WITH purchases AS (
            SELECT
                user_id,
                COUNT(product_id) AS frequency,
                SUM(price) AS total_spent
            FROM customers
            WHERE event_type = 'purchase'
            GROUP BY user_id
        ),
        recency AS (
            SELECT
                user_id,
                (EXTRACT(DAY FROM (DATE '2023-03-01' - MAX(event_time)))) / 30.2 AS recency
            FROM customers
            WHERE event_type = 'purchase'
            GROUP BY user_id
        )

        SELECT
            p.frequency,
            p.total_spent,
            r.recency
        FROM purchases p
        JOIN recency r
        ON p.user_id = r.user_id
    ) TO STDOUT WITH CSV HEADER;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open('raw_data.csv', 'w') as f:
                    cur.copy_expert(command, f)
        print("Data exported successfully to raw_data.csv.\n")

    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    config = load_config()
    connect(config)
    export_to_csv()


#################################################################

        # SELECT
        #     COUNT(*) / COUNT(DISTINCT user_id) AS purchase_frequency,
        #     COUNT(DISTINCT EXTRACT(MONTH FROM event_time)) AS month_with_purchase_count,
        #     CASE
        #         WHEN EXTRACT(MONTH FROM MIN(event_time)) = 1 THEN 13
        #         WHEN EXTRACT(MONTH FROM MIN(event_time)) = 2 THEN 14
        #         ELSE EXTRACT(MONTH FROM MIN(event_time))
        #     END AS first_purchase_month,
        #     CASE
        #         WHEN EXTRACT(MONTH FROM MAX(event_time)) = 1 THEN 13
        #         WHEN EXTRACT(MONTH FROM MAX(event_time)) = 2 THEN 14
        #         ELSE EXTRACT(MONTH FROM MAX(event_time))
        #     END AS last_purchase_month
        # FROM customers
        # WHERE event_type = 'purchase'
        # GROUP BY user_id
        # ORDER BY first_purchase_month



        # SELECT event_time, event_type, price, user_id, user_session
        # FROM customers

        # SELECT 
        #     event_type, product_id, price, user_id, user_session,
        #     DATE(event_time) AS date, 
        #     ROUND(EXTRACT(HOUR FROM event_time) + EXTRACT(MINUTE FROM event_time) / 60.0, 1) AS decimal_time
        # FROM customers
        # WHERE event_type='purchase'
        # ORDER BY decimal_time
        
        # WITH purchases AS (
        #     SELECT
        #         user_id,
        #         COUNT(*) AS total_purchases,
        #         COUNT(DISTINCT EXTRACT(MONTH FROM event_time)) AS month_with_purchase,
        #         MIN(event_time) AS first_purchase_time,
        #         MAX(event_time) AS last_purchase_time
        #     FROM customers
        #     WHERE event_type = 'purchase'
        #     GROUP BY user_id
        # )
        # SELECT
        #     total_purchases / COUNT(DISTINCT user_id) AS purchase_frequency,
        #     month_with_purchase,
        #     CASE
        #         WHEN EXTRACT(MONTH FROM first_purchase_time) = 1 THEN 13
        #         WHEN EXTRACT(MONTH FROM first_purchase_time) = 2 THEN 14
        #         ELSE EXTRACT(MONTH FROM first_purchase_time)
        #     END AS first_purchase_month,
        #     CASE
        #         WHEN EXTRACT(MONTH FROM last_purchase_time) = 1 THEN 13
        #         WHEN EXTRACT(MONTH FROM last_purchase_time) = 2 THEN 14
        #         ELSE EXTRACT(MONTH FROM last_purchase_time)
        #     END AS last_purchase_month
        # FROM purchases
        # GROUP BY user_id, total_purchases, month_with_purchase, first_purchase_time, last_purchase_time
        # ORDER BY first_purchase_month

#################################################################