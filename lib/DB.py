import mysql.connector

from lib.Config import Config


class DB(object):
    db = None

    def __init__(self):
        self.db = mysql.connector.connect(**Config.get('Database'))

    def commit(self):
        self.db.commit()

    def close(self):
        self.commit()
        self.close()


class DBInserter(DB):
    """ Inserts quotes to the relevant table and fills indicators tables with the proper entries too """
    indicators_tables = []

    def __init__(self, limit=1000):
        DB.__init__(self)
        self.limit = limit
        self.indicators_tables = set(Config.get('Indicators', fallback={}).values())
        self.quotes_query_base = 'insert ignore into `quotes` (`ticker`, `dtime`, `open`, `high`, `low`, `close`, `vol`) values '
        self.indicators_query_base = 'insert ignore into `{}` (`ticker`, `dtime`) values '
        self.quotes_entries = []
        self.indicators_entries = []

    def insert(self, ticker, dtime, open, high, low, close, vol):
        query_keys = '"%s", "%s"' % (ticker, dtime.strftime('%Y-%m-%d %H:%M:%S'))
        query_values = '%d, %d, %d, %d, %d' % (int(float(open) * 100),
                                               int(float(high) * 100),
                                               int(float(low) * 100),
                                               int(float(close) * 100),
                                               int(vol))
        self.quotes_entries.append('(' + query_keys + ', ' + query_values + ')')
        if len(self.indicators_tables) > 0:
            self.indicators_entries.append('(' + query_keys + ')')
        if len(self.quotes_entries) >= self.limit:
            self.commit()

    def commit(self):
        if len(self.quotes_entries) == 0:
            return
        cursor = self.db.cursor()
        cursor.execute(self.quotes_query_base + ', '.join(self.quotes_entries))
        self.quotes_entries.clear()
        if len(self.indicators_tables) > 0:
            for indicator_table in self.indicators_tables:
                cursor.execute(self.indicators_query_base.format(indicator_table) + ', '.join(self.indicators_entries))
            self.indicators_entries.clear()
        self.db.commit()
