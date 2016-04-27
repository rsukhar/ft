import datetime
import mysql.connector

if __name__ == '__main__':
    import tradetime
else:
    import lib.tradetime as tradetime


class MySQLQuotesInsert(object):
    db = None
    limit = 1000
    # We also need to insert relevant lines to all the indicator tables
    indicators_tables = ['ema']

    def __init__(self, host='localhost', user='root', password='', database='ft', insert_limit=1000):
        # TODO Get connection params from config
        self.db = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.limit = insert_limit
        self.stocks_query_base = 'insert ignore into `quotes` (`ticker`, `dtime`, `open`, `high`, `low`, `close`, `vol`) values '
        self.indicators_query_base = 'insert ignore into `{}` (`ticker`, `dtime`) values '
        self.quotes_entries = []
        self.indicators_entries = []

    def insert(self, ticker, dtime, open, high, low, close, vol):
        self.quotes_entries.append("('{}', '{}', {}, {}, {}, {}, {})".format(ticker,
                                                                             dtime.strftime('%Y-%m-%d %H:%M:%S'),
                                                                             int(float(open) * 100),
                                                                             int(float(high) * 100),
                                                                             int(float(low) * 100),
                                                                             int(float(close) * 100),
                                                                             int(vol)))
        self.indicators_entries.append("('{}', '{}')".format(ticker,
                                                             dtime.strftime('%Y-%m-%d %H:%M:%S')))
        if len(self.quotes_entries) >= self.limit:
            self.commit()

    def commit(self):
        if len(self.quotes_entries) == 0:
            return
        cursor = self.db.cursor()
        cursor.execute(self.stocks_query_base + ', '.join(self.quotes_entries))
        for indicator_table in self.indicators_tables:
            cursor.execute(self.indicators_query_base.format(indicator_table) + ', '.join(self.indicators_entries))
        self.quotes_entries.clear()
        self.indicators_entries.clear()
        self.db.commit()

    def close(self):
        self.commit()
        self.db.close()


class ImportFromFile(MySQLQuotesInsert):
    ticker = None

    def __init__(self, ticker):
        MySQLQuotesInsert.__init__(self)
        self.ticker = ticker

    def import_year(self, year):
        filename = '/srv/ft/data/{}-{}.csv'.format(self.ticker, year)
        last_dtime = None
        last_close = None
        minute = datetime.timedelta(minutes=1)
        for line in open(filename):
            data = line.split(';')
            dtime = datetime.datetime.strptime(data[0] + data[1], '%Y%m%d%H%M%S')
            if last_close is not None:
                # Filling the missing candles if needed
                if last_dtime.date() != dtime.date():
                    # The day is changed, checking if we need to fill the missing points
                    if last_dtime < tradetime.dayend(last_dtime):
                        self.fill_empty_values(last_dtime + minute, tradetime.dayend(last_dtime), last_close)
                    if dtime > tradetime.daystart(dtime):
                        self.fill_empty_values(tradetime.daystart(dtime), dtime - minute, last_close)
                elif (dtime - last_dtime).total_seconds() > 60:
                    self.fill_empty_values(last_dtime + minute, dtime - minute, last_close)
            self.insert(self.ticker, dtime, data[2], data[3], data[4], data[5], data[6])
            last_dtime = dtime
            last_close = data[5]
        # Filling missing values till the end of the day
        if last_dtime < tradetime.dayend(last_dtime):
            self.fill_empty_values(last_dtime + minute, tradetime.dayend(last_dtime), last_close)
        self.commit()

    def fill_empty_values(self, dtime_start, dtime_end, last_close):
        """ Fill missing trade quotes values including both dtime_start and dtime_end minutes """
        for dtime in tradetime.timerange(dtime_start, dtime_end):
            self.insert(self.ticker, dtime, last_close, last_close, last_close, last_close, 0)


if __name__ == '__main__':
    aaplImporter = ImportFromFile('AAPL')
    for year in range(2009, 2017):
        aaplImporter.import_year(year)
