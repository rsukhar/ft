import mysql.connector

from collections import OrderedDict

from lib.Config import Config


class DB(object):
    db = None

    def __init__(self):
        self.db = mysql.connector.connect(**Config.get('db'))
        self.cursor = self.db.cursor()

    def commit(self):
        self.db.commit()

    def close(self):
        self.commit()
        self.cursor.close()
        self.db.close()


class DBInstaller(DB):
    """
    Create all the needed tables and columns for quotes and indicators based on config and provide the database
    consistency, so for every entry in quote table there are relevant entries in the indicators tables.
    If safe is set to False, then the database will be erased before installation.
    """

    def install(self, safe=True):
        if not safe:
            # Deleting all the existing tables before proceeding
            self.cursor.execute('show tables')
            tables = [table for (table,) in self.cursor]
            for table in tables:
                self.cursor.execute('drop table `%s`' % table)
            self.db.commit()
        cur_db = self.__get_existing_structure()
        req_db = self.__get_required_structure()
        # Deleting excess tables
        self.__delete_tables([table for table in cur_db if table not in req_db])
        for table, req_columns in req_db.items():
            if table not in cur_db:
                # Creating missing table
                self.__create_table(table, req_columns)
                if table != 'quotes':
                    self.__import_keys_from_quotes(table)
            elif cur_db[table] != req_columns:
                # Updating the existing tables that differ from the target
                self.__update_table(table, cur_db[table], req_columns)
            self.__fix_indexes(table)
        pass

    def __get_existing_structure(self):
        """ Get the existing database schema """
        # Obtaining the existing database structure from the database
        db_structure = OrderedDict()
        self.cursor.execute('show tables')
        tables = [table for (table,) in self.cursor]
        for table in tables:
            self.cursor.execute('show columns from `%s`' % table)
            db_structure[table] = OrderedDict()
            for cname, ctype, cnull, ckey, cdefault, cextra in self.cursor:
                db_structure[table][cname] = ctype
        return db_structure

    def __get_required_structure(self):
        """ Get required database schema from config file """
        # Note: using ordered dict because quotes table should always go first
        db_structure = OrderedDict()
        for table, columns in Config.get('dbstructure').items():
            db_structure[table] = OrderedDict([('ticker', 'varchar(6)'), ('dtime', 'datetime')])
            for column, type in columns.items():
                if column == 'ticker' or column == 'dtime':
                    continue
                db_structure[table][column] = type
        return db_structure

    def __create_table(self, table, columns):
        """ Create the database table based on the provided columns list """
        create_spec = []
        for col_name, col_type in columns.items():
            create_spec.append('`%s` %s null' % (col_name, col_type))
        self.cursor.execute(('create table `%s` (' % table) + ', '.join(create_spec) + ')')

    def __fix_indexes(self, table):
        """ Make sure the table has all the needed indexes """
        # Getting the current table indexes
        self.cursor.execute('show keys from `%s`' % table)
        cur_indexes = {}
        for entry in self.cursor:
            iname = entry[2]
            icolumn = entry[4]
            iunique = not entry[1]
            if iname not in cur_indexes:
                cur_indexes[iname] = {
                    'columns': [icolumn],
                    'unique': iunique
                }
            else:
                cur_indexes[iname]['columns'].append(icolumn)
        alter_spec = []
        # Removing wrong excess keys
        for index_name, index_params in cur_indexes.items():
            if index_name == 'candle' and index_params['columns'] == ['ticker', 'dtime'] and index_params['unique']:
                continue
            alter_spec.append('drop key `%s`' % index_name)
            del cur_indexes[index_name]
        # Adding the needed keys
        if 'candle' not in cur_indexes:
            alter_spec.append('add unique key `candle` (`ticker`, `dtime`)')
        self.cursor.execute(('alter table `%s` ' % table) + ', '.join(alter_spec))
        self.db.commit()

    def __import_keys_from_quotes(self, table):
        """ Make sure the table has the same ticker/dtime entries as the quotes table does """
        self.cursor.execute('insert ignore into `%s` (`ticker`, `dtime`) '
                            'select `ticker`, `dtime` from `quotes`' % table)
        self.db.commit()

    def __update_table(self, table, old_columns, new_columns):
        """ Update the database table from the old_columns state to the new_columns state """
        alter_spec = []
        cur_col_names = list(old_columns.keys())
        # Removing the excess columns first
        for col_name in old_columns:
            if col_name not in new_columns:
                alter_spec.append('drop column `%s`' % col_name)
                cur_col_names.remove(col_name)
        column_position = 'first'
        index = 0
        for col_name, new_type in new_columns.items():
            if col_name not in old_columns:
                # Creating missing column
                alter_spec.append('add column `%s` %s null %s' % (col_name, new_type, column_position))
                cur_col_names[index:index] = [col_name]
            elif old_columns[col_name] != new_type or cur_col_names[index] != col_name:
                # Changing column type and/or moving it
                alter_spec.append('modify column `%s` %s null %s' % (col_name, new_type, column_position))
                cur_col_names.remove(col_name)
                cur_col_names[index:index] = [col_name]
            index += 1
            column_position = 'after `%s`' % col_name
        self.cursor.execute(('alter table `%s` ' % table) + ', '.join(alter_spec))
        self.db.commit()
        pass

    def __delete_tables(self, tables):
        """ Delete the provided tables """
        if len(tables) > 0:
            for table in tables:
                self.cursor.execute('drop table `%s`' % table)
            self.db.commit()


class DBInserter(DB):
    """ Inserts quotes to the relevant table and fills indicators tables with the proper entries too """

    def __init__(self, limit=1000):
        DB.__init__(self)
        self.limit = limit
        self.quotes_query_base = 'insert ignore into `quotes` (`ticker`, `dtime`, `open`, `high`, `low`, `close`, `vol`) values '
        self.quotes_entries = []
        self.indicators_tables = set([table for table in Config.get('dbstructure') if table != 'quotes'])
        self.indicators_query_base = 'insert ignore into `{}` (`ticker`, `dtime`) values '
        self.indicators_entries = []

    def insert(self, ticker, dtime, open, high, low, close, vol):
        query_keys = '"%s", "%s"' % (ticker, dtime)
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
        self.cursor.execute(self.quotes_query_base + ', '.join(self.quotes_entries))
        self.quotes_entries.clear()
        if len(self.indicators_tables) > 0:
            for indicator_table in self.indicators_tables:
                self.cursor.execute(
                    self.indicators_query_base.format(indicator_table) + ', '.join(self.indicators_entries))
            self.indicators_entries.clear()
        self.db.commit()


class DBUpdater(DB):
    """
    Updates indicators in the relevant tables.
    Note: the range of entries updated within a single commit should be continuous.
    """

    def __init__(self, ticker, indicator, limit=1000):
        DB.__init__(self)
        self.limit = limit
        tables = [table for table, indicators in Config.get('dbstructure').items() if indicator in indicators]
        if len(tables) == 0:
            raise Exception('Indicator %s is not found in database' % indicator)
        self.query_start = 'update `%s` set `%s` = (case ' % (tables[0], indicator)
        self.query_end = ' end) where `ticker` = "%s" and `dtime` between "{}" and "{}"' % ticker
        self.entries = []
        self.min_dtime = None
        self.max_dtime = None

    def update(self, dtime, value):
        self.entries.append('when `dtime` = "%s" then %s' % (dtime, value))
        if self.min_dtime is None or dtime < self.min_dtime:
            self.min_dtime = dtime
        if self.max_dtime is None or dtime > self.max_dtime:
            self.max_dtime = dtime
        if len(self.entries) >= self.limit:
            self.commit()

    def commit(self):
        if len(self.entries) == 0:
            return
        query_end = self.query_end.format(self.min_dtime, self.max_dtime)
        self.cursor.execute(self.query_start + ' '.join(self.entries) + query_end)
        self.min_dtime = None
        self.max_dtime = None
        self.entries.clear()
        self.db.commit()
