import datetime
import re
import lib.tradetime as tradetime

from importlib import import_module
from lib.Config import Config
from lib.Data import Data
from lib.DB import DBUpdater


class DBIndicatorCounter(DBUpdater):
    def __init__(self, ticker, indicator):
        DBUpdater.__init__(self, ticker, indicator)
        match = re.match(r'^(?P<type>[A-Za-z]+)\((?P<params>[^\)]+)\)$', indicator)
        if match is None or ('_count_' + match.group('type').lower()) not in dir(self):
            raise Exception('Wrong indicator name for moving average: ' + indicator)
        self.type = match.group('type')
        self.params = []
        for param in match.group('params').split(', '):
            if '.' in param:
                self.params.append(float(param))
            else:
                self.params.append(int(param))
        self.ticker = ticker

    def count(self, date):
        """ Count indicator values for the given date. Data for the given day can be provided no to be fetched once again. """
        method = getattr(self, '_count_' + self.type.lower())
        method(date)


class Count(object):
    __modules = {}
    __counters = {}

    @staticmethod
    def count(indicators, ticker, date=None):
        """ Count the requested set of indicators """
        indicators = Count.__fix_indicators_list(indicators)
        if date is not None and isinstance(date, str):
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
        for indicator in indicators:
            counter = Count.__get_indicator_counter(ticker, indicator)
            if date is not None:
                # Counting for one particular date
                counter.count(date)
            else:
                # Counting indicator for all trade days
                for date in Data.trade_dates(ticker):
                    counter.count(date)
        return None

    @staticmethod
    def count_once(indicators, ticker, date=None):
        """ Count the requested set of indicators if they were not counted previously """
        indicators = Count.__fix_indicators_list(indicators)
        # Getting data 1-minute slice from the very middle of the day to check which data presents and which is missing
        if date is not None and isinstance(date, str):
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
        date_mid = tradetime.daymid(date)
        missing_indicators = []
        data = list(Data.get(indicators, ticker, dtime_from=date_mid, dtime_to=date_mid, market_hours=False))
        if len(data) == 0:
            missing_indicators = list(indicators)
        else:
            for index, value in enumerate(data[0]):
                if index > 0 and value is None:
                    missing_indicators.append(indicators[index - 1])
        if len(missing_indicators) > 0:
            Count.count(missing_indicators, ticker, date)

    @staticmethod
    def __fix_indicators_list(old_indicators):
        indicators = []
        if isinstance(old_indicators, str):
            old_indicators = [old_indicators]
        for indicator in old_indicators:
            if '(' not in indicator:
                indicators.extend(Config.get('dbstructure.' + old_indicators, []).keys())
            else:
                indicators.append(indicator)
        return indicators

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
            counter_class = getattr(Count.__modules[table], 'Count' + table)
            Count.__counters[(ticker, indicator)] = counter_class(ticker, indicator)
        return Count.__counters[(ticker, indicator)]
