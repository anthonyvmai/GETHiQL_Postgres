import time

import scraper
import processor
import database

web3 = scraper.web3


if __name__ == '__main__':
    # continuously look for the latest block
    seconds_per_block = 15
    batch_size = 10

    while True:
        latest = web3.eth.blockNumber
        print('latest block: {}'.format(latest))

        last_seen = database.max_block()
        print('last seen: {}'.format(last_seen))

        # print(database.last_block())

        # if the latest block is greater than our latest block, fetch data
        if latest > last_seen:
            # print('new batch')
            first = last_seen + 1
            to_process = min(latest - first, batch_size)
            processor.process(first, to_process)
            last_seen += to_process

        time.sleep(seconds_per_block)
