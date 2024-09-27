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


def export_to_csv_nb_customers():
    """ Export the sum_event_type table to a CSV file """
    command = """
    COPY (
        SELECT
            DATE(event_time) AS date,
            COUNT(DISTINCT user_id) AS num_customers
        FROM customers
        WHERE event_type='purchase'
        GROUP BY DATE(event_time)
        ORDER BY DATE(event_time)
    ) TO STDOUT WITH CSV HEADER;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open('out_nb_customers.csv', 'w') as f:
                    cur.copy_expert(command, f)
        print("Data exported successfully to out_nb_customers.csv.\n")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")


def export_to_csv_sales_by_month():
    """ """
    command = """
    COPY (
        SELECT 
            SUM(price) / 1000000 AS num_sales,
            EXTRACT (MONTH FROM event_time) AS MONTH,
            EXTRACT (YEAR FROM event_time) AS YEAR
        FROM customers
        WHERE event_type='purchase'
        GROUP BY EXTRACT(YEAR FROM event_time), EXTRACT(MONTH FROM event_time)
        ORDER BY EXTRACT(YEAR FROM event_time), EXTRACT(MONTH FROM event_time)
    ) TO STDOUT WITH CSV HEADER;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open('out_sales_by_month.csv', 'w') as f:
                    cur.copy_expert(command, f)
        print("Data exported successfully to out_sales_by_month.csv.\n")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")


def export_to_csv_average_spend():
    """ """
    command = """
    COPY (
        SELECT
            DATE(event_time) AS date,
            SUM(price)/COUNT(DISTINCT user_id) AS tot_sales
        FROM customers
        WHERE event_type='purchase'
        GROUP BY DATE(event_time)
        ORDER BY DATE(event_time)
    ) TO STDOUT WITH CSV HEADER;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open('out_average_spend.csv', 'w') as f:
                    cur.copy_expert(command, f)
        print("Data exported successfully to out_average_spend.csv.\n")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    config = load_config()
    connect(config)
    export_to_csv_nb_customers()
    export_to_csv_sales_by_month()
    export_to_csv_average_spend()

