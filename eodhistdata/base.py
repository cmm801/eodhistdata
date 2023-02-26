"""Define methods for downloading data from eodhistoricaldata.com.

This file contains the core logic used for downloading and caching
data from eodhistoricaldata.com.
"""


import datetime
import functools
import json
import pandas as pd
import eodhd.apiclient
import os
import tqdm

from eod import EodHistoricalData
from typing import Optional, Union
from enum import Enum

class EODDataTypes(Enum):
    """An Enum class enumerating the various available data sets."""
    EXCHANGE_LIST = 'exchange_list'
    EXCHANGE_SYMBOLS = 'exchange_symbols'
    HISTORICAL_TIME_SERIES = 'historical_time_series'
    MARKET_CAP = 'market_cap'
    FUNDAMENTAL_EQUITY = 'fundamental_equity'


class DBHelper:
    """A helper class for caching data and fetching cached data.

    Given a user-specified file path, this class will save different
    data sets into different subdirectories.
    """
    def __init__(self, base_path: str) -> None:
        self.base_path = base_path  # where data is cached

    def get_cached_data(
        self,
        data_type: str,
        exchange: Optional[str] = None,
        as_of_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = datetime.date.today(),
        stale_days: Optional[int] = None,
        **kwargs) -> Union[dict, pd.DataFrame]:
        filename = self._find_cached_data_filename(
            data_type=data_type, as_of_date=as_of_date, exchange=exchange, 
            stale_days=stale_days, **kwargs)
        
        _, file_extension = os.path.splitext(filename)
        if file_extension == '.csv':
            return pd.read_csv(filename)
        elif file_extension == '.json':
            with open (filename, "r") as f:
                data = json.loads(f.read())
            return data
        else:
            raise ValueError(f'Unsupported file extension: {file_extension}')
        
    def cache_data(
        self,
        data: Union[dict, pd.DataFrame],
        data_type: str,
        exchange: Optional[str] = None,
        as_of_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = datetime.date.today(),
        **kwargs) -> Union[dict, pd.DataFrame]:
        filename = self._get_cached_data_filename(
            data_type=data_type, exchange=exchange, as_of_date=as_of_date, **kwargs)

        # Create the directory path if it does not exist
        p, f = os.path.split(filename)
        if not os.path.isdir(p):
            os.makedirs(p)

        # Write data to file
        _, file_extension = os.path.splitext(f)
        if file_extension == '.csv':
            data.to_csv(filename, index=False)
        elif file_extension == '.json':
            with open(filename, "w") as f:
                f.write(json.dumps(data))
                f.close()
        else:
            raise ValueError(f'Unsupported file extension: {file_extension}')

    def _find_cached_data_filename(
        self,
        data_type: str,
        exchange: Optional[str] = None,
        as_of_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = datetime.date.today(),
        stale_days: Optional[int] = None,
        **kwargs) -> str:
        # Cast the as_of_date to pd.Timestamp
        as_of_date = pd.Timestamp(as_of_date)

        # Find the limit on how old cached data can be
        if stale_days is None:
            stale_days = self._get_default_stale_days(data_type)

        # Find the most recent cached data that is allowable by stale_days
        as_of_date_str = as_of_date.strftime('%Y%m%d')
        data_path = self._get_cached_data_path(data_type, exchange=exchange, **kwargs)            

        # Get the most recent cached date
        cached_date_str_list = sorted(os.listdir(data_path))
        oldest_date = as_of_date - pd.Timedelta(stale_days, unit='d')
        target_date_str = ''
        for cached_date_str in cached_date_str_list:
            cached_date = pd.Timestamp(cached_date_str)
            if cached_date > as_of_date:
                break
            if oldest_date <= cached_date:
                target_date_str = cached_date_str        
        
        if target_date_str:
            # Get the file extension type for the data type
            return self._get_cached_data_filename(
                data_type=data_type, exchange=exchange, as_of_date=target_date_str, **kwargs)
        else:
            return ''

    def _get_cached_data_filename(
        self,
        data_type: str,
        as_of_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp],    
        exchange: Optional[str] = None,
        **kwargs) -> str:
        """Get the filename for a cached data set.
        """
        data_path = self._get_cached_data_path(data_type, exchange=exchange, **kwargs)
        file_type = self._get_file_extension_type(data_type)
        date_str = pd.Timestamp(as_of_date).strftime('%Y%m%d')
        return os.path.join(data_path, date_str, f'{data_type}_{date_str}.{file_type}')

    def _get_file_extension_type(self, data_type: str) -> str:
        if data_type in (EODDataTypes.EXCHANGE_LIST.value,
                         EODDataTypes.EXCHANGE_SYMBOLS.value):
            return 'csv'
        elif data_type == EODDataTypes.FUNDAMENTAL_EQUITY.value:
            return 'json'
        else:
            raise ValueError(f'Unsupported data type: {data_type}')        

    def _get_default_stale_days(self, data_type: str) -> int:
        if data_type in (EODDataTypes.EXCHANGE_LIST.value,
                         EODDataTypes.EXCHANGE_SYMBOLS.value):
            return 0
        elif data_type == EODDataTypes.FUNDAMENTAL_EQUITY.value:
            return 30
        else:
            raise ValueError(f'Unsupported data type: {data_type}')        
            
    def _get_cached_data_path(
        self,
        data_type: str,
        exchange: Optional[str] = None,
        **kwargs) -> str:
        if data_type not in [dt.value for dt in EODDataTypes]:
            raise ValueError(f'Unsupported data type: {data_type}')

        file_path = os.path.join(self.base_path, data_type)
        if data_type == EODDataTypes.EXCHANGE_LIST.value:
            return file_path
        elif data_type in (EODDataTypes.EXCHANGE_SYMBOLS.value,
                           EODDataTypes.FUNDAMENTAL_EQUITY.value):
            if exchange is None:
                raise ValueError('The exchange ID must be provided.')
            return os.path.join(file_path, exchange)
        else:
            raise ValueError(f'Unsupported data type: {data_type}')


class EODHelper():
    """A class that allows fetching data from eodhistoricaldata.
    """
    def __init__(self, api_token: str, base_path: str = '/tmp') -> None:
        self.api_token = api_token
        self.db_helper = DBHelper(base_path)  # class to help get/save data from/to DB

        self.eodhd_client = eodhd.apiclient.APIClient(self.api_token)
        self.eod_client = EodHistoricalData(self.api_token)

    def _use_cache(data_type, default_stale_days):
        """Create decorator to check first for cached data."""
        def _decorator(func):
            @functools.wraps(func)
            def inner(self, **kwargs):
                
                # If user specifies stale days, use it instead of default
                if 'stale_days' in kwargs:
                    stale_days = kwargs.pop('stale_days')
                else:
                    stale_days = default_stale_days

                cached_filename = self.db_helper._find_cached_data_filename(
                    data_type, stale_days=stale_days, **kwargs)
                if cached_filename:
                    print('Getting cached data')
                    return self.db_helper.get_cached_data(
                        data_type, stale_days=stale_days, **kwargs)
                else:
                    print('Fetching')
                    data = func(self, **kwargs)
                    self.db_helper.cache_data(data, data_type, **kwargs)
                    return data
            return inner
        return _decorator
    
    @_use_cache(data_type=EODDataTypes.EXCHANGE_LIST.value,
                default_stale_days=0)
    def get_exchange_list(self):
        return self.eodhd_client.get_exchanges()
        
    @_use_cache(data_type=EODDataTypes.EXCHANGE_SYMBOLS.value,
                default_stale_days=0)
    def get_exchange_symbols(self, exchange: Optional[str] = None):
        return self.eodhd_client.get_exchange_symbols(exchange)

    @_use_cache(data_type=EODDataTypes.FUNDAMENTAL_EQUITY.value,
                default_stale_days=30)
    def get_fundamentals_bulk(self,
                              exchange: Optional[str] = None,
                              symbols: str = '',
                              max_requests=200,
                              **query_params) -> dict:
        """Get fundamental data for many instruments simultaneously.
        
        Arguments:
            exchange: the exchange for which we want to get all symbols.
            symbols: restrict request to a comma-separated subset of the exchange's symbols.
            limit: the maximum number of symbols to return
            offset: the offset of all of exchange's symbols with which to begin the request.
        """
        n_symbols = self.get_exchange_symbols(exchange=exchange).shape[0]
        results = dict()
        offset = 0
        offset_list = list(range(0, n_symbols, max_requests))
        for offset in tqdm.tqdm(offset_list):
            batch_result = self.eod_client.get_fundamentals_bulk(
                exchange=exchange, symbols=symbols, limit=max_requests, 
                offset=offset, **query_params)
            new_index = range(len(batch_result))
            values = list(batch_result.values())
            reindexed_results = {str(offset + idx): values[idx] for idx in new_index}
            results.update(reindexed_results)
            offset += max_requests
        return results

    def get_fundamental_equity(self,
                               exchange: Optional[str] = None,
                               symbol: str = '',
                               **query_params) -> dict:
        if exchange in US_EXCHANGES:
            exchange_id = 'US'
        else:
            exchange_id = exchange

        ticker = f'{symbol}.{exchange_id}'
        return self.eod_client.get_fundamental_equity(ticker, **query_params)

    def get_historical_data(
        self,
        symbol: str, 
        start: Union[str, datetime.date, datetime.datetime, pd.Timestamp],
        end: Union[str, datetime.date, datetime.datetime, pd.Timestamp],
        frequency: str = '1d',
    ) -> pd.DataFrame:
        if not isinstance(start, str):
            start = start.strftime('%Y-%m-%d')
            
        if not isinstance(end, str):
            end = end.strftime('%Y-%m-%d')

        return self.eodhd_client.get_historical_data(
            symbol=symbol,
            interval=frequency,
            range_start=start,
            range_end=end)

    def get_market_cap(self, symbol: str) -> pd.DataFrame:
        result = self.eod_client.get_market_cap(symbol)
        if result:
            mc = pd.DataFrame(result).T.set_index('date')
            mc.index = pd.DatetimeIndex(mc.index)            
            return mc
        else:
            return pd.DataFrame()

