#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
import threading
import inspect
import ctypes
from ui import uidef
from ui import uilang
from ui import uivar
from ui import uicore

g_main_win = None
g_task_loadTestCases = None
g_task_receiveUartData = None

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
        uicore.faTesterUi.__init__(self, parent)
        self.isUartOpened = False

    def _setupMcuTargets( self ):
        self.setTargetSetupValue()
        self.initUi()

    def callbackSetMcuDevice( self, event ):
        self._setupMcuTargets()

    def callbackSetLoaderExe( self, event ):
        self.selectLoaderExe()

    def callbackDetectTestCases( self, event ):
        self.findTestCases()

    def callbackRunTestCases( self, event ):
        self.isLoadTestCasesTaskPending = True

    def callbackResetTestResult( self, event ):
        self.resetTestResult()

    def callbackOpenUart( self, event ):
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
        self._stopTask(g_task_receiveUartData)
        try:
            self.Destroy()
        except:
            pass

    def callbackExit( self, event ):
        self._deinitToolToExit()

    def callbackClose( self, event ):
        self._deinitToolToExit()

    def callbackShowHomePage( self, event ):
        msgText = ((uilang.kMsgLanguageContentDict['homePage_info'][0]))
        wx.MessageBox(msgText, uilang.kMsgLanguageContentDict['homePage_title'][0], wx.OK | wx.ICON_INFORMATION)

    def callbackShowAboutAuthor( self, event ):
        msgText = ((uilang.kMsgLanguageContentDict['aboutAuthor_author'][0]) +
                   (uilang.kMsgLanguageContentDict['aboutAuthor_email1'][0]) +
                   (uilang.kMsgLanguageContentDict['aboutAuthor_email2'][0]) +
                   (uilang.kMsgLanguageContentDict['aboutAuthor_blog'][0]))
        wx.MessageBox(msgText, uilang.kMsgLanguageContentDict['aboutAuthor_title'][0], wx.OK | wx.ICON_INFORMATION)

    def callbackShowRevisionHistory( self, event ):
        msgText = ((uilang.kMsgLanguageContentDict['revisionHistory_v0_1_0'][0]))
        wx.MessageBox(msgText, uilang.kMsgLanguageContentDict['revisionHistory_title'][self.languageIndex], wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()

    g_main_win = faTesterMain(None)
    g_main_win.SetTitle(u"MCU FA Test Suite v0.1")
    g_main_win.Show()

    g_task_loadTestCases = threading.Thread(target=g_main_win.task_loadTestCases)
    g_task_loadTestCases.setDaemon(True)
    g_task_loadTestCases.start()

    g_task_receiveUartData = threading.Thread(target=g_main_win.task_receiveUartData)
    g_task_receiveUartData.setDaemon(True)
    g_task_receiveUartData.start()

    app.MainLoop()

