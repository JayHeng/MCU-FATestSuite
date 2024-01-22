#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
import bincopy
import serial.tools.list_ports
import uidef
import uivar
import uilang
import debugger_utils
sys.path.append(os.path.abspath(".."))
from win import faTesterWin

s_serialPort = serial.Serial()
s_recvInterval = 0.5
s_recvPrintBuf = ""

kFAT_LOG_START = 'FAT FW Start'
kFAT_LOG_PASS  = 'FAT FW Pass'
kFAT_LOG_FAIL  = 'FAT FW Fail'

kFAT_REG_ADDR  = 0x50062FE0
kFAT_REG_START = 0x5A
kFAT_REG_PASS  = 0xA7
kFAT_REG_FAIL  = 0x9F

kTIMEOUT_LOAD_APP = 5.0
kTIMEOUT_WAIT_APP = 30.0

class faTesterUi(faTesterWin.faTesterWin):

    def __init__(self, parent):
        faTesterWin.faTesterWin.__init__(self, parent)
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
        self.enableUartToRecvData = False

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
        lastPort = self.m_choice_comPort.GetString(self.m_choice_comPort.GetSelection())
        lastBaud = self.m_choice_baudrate.GetString(self.m_choice_baudrate.GetSelection())
        self.m_choice_comPort.Clear()
        self.m_choice_comPort.SetItems(ports)
        if lastPort in ports:
            self.m_choice_comPort.SetSelection(self.m_choice_comPort.FindString(lastPort))
        else:
            self.m_choice_comPort.SetSelection(0)
        baudItems = ['115200']
        self.m_choice_baudrate.Clear()
        self.m_choice_baudrate.SetItems(baudItems)
        if lastBaud in baudItems:
            self.m_choice_baudrate.SetSelection(self.m_choice_baudrate.FindString(lastBaud))
        else:
            self.m_choice_baudrate.SetSelection(0)

    def _initTargetSetupValue( self ):
        self.m_choice_mcuDevice.Clear()
        self.m_choice_mcuDevice.SetItems(uidef.kMcuDevice_v1_0)
        self.m_choice_mcuDevice.SetSelection(self.toolCommDict['mcuDevice'])
        self.m_choice_testLoader.SetSelection(self.toolCommDict['testLoader'])
        if self.toolCommDict['loaderExe'] != None and os.path.isfile(self.toolCommDict['loaderExe']):
            self.loaderExe = self.toolCommDict['loaderExe']
            self.m_filePicker_setLoaderExe.SetPath(self.loaderExe)

    def setTargetSetupValue( self ):
        self.mcuDevice = self.m_choice_mcuDevice.GetString(self.m_choice_mcuDevice.GetSelection())
        self.toolCommDict['mcuDevice'] = self.m_choice_mcuDevice.GetSelection()
        self.testLoader = self.m_choice_testLoader.GetString(self.m_choice_testLoader.GetSelection())
        self.toolCommDict['testLoader'] = self.m_choice_testLoader.GetSelection()

    def updatePortSetupValue( self ):
        self.uartComPort = self.m_choice_comPort.GetString(self.m_choice_comPort.GetSelection())
        self.uartBaudrate = self.m_choice_baudrate.GetString(self.m_choice_baudrate.GetSelection())

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
            self.showInfoMessage('Port Error', 'Com Port cannot be opened!')
            return
        s_serialPort.set_buffer_size(rx_size=1024 * 16)
        s_serialPort.reset_input_buffer()
        s_serialPort.reset_output_buffer()
        self.enableUartToRecvData = True
        self.m_button_open.SetLabel('Close')
        self.m_button_open.SetBackgroundColour(uidef.kButtonColor_Green)

    def closeUartPort ( self ):
        if s_serialPort.isOpen():
            s_serialPort.close()
            self.enableUartToRecvData = False
            self.m_button_open.SetLabel('Open')
            self.m_button_open.SetBackgroundColour(uidef.kButtonColor_White)

    def task_receiveUartData( self ):
        while True:
            if self.enableUartToRecvData:
                if s_serialPort.isOpen():
                    num = s_serialPort.inWaiting()
                    if num != 0:
                        global s_recvPrintBuf
                        data = s_serialPort.read(num)
                        string = data.decode()
                        s_recvPrintBuf += string
                        self.showContentOnMainPrintWin(string)
            time.sleep(s_recvInterval)

    def selectLoaderExe( self ):
        loaderPath = self.m_filePicker_setLoaderExe.GetPath()
        self.loaderExe = loaderPath.encode('utf-8').encode("gbk")
        try:
            if os.path.isfile(self.loaderExe):
                self.toolCommDict['loaderExe'] = loaderPath.encode("utf-8")
            else:
                pass
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
        for file in files:
            filename, filetype = os.path.splitext(file)
            if filetype == '.srec':
                fwAppFiles.append(os.path.join(fwFolderPath, file))
                caseTestResultMsg += "( TBD ) -- " + filename + "\n"
        self.fwAppFiles = fwAppFiles[:]
        if len(fwAppFiles) == 0:
            self.showInfoMessage('App Error', 'Cannot find any test case files (.srec)')
        else:
            self.showContentOnMainResWin(caseTestResultMsg)
            self.m_button_detectTestCases.SetBackgroundColour(uidef.kButtonColor_Green)

    def _getVal32FromByteArray( self, binarray, offset=0):
        val32Vaule = ((binarray[3+offset]<<24) + (binarray[2+offset]<<16) + (binarray[1+offset]<<8) + binarray[0+offset])
        return val32Vaule

    def _loadTestCases( self ):
        if os.path.isfile(self.loaderExe):
            self.resetTestResult()
            appLen = len(self.fwAppFiles)
            if appLen == 0:
                self.showInfoMessage('Flow Error', 'You need to detect test cases first.')
                return 
            self.m_button_runTestCases.SetBackgroundColour(uidef.kButtonColor_Yellow)
            global s_recvPrintBuf
            s_recvPrintBuf = ""
            if s_serialPort.isOpen():
                s_serialPort.reset_input_buffer()
            else:
                self.showInfoMessage('Flow Error', 'Com Port is not opened.')
                return 
            jlinkcmdFolderPath = os.path.join(self.exeTopRoot, 'src', 'ui', 'debuggers', 'jlink')
            self._debugger = debugger_utils.createDebugger(debugger_utils.kDebuggerType_JLink, 'MIMXRT798S_M33_0', 'SWD', 4000, self.loaderExe, jlinkcmdFolderPath)
            self._debugger.open()
            lastBeg = 0
            for appIdx in range(appLen):
                self.m_button_runTestCases.SetLabel('Running Test Case ' + str(appIdx+1) + '/' + str(appLen))
                self.showContentOnMainPrintWin('---------Case ' + str(appIdx+1) + '/' + str(appLen) + '----------\n')
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
                    deltaTimeStart = time.clock()
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
                                    self.showContentOnMainResWin('( PASS ) -- ' + filename + '\n')
                                    break
                                if (res2 != -1):
                                    lastBeg = res2
                                    self.showContentOnMainResWin('( FAIL ) -- ' + filename + '\n')
                                    break
                                deltaTime_check = time.clock() - deltaTimeStart
                                if (deltaTime_check > kTIMEOUT_WAIT_APP):
                                    self.showContentOnMainResWin('( TIMEOUT ) -- ' + filename + '\n')
                                    time.sleep(1)
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
                                        self.showContentOnMainResWin('( PASS ) -- ' + filename + '\n')
                                        break
                                    elif resx == kFAT_REG_FAIL:
                                        self.showContentOnMainResWin('( FAIL ) -- ' + filename + '\n')
                                        break
                                time.sleep(0.5)
                            break
                        ##############################################################
                        deltaTime_load = time.clock() - deltaTimeStart
                        if (deltaTime_load > kTIMEOUT_LOAD_APP):
                            time.sleep(1)
                            break
                        time.sleep(0.5)
                        ##############################################################
            self.m_button_runTestCases.SetLabel('Run Test Cases')
            self.m_button_runTestCases.SetBackgroundColour(uidef.kButtonColor_White)
        else:
            self.showInfoMessage('Loader Error', 'You need to set Loader EXE first.')

    def task_loadTestCases( self ):
        while True:
            if self.isLoadTestCasesTaskPending:
                self._loadTestCases()
                self.isLoadTestCasesTaskPending = False
            time.sleep(1)

    def showContentOnMainPrintWin( self, text ):
        self.m_textCtrl_printWin.AppendText(text)

    def showContentOnMainResWin( self, text ):
        self.m_textCtrl_resWin.AppendText(text)

    def resetTestResult( self ):
        self.m_textCtrl_resWin.Clear()
        self.m_textCtrl_printWin.Clear()

    def showInfoMessage( self, myTitle, myContent):
        wx.MessageBox(myContent, myTitle, wx.OK | wx.ICON_INFORMATION)

