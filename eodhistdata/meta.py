"""Provides a set of functions for getting meta-data about the 
historicaldata that has been downloaded.
"""

import json
import os
import pandas as pd

from eodhistdata.constants import EODDataTypes
from eodhistdata.private_constants import BASE_PATH


def get_historical_meta_data():
    """Get meta-data about the historical data that has been downloaded."""
    hist_base_path = os.path.join(BASE_PATH, EODDataTypes.HISTORICAL_TIME_SERIES.value)
    frequencies = os.listdir(hist_base_path)

    summary_list = []
    for frequency in frequencies:
        hist_freq_path = os.path.join(hist_base_path, frequency)
        exchanges = os.listdir(hist_freq_path)
        for exchange_id in exchanges:
            hist_ts_path = os.path.join(
                BASE_PATH, EODDataTypes.HISTORICAL_TIME_SERIES.value,
                frequency, exchange_id)
            symbols = os.listdir(hist_ts_path)

            for symbol in symbols:
                dates = os.listdir(os.path.join(hist_ts_path, symbol))
                max_date = max(dates)
                file_path = os.path.join(hist_ts_path, symbol, max_date)
                file_names = os.listdir(file_path)
                assert len(file_names) == 1, 'Should only be one file name per directory.'
                df = pd.read_csv(os.path.join(file_path, file_names[0]))
                summary_list.append(dict(symbol=symbol,
                                         frequency=frequency,
                                         exchange_id=exchange_id,
                                         as_of_date=pd.Timestamp(max_date),
                                         first_date=df.date.min(),
                                         last_date=df.date.max(),
                                         n_obs=df.shape[0]))

    df_summary = pd.DataFrame(summary_list)

    delta = pd.DatetimeIndex(df_summary.as_of_date) - pd.DatetimeIndex(df_summary.last_date)
    n_days_since_last_obs = delta / pd.Timedelta('1d')
    df_summary['is_active'] = n_days_since_last_obs < 10
    return df_summary

def remove_empty_directories(data_type: str, frequency: str = '1d',
                             exchange_id: str = 'US') -> int:
    """Remove empty data directories."""
    base_path = os.path.join(BASE_PATH, data_type, frequency, exchange_id)
    tickers = os.listdir(base_path)

    count = 0
    for ticker in tickers:
        subpath = os.path.join(base_path, ticker)
        dates = os.listdir(subpath)
        for date in dates:
            datepath = os.path.join(subpath, date)
            if not os.listdir(datepath):
                os.rmdir(datepath)
                count += 1
    return count

def get_fundamantal_data_summary():
    """Get meta-data about the fundamental data that has been downloaded."""
    summary_list = []
    empty_list = []
    no_files = []

    hist_base_path = os.path.join(BASE_PATH, EODDataTypes.FUNDAMENTAL_EQUITY.value)
    exchanges = os.listdir(hist_base_path)
    for exchange_id in exchanges:
        hist_ts_path = os.path.join(hist_base_path, exchange_id)
        symbols = os.listdir(hist_ts_path)
        for symbol in sorted(symbols):
            dates = os.listdir(os.path.join(hist_ts_path, symbol))
            max_date = max(dates)
            file_path = os.path.join(hist_ts_path, symbol, max_date)
            file_names = os.listdir(file_path)

            if len(file_names) == 0:
                no_files.append(file_path)
                continue

            filename = os.path.join(file_path, file_names[0])
            gen_info = _process_fundamental_data_for_file(filename)
            if len(gen_info) > 0:
                summary_list.append(gen_info)
            else:
                empty_list.append(symbol)

        df_fund_summary = pd.concat(summary_list, axis=1).T
        return df_fund_summary, empty_list, no_files

def _process_fundamental_data_for_file(filename):
    """Process the fundamental data for a single file."""
    cols_to_drop = ['Description', 'AddressData', 'Listings', 'Officers']    
    with open (filename, "r", encoding='utf-8') as f:
        data = json.loads(f.read())
        if not data:
            return pd.Series([], dtype=float)
        gen_data = {k: v for k, v in data['General'].items() if k not in cols_to_drop}
        gen_info = pd.Series(gen_data)
    return gen_info
