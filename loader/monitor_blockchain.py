import argparse
import time

import scraper
import processor
import database

web3 = scraper.web3

def recent_blocks(start, max_block):
    """Generator of block numbers starting from a specific block."""
    for i in range(start, max_block):
        yield i


def unseen_blocks(max_block):
    start = database.max_block() + 1
    print('First unseen block: {:,}'.format(start))
    for i in range(start, max_block):
        yield i


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Continuously look for the target_block block')
    parser.add_argument('--starting-block', type=int, default=0,
                        help='Optionally start from a specific block')
    parser.add_argument('--latest', action='store_true', default=False)
    parser.add_argument('--interval', type=int, default=15, help='Polling interval')
    parser.add_argument('--batch-size', type=int, default=0,
                        help='Batch size: 0 to process all available')
    parser.add_argument('--block-cap', '--confirmations', type=int, default=5,
                        help='Number of blocks to stay behind the tip')
    parser.add_argument('--dry-run', '-n', action='store_true', default=False)
    args = parser.parse_args()

    starting_block = args.starting_block
    polling_interval = args.interval
    batch_size = args.batch_size
    block_cap = args.block_cap
    dry_run = args.dry_run

    print(args)
    # exit(1)

    def targets():
        tip = web3.eth.blockNumber
        target = tip - block_cap
        print('latest block: {:,}'.format(tip))
        print('target block: {:,}'.format(target))

        return tip, target

    def process(i):
        if not dry_run:
            processor.process_block(i)
            print("Processed block <{}>".format(i))
        else:
            print('process {}'.format(i))

    last_seen = None
    latest, target_block = targets()

    # start from a specific block, or latest
    if args.latest:
        starting_block = latest

    if starting_block > 0:
        if starting_block > target_block:
            starting_block = target_block

        last_seen = starting_block - 1
        while True:
            try:
                latest, target_block = targets()

                print('process blocks from {} to {}'.format(last_seen + 1, target_block))
                for i in recent_blocks(last_seen + 1, target_block):
                    process(i)
                    last_seen = i
                time.sleep(polling_interval)
            except KeyboardInterrupt:
                print('interrupted, exiting...')
                break
    else:
        # just start from the latest in the database
        print('processing from latest in database')
        while True:
            try:
                latest, target_block = targets()

                for i in unseen_blocks(target_block):
                    process(i)

                time.sleep(polling_interval)
            except KeyboardInterrupt:
                print('interrupted, exiting...')
                break
