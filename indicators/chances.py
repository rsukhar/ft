from lib.Count import DBIndicatorCounter
from lib.Data import Data


class CountChances(DBIndicatorCounter):
    def _count_c(self, date, data=None):
        """
        Relative price difference in the next N minutes
        """
        if data is None:
            data = Data.day_quotes(['open', 'vwap'], self.ticker, date, market_hours=True, order='desc')
        history = []
        index = 0
        for dtime, open, vwap in data:
            index += 1
            if index > self.period:
                index = 1
            if len(history) < index:
                history.append(vwap)
            else:
                value = round((history[index - 1] - open) / open * 100, 2)
                history[index - 1] = vwap
                self.update(dtime, value)
        self.commit()
