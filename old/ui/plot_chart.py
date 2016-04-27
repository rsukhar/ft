from __future__ import unicode_literals
import random
from matplotlib.backends import qt_compat

use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator, MinuteLocator, HOURLY
from matplotlib.finance import candlestick_ohlc


class Ui_Plot(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.draw_chart()

    def draw_chart(self):
        pass


class Ui_PlotChart(Ui_Plot):
    chart_data = []

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        Ui_Plot.__init__(self, parent=parent, width=width, height=height, dpi=dpi)
        # hours = HourLocator(HOURLY)
        # minutes = MinuteLocator()
        # hour_formatter = DateFormatter('%h')
        # self.axes.xaxis.set_major_locator(hours)
        # self.axes.xaxis.set_minor_locator(minutes)
        # self.axes.xaxis.set_major_formatter(hour_formatter)

    def draw_chart(self):
        self.axes.clear()
        candlestick_ohlc(self.axes, self.chart_data, width=0.6, colorup='g', colordown='r')
        # self.axes.plot(range(len(self.chart_data)), self.chart_data, 'r')
        self.draw()
