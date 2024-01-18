#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys
import os
import time
import serial.tools.list_ports
from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from . import uidef
from . import uivar
from . import uilang
from . import debugger_utils
sys.path.append(os.path.abspath(".."))
from win import faTesterWin

s_serialPort = serial.Serial()
s_recvInterval = 1

s_testCaseResultDict = {}

class uartRecvWorker(QThread):
    sinOut = pyqtSignal()

    def __init__(self, parent=None):
        super(uartRecvWorker, self).__init__(parent)
        self.working = True

    def __del__(self):
        self.working = False

    def run(self):
        while self.working == True:
            self.sinOut.emit()
            self.sleep(s_recvInterval)

class resultFigure(FigureCanvas):

    def __init__(self,width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(resultFigure,self).__init__(self.fig)
        global s_testCaseResultDict
        if (False):
            s_testCaseResultDict = {"app_fc0_uart":None,
                                    "app_xspi0":None,
                                    "app_xspi1":True,
                                    "app_xspi2":False,
                                    "app_usdhc0":None,
                                    "app_usdhc1":True,
                                    "app_mipi_dsi":False,
                                    "app_sai0":None,
                                    "app_sai2":True,
                                    "app_sai3":False,
                                    }

        ncol = 3
        nrow = int(len(s_testCaseResultDict) / ncol) + 1

        axs = (self.fig).add_gridspec(1 + nrow, ncol, wspace=.5).subplots()
        for ax in axs.flat:
            ax.set_axis_off()

        if len(s_testCaseResultDict) == 0:
            return

        for ax, (caseName, caseResult) in zip(axs[1:, :].T.flat, s_testCaseResultDict.items()):
            if caseResult == None:
                fcolor = "w"
            elif caseResult == True:
                fcolor = "c"
            elif caseResult == False:
                fcolor = "r"
            ax.text(.2, .5, caseName, bbox=dict(boxstyle='round', fc=fcolor, ec="k"),
                    transform=ax.transAxes, size="large", color="tab:blue",
                    horizontalalignment="left", verticalalignment="center")

class faTesterUi(QMainWindow, faTesterWin.Ui_faTesterWin):

    def __init__(self, parent=None):
        super(faTesterUi, self).__init__(parent)
        self.setupUi(self)
        self.uartRecvThread = uartRecvWorker()
        self.uartRecvThread.sinOut.connect(self.receiveUartData)

        self.exeBinRoot = os.getcwd()
        self.exeTopRoot = os.path.dirname(self.exeBinRoot)
        exeMainFile = os.path.join(self.exeTopRoot, 'src', 'main.py')
        if not os.path.isfile(exeMainFile):
            self.exeTopRoot = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        uivar.setRuntimeSettings(None, self.exeTopRoot)
        uivar.initVar(os.path.join(self.exeTopRoot, 'bin', 'fat_settings.json'))
        toolCommDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_Tool)
        self.toolCommDict = toolCommDict.copy()

        self.mcuDevice = None
        self.testCaseLoader = None
        self.loaderExe = None
        self._initTargetSetupValue()
        self.setTargetSetupValue()
        self.initUi()

        self.resultGridlayout = QGridLayout(self.groupBox_testResult)
        self.fwAppFiles = []
        self.isLoadTestCasesTaskPending = False

    def initUi( self ):
        self.uartComPort = None
        self.uartBaudrate = None
        self.setPortSetupValue()

    def selectLoaderExe( self ):
        fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(self, "Select EXE", os.getcwd(), "All Files(*);;EXE Files(*.exe)")
        self.loaderExe = fileName
        try:
            if os.path.isfile(self.loaderExe):
                self.toolCommDict['loaderExe'] = self.loaderExe
                self.pushButton_setLoaderExe.setStyleSheet("background-color: green")
            else:
                self.pushButton_setLoaderExe.setStyleSheet("background-color: grey")
        except:
            pass

    def findTestCases( self ):
        #appFolderPath = self.m_dirPicker_appFolderPath.GetPath()
        #self.sbAppFolderPath = appFolderPath.encode('utf-8').encode("gbk")
        global s_testCaseResultDict
        s_testCaseResultDict.clear()
        fwAppFiles = []
        cpu = None
        if self.mcuDevice == uidef.kMcuDevice_iMXRT700:
            cpu = "MIMXRT798"
        else:
            pass
        fwFolderPath = os.path.join(self.exeTopRoot, 'src', 'targets', cpu)
        files = os.listdir(fwFolderPath)
        for file in files:
            filename, filetype = os.path.splitext(file)
            if filetype == '.srec':
                fwAppFiles.append(os.path.join(fwFolderPath, file))
                s_testCaseResultDict[filename] = None
        self.fwAppFiles = fwAppFiles[:]
        if len(fwAppFiles) == 0:
            self.showInfoMessage('Error', 'Cannot find any test case files (.srec)')
        else:
            self.updateMainResultWin()
            self.pushButton_detectTestCases.setStyleSheet("background-color: green")

    def _loadTestCases( self ):
        global s_testCaseResultDict
        if os.path.isfile(self.loaderExe):
            self._debugger = debugger_utils.createDebugger(debugger_utils.kDebuggerType_JLink, 'MIMXRT798S_M33_0', 'SWD', 4000, self.loaderExe)
            self._debugger.open()
            self._debugger.JumpToApp(self.fwAppFiles[0], 0x20200000, 0x00083035)
        else:
            self.showInfoMessage('Error', 'You need to set Loader EXE first.')

    def task_loadTestCases( self ):
        while True:  
            if self.isLoadTestCasesTaskPending:
                self._loadTestCases()
                self.isLoadTestCasesTaskPending = False
            time.sleep(1)

    def showAboutMessage( self, myTitle, myContent):
        QMessageBox.about(self, myTitle, myContent )

    def showInfoMessage( self, myTitle, myContent):
        QMessageBox.information(self, myTitle, myContent )

    def adjustPortSetupValue( self ):
        # Auto detect available ports
        comports = list(serial.tools.list_ports.comports())
        ports = [None] * len(comports)
        for i in range(len(comports)):
            comport = list(comports[i])
            ports[i] = comport[0]
        lastPort = self.comboBox_comPort.currentText()
        lastBaud = self.comboBox_baudrate.currentText()
        self.comboBox_comPort.clear()
        self.comboBox_comPort.addItems(ports)
        if lastPort in ports:
            self.comboBox_comPort.setCurrentIndex(self.comboBox_comPort.findText(lastPort))
        else:
            self.comboBox_comPort.setCurrentIndex(0)
        baudItems = ['115200']
        self.comboBox_baudrate.clear()
        self.comboBox_baudrate.addItems(baudItems)
        if lastBaud in baudItems:
            self.comboBox_baudrate.setCurrentIndex(self.comboBox_baudrate.findText(lastBaud))
        else:
            self.comboBox_baudrate.setCurrentIndex(0)

    def _initTargetSetupValue( self ):
        self.comboBox_mcuDevice.clear()
        self.comboBox_mcuDevice.addItems(uidef.kMcuDevice_v1_0)
        self.comboBox_mcuDevice.setCurrentIndex(self.toolCommDict['mcuDevice'])
        self.comboBox_testCaseLoader.setCurrentIndex(self.toolCommDict['testCaseLoader'])
        if self.toolCommDict['loaderExe'] != None and os.path.isfile(self.toolCommDict['loaderExe']):
            self.loaderExe = self.toolCommDict['loaderExe']
            self.pushButton_setLoaderExe.setStyleSheet("background-color: green")

    def setTargetSetupValue( self ):
        self.mcuDevice = self.comboBox_mcuDevice.currentText()
        self.toolCommDict['mcuDevice'] = self.comboBox_mcuDevice.currentIndex()
        self.testCaseLoader = self.comboBox_testCaseLoader.currentText()
        self.toolCommDict['testCaseLoader'] = self.comboBox_testCaseLoader.currentIndex()

    def updatePortSetupValue( self ):
        self.uartComPort = self.comboBox_comPort.currentText()
        self.uartBaudrate = self.comboBox_baudrate.currentText()

    def setPortSetupValue( self ):
        self.adjustPortSetupValue()
        self.updatePortSetupValue()

    def openUartPort ( self ):
        s_serialPort.port = self.uartComPort
        s_serialPort.baudrate = int(self.uartBaudrate)
        s_serialPort.bytesizes = serial.EIGHTBITS
        s_serialPort.stopbits = serial.STOPBITS_ONE
        s_serialPort.parity = serial.PARITY_NONE
        try:
            s_serialPort.open()
        except:
            QMessageBox.information(self, 'Port Error', 'Com Port cannot opened!')
            return
        s_serialPort.set_buffer_size(rx_size=1024 * 16)
        s_serialPort.reset_input_buffer()
        s_serialPort.reset_output_buffer()
        self.uartRecvThread.start()
        self.pushButton_open.setText('Close')
        self.pushButton_open.setStyleSheet("background-color: green")

    def closeUartPort ( self ):
        if s_serialPort.isOpen():
            s_serialPort.close()
            self.uartRecvThread.quit()
            self.pushButton_open.setText('Open')
            self.pushButton_open.setStyleSheet("background-color: grey")

    def receiveUartData( self ):
        if s_serialPort.isOpen():
            num = s_serialPort.inWaiting()
            if num != 0:
                data = s_serialPort.read(num)
                string = data.decode()
                self.showContentOnMainPrintWin(string)

    def showContentOnMainPrintWin( self, contentStr ):
        self.textEdit_printWin.append(contentStr)

    def updateMainResultWin( self ):
        self.resultFig = resultFigure(width=6, height=4, dpi=80)
        try:
            self.resultGridlayout.removeWidget(self.resultFig,0,0)
        except:
            pass
        self.resultGridlayout.addWidget(self.resultFig,0,0)

    def resetTestResult( self ):
        global s_testCaseResultDict
        if len(s_testCaseResultDict) != 0:
            for key in s_testCaseResultDict.keys():
                s_testCaseResultDict[key] = None
            self.updateMainResultWin()
        self.textEdit_printWin.clear()

