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


def export_to_csv_box_plot():
    """ Export the sum_event_type table to a CSV file """
    command = """
    COPY (
        SELECT price
        FROM customers
        WHERE event_type='purchase'
        ORDER BY price
    ) TO STDOUT WITH CSV HEADER;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open('out_price.csv', 'w') as f:
                    cur.copy_expert(command, f)
        print("Data exported successfully to out_price.csv.\n")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")


def export_to_csv_average_price():
    """ Export the sum_event_type table to a CSV file """
    command = """
    COPY (
        SELECT
            user_id,
            AVG(price) AS average_price
        FROM customers
        WHERE 
            event_type='purchase'
        GROUP BY user_id
        HAVING AVG(price) BETWEEN 27 AND 42
    ) TO STDOUT WITH CSV HEADER;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open('out_average_price.csv', 'w') as f:
                    cur.copy_expert(command, f)
        print("Data exported successfully to out_average_price.csv.\n")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    config = load_config()
    connect(config)
    export_to_csv_box_plot()
    export_to_csv_average_price()

