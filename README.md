# eodhistdata
A library containing useful functions for downloading data from eodhistoricaldata.com. 
    
# Meta

Christopher Miller – cmm801@gmail.com
February 24, 2023

Distributed under the MIT license. See ``LICENSE`` for more information.

# Overview

This package's core functionality mostly encapsulates other packages'
existing functionality for fetching data from eodhistoricaldata.com - especially the [eod](https://github.com/LautaroParada/eod-data) and [eodhd](https://github.com/EodHistoricalData/EODHD-APIs-Python-Financial-Library) packages.

There are two main reasons for building this package:

* to assemble the best functions from the various packages that work with this data set.

* to build cache functionality that prevents having to download the same time series again and again.


## More Caching Details

The caching saves different data sets to different filepaths, all based on a user-defined base file path.

By default, the data-fetching methods exposed to the user will first try to get data from the cache. For some data sets, such as fundamental data, the data is only updated infrequently on the server. Therefore, 
the caching mechanism will retrieve data cached several days ago for these data sets rather than querying the server. The parameter `stale_days` is specified per-method to define how many days old cached data is allowed to be before we would prefer to get the data from the server.

# Requirements

Some of this data set will be available for free, but all will require that the user register to get an API key from eodhistoricaldata.com. To be able to use this data for anything besides small examples will most likely require a paid subscription.

# Installation

This package can be installed using your favorite package manager. For example, you can download this package from GIT into your desired local directory, then CD into that directory and run
```pip install -e .```

import eodhistdata
from eodhistdata.private_constants import API_TOKEN, BASE_PATH

# Examples

Create a helper class instance by specifying your personal API token and the local path to which you want
cached data to be saved.

```
import eodhistdata
eod_helper = eodhistdata.EODHelper(
    api_token=API_TOKEN, base_path=BASE_PATH)
```

To get a pandas DataFrame containing a list of all the exchanges, run
```
eod_helper.get_exchange_list()
```

To get all the ticker symbols for a given exchange (e.g. for NYSE), run
```
exchange_symbols = eod_helper.get_exchange_symbols(exchange='NYSE')
```
Note that passing `exchange='US'` into this function will return symbol info for all major US stock exchanges (including OTC/PINK).


To get historical time series data, run:
```
eod_helper.get_historical_data(symbol='MSFT', frequency='1d')
```

To download fundamental equity data for AAPL, you would run
```
fundamental_data = eod_helper.get_fundamental_equity(exchange="NASDAQ", symbol="AAPL")
```

If you have a subscription to their Extended Fundamentals package, then you can bulk download fundamental data using pagination. For example, to get data for NYSE's symbols indexed from 200 to 400, you would run
```
fundamental_data = eod_helper.get_fundamentals_bulk(exchange='NYSE', max_requests=200, offset=200)
```

# Contributing

1. Fork it (<https://github.com/cmm801/eodhistdata/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
