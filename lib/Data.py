import datetime
import lib.tradetime as tradetime

from lib.Config import Config
from lib.DB import DB


class Data(object):
    _db = None
    _cursor = None

    @staticmethod
    def trade_dates(ticker, min_date=None, max_date=None, as_dtime=True):
        """ Get a list of trade days for provided ticker """
        db = DB()
        query = 'select distinct(date(`dtime`)) as `d` from `quotes` where `ticker` = "%s" ' % ticker
        if min_date is not None or max_date is not None:
            if min_date is not None and not isinstance(min_date, datetime.datetime):
                min_date = datetime.datetime.combine(min_date, datetime.time(0, 0))
            if max_date is not None and not isinstance(max_date, datetime.datetime):
                max_date = datetime.datetime.combine(max_date, datetime.time(23, 59))
            if min_date is not None and max_date is not None:
                query += 'and `dtime` between "%s" and "%s" ' % (min_date, max_date)
            elif min_date is not None:
                query += 'and `dtime` >= "%s" ' % min_date
            else:
                query += 'and `dtime` <= "%s"' % max_date
        query += 'order by `d` asc'
        db.cursor.execute(query)
        midnight = datetime.time(0, 0)
        for date in db.cursor:
            if as_dtime:
                yield datetime.datetime.combine(date[0], midnight)
            else:
                yield date[0]
        db.close()
        pass

    @staticmethod
    def get(columns, ticker, dtime_from=None, dtime_to=None, date=None, market_hours=True, order='asc'):
        """
        Get minutely quote values for the given time range or date
        :param columns: Iterable set of columns that should be obtained
        :param ticker: Ticker name
        :param dtime_from: When selecting by time range: Time range start
        :param dtime_to: When selecting by time range: Time range end
        :param date: When selecting by date: Date
        :param market_hours: Should the data be obtained only within market hours?
        :param order: Records datetime order: 'asc' - old first, 'desc' - new first
        :return: Iterable generator with tuples for dtime + specified columns
        """
        if Data._db is None:
            Data._db = DB().db
            Data._cursor = Data._db.cursor()
        if isinstance(columns, str):
            # Specified indicators group: need to get all of them
            columns = Config.get('dbstructure.' + columns).keys()
        # MySQL tables that will be used and inner columns
        tables = []
        query_columns = []
        for column in columns:
            for table, table_indicators in Config.get('dbstructure').items():
                if column in table_indicators:
                    if len(query_columns) == 0:
                        query_columns.append('`%s`.`dtime`' % table)
                    query_columns.append('`%s`.`%s`' % (table, column))
                    if table not in tables:
                        tables.append(table)
                    break
        if len(tables) == 0:
            return
        query = 'select ' + ', '.join(query_columns) + ' from `' + '`, `'.join(tables) + '` '
        query += 'where `%s`.`ticker` = "%s" ' % (tables[0], ticker)
        if date is not None:
            if isinstance(date, datetime.date):
                date = datetime.datetime.combine(date, datetime.time(0, 0))
            elif isinstance(date, str):
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
            if market_hours:
                dtime_from = tradetime.daystart(date)
                dtime_to = tradetime.dayend(date)
            else:
                dtime_from = date.replace(hour=0, minute=0)
                dtime_to = date.replace(hour=23, minute=59)
        query += 'and `%s`.`dtime` between "%s" and "%s" ' % (tables[0], dtime_from, dtime_to)
        if market_hours and date is None:
            query += 'and time(`%s`.`dtime`) between "%s" and "%s" ' % (tables[0], tradetime.start, tradetime.end)
        # Joining tables
        for table in tables:
            if table == tables[0]:
                continue
            query += 'and `%s`.`ticker` = `%s`.`ticker` ' % (table, tables[0])
            query += 'and `%s`.`dtime` = `%s`.`dtime` ' % (table, tables[0])
        query += 'order by `dtime` ' + order
        Data._cursor.execute(query)
        for entry in Data._cursor:
            yield entry
        Data._db.commit()
