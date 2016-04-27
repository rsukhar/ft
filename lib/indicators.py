import datetime
import mysql.connector


class MySQLIndicatorsUpdate(object):
    db = None
    limit = 1000

    def __init__(self, ticker, table, column, host='localhost', user='root', password='', database='ft', insert_limit=1000):
        # TODO Get connection params from config
        self.db = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.limit = insert_limit
        self.query_start = 'update `' + table + '` set `' + column + '` = (case '
        self.query_end = ' end) where `ticker` = "' + ticker + '" and `dtime` between "{}" and "{}"'
        self.entries = []
        self.min_dtime = None
        self.max_dtime = None

    def insert(self, dtime, value):
        """ Note: insertions should be continuous """
        self.entries.append('when `dtime` = "' + dtime.strftime('%Y-%m-%d %H:%M:%S') + '" then ' + str(value))
        if self.min_dtime is None:
            self.min_dtime = dtime
        self.max_dtime = dtime
        if len(self.entries) >= self.limit:
            self.commit()

    def commit(self):
        if len(self.entries) == 0:
            return
        cursor = self.db.cursor()
        query_end = self.query_end.format(self.min_dtime.strftime('%Y-%m-%d %H:%M:%S'),
                                          self.max_dtime.strftime('%Y-%m-%d %H:%M:%S'))
        cursor.execute(self.query_start + ' '.join(self.entries) + query_end)
        self.min_dtime = None
        self.max_dtime = None
        self.entries.clear()
        self.db.commit()

    def close(self):
        self.commit()
        self.db.close()
