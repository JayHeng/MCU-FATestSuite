#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import time
from PyQt5.Qt import *
from win import faTesterWin

class faTesterMain(QMainWindow, faTesterWin.Ui_faTesterWin):

    def __init__(self, parent=None):
        super(faTesterMain, self).__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = faTesterMain(None)
    mainWin.setWindowTitle(u"MCU FA Test Suite v0.1")
    mainWin.show()

    sys.exit(app.exec_())

