CREATE TABLE IF NOT EXISTS substances (
    id SERIAL PRIMARY KEY,
    name varchar(255),
    molecular_formula VARCHAR(255),
    molecular_weight VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    content BYTEA,
    mimetype VARCHAR(255),
    substance_id INT REFERENCES substances(id)
);