# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app.ui'
#
# Created: Wed Apr 20 13:53:24 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_windowApp(object):
    def setupUi(self, windowApp):
        windowApp.setObjectName(_fromUtf8("windowApp"))
        windowApp.resize(600, 400)
        self.verticalLayout = QtGui.QVBoxLayout(windowApp)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(windowApp)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.comboTicker = QtGui.QComboBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboTicker.sizePolicy().hasHeightForWidth())
        self.comboTicker.setSizePolicy(sizePolicy)
        self.comboTicker.setObjectName(_fromUtf8("comboTicker"))
        self.horizontalLayout_2.addWidget(self.comboTicker)
        self.label_2 = QtGui.QLabel(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.dateDay = QtGui.QDateEdit(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateDay.sizePolicy().hasHeightForWidth())
        self.dateDay.setSizePolicy(sizePolicy)
        self.dateDay.setCalendarPopup(True)
        self.dateDay.setObjectName(_fromUtf8("dateDay"))
        self.horizontalLayout_2.addWidget(self.dateDay)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.quotesChart = Ui_PlotChart(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quotesChart.sizePolicy().hasHeightForWidth())
        self.quotesChart.setSizePolicy(sizePolicy)
        self.quotesChart.setObjectName(_fromUtf8("quotesChart"))
        self.verticalLayout_2.addWidget(self.quotesChart)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(windowApp)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(windowApp)

    def retranslateUi(self, windowApp):
        windowApp.setWindowTitle(_translate("windowApp", "Form", None))
        self.label.setText(_translate("windowApp", "Ticker:", None))
        self.label_2.setText(_translate("windowApp", "Date:", None))
        self.dateDay.setDisplayFormat(_translate("windowApp", "dd.MM.yyyy", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("windowApp", "Quotes", None))

from ui.plot_chart import Ui_PlotChart
