CREATE TABLE users (
   id SERIAL PRIMARY KEY,
   email VARCHAR(1000) NOT NULL UNIQUE,
   password VARCHAR(1000) NOT NULL
);