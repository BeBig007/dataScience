import csv
import sys
from os import listdir
from os.path import join
from datetime import datetime

docker_path = '/docker-entrypoint-initdb.d/'
data_path = '/data/'
# data_path = './customer/'        # for test purpose

column_types = {
    'event_time': 'TIMESTAMP WITH TIME ZONE',
    'event_type': 'VARCHAR(255)',
    'category_code': 'VARCHAR(255)',
    'product_id': 'INTEGER',
    'price': 'NUMERIC(10, 2)',
    'user_id': 'BIGINT',
    'user_session': 'UUID',
    'category_id': 'BIGINT',
    'brand': 'VARCHAR(100)'
}

def is_datetime_column(file_path, column_index=0):
    print(f'Checking if column {column_index} is in DATETIME format...')
    with open(file_path, 'r') as file:
        total_lines = sum(1 for _ in file) - 1

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        line_count = 0
        for row in reader:
            line_count += 1
            progress_percentage = (line_count / total_lines) * 100
            if line_count % 100 == 0:
                sys.stdout.write(f'\rProgress: {progress_percentage:.2f}%')
                sys.stdout.flush()
            try:
                datetime.strptime(row[column_index], '%Y-%m-%d %H:%M:%S %Z')
            except ValueError:
                return False
        print(f'\nAll {line_count} lines are in DATETIME format. Progress: 100%')
    return True

def generate_sql(f):
    file_path = join(data_path, f)
    with open(file_path, 'r') as file:
        columns = next(csv.reader(file))

    print(f'Processing {f}..., columns: {columns}')
    if columns[0] != 'event_time':
        raise ValueError(f"First column of {f} is not 'event_time'")

    print(f'Checking if event_time is in DATETIME format...')
    if not is_datetime_column(file_path):
        raise ValueError(f"Column 'event_time' of {f} is not in DATETIME format")

    sql_col = ',\n\t'.join([f'{col} {column_types.get(col, "VARCHAR")}' for col in columns])
    return f'CREATE TABLE {f[:-4]} (\n\t{sql_col}\n);\n'

csv_files = [f for f in listdir(data_path) if f.endswith('.csv')]

sql_content = '-- setup.sql\n\n'

for f in csv_files:
    try:
        sql_content += generate_sql(f)
        sql_content += f'COPY {f[:-4]} FROM \'{docker_path}{f}\' DELIMITER \',\' CSV HEADER;\n'
    except ValueError as e:
        print(e)

sql_content += 'CREATE TABLE customers AS (\n'

size = len(csv_files)
for f in csv_files:
    sql_content += f'SELECT * FROM {f[:-4]}\n'
    if size > 1:
        sql_content += 'UNION ALL\n'
    size -= 1
sql_content += ');\n'

with open('setup.sql', 'w') as table:
    table.write(sql_content)


# SELECT event_time, event_type, product_id, price, user_id, user_session, COUNT(*) AS count 
# FROM customers 
# GROUP BY event_time, event_type, product_id, price, user_id, user_session 
# HAVING COUNT(*)>1;

# 1 045 762

# SELECT * FROM customers WHERE event_time='2023-01-12 12:39:18+00' AND event_type='remove_from_cart' AND product_id='5700082' AND price='16.51' AND user_id='245068553';


# DELETE FROM customers
# WHERE (event_time, event_type, product_id, price, user_id, user_session) IN (
#   SELECT event_time, event_type, product_id, price, user_id, user_session
#   FROM customers
#   GROUP BY event_time, event_type, product_id, price, user_id, user_session
#   HAVING COUNT(*)>1
# );

# SELECT 19 583 742 #union
# SELECT 20 692 840 #union ALL
# DELETE  2 153 966

# SELECT * FROM data_2023_jan WHERE event_time='2023-01-01 00:01:02+00' AND event_type='remove_from_cart' AND product_id='5850281' AND price='137.78' AND user_id='593016733';

# SELECT *,
# ROW_NUMBER() OVER (PARTITION BY event_time, event_type, product_id, price, user_id, user_session ORDER BY event_time) AS row_num
# FROM data_2023_jan;


# WITH duplicates AS (
#   SELECT *,
#   	ROW_NUMBER() OVER (PARTITION BY event_time, event_type, product_id, price, user_id, user_session ORDER BY event_time) AS row_num
#   FROM data_2023_jan
# )
# DELETE FROM data_2023_jan
# WHERE (event_time, event_type, product_id, price, user_id, user_session) IN (
#     SELECT event_time, event_type, product_id, price, user_id, user_session
#     FROM duplicates
#     WHERE row_num > 1
# );


# DELETE FROM data_2023_jan
# WHERE (event_time, event_type, product_id, price, user_id, user_session) IN (
#     SELECT *, ROW_NUMBER() OVER (PARTITION BY event_time, event_type, product_id, price, user_id, user_session ORDER BY event_time) AS row_num
#     FROM data_2023_jan
#     WHERE row_num > 1
# );

# WITH duplicates AS (
#     SELECT *,
#            ROW_NUMBER() OVER (PARTITION BY event_time, event_type, product_id, price, user_id, user_session ORDER BY event_time) AS row_num
#     FROM data_2023_jan
# )
# DELETE FROM data_2023_jan
# WHERE ctid IN (
#     SELECT ctid
#     FROM duplicates
#     WHERE row_num > 1
# );
