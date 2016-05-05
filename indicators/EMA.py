from lib.Count import DBIndicatorCounter
from lib.Data import Data


class CountEMA(DBIndicatorCounter):
    def _count_ema(self, date):
        """
        Exponential Moving Average
        :link https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
        """
        data = Data.get(['vwap'], self.ticker, date=date, market_hours=True)
        period = self.params[0]
        alpha = 2 / (period + 1)
        initial_sum = 0
        prev_value = 0
        for index, (dtime, price) in enumerate(data):
            if index < period - 1:
                initial_sum += price
                continue
            elif index == period - 1:
                value = round((initial_sum + price) / period)
            else:
                value = round(price * alpha + prev_value * (1 - alpha))
            self.update(dtime, value)
            prev_value = value
        self.commit()