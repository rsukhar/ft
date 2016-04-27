import datetime
import redis
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
r = redis.Redis(host='localhost', port=6379, password='')


def key_to_date(key):
    return datetime.date(int('20' + key[:2]), int(key[2:4]), int(key[4:6]))


def date_to_key(date):
    return date.strftime('%y%m%d')


def trade_days(dtime_start, dtime_end):



def trade_dates(dtime_start, dtime_end):
    schedule = (930, 1559)
    day = key_to_date(dtime_start)
    day_end = key_to_date(dtime_end)
    while day <= day_end:
        time = schedule[0]
        day_key = date_to_key(day)
        while time <= schedule[1]:
            time_key = str(time)
            if len(time_key) < 4:
                time_key = '0' + time_key
            yield day_key + time_key
            time += 1
            if time % 100 > 59:
                time += 40
        day = day.fromordinal(day.toordinal() + 1)


for dkey in trade_dates('0910100930', '0910101600'):
    print(dkey)