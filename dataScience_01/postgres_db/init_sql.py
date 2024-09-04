import csv
import sys
from os import listdir
from os.path import join
from datetime import datetime

docker_path = '/docker-entrypoint-initdb.d/'
data_path = '/data/'
# data_path = './customer/'        for test purpose

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
    print(f'\tChecking if column {column_index} is in DATETIME format...')
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
    # if columns[0] != 'event_time':
    #     raise ValueError(f"First column of {f} is not 'event_time'")

    print(f'Checking if event_time is in DATETIME format...')
    # if not is_datetime_column(file_path):
    #     raise ValueError(f"Column 'event_time' of {f} is not in DATETIME format")

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

sql_content += 'CREATE TABLE customers_all AS (\n'

size = len(csv_files)
for f in csv_files:
    sql_content += f'SELECT * FROM {f[:-4]}\n'
    if size > 1:
        sql_content += 'UNION ALL\n'
    size -= 1
sql_content += ');\n'

sql_content += 'CREATE TABLE customers AS (\n'

size = len(csv_files)
for f in csv_files:
    sql_content += f'SELECT * FROM {f[:-4]}\n'
    if size > 1:
        sql_content += 'UNION\n'
    size -= 1
sql_content += ');\n'

# sql_content += 'CREATE TEMPORARY TABLE tmp AS SELECT DISTINCT * FROM customers;\nTRUNCATE customers;\nINSERT INTO customers SELECT * FROM tmp;'

with open('setup.sql', 'w') as table:
    table.write(sql_content)
