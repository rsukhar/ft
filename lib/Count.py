class Count(object):
    @staticmethod
    def indicator(name, ticker, date):
        """ Count the ticker indicator for the given date """
        pass

    @staticmethod
    def indicators(names, ticker, date):
        """ Count the ticker indicators for the given date """
        for name in names:
            Count.indicator(name, ticker, date)

    @staticmethod
    def chances(ticker, date, duration=15):
        """ Count the minutely ticker chances for the given date and duration """
        Count.indicator('c' + str(duration), ticker, date)
