CREATE TABLE IF NOT EXISTS blocks (
    number BIGINT PRIMARY KEY,
    hash TEXT NOT NULL,
    tx_count INT
);

CREATE TABLE IF NOT EXISTS transactions (
    hash TEXT PRIMARY KEY,
    block_number BIGINT REFERENCES blocks(number),
    from_address TEXT,
    to_address TEXT,
    value NUMERIC
);
