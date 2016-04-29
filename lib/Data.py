import datetime
import lib.tradetime as tradetime

from lib.Config import Config
from lib.DB import DB


class Data(object):
    db = None

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
    def quotes(columns, ticker, dtime_from, dtime_to, market_hours=True, order='asc'):
        """ Get minutely ticker quotes for the given time range """
        if Data.db is None:
            Data.db = DB().db
        if 'dtime' not in columns:
            columns[0:0] = ['dtime']
        cursor = Data.db.cursor()
        query = 'select `' + '`, `'.join(columns) + '` from `quotes` '
        query += 'where `ticker` = %s and `dtime` between %s and %s '
        if market_hours:
            query += 'and time(`dtime`) between "%s" and "%s" ' % (tradetime.start, tradetime.end)
        query += 'order by `dtime` ' + order
        cursor.execute(query, (ticker, dtime_from, dtime_to))
        for entry in cursor:
            yield entry
        cursor.close()

    @staticmethod
    def day_quotes(columns, ticker, date, market_hours=True, order='asc'):
        """ Get minutely ticker quotes for the given day """
        if isinstance(date, datetime.date):
            date = datetime.datetime.combine(date, datetime.time(0, 0))
        if market_hours:
            dtime_from = tradetime.daystart(date)
            dtime_to = tradetime.dayend(date)
        else:
            dtime_from = date.replace(hour=0, minute=0)
            dtime_to = date.replace(hour=23, minute=59)
        # No need to separately filter market hours in Data.quotes as the needed time range is already set here
        return Data.quotes(columns, ticker, dtime_from, dtime_to, market_hours=False, order=order)

    @staticmethod
    def indicators(indicators, ticker, dtime_from, dtime_to, market_hours=True, order='asc'):
        """ Get minutely ticker indicators' values for the given time range """
        if Data.db is None:
            Data.db = DB().db
        if isinstance(indicators, str):
            # Specified indicators group: need to get all of them
            indicators = Config.get('dbstructure.' + indicators).keys()
        # MySQL tables that will be used and inner columns
        tables = []
        query_columns = []
        for indicator in indicators:
            for table, table_indicators in Config.get('dbstructure').items():
                if indicator in table_indicators:
                    if len(query_columns) == 0:
                        query_columns.append('`%s`.`dtime`' % table)
                    query_columns.append('`%s`.`%s`' % (table, indicator))
                    if table not in tables:
                        tables.append(table)
                    break
        if len(tables) == 0:
            return
        query = 'select ' + ', '.join(query_columns) + ' from `' + '`, `'.join(tables) + '` '
        query += 'where `%s`.`ticker` = "%s" ' % (tables[0], ticker)
        query += 'and `%s`.`dtime` between "%s" and "%s" ' % (tables[0], dtime_from, dtime_to)
        if market_hours:
            query += 'and time(`%s`.`dtime`) between "%s" and "%s" ' % (tables[0], tradetime.start, tradetime.end)
        # Joining tables
        for table in tables:
            if table == tables[0]:
                continue
            query += 'and `%s`.`ticker` = `%s`.`ticker` ' % (table, tables[0])
            query += 'and `%s`.`dtime` = `%s`.`dtime` ' % (table, tables[0])
        query += 'order by `dtime` ' + order
        print(query)
        pass

    @staticmethod
    def day_indicators(names, ticker, date, order='asc'):
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
