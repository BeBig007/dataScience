import csv
from os import listdir
from os.path import join

docker_path = '/docker-entrypoint-initdb.d/'
data_path = '/data/'

def generate_sql(f):
    with open(join(data_path, f), 'r') as file:
        columns = next(csv.reader(file))

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

    sql_col = ',\n\t'.join([f'{col} {column_types.get(col, "VARCHAR")}' for col in columns])
    return f'CREATE TABLE {f[:-4]} (\n\t{sql_col}\n);\n'

csv_files = [f for f in listdir(data_path) if f.endswith('.csv')]

sql_content = '-- setup.sql\n\n'

for f in csv_files:
    sql_content += generate_sql(f)
    sql_content += f'COPY {f[:-4]} FROM \'{docker_path}{f}\' DELIMITER \',\' CSV HEADER;\n'

with open('setup.sql', 'w') as table:
    table.write(sql_content)
