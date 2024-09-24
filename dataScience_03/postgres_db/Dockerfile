FROM postgres:16.3

RUN apt-get update \
    && apt-get install -y python3 python3-pip python3-psycopg2 python3-matplotlib python3-pandas vim python3-seaborn python3-sklearn python3-scipy

COPY ../data/* data/customer/


COPY postgres_db/app/* app/

COPY postgres_db/init_sql.py data/
RUN python3 /data/init_sql.py

RUN mv setup.sql /docker-entrypoint-initdb.d/ \
    && mv /data/*.csv /docker-entrypoint-initdb.d/ \
    && mv /data/customer/*.csv /docker-entrypoint-initdb.d/

EXPOSE 5432
