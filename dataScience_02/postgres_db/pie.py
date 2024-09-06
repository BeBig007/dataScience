import psycopg2
import csv
from connect_db import load_config

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
        print(config)
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
                conn.commit()
        print("Table created successfully.")
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
                print(rows)
                for row in rows:
                    cur.execute(insert_command, row)
                conn.commit()
        print("Data inserted/updated successfully in sum_event_type.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")


def export_to_csv():
    """ Export the sum_event_type table to a CSV file """
    select_command = """SELECT * FROM sum_event_type ;"""
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(select_command)
                rows = cur.fetchall()
                with open('sum_event_type.csv', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerow([col[0] for col in cur.description])
                    writer.writerow(rows)
        print("Data exported successfully to sum_event_type.csv.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    create_tables()
    insert_event_type_counts()
    export_to_csv()

# psql -U bebigel -d piscineds -h localhost