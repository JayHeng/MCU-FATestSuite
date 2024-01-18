#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import time
import threading
import inspect
import ctypes
from PyQt5.Qt import *
from ui import uidef
from ui import uilang
from ui import uivar
from ui import uicore

g_main_win = None
g_task_loadTestCases = None

def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

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
        self.pushButton_setLoaderExe.clicked.connect(self.callbackSetLoaderExe)
        self.pushButton_detectTestCases.clicked.connect(self.callbackDetectTestCases)
        self.pushButton_runTestCases.clicked.connect(self.callbackRunTestCases)
        self.pushButton_resetTestResult.clicked.connect(self.callbackResetTestResult)
        self.pushButton_open.clicked.connect(self.callbackOpenUart)

    def _setupMcuTargets( self ):
        self.setTargetSetupValue()
        self.initUi()

    def callbackSetMcuDevice( self ):
        self._setupMcuTargets()

    def callbackSetLoaderExe( self ):
        self.selectLoaderExe()

    def callbackDetectTestCases( self ):
        self.findTestCases()

    def callbackRunTestCases( self ):
        self.isLoadTestCasesTaskPending = True

    def callbackResetTestResult( self ):
        self.resetTestResult()

    def callbackOpenUart( self ):
        if not self.isUartOpened:
            self.updatePortSetupValue()
            self.openUartPort()
            self.isUartOpened = True

        else:
            self.isUartOpened = False
            self.closeUartPort()

    def _stopTask( self, thread ):
        _async_raise(thread.ident, SystemExit)

    def _deinitToolToExit( self ):
        uivar.setAdvancedSettings(uidef.kAdvancedSettings_Tool, self.toolCommDict)
        uivar.deinitVar()
        self._stopTask(g_task_loadTestCases)
        try:
            self.Destroy()
        except:
            pass

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
    g_main_win = faTesterMain(None)
    g_main_win.setWindowTitle(u"MCU FA Test Suite v0.1")
    g_main_win.show()

    g_task_loadTestCases = threading.Thread(target=g_main_win.task_loadTestCases)
    g_task_loadTestCases.setDaemon(True)
    g_task_loadTestCases.start()

    sys.exit(app.exec_())

