import csv
from os import listdir
from os.path import join
from datetime import datetime

docker_path = '/docker-entrypoint-initdb.d/'
data_path = '/data/'
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
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            try:
                datetime.strptime(row[column_index], '%Y-%m-%d %H:%M:%S %Z')
            except ValueError:
                return False
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

sql_content += 'CREATE TABLE customers_table AS (\n'

size = len(csv_files)
for f in csv_files:
    sql_content += f'SELECT * FROM {f[:-4]}\n'
    if size > 1:
        sql_content += 'UNION ALL\n'
    size -= 1
sql_content += ');\n'


# def union_sql(f):
    
#     return f'CREATE TABLE customers (\n\t{sql_col}\n);\n'

# CREATE TABLE customers_table AS (
# SELECT * FROM data_2022_oct 
# UNION ALL
# SELECT * FROM data_2022_nov
# UNION ALL
# SELECT * FROM data_2022_dec
# UNION ALL
# SELECT * FROM data_2023_jan
# UNION ALL
# SELECT * FROM data_2023_feb
# );

with open('setup.sql', 'w') as table:
    table.write(sql_content)
