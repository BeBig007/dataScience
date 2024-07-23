FROM postgres:16.3

COPY ../customer/* /docker-entrypoint-initdb.d/
COPY postgres_db/setup.sql /docker-entrypoint-initdb.d/

EXPOSE 5432