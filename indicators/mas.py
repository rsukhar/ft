from lib.Count import DBIndicatorCounter
from lib.Data import Data


class CountMas(DBIndicatorCounter):
    def _count_ema(self, date, data=None):
        """
        Exponential Moving Average
        :link https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
        """
        if data is None:
            data = Data.day_quotes(['vwap'], self.ticker, date, market_hours=True)
        alpha = 2 / (self.period + 1)
        index = 0
        initial_sum = 0
        prev_value = 0
        for dtime, price in data:
            index += 1
            if index < self.period:
                initial_sum += price
                continue
            elif index == self.period:
                value = round((initial_sum + price) / self.period)
            else:
                value = round(price * alpha + prev_value * (1 - alpha))
            self.update(dtime, value)
            prev_value = value
        self.commit()
