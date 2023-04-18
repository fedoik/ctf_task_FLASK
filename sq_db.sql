CREATE TABLE IF NOT EXISTS users(
id integer PRIMARY KEY AUTOINCREMENT,
username text NOT NULL,
password text NOT NULL,
status text NOT NULL
);
