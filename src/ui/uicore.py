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

RES_TEXT_TYPE_IS_LINE   = True
LOG_TEXT_TYPE_IS_MANUAL = True

s_serialPort = serial.Serial()
s_recvInterval = 1
s_recvPrintBuf = ""
s_isPrintUpdated = False
s_caseResInfo = ""
s_isResInfoUpdated = False

kFAT_LOG_START = 'FAT FW Start'
kFAT_LOG_PASS  = 'FAT FW Pass'
kFAT_LOG_FAIL  = 'FAT FW Fail'

kFAT_REG_ADDR  = 0x50062FE0
kFAT_REG_START = 0x5A
kFAT_REG_PASS  = 0xA7
kFAT_REG_FAIL  = 0x9F

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

class uartLogWorker(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.infoLen = 0

    def run(self):
        while True:
            try:
                global s_isPrintUpdated
                if s_isPrintUpdated:
                    self.sinOut.emit(s_recvPrintBuf)
                    s_isPrintUpdated = False
            except IOError as e:
                pass
            QThread.msleep(100)

class resLogWorker(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            try:
                global s_isResInfoUpdated
                if s_isResInfoUpdated:
                    self.sinOut.emit(s_caseResInfo)
                    s_isResInfoUpdated = False
            except IOError as e:
                pass
            QThread.msleep(100)

class faTesterUi(QMainWindow, faTesterWin.Ui_faTesterWin):

    def __init__(self, parent=None):
        super(faTesterUi, self).__init__(parent)
        self.setupUi(self)
        self.uartRecvThread = uartRecvWorker()
        self.uartRecvThread.sinOut.connect(self.thread_receiveUartData)

        if not LOG_TEXT_TYPE_IS_MANUAL:
            self.uartLogThread = uartLogWorker()
            self.uartLogThread.sinOut.connect(self.textEdit_printWin.setText)
            self.uartLogThread.start()
        if not RES_TEXT_TYPE_IS_LINE:
            self.resLogThread = resLogWorker()
            self.resLogThread.sinOut.connect(self.textEdit_resWin.setText)
            self.resLogThread.start()

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
        self.testLoader = None
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
        self.comboBox_testLoader.setCurrentIndex(self.toolCommDict['testLoader'])
        if self.toolCommDict['loaderExe'] != None and os.path.isfile(self.toolCommDict['loaderExe']):
            self.loaderExe = self.toolCommDict['loaderExe']
            self.pushButton_setLoaderExe.setStyleSheet("background-color: green")

    def setTargetSetupValue( self ):
        self.mcuDevice = self.comboBox_mcuDevice.currentText()
        self.toolCommDict['mcuDevice'] = self.comboBox_mcuDevice.currentIndex()
        self.testLoader = self.comboBox_testLoader.currentText()
        self.toolCommDict['testLoader'] = self.comboBox_testLoader.currentIndex()

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
            self.pushButton_open.setStyleSheet("background-color: white")

    def thread_receiveUartData( self ):
        if s_serialPort.isOpen():
            num = s_serialPort.inWaiting()
            if num != 0:
                global s_recvPrintBuf
                data = s_serialPort.read(num)
                string = data.decode()
                s_recvPrintBuf += string
                self.showContentOnMainPrintWin(string)

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
        self.resetTestResult()
        caseTestResultMsg = ""
        fwAppFiles = []
        cpu = None
        if self.mcuDevice == uidef.kMcuDevice_iMXRT700:
            cpu = "MIMXRT798"
        else:
            pass
        fwFolderPath = os.path.join(self.exeTopRoot, 'src', 'targets', cpu)
        files = os.listdir(fwFolderPath)
        fileIdx = 0
        for file in files:
            filename, filetype = os.path.splitext(file)
            if filetype == '.srec':
                fwAppFiles.append(os.path.join(fwFolderPath, file))
                caseTestResultMsg += "( TBD ) -- " + filename + "\n"
                self.showContentOnMainResWin("( TBD ) -- " + filename, fileIdx)
                fileIdx += 1
        self.fwAppFiles = fwAppFiles[:]
        if len(fwAppFiles) == 0:
            self.showInfoMessage('Error', 'Cannot find any test case files (.srec)')
        else:
            global s_caseResInfo
            s_caseResInfo = caseTestResultMsg
            self.showContentOnMainResWin(caseTestResultMsg)
            self.pushButton_detectTestCases.setStyleSheet("background-color: green")

    def _getVal32FromByteArray( self, binarray, offset=0):
        val32Vaule = ((binarray[3+offset]<<24) + (binarray[2+offset]<<16) + (binarray[1+offset]<<8) + binarray[0+offset])
        return val32Vaule

    def _loadTestCases( self ):
        if os.path.isfile(self.loaderExe):
            #self.resetTestResult()
            self.pushButton_runTestCases.setStyleSheet("background-color: yellow")
            global s_recvPrintBuf
            global s_caseResInfo
            s_recvPrintBuf = ""
            s_caseResInfo = ""
            s_serialPort.reset_input_buffer()
            jlinkcmdFolderPath = os.path.join(self.exeTopRoot, 'src', 'ui', 'debuggers', 'jlink')
            self._debugger = debugger_utils.createDebugger(debugger_utils.kDebuggerType_JLink, 'MIMXRT798S_M33_0', 'SWD', 4000, self.loaderExe, jlinkcmdFolderPath)
            self._debugger.open()
            lastBeg = 0
            appLen = len(self.fwAppFiles)
            for appIdx in range(appLen):
                self.pushButton_runTestCases.setText('Running Test Case ' + str(appIdx+1) + '/' + str(appLen))
                s_recvPrintBuf += '\n---------Case ' + str(appIdx+1) + '/' + str(appLen) + '----------\n'
                self.showContentOnMainPrintWin('---------Case ' + str(appIdx+1) + '/' + str(appLen) + '----------')
                srecObj = bincopy.BinFile(str(self.fwAppFiles[appIdx]))
                filepath, file = os.path.split(self.fwAppFiles[appIdx])
                filename, filetype = os.path.splitext(file)
                startAddress = srecObj.minimum_address
                initialAppBytes = srecObj.as_binary(startAddress, startAddress + 8)
                sp = self._getVal32FromByteArray(initialAppBytes[0:4])
                pc = self._getVal32FromByteArray(initialAppBytes[4:8])
                appIsLoaded = False
                while (not appIsLoaded):
                    self._debugger.JumpToApp(self.fwAppFiles[appIdx], sp, pc, None)
                    deltaTimeStart = time.perf_counter()
                    while True:
                        res0 = s_recvPrintBuf.find(kFAT_LOG_START, lastBeg)
                        ##############################################################
                        if (res0 != -1):
                            appIsLoaded = True
                            lastBeg = res0
                            while True:
                                res1 = s_recvPrintBuf.find(kFAT_LOG_PASS, lastBeg)
                                res2 = s_recvPrintBuf.find(kFAT_LOG_FAIL, lastBeg)
                                if (res1 != -1):
                                    lastBeg = res1
                                    s_caseResInfo += '( PASS ) -- ' + filename + '\n'
                                    self.showContentOnMainResWin('( PASS ) -- ' + filename, appIdx)
                                    break
                                if (res2 != -1):
                                    lastBeg = res2
                                    s_caseResInfo += '( FAIL ) -- ' + filename + '\n'
                                    self.showContentOnMainResWin('( FAIL ) -- ' + filename, appIdx)
                                    break
                                time.sleep(0.5)
                            break
                        ##############################################################
                        #status, res0 = self._debugger.readMem32(kFAT_REG_ADDR)
                        if False: #status and ((res0 & 0xFF) == kFAT_REG_START):
                            appIsLoaded = True
                            while True:
                                status, resx = self._debugger.readMem32(kFAT_REG_ADDR)
                                if status:
                                    resx = resx >> 24
                                    if resx == kFAT_REG_PASS:
                                        s_caseResInfo += '( PASS ) -- ' + filename + '\n'
                                        self.showContentOnMainResWin('( PASS ) -- ' + filename, appIdx)
                                        break
                                    elif resx == kFAT_REG_FAIL:
                                        s_caseResInfo += '( FAIL ) -- ' + filename + '\n'
                                        self.showContentOnMainResWin('( FAIL ) -- ' + filename, appIdx)
                                        break
                                time.sleep(0.5)
                            break
                        ##############################################################
                        deltaTime = time.perf_counter() - deltaTimeStart
                        if (deltaTime > 5.0):
                            time.sleep(1)
                            break
                        time.sleep(0.5)
                        ##############################################################
            self.pushButton_runTestCases.setText('Run Test Cases')
            self.pushButton_runTestCases.setStyleSheet("background-color: white")
        else:
            self.showInfoMessage('Error', 'You need to set Loader EXE first.')

    def task_loadTestCases( self ):
        while True:
            if self.isLoadTestCasesTaskPending:
                self._loadTestCases()
                self.isLoadTestCasesTaskPending = False
            time.sleep(1)

    def showContentOnMainPrintWin( self, text ):
        if not LOG_TEXT_TYPE_IS_MANUAL:
            global s_isPrintUpdated
            s_isPrintUpdated = True
            while (s_isPrintUpdated):
                pass
            #self.textEdit_printWin.append(contentStr)
        else:
            pass

    def showContentOnMainResWin( self, text, lineIdx=None ):
        if not RES_TEXT_TYPE_IS_LINE:
            global s_isResInfoUpdated
            s_isResInfoUpdated = True
            while (s_isResInfoUpdated):
                pass
            #self.textEdit_resWin.append(contentStr)
        else:
            if lineIdx == None:
                pass
            elif lineIdx == 0:
                self.lineEdit_resWin_0.setText(text)
            elif lineIdx == 1:
                self.lineEdit_resWin_1.setText(text)
            elif lineIdx == 2:
                self.lineEdit_resWin_2.setText(text)
            elif lineIdx == 3:
                self.lineEdit_resWin_3.setText(text)
            elif lineIdx == 4:
                self.lineEdit_resWin_4.setText(text)
            elif lineIdx == 5:
                self.lineEdit_resWin_5.setText(text)
            elif lineIdx == 6:
                self.lineEdit_resWin_6.setText(text)
            elif lineIdx == 7:
                self.lineEdit_resWin_7.setText(text)
            elif lineIdx == 8:
                self.lineEdit_resWin_8.setText(text)
            elif lineIdx == 9:
                self.lineEdit_resWin_9.setText(text)
            elif lineIdx == 10:
                self.lineEdit_resWin_10.setText(text)
            elif lineIdx == 11:
                self.lineEdit_resWin_11.setText(text)
            elif lineIdx == 12:
                self.lineEdit_resWin_12.setText(text)
            elif lineIdx == 13:
                self.lineEdit_resWin_13.setText(text)
            pass

    def resetTestResult( self ):
        if RES_TEXT_TYPE_IS_LINE:
            self.lineEdit_resWin_0.clear()
            self.lineEdit_resWin_1.clear()
            self.lineEdit_resWin_2.clear()
            self.lineEdit_resWin_3.clear()
            self.lineEdit_resWin_4.clear()
            self.lineEdit_resWin_5.clear()
            self.lineEdit_resWin_6.clear()
            self.lineEdit_resWin_7.clear()
            self.lineEdit_resWin_8.clear()
            self.lineEdit_resWin_9.clear()
            self.lineEdit_resWin_10.clear()
            self.lineEdit_resWin_11.clear()
            self.lineEdit_resWin_12.clear()
            self.lineEdit_resWin_13.clear()
        else:
            self.textEdit_resWin.clear()
        self.textEdit_printWin.clear()

    def showAboutMessage( self, myTitle, myContent):
        QMessageBox.about(self, myTitle, myContent )

    def showInfoMessage( self, myTitle, myContent):
        QMessageBox.information(self, myTitle, myContent )

