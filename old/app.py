from __future__ import unicode_literals
import sys
import os
from matplotlib.backends import qt_compat
from old import lib
import redis

r = redis.Redis(host='localhost', port=6379, password='')

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

import ui.app as ui_app
from matplotlib import dates
import datetime

class FT_App(QtGui.QMainWindow, ui_app.Ui_windowApp):
    def __init__(self):
        app = QtGui.QApplication(sys.argv)
        form = QtGui.QWidget()
        self.setupUi(form)
        form.show()
        self.fill_tickers_combobox()
        self.comboTicker.currentIndexChanged[str].connect(self.quotes_params_changed)
        self.dateDay.dateChanged.connect(self.quotes_params_changed)
        self.dateDay.setDate(QtCore.QDate.currentDate())
        dt = QtCore.QDate()
        dt.getDate()
        sys.exit(app.exec_())

    def fill_tickers_combobox(self):
        tickers = ['AAPL', 'DIS', 'GOOG', 'MSFT']
        self.comboTicker.clear()
        self.comboTicker.addItems(tickers)

    def render_chart(self, ticker, date):
        self.quotesChart.chart_data = []
        i = 0
        for time in lib.helpers.trade_minutes():
            value = r.hgetall(ticker + ':' + date + time)
            if len(value) == 0:
                continue
            i += 1
            # dtime = dates.date2num(datetime.datetime(int('20' + date[:2]),
            #                           int(date[2:4]),
            #                           int(date[4:6]),
            #                           int(time[:2]),
            #                           int(time[2:])))
            candle_value = (i,
                            float(value['open']) / 100,
                            float(value['high']) / 100,
                            float(value['low']) / 100,
                            float(value['close']) / 100,
                            int(value['vol']))
            print(candle_value)
            self.quotesChart.chart_data.append(candle_value)
        self.quotesChart.draw_chart()

    def quotes_params_changed(self):
        ticker = str(self.comboTicker.currentText())
        date = self.dateDay.date().toPyDate().strftime('%y%m%d')
        self.render_chart(ticker, date)


if __name__ == "__main__":
    FT_App()
