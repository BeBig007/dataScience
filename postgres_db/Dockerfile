FROM postgres:latest

COPY customer/* /docker-entrypoint-initdb.d/
COPY setup.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
