import lib.daydata as daydata
import lib.tradetime as tradetime
import lib.indicators as indicators


class Indicator:
    ticker = None

    def __init__(self, ticker):
        self.ticker = ticker
        self.dd = daydata.daydata(self.ticker)


class EMA(Indicator):
    period = 26

    def __init__(self, ticker, period=26):
        Indicator.__init__(self, ticker)
        self.period = period

    def get_all(self):
        alpha = 2 / (self.period + 1)
        dates = [date for date in self.dd.get_dates()]
        for date in dates:
            index = 0
            initial_sum = 0
            prev_value = 0
            for dtime, close in self.dd.get_quotes(date, ('dtime', 'close')):
                index += 1
                if index < self.period:
                    initial_sum += close
                    continue
                elif index == self.period:
                    value = round((initial_sum + close) / self.period)
                else:
                    value = round(close * alpha + prev_value * (1 - alpha))
                yield dtime, value
                prev_value = value

