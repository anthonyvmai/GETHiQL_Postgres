DROP TABLE IF EXISTS transaction;
DROP TABLE IF EXISTS block;

CREATE TABLE block (
    height integer PRIMARY KEY,
    timestamp date,
    hash text,
    parentHash text,
    miner text,
    difficulty double precision,
    totalDifficulty double precision,
    size integer,
    gasUsed integer,
    gasLimit integer,
    nonce integer,
    blockReward integer,
    unclesReward integer,
    transactionsRoot text,
    stateRoot text,
    receiptsRoot text
);

CREATE TABLE transaction (
    transactionHash text PRIMARY KEY,
    blockNumber integer REFERENCES block (height),
    timestamp text,
    fromAddress text,
    toAddress text,
    value integer,
    gasLimit integer,
    gasUsedByTxn integer,
    gasPrice integer,
    actualTxFee integer,
    cumulativeGasUsed integer,
    txtReciptStatus text,
    nonce integer,
    inputData text
);
