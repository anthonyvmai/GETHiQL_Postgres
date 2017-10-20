#!/usr/bin/env python3

import database

def event_handler(event, context):
    print("Creating blocks table")
    database.create_blocks_table()

    print("Creating transactions table")
    database.create_transactions_table()

    return "Success!"
