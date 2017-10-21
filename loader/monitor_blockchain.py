import argparse
import time

import scraper
import processor
import database

web3 = scraper.web3


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Continuously look for the latest block')
    parser.add_argument('--interval', type=int, default=15, help='Polling interval')
    parser.add_argument('--batch-size', type=int, default=0,
                        help='Batch size: 0 to process all available')
    args = parser.parse_args()

    polling_interval = args.interval
    batch_size = args.batch_size

    while True:
        try:
            latest = web3.eth.blockNumber
            print('latest block: {:,}'.format(latest))

            last_seen = database.max_block()
            print('last seen: {:,}'.format(last_seen))

            # print(database.last_block())

            # if the latest block is greater than our latest block, fetch data
            if latest > last_seen:
                first = last_seen + 1

                if batch_size == 0:
                    to_process = latest - first
                else:
                    to_process = min(latest - first, batch_size)

                print('Processing {:,} blocks...'.format(to_process))
                processor.process(first, to_process)
                last_seen += to_process

            time.sleep(polling_interval)
        except KeyboardInterrupt:
            print('interrupted, exiting...')
            break
