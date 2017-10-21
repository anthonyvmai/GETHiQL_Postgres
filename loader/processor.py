#!/usr/bin/env python3

import sys
import psycopg2
import scraper
import database

""" Loads and processes all data related to block with given number """
def process_block(block_number):
    b = scraper.load_block(block_number)
    try:
        database.save_block(b)
    except psycopg2.IntegrityError:
        print("Block <{}> already loaded".format(block_number))

    for tx_hash in b["transactions"]:
        tx = scraper.load_transaction(tx_hash)
        try:
            database.save_transaction(tx)
        except psycopg2.IntegrityError:
            print("Transaction <{}> already loaded".format(tx_hash))

        for log in tx["logs"]:
            try:
                database.save_log(log)
            except psycopg2.IntegrityError:
                print("Log <{}> in tx <{}>".format(log["log_index"], tx_hash))

""" Processes given number of blocks from starting_block """
def process(starting_block, blocks):
    for i in range(0, blocks):
        process_block(starting_block + i)
        print("Processed block <{}>".format(starting_block + i))


""" Processes blocks from starting_block to ending_block, inclusive """
def process_range(starting_block, ending_block):
    for i in range(starting_block, ending_block + 1):
        process_block(i)
        print("Processed block <{}>".format(i))


if __name__ == '__main__':
    """ Processes blocks as per CLI args """
    if len(sys.argv) != 3:
        print("Pass block number and number of blocks as arguments")
        exit(1)

    starting_block = int(sys.argv[1])
    blocks = int(sys.argv[2])
    process(starting_block, blocks)
