CREATE TABLE urls (
    id smallint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255),
    created_at timestamp
);

CREATE TABLE url_checks (
    id smallint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id smallint  REFERENCES urls  (id),
    status_code smallint,
    h1 text,
    title text,
    description text,
    created_at timestamp
);