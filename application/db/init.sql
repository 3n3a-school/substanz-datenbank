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

CREATE TABLE IF NOT EXISTS synonyms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    substance_id INT REFERENCES substances(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);


CREATE TABLE IF NOT EXISTS substance_groups (
    substance_id INT REFERENCES substances(id) ON DELETE CASCADE,
    group_id INT REFERENCES groups(id) ON DELETE NO ACTION
);

-- INITIAL VALUES
INSERT INTO groups (name) VALUES ('approved'),
                                ('illicit'),
                                ('experimental'),
                                ('withdrawn'),
                                ('nutraceutical'),
                                ('investigational'),
                                ('vet_approved');