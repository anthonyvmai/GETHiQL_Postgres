DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS blocks;

CREATE TABLE blocks (
    height integer PRIMARY KEY,
    block_time timestamp,
    hash text,
    parent_hash text,
    miner text,
    difficulty numeric(32),
    total_difficulty numeric(32),
    size integer,
    gas_used integer,
    gas_limit integer,
    nonce text,
    transactions_root text,
    state_root text,
    receipts_root text,
    transactions_count integer,
    uncles_count integer
);

CREATE TABLE transactions (
    transaction_hash text PRIMARY KEY,
    block_height integer REFERENCES blocks(height),
    from_address text,
    to_address text,
    value numeric(32),
    gas_limit integer,
    gas_used integer,
    gas_price numeric(32),
    cumulative_gas_used integer,
    nonce integer,
    transaction_index integer,
    created_contract_address text,
    input text,
    logs_count integer
);

GRANT ALL PRIVILEGES ON DATABASE gethiql_db TO gethiql_user;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA PUBLIC TO gethiql_user;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA PUBLIC TO gethiql_user;
