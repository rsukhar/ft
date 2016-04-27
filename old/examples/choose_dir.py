import os
import sys

from PyQt4 import QtGui

import choose_dir_interface


class ExampleApp(QtGui.QMainWindow, choose_dir_interface.Ui_MainWindow):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.btnBrowse.clicked.connect(self.browse_folder)

    def browse_folder(self):
        self.listWidget.clear()
        directory = QtGui.QFileDialog.getExistingDirectory(self, "Pick a folder")
        if directory:
            for file_name in os.listdir(directory):
                self.listWidget.addItem(file_name)


def main():
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
