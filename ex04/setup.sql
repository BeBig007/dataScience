-- setup.sql

-- Create tables
CREATE TABLE item (
    product_id INTEGER,
    category_id BIGINT,
    category_code VARCHAR(100),
    brand VARCHAR(50)
);

-- Import data into tables
COPY item FROM '/docker-entrypoint-initdb.d/item.csv' DELIMITER ',' CSV HEADER;