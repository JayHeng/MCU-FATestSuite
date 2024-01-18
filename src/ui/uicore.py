#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys
import os
import time
import bincopy
import serial.tools.list_ports
from PyQt5 import QtWidgets
from PyQt5.Qt import *
from . import uidef
from . import uivar
from . import uilang
from . import debugger_utils
sys.path.append(os.path.abspath(".."))
from win import faTesterWin

s_serialPort = serial.Serial()
s_recvInterval = 1
s_recvPrintBuffer = ""
s_testCaseResultDict = {}

kFAT_FW_START = 'FAT FW Start'
kFAT_FW_PASS  = 'FAT FW Pass'
kFAT_FW_FAIL  = 'FAT FW Fail'

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
            self.pushButton_detectTestCases.setStyleSheet("background-color: green")

    def _getVal32FromByteArray( self, binarray, offset=0):
        val32Vaule = ((binarray[3+offset]<<24) + (binarray[2+offset]<<16) + (binarray[1+offset]<<8) + binarray[0+offset])
        return val32Vaule

    def _loadTestCases( self ):
        global s_testCaseResultDict
        if os.path.isfile(self.loaderExe):
            global s_recvPrintBuffer
            s_recvPrintBuffer = ""
            s_serialPort.reset_input_buffer()
            self._debugger = debugger_utils.createDebugger(debugger_utils.kDebuggerType_JLink, 'MIMXRT798S_M33_0', 'SWD', 4000, self.loaderExe)
            self._debugger.open()
            lastBeg = 0
            for i in range(len(self.fwAppFiles)):
                srecObj = bincopy.BinFile(str(self.fwAppFiles[i]))
                filepath, file = os.path.split(self.fwAppFiles[i])
                filename, filetype = os.path.splitext(file)
                startAddress = srecObj.minimum_address
                initialAppBytes = srecObj.as_binary(startAddress, startAddress + 8)
                sp = self._getVal32FromByteArray(initialAppBytes[0:4])
                pc = self._getVal32FromByteArray(initialAppBytes[4:8])
                self._debugger.JumpToApp(self.fwAppFiles[i], sp, pc)
                self.showContentOnMainPrintWin('---------New Case----------')
                while True:
                    res0 = s_recvPrintBuffer.find(kFAT_FW_START, lastBeg)
                    if (res0 != -1):
                        lastBeg = res0
                        while True:
                            res1 = s_recvPrintBuffer.find(kFAT_FW_PASS, lastBeg)
                            res2 = s_recvPrintBuffer.find(kFAT_FW_FAIL, lastBeg)
                            if (res1 != -1):
                                lastBeg = res1
                                s_testCaseResultDict[filename] = True
                                self.showContentOnMainResWin('(PASS) -- ' + filename)
                                break
                            if (res2 != -1):
                                lastBeg = res2
                                s_testCaseResultDict[filename] = False
                                self.showContentOnMainResWin('(FAIL) -- ' + filename)
                                break
                        break
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
                global s_recvPrintBuffer
                data = s_serialPort.read(num)
                string = data.decode()
                s_recvPrintBuffer += string
                self.showContentOnMainPrintWin(string)

    def showContentOnMainPrintWin( self, contentStr ):
        self.textEdit_printWin.append(contentStr)

    def showContentOnMainResWin( self, contentStr ):
        self.textEdit_resWin.append(contentStr)

    def resetTestResult( self ):
        global s_testCaseResultDict
        if len(s_testCaseResultDict) != 0:
            for key in s_testCaseResultDict.keys():
                s_testCaseResultDict[key] = None
        self.textEdit_resWin.clear()
        self.textEdit_printWin.clear()

