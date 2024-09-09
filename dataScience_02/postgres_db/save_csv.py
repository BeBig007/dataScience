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
    command = """ COPY (SELECT * FROM customers WHERE event_type='purchase') TO STDOUT WITH CSV HEADER; """
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

# SELECT *  FROM customers 
# WHERE event_type='purchase'
# 1286102


# SELECT DISTINCT user_id FROM customers
# WHERE event_type='purchase' AND event_time BETWEEN '2022-10-01' AND '2022-10-02';
# SELECT DISTINCT user_id FROM customers
# WHERE event_type='purchase' AND event_time BETWEEN '2022-10-01 00:00:00' AND '2022-10-01 23:59:59';
# 1001

# SELECT DISTINCT user_id FROM customers
# WHERE event_type='purchase' AND event_time BETWEEN '2022-10-02' AND '2022-10-03';
# 1045 rows

# SELECT DISTINCT user_id FROM customers
# WHERE event_type='purchase' AND event_time BETWEEN '2022-10-03' AND '2022-10-04';
# 1048


# def create_tables():
#     """ Create tables in the PostgreSQL database """
#     command = """
#         CREATE TABLE IF NOT EXISTS customer_count (
#             event_time IMESTAMP WITH TIME ZONE PRIMARY KEY,
#             user_id BIGINT
#         )
#         """
#     try:
#         config = load_config()
#         with psycopg2.connect(**config) as conn:
#             with conn.cursor() as cur:
#                 cur.execute(command)
#                 conn.commit()
#         print("Table created successfully.\n")
#     except (psycopg2.DatabaseError, Exception) as error:
#         print(error)


# def insert_event_type_counts():
#     """ Insert event_type and their counts from customers into customer_count """
#     select_command = """
#         SELECT * FROM customers WHERE event_type='purchase'
#         GROUP BY event_time, user_id;
#     """
#     insert_command = """
#         INSERT INTO customer_count(event_time, user_id)
#         VALUES (%s, %s);
#     """
#     try:
#         config = load_config()
#         with psycopg2.connect(**config) as conn:
#             with conn.cursor() as cur:
#                 cur.execute(select_command)
#                 rows = cur.fetchall()
#                 for row in rows:
#                     cur.execute(insert_command, row)
#                 conn.commit()
#         print("Data inserted/updated successfully in customer_count.\n")
#     except (psycopg2.DatabaseError, Exception) as error:
#         print(f"Error: {error}")
