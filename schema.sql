CREATE TABLE IF NOT EXISTS auth (
    user_id TEXT PRIMARY KEY,
    username TEXT,
    password_hash TEXT
);

CREATE TABLE IF NOT EXISTS users (
  user_id TEXT,
  username TEXT,
  first_name TEXT,
  last_name TEXT
);
