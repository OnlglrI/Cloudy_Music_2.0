\c music_db


CREATE TABLE musicsid (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    author TEXT NOT NULL,
    album TEXT,
--    domain_name TEXT NOT NULL,
    genre TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);







