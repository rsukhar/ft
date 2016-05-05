import datetime

start = datetime.time(10, 30)
end = datetime.time(16, 59)


def daystart(dtime):
    """The first trading minute of the provided day"""
    return dtime.replace(hour=start.hour, minute=start.minute)


def dayend(dtime):
    """The last trading minute of the provided day"""
    return dtime.replace(hour=end.hour, minute=end.minute)


def daymid(dtime):
    """ Select the very middle minute of the day """
    start_minute = start.hour * 60 + start.minute
    end_minute = end.hour * 60 + end.minute
    mid_minute = (start_minute + end_minute) / 2
    return dtime.replace(hour=int(mid_minute / 60), minute=int(mid_minute % 60))


def timerange(dtime_start, dtime_end):
    """ Get each minute of market working hours within the requested range """
    dtime = dtime_start
    minute = datetime.timedelta(minutes=1)
    while dtime <= dtime_end:
        yield dtime
        if dtime.hour == end.hour and dtime.minute == end.minute:
            dtime = daystart(dtime + datetime.timedelta(days=1))
        else:
            dtime += minute
