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
    substance_id INT REFERENCES substances(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);


CREATE TABLE IF NOT EXISTS substance_groups (
    substance_id INT REFERENCES substances(id) ON DELETE NO ACTION,
    group_id INT REFERENCES groups(id) ON DELETE NO ACTION
);

-- INITIAL VALUES
INSERT INTO groups (name) VALUES ('approved');
INSERT INTO groups (name) VALUES ('illicit');
INSERT INTO groups (name) VALUES ('experimental');
INSERT INTO groups (name) VALUES ('withdrawn');
INSERT INTO groups (name) VALUES ('nutraceutical');
INSERT INTO groups (name) VALUES ('investigational');
INSERT INTO groups (name) VALUES ('vet_approved');