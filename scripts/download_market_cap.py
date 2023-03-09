"""Script to quickly download market cap data using multiple threads."""

import argparse
import sys
import time

from eodhistdata import EODHelper
from eodhistdata.constants import EXCLUDED_EXCHANGES
from eodhistdata.private_constants import API_TOKEN, BASE_PATH


def main(argv):
    t0 = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=str, default='',
                        help="First date of data to download")
    parser.add_argument("--end", type=str, default='',
                        help="Last date of data to download")
    parser.add_argument("--duration", type=str, default='',
                        help="Duration of data to download")
    parser.add_argument("--frequency", type=str, default='1d',
                        help="Frequency of data to download")
    parser.add_argument("--exchange_id", help="Exchange ID of tickers to download.",
                        type=str, default='US')
    parser.add_argument("--stale_days", help="Days old cached data is allowed to be.",
                        type=int, default=0)
    parser.add_argument("--n_threads", type=int, default=20,
                        help="Number of threads to use for download")                        
    args = parser.parse_args()

    eod_helper = EODHelper(
        api_token=API_TOKEN, base_path=BASE_PATH)

    _ = eod_helper.download_market_cap_all(
        exchange_id=args.exchange_id,
        stale_days=args.stale_days,
        n_threads=args.n_threads,
        start=args.start,
        end=args.end,
        duration=args.duration,
        frequency=args.frequency)

    print('======================================================')                
    print(f'Download Complete. Elapsed time = {time.time() - t0}')


if __name__ == "__main__":
    main(sys.argv[1:])
