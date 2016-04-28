import lib.tradetime as tradetime
import mysql.connector
import datetime


class daydata:
    ticker = None

    def __init__(self, ticker, host='localhost', user='root', password='', database='ft'):
        self.ticker = ticker
        # TODO Get connection params from config
        self.db = mysql.connector.connect(host=host, user=user, password=password, database=database)

    def get_quotes(self, date, fields=('dtime', 'open', 'high', 'low', 'close', 'vol')):
        """ Get minutely quotes for the provided date """
        cursor = self.db.cursor()
        query = 'select `' + '`, `'.join(fields) + '` from `quotes` '
        query += 'where `ticker` = %s and `dtime` between %s and %s order by `dtime` asc'
        cursor.execute(query, (self.ticker, tradetime.daystart(date), tradetime.dayend(date)))
        for entry in cursor:
            yield entry
        cursor.close()
