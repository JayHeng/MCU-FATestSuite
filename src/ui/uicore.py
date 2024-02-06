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
import serial.tools.list_ports
import uidef
import uivar
import uilang
sys.path.append(os.path.abspath(".."))
from win import faTesterWin

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
        self.mcuBoard = None
        self.boardSN = None
        self.testLoader = None
        self.loaderExe = None
        self._initTargetSetupValue()
        self.setTargetSetupValue()
        self.initUi()
        self.fwAppFiles = []
        self.isLoadTestCasesTaskPending = False
        self.enableUartToRecvData = False
        self.serialPort = serial.Serial()
        self.caseResultLog = ""
        self.recvPrintBuf = ""

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
            self.enableUartToRecvData = False
            self.m_button_open.SetLabel('Open')
            self.m_button_open.SetBackgroundColour(uidef.kButtonColor_White)
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
        self.m_choice_mcuBoard.SetSelection(self.toolCommDict['mcuBoard'])
        self.m_textCtrl_boardSN.Clear()
        self.m_textCtrl_boardSN.write(self.toolCommDict['boardSN'])
        self.m_choice_testLoader.SetSelection(self.toolCommDict['testLoader'])
        if self.toolCommDict['loaderExe'] != None and os.path.isfile(self.toolCommDict['loaderExe']):
            self.loaderExe = self.toolCommDict['loaderExe']
            self.m_filePicker_setLoaderExe.SetPath(self.loaderExe)

    def setTargetSetupValue( self ):
        self.mcuDevice = self.m_choice_mcuDevice.GetString(self.m_choice_mcuDevice.GetSelection())
        self.toolCommDict['mcuDevice'] = self.m_choice_mcuDevice.GetSelection()
        self.mcuBoard = self.m_choice_mcuBoard.GetString(self.m_choice_mcuBoard.GetSelection())
        self.toolCommDict['mcuBoard'] = self.m_choice_mcuBoard.GetSelection()
        self.boardSN = self.m_textCtrl_boardSN.GetLineText(0)
        self.toolCommDict['boardSN'] = self.boardSN
        self.testLoader = self.m_choice_testLoader.GetString(self.m_choice_testLoader.GetSelection())
        self.toolCommDict['testLoader'] = self.m_choice_testLoader.GetSelection()

    def updateBoardSN ( self ):
        self.boardSN = self.m_textCtrl_boardSN.GetLineText(0)
        if len(self.boardSN) == 0:
            self.boardSN = "SNxxxxxxxx"
        else:
            self.toolCommDict['boardSN'] = self.boardSN

    def updatePortSetupValue( self ):
        self.uartComPort = self.m_choice_comPort.GetString(self.m_choice_comPort.GetSelection())
        self.uartBaudrate = self.m_choice_baudrate.GetString(self.m_choice_baudrate.GetSelection())

    def setPortSetupValue( self ):
        self.adjustPortSetupValue()
        self.updatePortSetupValue()

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

    def setButtonProperty ( self, name, color = None, label = None):
        if name == "runTestCases":
            if color != None:
                self.m_button_runTestCases.SetBackgroundColour(color)
            if label != None:
                self.m_button_runTestCases.SetLabel(label)
        elif name == "detectTestCases":
            if color != None:
                self.m_button_detectTestCases.SetBackgroundColour(color)
            if label != None:
                self.m_button_detectTestCases.SetLabel(label)
        else:
            pass

    def openUartPort ( self ):
        self.serialPort.port = self.uartComPort
        self.serialPort.baudrate = int(self.uartBaudrate)
        self.serialPort.bytesizes = serial.EIGHTBITS
        self.serialPort.stopbits = serial.STOPBITS_ONE
        self.serialPort.parity = serial.PARITY_NONE
        try:
            self.serialPort.open()
        except:
            self.showInfoMessage('Port Error', 'Com Port cannot be opened!')
            return
        self.serialPort.set_buffer_size(rx_size=1024 * 16)
        self.serialPort.reset_input_buffer()
        self.serialPort.reset_output_buffer()
        self.enableUartToRecvData = True
        self.m_button_open.SetLabel('Close')
        self.m_button_open.SetBackgroundColour(uidef.kButtonColor_Green)

    def closeUartPort ( self ):
        if self.serialPort.isOpen():
            self.serialPort.close()
            self.enableUartToRecvData = False
            self.m_button_open.SetLabel('Open')
            self.m_button_open.SetBackgroundColour(uidef.kButtonColor_White)

    def appendContentOnMainPrintWin( self, text ):
        self.m_textCtrl_printWin.AppendText(text)

    def flushContentOnMainPrintWin( self ):
        self.m_textCtrl_printWin.Clear()
        self.m_textCtrl_printWin.AppendText(self.recvPrintBuf)

    def appendContentOnMainResWin( self, text ):
        self.m_textCtrl_resWin.AppendText(text)

    def resetTestResult( self , portReset = True):
        self.m_textCtrl_resWin.Clear()
        self.m_textCtrl_printWin.Clear()
        if portReset:
            self.setPortSetupValue()

    def showInfoMessage( self, myTitle, myContent):
        wx.MessageBox(myContent, myTitle, wx.OK | wx.ICON_INFORMATION)

