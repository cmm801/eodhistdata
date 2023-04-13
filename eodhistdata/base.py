"""Define methods for analyzing fundamental equity data from eodhistoricaldata.com.

This file contains the core logic used for analyzing the data.
"""

import concurrent.futures
import datetime
import functools
import json
import pandas as pd
import requests
import tqdm

import os
from typing import Optional, Union

from abc import ABC, abstractmethod
from eod import EodHistoricalData
from typing import Optional, Union

from eodhistdata.constants import EODDataTypes, US_EXCHANGES, EXCLUDED_EXCHANGES, HISTORICAL_DATA_START_DATE

MAX_INTRADAY_DURATION = 120  # Max # of days of data that can be made for an intraday request
INTRADAY_FREQUENCIES = ('1m', '5m', '1h')


class EODHelper():
    """A class that allows fetching data from eodhistoricaldata.
    """
    def __init__(self, api_token: str, base_path: str = '/tmp') -> None:
        self.api_token = api_token
        self.base_path = base_path
        self._data_getters = dict()

        self.eod_client = EodHistoricalData(self.api_token)

    def _get_data_getter(self, data_type):
        if data_type not in self._data_getters:
            self._data_getters[data_type] = get_cache_helper(
                api_token=self.api_token, data_type=data_type, 
                base_path=self.base_path)
        return self._data_getters[data_type]

    def get_exchange_list(self, stale_days: Optional[int] = None):
        data_type = EODDataTypes.EXCHANGE_LIST.value
        data_getter = self._get_data_getter(data_type)
        return data_getter.get_data(stale_days=stale_days)
        
    def get_exchange_symbols(self, exchange: str, stale_days: Optional[str] = None):
        data_type = EODDataTypes.EXCHANGE_SYMBOLS.value
        data_getter = self._get_data_getter(data_type)
        return data_getter.get_data(exchange=exchange, stale_days=stale_days)

    def get_non_excluded_exchange_symbols(self, exchange_id: str = 'US'):
        """Get the list of all symbols in non-excluded exchanges."""
        exchange_symbols = self.get_exchange_symbols(
            exchange=exchange_id)
        exchange_symbols = exchange_symbols.query('Type == "Common Stock"')
        idx = exchange_symbols.Code.notna() & exchange_symbols.Exchange.notna()
        exchange_symbols = exchange_symbols.loc[idx]
        idx_good_exchanges = ~exchange_symbols.Exchange.isin(EXCLUDED_EXCHANGES)
        symbols = list(set(exchange_symbols.loc[idx_good_exchanges, 'Code']))

        # Drop symbols containing punctuation since we can't get time series for these
        excluded_punctuation = ['.', '(', '/']
        symbols = [s for s in symbols if not any([p in s for p in excluded_punctuation])]
        return sorted(symbols)

    def get_historical_data(
        self,
        symbol: str, 
        exchange_id: str = 'US',
        start: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
        end: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
        frequency: str = '1d',
        duration: str = '',
        stale_days: Optional[str] = None) -> pd.DataFrame:
        data_type = EODDataTypes.HISTORICAL_TIME_SERIES.value
        data_getter = self._get_data_getter(data_type)
        return data_getter.get_data(
            symbol=symbol, 
            exchange_id='US' if exchange_id in US_EXCHANGES else exchange_id,
            start=start, end=end, frequency=frequency, duration=duration,
            stale_days=stale_days, as_of_date=end)

    def get_market_cap(
        self,
        symbol: str, 
        exchange_id: str = 'US',
        start: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
        end: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
        frequency: str = '1d',
        duration: str = '',
        stale_days: Optional[str] = None) -> pd.DataFrame:
        data_type = EODDataTypes.MARKET_CAP.value
        data_getter = self._get_data_getter(data_type)
        return data_getter.get_data(
            symbol=symbol, 
            exchange_id='US' if exchange_id in US_EXCHANGES else exchange_id,
            start=start, end=end, frequency=frequency, duration=duration,
            stale_days=stale_days, as_of_date=end)

    def get_fundamental_equity(self,
                               symbol: str = '',
                               exchange_id: str = 'US',
                               stale_days: Optional[str] = None) -> dict:
        data_type = EODDataTypes.FUNDAMENTAL_EQUITY.value
        data_getter = self._get_data_getter(data_type)
        return data_getter.get_data(
            symbol=symbol, exchange_id=exchange_id, stale_days=stale_days)

    def get_fundamentals_bulk(self,
                              exchange: Optional[str] = None,
                              symbols: str = '',
                              max_requests=200,
                              stale_days: Optional[str] = None) -> dict:
        """Get fundamental data for many instruments simultaneously.

        Arguments:
            exchange: the exchange for which we want to get all symbols.
            symbols: restrict request to a comma-separated subset of the exchange's symbols.
            limit: the maximum number of symbols to return
            offset: the offset of all of exchange's symbols with which to begin the request.
        """
        data_type = EODDataTypes.FUNDAMENTAL_EQUITY.value
        data_getter = self._get_data_getter(data_type)
        return data_getter.get_data(exchange=exchange, symbols=symbols,
                                    max_requests=max_requests, stale_days=stale_days)

    def _download_data_all(self, func_handle, exchange_id: str = 'US',
                           n_threads: int = 20, **kwargs) -> None:
        """Download fundamental equity data for all tickers on an exchange."""

        def worker(symbol):
            """This function is used by individual workers to download fundamental data."""
            func_handle(symbol, exchange_id=exchange_id, **kwargs)

        # create a pool with N threads
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=n_threads)
        
        # Get exchange symbols
        symbols = self.get_non_excluded_exchange_symbols(exchange_id)

        # submit tasks to the pool
        for idx, symbol in enumerate(symbols):
            if idx % 500 == 0:
                print(idx, symbol)
            args = (symbol,)
            pool.submit(worker, *args)

        # wait for all tasks to complete
        pool.shutdown(wait=True)

    def download_fundamental_equity_all(self,
                                        exchange_id: str = 'US',
                                        stale_days: Optional[int] = None,
                                        n_threads: int = 20) -> None:
        """Download fundamental equity data for all tickers on an exchange."""
        self._download_data_all(
            self.get_fundamental_equity, exchange_id=exchange_id,
            n_threads=n_threads, stale_days=stale_days)

    def download_historical_data_all(
            self,
            exchange_id: str = 'US',
            start: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
            end: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
            frequency: str = '1d',
            duration: str = '',
            stale_days: Optional[int] = None,
            n_threads: int = 20) -> None:
        """Download fundamental equity data for all tickers on an exchange."""
        self._download_data_all(
            self.get_historical_data, exchange_id=exchange_id, n_threads=n_threads,
            stale_days=stale_days, start=start, end=end, frequency=frequency, duration=duration)

    def download_market_cap_all(
            self,
            exchange_id: str = 'US',
            start: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
            end: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
            frequency: str = '1d',
            duration: str = '',
            stale_days: Optional[int] = None,
            n_threads: int = 20) -> None:
        """Download fundamental market cap data for all tickers on an exchange."""
        self._download_data_all(
            self.get_market_cap, exchange_id=exchange_id, n_threads=n_threads,
            stale_days=stale_days, start=start, end=end, frequency=frequency, duration=duration)


class AbstractDataGetter(ABC):
    """A class for getting, caching and fetching cached data.

    Given a user-specified file path, this class will save different
    data sets into different subdirectories.
    """
    def __init__(self, api_token: str, base_path: str,
                 default_stale_days: int = 0) -> None:
        self.api_token = api_token
        self.base_path = base_path  # where data is cached
        self.default_stale_days = default_stale_days

        self.eod_client = EodHistoricalData(self.api_token)        

    @property
    @abstractmethod
    def data_type(self) -> str:
        pass

    @abstractmethod
    def get_data_from_server(self, **kwargs):
        pass

    @abstractmethod
    def get_file_extension_type(self) -> str:
        pass

    @abstractmethod
    def get_cached_data_path(self, **kwargs) -> str:
        pass

    def get_data(
            self, 
            as_of_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
            stale_days: Optional[int] = None, **kwargs):
        # If user specifies stale days, use it instead of default
        if stale_days is None:
            stale_days = self.default_stale_days

        cached_filename = self.find_cached_data_filename(
            as_of_date=as_of_date, stale_days=stale_days, **kwargs)
        if cached_filename:
            return self.get_data_from_cache(
                stale_days=stale_days, as_of_date=as_of_date, **kwargs)
        else:
            print('Fetching', kwargs)
            data = self.get_data_from_server(**kwargs)
            self.cache_data(data, as_of_date=as_of_date, **kwargs)
            return data
    
    def cache_data(
            self,
            data: Union[dict, pd.DataFrame],
            as_of_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
            **kwargs) -> Union[dict, pd.DataFrame]:
        """Abstract method for caching data."""
        if not as_of_date:
            as_of_date = pd.Timestamp.today().round('d')

        filename = self.create_cached_data_filename(
            as_of_date=as_of_date, **kwargs)

        # Create the directory path if it does not exist
        p, f = os.path.split(filename)
        if not os.path.isdir(p):
            os.makedirs(p)

        # Write data to file
        _, file_extension = os.path.splitext(f)
        if file_extension == '.csv':
            if data.index.name is not None:
                data.to_csv(filename, index=True)
            else:
                data.to_csv(filename, index=False)
        elif file_extension == '.json':
            with open(filename, "w") as f:
                f.write(json.dumps(data))
                f.close()
        else:
            raise ValueError(f'Unsupported file extension: {file_extension}')

    def get_data_from_cache(
            self, 
            as_of_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
            stale_days: Optional[int] = None,
            **kwargs) -> Union[dict, pd.DataFrame]:
        """Abstract method for obtaining cached data."""
        filename = self.find_cached_data_filename(
            as_of_date=as_of_date, stale_days=stale_days, **kwargs)
        _, file_extension = os.path.splitext(filename)
        if file_extension == '.csv':
            try:
                df = pd.read_csv(filename)
            except pd.errors.EmptyDataError:
                df = pd.DataFrame()
            
            if df.size and 'date' == df.columns[0]:
                df.set_index('date', inplace=True)
                df.index = pd.DatetimeIndex(df.index)
            return df
        elif file_extension == '.json':
            with open (filename, "r") as f:
                data = json.loads(f.read())
            return data
        else:
            raise ValueError(f'Unsupported file extension: {file_extension}')

    def find_cached_data_filename(
            self,
            as_of_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
            stale_days: Optional[int] = None,
            **kwargs) -> str:
        """Abstract method for getting the filename containing cached data."""
        # Cast the as_of_date to pd.Timestamp
        if not as_of_date:
            as_of_date = pd.Timestamp.today().round('d')
        else:
            as_of_date = pd.Timestamp(as_of_date)

        # Find the limit on how old cached data can be
        if stale_days is None:
            stale_days = self.default_stale_days

        # Find the most recent cached data that is allowable by stale_days
        as_of_date_str = as_of_date.strftime('%Y%m%d')
        data_path = self.get_cached_data_path(**kwargs)

        # Check if no data has been cached on this filepath
        if not os.path.isdir(data_path):
            return ''

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
            return self.create_cached_data_filename(
                as_of_date=target_date_str, **kwargs)
        else:
            return ''

    def create_cached_data_filename(
            self,
            as_of_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
            **kwargs) -> str:
        data_path = self.get_cached_data_path(**kwargs)
        file_type = self.get_file_extension_type()
        date_str = pd.Timestamp(as_of_date).strftime('%Y%m%d')
        filename = f'{self.data_type}_{date_str}.{file_type}'
        return os.path.join(data_path, date_str, filename)


class ExchangeListDataGetter(AbstractDataGetter):
    """A class for caching data and fetching cached data.

    Given a user-specified file path, this class will save different
    data sets into different subdirectories.
    """
    # Implementing abstract method    
    @property
    def data_type(self) -> str:
        return EODDataTypes.EXCHANGE_LIST.value

    # Implementing abstract method
    def get_data_from_server(self) -> pd.DataFrame:
        url = f'https://eodhistoricaldata.com/api/exchanges-list/?api_token={self.api_token}&fmt=json'
        response = requests.get(url)
        return pd.DataFrame(json.loads(response.text))

    # Implementing abstract method    
    def get_file_extension_type(self) -> str:
        return 'csv'

    # Implementing abstract method
    def get_cached_data_path(self, **kwargs) -> str:
        return os.path.join(self.base_path, self.data_type)


class ExchangeSymbolsDataGetter(AbstractDataGetter):
    """A class for caching data and fetching cached data.

    Given a user-specified file path, this class will save different
    data sets into different subdirectories.
    """
    # Implementing abstract method   
    @property 
    def data_type(self) -> str:
        return EODDataTypes.EXCHANGE_SYMBOLS.value

    # Implementing abstract method
    def get_data_from_server(
            self, exchange: Optional[str] = '') -> pd.DataFrame:
        url_listed = self._get_eod_url(exchange=exchange, delisted=False)
        res_listed = requests.get(url_listed)
        df_listed = pd.DataFrame(json.loads(res_listed.text))
        df_listed.loc[:, 'delisted'] = False

        url_delisted = self._get_eod_url(exchange=exchange, delisted=True)
        res_delisted = requests.get(url_delisted)
        df_delisted = pd.DataFrame(json.loads(res_delisted.text))
        df_delisted.loc[:, 'delisted'] = True
        return pd.concat([df_listed, df_delisted], axis=0)

    # Implementing abstract method    
    def get_file_extension_type(self) -> str:
        return 'csv'

    # Implementing abstract method
    def get_cached_data_path(self, exchange: str = '', **kwargs) -> str:
        if exchange is None:
            raise ValueError('The exchange ID must be provided.')
        return os.path.join(self.base_path, self.data_type, exchange)

    def _get_eod_url(self, exchange: str, delisted: int = False):
        """Returns the API endpoint for getting (de)listed exchange symbols."""
        return ('https://eodhistoricaldata.com/api/exchange-symbol-list/'
               f'{exchange}?api_token={self.api_token}&fmt=json&delisted={int(delisted)}')


class AbstractHistoricalTimeSeriesDataGetter(AbstractDataGetter):
    """An abstract class for caching data and fetching cached time series data.

    Given a user-specified file path, this class will save different
    data sets into different subdirectories.
    """
    @abstractmethod
    def get_time_series_data(
        self, symbol: str, frequency: str = '1d', 
        start: str = '', end: str = '') -> pd.DataFrame:
        pass

    # Implementing abstract method
    def get_data_from_server(
            self,
            symbol: str, 
            exchange_id: str = 'US',
            start: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
            end: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
            frequency: str = '1d',
            duration: str = '') -> pd.DataFrame:
        if not end:
            end = pd.Timestamp.today().round('d') - pd.Timedelta('1d')
        else:
            end = pd.Timestamp(end)

        if not start:
            if not duration:
                if frequency == '1d':
                    start = pd.Timestamp(HISTORICAL_DATA_START_DATE)
                elif frequency in INTRADAY_FREQUENCIES:
                    duration = f'{MAX_INTRADAY_DURATION}d'
                    start = end - pd.Timedelta(duration)
                else:
                    raise NotImplementedError(f'Unsupported frequency: {frequency}')

        else:
            start = pd.Timestamp(start)
            if frequency in INTRADAY_FREQUENCIES:  # Check intraday request is not too big
                if (end - start) / pd.Timedelta('1d') > MAX_INTRADAY_DURATION:
                    raise ValueError('Request is too long and must be broken into smaller requests.')

        return self.get_time_series_data(
            symbol=f'{symbol}.{exchange_id}', frequency=frequency,
            start=start, end=end)

    # Implementing abstract method    
    def get_file_extension_type(self) -> str:
        return 'csv'

    # Implementing abstract method
    def get_cached_data_path(
            self, 
            symbol: str = '',
            exchange_id: str = '', 
            frequency: str = '',
            **kwargs) -> str:
        if exchange_id is None:
            raise ValueError('The exchange ID must be provided.')
        return os.path.join(self.base_path, self.data_type, frequency,
                            exchange_id, symbol)


class HistoricalTimeSeriesDataGetter(AbstractHistoricalTimeSeriesDataGetter):
    """An abstract class for caching data and fetching cached data.

    Given a user-specified file path, this class will save different
    data sets into different subdirectories.
    """
    # Implementing abstract method
    @property
    def data_type(self) -> str:
        return EODDataTypes.HISTORICAL_TIME_SERIES.value

    # Implementing abstract method
    def get_time_series_data(
            self,
            symbol: str, 
            start: pd.Timestamp,
            end: pd.Timestamp,
            frequency: str = '1d',
        ) -> pd.DataFrame:
        url = self._get_historical_prices_url(
            symbol, frequency, start, end)
        response = requests.get(url)

        cols = ['open', 'high', 'low', 'close', 'volume']
        if frequency not in INTRADAY_FREQUENCIES:
            cols.append('adjusted_close')

        json_data = json.loads(response.text)
        if json_data:
            df = pd.DataFrame(json_data)
        else:
            df = pd.DataFrame([], columns=['date'] + cols)

        if 'datetime' in df.columns:
            df.rename({'datetime': 'date'}, axis=1, inplace=True)
        df.set_index('date', inplace=True)
        df.index = pd.DatetimeIndex(df.index)
        return df[cols]

    def _get_historical_prices_url(self, symbol,
            frequency, start, end):
        if frequency in INTRADAY_FREQUENCIES:
            freq_arg = 'interval'
            url_subpath = 'intraday'
            from_val = int(pd.Timestamp(start).timestamp())
            to_val = int(pd.Timestamp(end).timestamp())
        else:
            freq_arg = 'period'
            url_subpath = 'eod'
            from_val = pd.Timestamp(start).strftime('%Y%m%d')
            to_val = pd.Timestamp(end).strftime('%Y%m%d')

        return (f'https://eodhistoricaldata.com/api/{url_subpath}/'
                f'{symbol}?api_token={self.api_token}&fmt=json'
                f'&{freq_arg}={frequency}&from={from_val}&to={to_val}'
        )        
            

class MarketCapDataGetter(AbstractHistoricalTimeSeriesDataGetter):
    """A class for caching data and fetching cached data.

    Given a user-specified file path, this class will save different
    data sets into different subdirectories.
    """
    # Implementing abstract method    
    @property
    def data_type(self) -> str:
        return EODDataTypes.MARKET_CAP.value

    # Implementing abstract method
    def get_time_series_data(
            self,
            symbol: str, 
            frequency: str = '1d',
            start: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
            end: Union[str, datetime.date, datetime.datetime, pd.Timestamp] = '',
        ) -> pd.DataFrame:
        if frequency != '1d':
            raise ValueError('Only daily frequency is supported for market cap.')
        result = self.eod_client.get_market_cap(symbol=symbol)

        # The result is in JSON, so convert to pandas DataFrame
        if result:
            mc = pd.DataFrame(result).T.set_index('date')
            mc.index = pd.DatetimeIndex(mc.index)
            return mc
        else:
            return pd.DataFrame()


class FundamentalEquityDataGetter(AbstractDataGetter):
    """A class for caching data and fetching fundamental equity data.

    Given a user-specified file path, this class will save different
    data sets into different subdirectories.
    """
    # Implementing abstract method    
    @property
    def data_type(self) -> str:
        return EODDataTypes.FUNDAMENTAL_EQUITY.value

    # Implementing abstract method
    def get_data_from_server(
            self, symbol: str = '', exchange_id: str = 'US') -> dict:
        if exchange_id in US_EXCHANGES:
            exchange_id = 'US'

        url = ('https://eodhistoricaldata.com/api/fundamentals/'
               f'{symbol}.{exchange_id}?api_token={self.api_token}')
        response = requests.get(url)
        return json.loads(response.text)

    # Implementing abstract method    
    def get_file_extension_type(self) -> str:
        return 'json'

    # Implementing abstract method
    def get_cached_data_path(self, symbol: str = '', exchange_id: str = 'US', **kwargs) -> str:
        if exchange_id is None:
            raise ValueError('The exchange ID must be provided.')
        return os.path.join(self.base_path, self.data_type, exchange_id, symbol)


class FundamentalEquityBulkDataGetter(AbstractDataGetter):
    """A class for caching data and fetching cached fundamental equity data.

    Given a user-specified file path, this class will save different
    data sets into different subdirectories.
    """
    # Implementing abstract method    
    @property
    def data_type(self) -> str:
        return EODDataTypes.FUNDAMENTAL_EQUITY_BULK.value

    # Implementing abstract method
    def get_data_from_server(self,
                          exchange: Optional[str] = None,
                          symbols: str = '',
                          max_requests=200) -> dict:
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

    # Implementing abstract method    
    def get_file_extension_type(self) -> str:
        return 'json'

    # Implementing abstract method
    def get_cached_data_path(self, exchange: str = '', **kwargs) -> str:
        if exchange is None:
            raise ValueError('The exchange ID must be provided.')
        return os.path.join(self.base_path, self.data_type, exchange)  


# Factory method for getting an instance of the object
def get_cache_helper(api_token: str, data_type: str, base_path: str):
    """Factory method to return an instance of the appropriate data type."""
    if data_type == EODDataTypes.EXCHANGE_LIST.value:
        return ExchangeListDataGetter(
            api_token=api_token, base_path=base_path, default_stale_days=0)
    if data_type == EODDataTypes.EXCHANGE_SYMBOLS.value:
        return ExchangeSymbolsDataGetter(
            api_token=api_token, base_path=base_path, default_stale_days=0)
    if data_type == EODDataTypes.HISTORICAL_TIME_SERIES.value:
        return HistoricalTimeSeriesDataGetter(
            api_token=api_token, base_path=base_path, default_stale_days=0)
    if data_type == EODDataTypes.MARKET_CAP.value:
        return MarketCapDataGetter(
            api_token=api_token, base_path=base_path, default_stale_days=0)
    if data_type == EODDataTypes.FUNDAMENTAL_EQUITY.value:
        return FundamentalEquityDataGetter(
            api_token=api_token, base_path=base_path, default_stale_days=30)
    if data_type == EODDataTypes.FUNDAMENTAL_EQUITY_BULK.value:
        return FundamentalEquityBulkDataGetter(
            api_token=api_token, base_path=base_path, default_stale_days=30)
    else:
        raise ValueError(f'Unsupported data type: {data_type}')
