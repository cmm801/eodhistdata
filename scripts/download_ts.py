import eodhistdata
from eodhistdata.private_constants import API_TOKEN, BASE_PATH

import argparse
import sys
import time


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
    args = parser.parse_args()
        
    eod_helper = eodhistdata.EODHelper(
        api_token=API_TOKEN, base_path=BASE_PATH)

    exchange_symbols = eod_helper.get_exchange_symbols(
        exchange=args.exchange_id)

    EXCLUDED_EXCHANGES = ('US', 'NMFQS', 'nan')
    idx = ~exchange_symbols.Exchange.isin(EXCLUDED_EXCHANGES)
    symbol_errors = []
    for symbol in exchange_symbols.loc[idx].Code.values:
        print(symbol)
        try:
            eod_helper.get_historical_data(
                symbol=symbol, 
                start=args.start,
                end=args.end,
                frequency=args.frequency,
                duration=args.duration,
                stale_days=args.stale_days)
        except KeyError:
            print(f'Key error for symbol {symbol}')
            symbol_errors.append(symbol)
    
    print('======================================================')                
    print(f'Download Complete. Elapsed time = {time.time() - t0}')
    print(f'Errors downloading some symbols: {symbol_errors}')


if __name__ == "__main__":
    main(sys.argv[1:])
