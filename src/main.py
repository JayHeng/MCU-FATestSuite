#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import time
from PyQt5.Qt import *
from ui import uidef
from ui import uilang
from ui import uivar
from ui import uicore

class faTesterMain(uicore.faTesterUi):

    def __init__(self, parent=None):
        super(faTesterMain, self).__init__(parent)
        self._register_callbacks()
        self.isUartOpened = False
        self._setupMcuTargets()

    def _register_callbacks(self):
        self.menuHelpAction_homePage.triggered.connect(self.callbackShowHomePage)
        self.menuHelpAction_aboutAuthor.triggered.connect(self.callbackShowAboutAuthor)
        self.menuHelpAction_revisionHistory.triggered.connect(self.callbackShowRevisionHistory)
        self.comboBox_mcuDevice.currentIndexChanged.connect(self.callbackSetMcuDevice)
        self.pushButton_open.clicked.connect(self.callbackOpenUart)
        self.pushButton_resetTestResult.clicked.connect(self.callbackResetTestResult)

    def _setupMcuTargets( self ):
        self.setTargetSetupValue()
        self.initUi()

    def callbackSetMcuDevice( self ):
        self._setupMcuTargets()

    def callbackOpenUart( self ):
        if not self.isUartOpened:
            self.updatePortSetupValue()
            self.openUartPort()
            self.isUartOpened = True

        else:
            self.isUartOpened = False
            self.closeUartPort()

    def _deinitToolToExit( self ):
        uivar.setAdvancedSettings(uidef.kAdvancedSettings_Tool, self.toolCommDict)
        uivar.deinitVar()

    def closeEvent(self, event):
        self._deinitToolToExit()
        event.accept()

    def callbackShowHomePage(self):
        self.showAboutMessage(uilang.kMsgLanguageContentDict['homePage_title'][0], uilang.kMsgLanguageContentDict['homePage_info'][0] )

    def callbackShowAboutAuthor(self):
        msgText = ((uilang.kMsgLanguageContentDict['aboutAuthor_author'][0]) +
                   (uilang.kMsgLanguageContentDict['aboutAuthor_email1'][0]) +
                   (uilang.kMsgLanguageContentDict['aboutAuthor_email2'][0]) +
                   (uilang.kMsgLanguageContentDict['aboutAuthor_blog'][0]))
        self.showAboutMessage(uilang.kMsgLanguageContentDict['aboutAuthor_title'][0], msgText )

    def callbackShowRevisionHistory(self):
        self.showAboutMessage(uilang.kMsgLanguageContentDict['revisionHistory_title'][0], uilang.kMsgLanguageContentDict['revisionHistory_v0_1_0'][0] )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = faTesterMain(None)
    mainWin.setWindowTitle(u"MCU FA Test Suite v0.1")
    mainWin.show()

    sys.exit(app.exec_())

