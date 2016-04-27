from lib.DB import DB


class Data(object):
    @staticmethod
    def trade_dates(ticker):
        """ Get a list of trade days for provided ticker """
        pass

    @staticmethod
    def quotes(columns, ticker, dtime_from, dtime_to, market_hours=True):
        """ Get minutely ticker quotes for the given time range """
        pass

    @staticmethod
    def day_quotes(columns, ticker, date, market_hours=True):
        """ Get minutely ticker quotes for the given day """
        pass

    @staticmethod
    def indicators(names, ticker, dtime_from, dtime_to):
        """ Get minutely ticker indicators' values for the given time range """
        pass

    @staticmethod
    def day_indicators(names, ticker, date):
        """ Get minutely ticker indicators' values for the given day """
        pass

    @staticmethod
    def chances(ticker, dtime_from, dtime_to):
        """ Get minutely ticker chances values for the given time range """
        pass

    @staticmethod
    def day_chances(ticker, date):
        """ Get minutely ticker chances values for the given day """
        pass
