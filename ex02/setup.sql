-- setup.sql

-- Create tables
CREATE TABLE data_2022_oct (
    event_time TIMESTAMP WITH TIME ZONE,
    event_type VARCHAR(100),
    product_id INTEGER,
    price NUMERIC(10, 2),
    user_id BIGINT,
    user_session UUID
);

CREATE TABLE data_2022_nov (
    event_time TIMESTAMP WITH TIME ZONE,
    event_type VARCHAR(100),
    product_id INTEGER,
    price NUMERIC(10, 2),
    user_id BIGINT,
    user_session UUID
);

CREATE TABLE data_2022_dec (
    event_time TIMESTAMP WITH TIME ZONE,
    event_type VARCHAR(100),
    product_id INTEGER,
    price NUMERIC(10, 2),
    user_id BIGINT,
    user_session UUID
);

CREATE TABLE data_2023_jan (
    event_time TIMESTAMP WITH TIME ZONE,
    event_type VARCHAR(100),
    product_id INTEGER,
    price NUMERIC(10, 2),
    user_id BIGINT,
    user_session UUID
);

-- Import data into tables
COPY data_2022_oct FROM '/docker-entrypoint-initdb.d/data_2022_oct.csv' DELIMITER ',' CSV HEADER;
COPY data_2022_nov FROM '/docker-entrypoint-initdb.d/data_2022_nov.csv' DELIMITER ',' CSV HEADER;
COPY data_2022_dec FROM '/docker-entrypoint-initdb.d/data_2022_dec.csv' DELIMITER ',' CSV HEADER;
COPY data_2023_jan FROM '/docker-entrypoint-initdb.d/data_2023_jan.csv' DELIMITER ',' CSV HEADER;
