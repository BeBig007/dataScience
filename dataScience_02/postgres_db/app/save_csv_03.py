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


def export_to_csv_frequency():
    """ Export the sum_event_type table to a CSV file """
    command = """
    COPY (
        SELECT
            user_id,
            COUNT(event_type) AS total_order
        FROM customers
        WHERE event_type='purchase'
        GROUP BY user_id
        HAVING COUNT(event_type) < 40
    ) TO STDOUT WITH CSV HEADER;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open('out_freq.csv', 'w') as f:
                    cur.copy_expert(command, f)
        print("Data exported successfully to out_freq.csv.\n")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")


def export_to_csv_monetary():
    """ Export the sum_event_type table to a CSV file """
    command = """
    COPY (
        SELECT
            user_id,
            SUM(price) AS total_price
        FROM customers
        WHERE event_type='purchase'
        GROUP BY user_id
        HAVING SUM(price) < 250
    ) TO STDOUT WITH CSV HEADER;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open('out_monetary.csv', 'w') as f:
                    cur.copy_expert(command, f)
        print("Data exported successfully to out_monetary.csv.\n")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    config = load_config()
    connect(config)
    export_to_csv_frequency()
    export_to_csv_monetary()