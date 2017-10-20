import psycopg2

""" Database connection object """
postgres = psycopg2.connect(
    dbname='gethiql_db',
    user='gethiql_user',
    host='localhost',
    password='foobar123'
)

""" Saves a row to table blocks """
def save_block(block_info):
    sql = """
        INSERT INTO blocks(
            height,
            block_time,
            hash,
            parent_hash,
            miner,
            difficulty,
            total_difficulty,
            size,
            gas_used,
            gas_limit,
            nonce,
            transactions_root,
            state_root,
            receipts_root,
            transactions_count,
            uncles_count
        ) VALUES (
            %(block_number)s,
            %(block_time)s,
            %(block_hash)s,
            %(parent_block_hash)s,
            %(miner)s,
            %(difficulty)s,
            %(total_difficulty)s,
            %(size)s,
            %(gas_used)s,
            %(gas_limit)s,
            %(nonce)s,
            %(transactions_root)s,
            %(state_root)s,
            %(receipts_root)s,
            %(transactions_count)s,
            %(uncles_count)s
        )
    """
    _execute_insert(sql, block_info)

""" Saves a row to table transactions """
def save_transaction(tx_info):
    sql = """
        INSERT INTO transactions(
            transaction_hash,
            block_height,
            from_address,
            to_address,
            value,
            gas_limit,
            gas_used,
            gas_price,
            cumulative_gas_used,
            nonce,
            transaction_index,
            created_contract_address,
            input,
            logs_count
        ) VALUES (
            %(transaction_hash)s,
            %(block_number)s,
            %(from_addr)s,
            %(to_addr)s,
            %(value)s,
            %(gas_limit)s,
            %(gas_used)s,
            %(gas_price)s,
            %(cumulative_gas_used)s,
            %(nonce)s,
            %(transaction_index)s,
            %(created_contract_address)s,
            %(input)s,
            %(logs_count)s
        )
    """
    _execute_insert(sql, tx_info)

""" Executes an insert transaction """
def _execute_insert(sql, desc):
    cursor = postgres.cursor()
    try:
        cursor.execute(sql, desc)
    finally:
        postgres.commit()
