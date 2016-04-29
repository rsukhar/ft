import datetime
import re

from importlib import import_module

from lib.Config import Config
from lib.Data import Data
from lib.DB import DBUpdater


class DBIndicatorCounter(DBUpdater):
    def __init__(self, ticker, indicator):
        DBUpdater.__init__(self, ticker, indicator)
        match = re.match(r'^(?P<type>[a-z]+)(?P<period>\d*)$', indicator)
        if match is None or ('_count_' + match.group('type')) not in dir(self):
            raise Exception('Wrong indicator name for moving average: ' + indicator)
        self.type, self.period = match.groups()
        if self.period != '':
            self.period = int(self.period)
        self.ticker = ticker

    def count(self, date, data=None):
        """ Count indicator values for the given date. Data for the given day can be provided no to be fetched once again. """
        method = getattr(self, '_count_' + self.type)
        method(date, data)


class Count(object):
    __modules = {}
    __counters = {}

    @staticmethod
    def indicator(indicator, ticker, date=None):
        """ Count the ticker indicators for the given date (or for all the trade days if no date is specified) """
        counter = Count.__get_indicator_counter(ticker, indicator)
        if date is not None:
            # Counting for one particular date
            counter.count(date)
        else:
            # Counting indicator for all trade days
            for date in Data.trade_dates(ticker):
                counter.count(date)

    @staticmethod
    def indicators(indicators, ticker, date=None):
        """ Count the ticker indicators for the given date (or for all the trade days if no date is specified) """
        if isinstance(indicators, str):
            # Specified indicators group: need to count all of them
            indicators = Config.get('dbstructure.' + indicators).keys()
        for indicator in indicators:
            Count.indicator(indicator, ticker, date)

    @staticmethod
    def __get_indicator_counter(ticker, indicator):
        if (ticker, indicator) not in Count.__counters:
            tables = [table for table, indicators in Config.get('dbstructure').items() if indicator in indicators]
            if len(tables) == 0:
                raise Exception('Indicator ' + indicator + ' is not found in database')
            table = tables[0]
            if table not in Count.__modules:
                try:
                    Count.__modules[table] = import_module('indicators.' + table)
                except ImportError:
                    raise Exception('Indicator counter indicator.' + tables[0] + ' not found')
            counter_class = getattr(Count.__modules[table], 'Count' + table.capitalize())
            Count.__counters[(ticker, indicator)] = counter_class(ticker, indicator)
        return Count.__counters[(ticker, indicator)]
