import datetime

DAY_START = {'hour': 10, 'minute': 30}
DAY_END = {'hour': 16, 'minute': 59}


def daystart(dtime):
    """The first trading minute of the provided day"""
    return dtime.replace(**DAY_START)


def dayend(dtime):
    """The last trading minute of the provided day"""
    return dtime.replace(**DAY_END)


def timerange(dtime_start, dtime_end):
    dtime = dtime_start
    minute = datetime.timedelta(minutes=1)
    while dtime <= dtime_end:
        yield dtime
        if dtime.hour == DAY_END['hour'] and dtime.minute == DAY_END['minute']:
            dtime = daystart(dtime + datetime.timedelta(days=1))
        else:
            dtime += minute


if __name__ == '__main__':
    # First: iteration
    dtime_start = datetime.datetime(2010, 10, 10, 15, 20)
    dtime_end = datetime.datetime(2010, 10, 11, 9, 45)
    for dtime in timerange(dtime_start, dtime_end):
        print(dtime)
        # Second: minutes diff
