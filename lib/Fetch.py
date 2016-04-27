import os.path
import urllib.request
import mysql.connector
import datetime
import lib.tradetime as tradetime

from lib.Config import Config
from lib.DB import DBInserter


class Fetch(object):
    @staticmethod
    def quotes_to_file(ticker, year, filename, force=False):
        if not force and os.path.isfile(filename):
            return
        remote_host = Config.get('Fetch', 'remote_host', fallback=None)
        ticker_code = Config.get('FetchTickerCodes', ticker, fallback=None)
        if remote_host is None or ticker_code is None:
            return
        # Imitating the website-generated URL for the whole year
        fname = 'US2.' + ticker + '_' + str(year)[2:4] + '0101_' + str(year)[2:4] + '1231'
        url = remote_host + fname + '.csv?market=25&em=' + str(ticker_code) + '&code=US2.' + ticker + '&apply=0&'
        url += 'df=1&mf=0&yf=' + str(year) + '&from=01.01.' + str(year) + '&'
        url += 'dt=31&mt=11&yt=' + str(year) + '&to=31.12.' + str(year) + '&'
        url += 'p=2&f=' + fname + '&e=.csv&cn=US2.' + ticker + '&dtf=1&tmf=1&MSOR=0&mstimever=0&sep=3&sep2=1&datf=5'
        urllib.request.urlretrieve(url, filename)

    @staticmethod
    def vwap_to_file(ticker, year, filename, force=False):
        pass

    @staticmethod
    def splits_to_file(ticker, filename, force=False):
        pass

    @staticmethod
    def import_quotes(ticker, filename):

        def fill_empty_values(dtime_start, dtime_end, last_close):
            """ Fill missing trade quotes' values including both dtime_start and dtime_end minutes """
            for dtime in tradetime.timerange(dtime_start, dtime_end):
                db.insert(ticker, dtime, last_close, last_close, last_close, last_close, 0)

        if not os.path.isfile(filename):
            return
        db = DBInserter()
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
                        fill_empty_values(last_dtime + minute, tradetime.dayend(last_dtime), last_close)
                    if dtime > tradetime.daystart(dtime):
                        fill_empty_values(tradetime.daystart(dtime), dtime - minute, last_close)
                elif (dtime - last_dtime).total_seconds() > 60:
                    fill_empty_values(last_dtime + minute, dtime - minute, last_close)
            db.insert(ticker, dtime, data[2], data[3], data[4], data[5], data[6])
            last_dtime = dtime
            last_close = data[5]
        # Filling missing values till the end of the day
        if last_dtime < tradetime.dayend(last_dtime):
            fill_empty_values(last_dtime + minute, tradetime.dayend(last_dtime), last_close)
        db.commit()

    @staticmethod
    def import_vwap(ticker, filename):
        pass
