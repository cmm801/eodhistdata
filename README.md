# eodhistdata
A library containing useful functions for downloading data from eodhistoricaldata.com. 

# Setup

This package's core functionality mostly encapsulates other packages'
existing functionality for fetching data from eodhistoricaldata.com - especially the `eod` and `eodhd` packages.

There are two main reasons for building this package:

* to assemble the best functions from the various packages that work with this data set.

* to build the cache functionality that I want to prevent having to download time series again and again.

The caching saves different data sets to different filepaths, all based on a user-defined base file path.

# Requirements

Some of this data set will be available for free, but all will require that the user register to get an API key from eodhistoricaldata.com. To be able to use this data for anything besides small examples will most likely require a paid subscription.

# Installation

This package can be installed using your favorite package manager. For example, you can download this package from GIT into your desired local directory, then CD into that directory and run
```pip install -e .```


# Meta

Christopher Miller – cmm801@gmail.com
February 24, 2023

Distributed under the MIT license. See ``LICENSE`` for more information.


## Contributing

1. Fork it (<https://github.com/cmm801/eodhistdata/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
