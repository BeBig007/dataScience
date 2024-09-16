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
        SELECT 
            event_type, product_id, price, user_id, user_session,
            DATE(event_time) AS date, 
            ROUND(EXTRACT(HOUR FROM event_time) + EXTRACT(MINUTE FROM event_time) / 60.0, 1) AS decimal_time
        FROM customers
        WHERE event_type='purchase'
        ORDER BY decimal_time
    ) TO STDOUT WITH CSV HEADER;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open('out.csv', 'w') as f:
                    cur.copy_expert(command, f)
        print("Data exported successfully to out.csv.\n")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    config = load_config()
    connect(config)
    export_to_csv()


#################################################################

# SELECT user_id, COUNT(*) AS purchases
# FROM customers
# WHERE event_type = 'purchase'
# GROUP BY user_id
# HAVING COUNT(*) < 100
# ORDER BY purchases DESC;


        # SELECT 
        #     event_type, product_id, price, user_id, user_session,
        #     DATE(event_time) AS date, 
        #     ROUND(EXTRACT(HOUR FROM event_time) + EXTRACT(MINUTE FROM event_time) / 60.0, 1) AS decimal_time
        # FROM customers
        # WHERE event_type='purchase'
        # ORDER BY decimal_time

#################################################################