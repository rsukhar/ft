import redis

from old import lib as lib_helpers

r = redis.Redis(host='localhost', port=6379, password='')


def fill_missing_minutes(ticker):
    """Fill missing minutes candles"""
    dtime_start = r.hget(ticker + ':params', 'dtime_start')
    dtime_end = r.hget(ticker + ':params', 'dtime_end')
    if dtime_start is None or dtime_end is None:
        return
    for date in lib_helpers.trade_days(dtime_start, dtime_end):
        if len(r.keys(ticker + ':' + date + '????')) == 0:
            # Day should have at least one candle to be filled
            continue
        last_close = None
        for time in lib_helpers.trade_minutes():
            if r.hlen(ticker + ':' + date + time) != 0:
                last_close = r.hget(ticker + ':' + date + time, 'close')
            elif last_close is not None:
                print('should fill: ' + date + time)
                r.hset(ticker + ':' + date + time, 'high', last_close)
                r.hset(ticker + ':' + date + time, 'close', last_close)
                r.hset(ticker + ':' + date + time, 'open', last_close)
                r.hset(ticker + ':' + date + time, 'low', last_close)
                r.hset(ticker + ':' + date + time, 'vol', 0)
