"""Provides a set of functions for getting meta-data about the historical data that has been downloaded.
"""

import os
import pandas as pd

from eodhistdata.constants import EODDataTypes
from eodhistdata.private_constants import BASE_PATH


def get_historical_meta_data(base_path):
    hist_base_path = os.path.join(BASE_PATH, EODDataTypes.HISTORICAL_TIME_SERIES.value)
    frequencies = os.listdir(hist_base_path)

    summary_list = []
    for frequency in frequencies:
        hist_freq_path = os.path.join(hist_base_path, frequency)
        exchanges = os.listdir(hist_freq_path)
        for exchange_id in exchanges:
            hist_ts_path = os.path.join(BASE_PATH, EODDataTypes.HISTORICAL_TIME_SERIES.value, frequency, exchange_id)
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

    n_days_since_last_obs = (pd.DatetimeIndex(df_summary.as_of_date) - pd.DatetimeIndex(df_summary.last_date)) / pd.Timedelta('1d')
    df_summary['is_active'] = (n_days_since_last_obs < 10)
    return df_summary
