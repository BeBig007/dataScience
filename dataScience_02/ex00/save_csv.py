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


def create_tables():
    """ Create tables in the PostgreSQL database """
    command = """
        CREATE TABLE IF NOT EXISTS sum_event_type (
            event_type VARCHAR(255) PRIMARY KEY,
            count BIGINT
        )
        """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
                conn.commit()
        print("Table created successfully.\n")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def insert_event_type_counts():
    """ Insert event_type and their counts from customers into sum_event_type """
    select_command = """
        SELECT event_type, COUNT(*) AS count
        FROM customers
        GROUP BY event_type;
    """
    insert_command = """
        INSERT INTO sum_event_type(event_type, count)
        VALUES (%s, %s);
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(select_command)
                rows = cur.fetchall()
                for row in rows:
                    cur.execute(insert_command, row)
                conn.commit()
        print("Data inserted/updated successfully in sum_event_type.\n")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")


def export_to_csv():
    """ Export the sum_event_type table to a CSV file """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM sum_event_type ;")
                with open('out.csv', 'w') as f:
                    cur.copy_expert('COPY sum_event_type TO STDOUT WITH CSV HEADER', f)
        print("Data exported successfully to out.csv.\n")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    config = load_config()
    connect(config)
    create_tables()
    insert_event_type_counts()
    export_to_csv()
