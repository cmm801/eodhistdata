"""Definitions of important constants."""

from enum import Enum

class EODDataTypes(Enum):
    """An Enum class enumerating the various available data sets."""
    EXCHANGE_LIST = 'exchange_list'
    EXCHANGE_SYMBOLS = 'exchange_symbols'
    HISTORICAL_TIME_SERIES = 'historical_time_series'
    MARKET_CAP = 'market_cap'
    FUNDAMENTAL_EQUITY = 'fundamental_equity'

# A list of the exchange codes that use exchange_id == 'US'
US_EXCHANGES = [
    'AMEX', 'BATS', 'NASDAQ', 'NMFQS', 'NYSE', 'NYSE ARCA',
    'NYSE MKT', 'OTC', 'OTCBB', 'OTCCE', 'OTCGREY', 'OTCMKTS',
    'OTCQB', 'OTCQX', 'PINK']