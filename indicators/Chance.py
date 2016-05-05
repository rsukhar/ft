from lib.Count import DBIndicatorCounter
from lib.Data import Data


class CountChance(DBIndicatorCounter):
    def _count_chance(self, date):
        """
        Relative price difference in the next N minutes
        """
        data = Data.get(['open', 'vwap'], self.ticker, date=date, market_hours=True, order='desc')
        period = self.params[0]
        history = []
        index = 0
        for dtime, open, vwap in data:
            index += 1
            if index > period:
                index = 1
            if len(history) < index:
                history.append(vwap)
            else:
                value = round((history[index - 1] - open) / open * 100, 2)
                history[index - 1] = vwap
                self.update(dtime, value)
        self.commit()
