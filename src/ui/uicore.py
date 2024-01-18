#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys
import os
import serial.tools.list_ports
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
sys.path.append(os.path.abspath(".."))
from win import faTesterWin

s_serialPort = serial.Serial()
s_recvInterval = 1

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

        results = {"app_fc0_uart":None,
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
        nrow = 5

        axs = (self.fig).add_gridspec(1 + nrow, ncol, wspace=.5).subplots()
        for ax in axs.flat:
            ax.set_axis_off()

        for ax, (caseName, caseResult) in zip(axs[1:, :].T.flat, results.items()):
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
        self._initTargetSetupValue()
        self.setTargetSetupValue()
        self.initUi()

        self.updateMainResultWin()

    def initUi( self ):
        self.uartComPort = None
        self.uartBaudrate = None
        self.setPortSetupValue()

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

    def setTargetSetupValue( self ):
        self.mcuDevice = self.comboBox_mcuDevice.currentText()
        self.toolCommDict['mcuDevice'] = self.comboBox_mcuDevice.currentIndex()

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
        self.resultGridlayout = QGridLayout(self.groupBox_testResult)
        self.resultGridlayout.addWidget(self.resultFig,0,0)

    def callbackResetTestResult( self ):
        self.textEdit_printWin.clear()
