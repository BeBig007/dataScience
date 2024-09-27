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
