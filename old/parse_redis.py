import redis
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
r = redis.Redis(host='localhost', port=6379, password='')


def parse_year(ticker, year):
    print('Starting: {}-{}'.format(ticker, year))
    fname = '/srv/ft/data/' + ticker + '-{}.csv'.format(year)
    dtime_start = r.hget(ticker + ':params', 'dtime_start')
    if not dtime_start is None:
        dtime_start = int('20' + dtime_start)
    dtime_end = r.hget(ticker + ':params', 'dtime_end')
    if not dtime_end is None:
        dtime_end = int('20' + dtime_end)
    with open(fname) as f:
        for line in f:
            data = line.split(';')
            date = data[0]
            time = data[1]
            dtime = int(date + time[:4])
            if dtime_start is None or dtime_start > dtime:
                dtime_start = dtime
            if dtime_end is None or dtime_end < dtime:
                dtime_end = dtime
            key = ticker + ':{}{}{}{}{}'.format(date[2:4], date[4:6], date[6:8], time[:2], time[2:4])
            r.hset(key, 'open', int(float(data[2]) * 100))
            r.hset(key, 'high', int(float(data[3]) * 100))
            r.hset(key, 'low', int(float(data[4]) * 100))
            r.hset(key, 'close', int(float(data[5]) * 100))
            r.hset(key, 'vol', int(data[6]))
    if not dtime_start is None:
        r.hset(ticker + ':params', 'dtime_start', str(dtime_start)[2:])
    if not dtime_end is None:
        r.hset(ticker + ':params', 'dtime_end', str(dtime_end)[2:])
    print('Done: {}-{}'.format(ticker, year))


for year in range(2009, 2017):
    parse_year('DIS', year)
