"""Script to quickly download fundamental equity data using multiple threads."""

import argparse
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
    parser.add_argument("--stale_days", type=int, default=30,
                        help="Max age of cached data (in days) considered acceptable.")
    parser.add_argument("--n_threads", type=int, default=20,
                        help="Number of threads to use for download")
    args = parser.parse_args()
        
    eod_helper = EODHelper(
        api_token=API_TOKEN, base_path=BASE_PATH)

    _ = eod_helper.download_fundamental_equity_all(
        exchange_id=args.exchange_id,
        stale_days=args.stale_days,
        n_threads=args.n_threads)

    print('======================================================')                
    print(f'Download Complete. Elapsed time = {time.time() - t0}')


if __name__ == "__main__":
    main(sys.argv[1:])
