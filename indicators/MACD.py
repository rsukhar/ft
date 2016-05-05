from lib.Count import DBIndicatorCounter, Count
from lib.Data import Data


class CountMACD(DBIndicatorCounter):
    def _count_macd(self, date):
        """
        Moving Average Convergence/Divergence
        :link https://en.wikipedia.org/wiki/MACD
        """
        period1, period2, period3 = self.params
        if period1 > period2:
            # period1 should always be less than period2
            period1, period2 = period2, period2
        # Obtaining the needed data
        Count.count_once(['EMA(' + str(period1) + ')', 'EMA(' + str(period2) + ')'], self.ticker, date=date)
        data = Data.get(['EMA(' + str(period1) + ')', 'EMA(' + str(period2) + ')'], self.ticker, date=date)
        alpha = 2 / (period3 + 1)
        initial_sum = 0
        prev_signal = 0
        for index, (dtime, ema1, ema2) in enumerate(data):
            ema_diff = ema1 - ema2
            if index < period3 - 1:
                initial_sum += ema_diff
                continue
            elif index == period3 - 1:
                signal = round((initial_sum + ema_diff) / period3)
            else:
                signal = round(ema_diff * alpha + prev_signal * (1 - alpha))
            self.update(dtime, signal)
            prev_signal = signal
        self.commit()
