FROM postgres:16.3

RUN apt-get update \
    && apt-get install -y python3 python3-pip python3-psycopg2 python3-matplotlib python3-pandas vim

COPY ../customer/* data/customer/
COPY ../item/* data/

COPY postgres_db/database.ini .
COPY postgres_db/save_csv.py .
COPY postgres_db/chart.py .

COPY postgres_db/init_sql.py data/
RUN python3 /data/init_sql.py

RUN mv setup.sql /docker-entrypoint-initdb.d/ \
    && mv /data/*.csv /docker-entrypoint-initdb.d/ \
    && mv /data/customer/*.csv /docker-entrypoint-initdb.d/

EXPOSE 5432
