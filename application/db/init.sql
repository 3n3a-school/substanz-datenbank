CREATE TABLE IF NOT EXISTS substances (
    id SERIAL PRIMARY KEY,
    name varchar(255),
    molecular_formula VARCHAR(255),
    molecular_weight VARCHAR(255)
);