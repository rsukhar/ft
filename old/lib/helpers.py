import datetime
# https://nikolak.com/pyqt-threading-tutorial/

SCHEDULE = (930, 1559)


def key_to_date(key):
    return datetime.date(int('20' + key[:2]), int(key[2:4]), int(key[4:6]))


def date_to_key(date):
    return date.strftime('%y%m%d')


def trade_days(date_start, date_end):
    """Generator of trade days between the provided date range"""
    # TODO Take into account holidays
    day = key_to_date(date_start)
    day_end = key_to_date(date_end)
    while day <= day_end:
        yield date_to_key(day)
        day = day.fromordinal(day.toordinal() + 1)


def trade_minutes():
    """Generator of trade minutes"""
    time = SCHEDULE[0]
    while time <= SCHEDULE[1]:
        time_key = str(time)
        if len(time_key) < 4:
            time_key = '0' + time_key
        yield time_key
        time += 1
        if time % 100 > 59:
            time += 40
