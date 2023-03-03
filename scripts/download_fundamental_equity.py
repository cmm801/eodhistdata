"""Script to quickly download fundamental equity data using multiple threads."""

import argparse
import concurrent.futures
import sys
import time

from eodhistdata import EODHelper
from eodhistdata.constants import EXCLUDED_EXCHANGES
from eodhistdata.private_constants import API_TOKEN, BASE_PATH


def main(argv):
    t0 = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--exchange_id", type=str, default='US',
                        help="Exchange for which to download data.")
    parser.add_argument("--n_threads", type=int, default=20,
                        help="Number of threads to use for download")
    args = parser.parse_args()
        
    eod_helper = EODHelper(
        api_token=API_TOKEN, base_path=BASE_PATH)

    def worker(symbol, exchange_id):
        """The function used by individual workers to download fundamental data."""
        eod_helper.get_fundamental_equity(symbol, exchange_id=exchange_id)

    # create a pool with N threads
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=args.n_threads)
    
    # Get the list of all symbols in that exchange
    exchange_symbols = eod_helper.get_exchange_symbols(exchange=args.exchange_id)
    exchange_symbols.Exchange = exchange_symbols.Exchange.astype('str')
    idx_good_exchanges = ~exchange_symbols.Exchange.isin(EXCLUDED_EXCHANGES)
    symbols = list(set(exchange_symbols.loc[idx_good_exchanges, 'Code']))
    print(args.exchange_id, len(symbols))

    t0 = time.time()
    # submit tasks to the pool
    for idx, symbol in enumerate(symbols):
        if idx % 500 == 0:
            print(idx, symbol)
        pool.submit(worker, *(symbol, args.exchange_id))

    # wait for all tasks to complete
    pool.shutdown(wait=True)

    print('======================================================')                
    print(f'Download Complete. Elapsed time = {time.time() - t0}')


if __name__ == "__main__":
    main(sys.argv[1:])
