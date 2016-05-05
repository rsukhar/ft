from lib.Count import DBIndicatorCounter
from lib.Data import Data


class CountSMA(DBIndicatorCounter):
    def _count_sma(self, date):
        """
        Simple Moving Average
        :link https://en.wikipedia.org/wiki/Moving_average#Simple_moving_average
        """
        data = Data.get(['vwap'], self.ticker, date=date, market_hours=True)
        period = self.params[0]
        prices = []
        for dtime, price in data:
            prices.append(price)
            if len(prices) > period:
                del prices[0]
            if len(prices) == period:
                value = round(sum(prices) / period)
                self.update(dtime, value)
        self.commit()
