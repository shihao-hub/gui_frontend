CREATE TABLE IF NOT EXISTS users
(
    id
    INTEGER
    PRIMARY
    KEY
    AUTOINCREMENT,
    username
    TEXT
    NOT
    NULL,
    password
    TEXT
    NOT
    NULL
);


CREATE TABLE IF NOT EXISTS diaries
(
    id
    INTEGER
    PRIMARY
    KEY,
    user_id
    INTEGER,
    title
    TEXT,
    content
    TEXT
);