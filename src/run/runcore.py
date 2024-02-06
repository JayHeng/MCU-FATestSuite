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
import rundef
import debugger_utils
import boot
sys.path.append(os.path.abspath(".."))
from ui import uicore
from ui import uidef
from ui import uilang
from boot import target

def createTarget(device, exeBinRoot):
    cpu = "MIMXRT798"
    if device == uidef.kMcuDevice_iMXRT700:
        cpu = "MIMXRT798"
    elif device == uidef.kMcuDevice_Custom:
        cpu = uidef.kMcuDevice_Custom
    else:
        pass
    targetBaseDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'targets', cpu)

    # Check for existing target directory.
    if not os.path.isdir(targetBaseDir):
        targetBaseDir = os.path.join(os.path.dirname(exeBinRoot), 'src', 'targets', cpu)
        if not os.path.isdir(targetBaseDir):
            raise ValueError("Missing target directory at path %s" % targetBaseDir)

    targetConfigFile = os.path.join(targetBaseDir, 'fattargetconfig.py')

    # Check for config file existence.
    if not os.path.isfile(targetConfigFile):
        raise RuntimeError("Missing target config file at path %s" % targetConfigFile)

    # Build locals dict by copying our locals and adjusting file path and name.
    targetConfig = locals().copy()
    targetConfig['__file__'] = targetConfigFile
    targetConfig['__name__'] = 'fattargetconfig'

    # Execute the target config script.
    execfile(targetConfigFile, globals(), targetConfig)

    # Create the target object.
    tgt = target.Target(**targetConfig)

    return tgt, targetBaseDir

##
# @brief
class faTesterRun(uicore.faTesterUi):

    def __init__(self, parent):
        uicore.faTesterUi.__init__(self, parent)
        self.tgt = None
        self.cpuDir = None
        self.createMcuTarget()

    def createMcuTarget( self ):
        self.tgt, self.cpuDir = createTarget(self.mcuDevice, self.exeBinRoot)

    def task_receiveUartData( self ):
        while True:
            if self.enableUartToRecvData:
                if self.serialPort.isOpen():
                    num = self.serialPort.inWaiting()
                    if num != 0:
                        data = self.serialPort.read(num)
                        string = data.decode()
                        self.recvPrintBuf += string
                        self.appendContentOnMainPrintWin(string)
            time.sleep(self.tgt.uartRecvInterval)

    def findTestCases( self ):
        self.resetTestResult(False)
        caseTestResultMsg = ""
        fwAppFiles = []
        fwFolderPath = os.path.join(self.exeTopRoot, 'src', 'targets', self.tgt.cpu, self.mcuBoard)
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
            self.appendContentOnMainResWin(caseTestResultMsg)
            self.setButtonProperty("detectTestCases", uidef.kButtonColor_Green)

    def _getVal32FromByteArray( self, binarray, offset=0):
        val32Vaule = ((binarray[3+offset]<<24) + (binarray[2+offset]<<16) + (binarray[1+offset]<<8) + binarray[0+offset])
        return val32Vaule

    def _getAppDelayTime( self, loc ):
        delay = 0
        magicLen = len(self.tgt.fatLogDelay)
        while True:
            if len(self.recvPrintBuf) > loc + magicLen:
                res = self.recvPrintBuf[loc:loc+magicLen+1].find(self.tgt.fatLogDelay)
                if (res != -1):
                    loc = loc + res + len(self.tgt.fatLogDelay)
                    time = ''
                    while len(self.recvPrintBuf) > loc:
                        if self.recvPrintBuf[loc] == 's':
                            delay = int(time)
                            break
                        else:
                            time += self.recvPrintBuf[loc]
                            loc = loc + 1
                else:
                    break
        #print('delay time = ' + str(delay))
        return delay

    def _flushTestResultLog (self, log ):
        self.caseResultLog += log
        self.appendContentOnMainResWin(log)

    def _loadTestCases( self ):
        if os.path.isfile(self.loaderExe):
            self.resetTestResult(False)
            appLen = len(self.fwAppFiles)
            if appLen == 0:
                self.showInfoMessage('Flow Error', 'You need to detect test cases first.')
                return 
            self.setButtonProperty("runTestCases", uidef.kButtonColor_Yellow)
            self.recvPrintBuf = ""
            self.caseResultLog = ""
            if self.serialPort.isOpen():
                self.serialPort.reset_input_buffer()
            else:
                self.showInfoMessage('Flow Error', 'Com Port is not opened.')
                return 
            jlinkcmdFolderPath = os.path.join(self.exeTopRoot, 'src', 'run', 'debuggers', 'jlink')
            #print('Creating JLink debugger object...')
            self._debugger = debugger_utils.createDebugger(debugger_utils.kDebuggerType_JLink, self.tgt.jlinkDevice, self.tgt.jlinkInterface, self.tgt.jlinkSpeedInkHz, self.loaderExe, jlinkcmdFolderPath)
            self._debugger.open()
            #print('Created JLink debugger object\r\n')
            lastBeg = 0
            for appIdx in range(appLen):
                self.setButtonProperty("runTestCases", None, 'Running Test Case ' + str(appIdx+1) + '/' + str(appLen))
                self.appendContentOnMainPrintWin('---------Case ' + str(appIdx+1) + '/' + str(appLen) + '----------\n')
                srecObj = bincopy.BinFile(str(self.fwAppFiles[appIdx]))
                filepath, file = os.path.split(self.fwAppFiles[appIdx])
                filename, filetype = os.path.splitext(file)
                startAddress = srecObj.minimum_address
                initialAppBytes = srecObj.as_binary(startAddress, startAddress + 8)
                sp = self._getVal32FromByteArray(initialAppBytes[0:4])
                pc = self._getVal32FromByteArray(initialAppBytes[4:8])
                appIsLoaded = False
                while (not appIsLoaded):
                    #print('Loading app ' + self.fwAppFiles[appIdx] + ' via JLink debugger...')
                    self._debugger.JumpToApp(self.fwAppFiles[appIdx], sp, pc, None)
                    #print('Loaded app via JLink debugger\r\n')
                    deltaTimeStart_load = time.clock()
                    while True:
                        res0 = self.recvPrintBuf.find(self.tgt.fatLogStart, lastBeg)
                        ##############################################################
                        if (res0 != -1):
                            deltaTimeStart_check = time.clock()
                            appIsLoaded = True
                            delayTimeApp = self._getAppDelayTime(res0 + len(self.tgt.fatLogStart))
                            lastBeg = res0
                            while True:
                                res1 = self.recvPrintBuf.find(self.tgt.fatLogPass, lastBeg)
                                res2 = self.recvPrintBuf.find(self.tgt.fatLogFail, lastBeg)
                                if (res1 != -1):
                                    lastBeg = res1
                                    self._flushTestResultLog('( PASS ) -- ' + filename)
                                    if delayTimeApp != 0:
                                        self._flushTestResultLog(', <case requires ' + str(delayTimeApp) + 's delay>\n')
                                        deltaTimeAppStart = time.clock()
                                        deltaTime_app = time.clock() - deltaTimeAppStart
                                        while (deltaTime_app < delayTimeApp):
                                            deltaTime_app = time.clock() - deltaTimeAppStart
                                            time.sleep(1)
                                    else:
                                        self._flushTestResultLog('\n')
                                    break
                                if (res2 != -1):
                                    lastBeg = res2
                                    self._flushTestResultLog('( FAIL ) -- ' + filename + '\n')
                                    break
                                deltaTime_check = time.clock() - deltaTimeStart_check
                                if (deltaTime_check > self.tgt.waitAppTimeout):
                                    self._flushTestResultLog('( TIMEOUT ) -- ' + filename + '\n')
                                    time.sleep(1)
                                    break
                                time.sleep(0.5)
                            break
                        ##############################################################
                        #status, res0 = self._debugger.readMem32(self.tgt.fatRegAddr)
                        if False: #status and ((res0 & 0xFF) == self.tgt.fatRegStart):
                            appIsLoaded = True
                            while True:
                                status, resx = self._debugger.readMem32(self.tgt.fatRegAddr)
                                if status:
                                    resx = resx >> 24
                                    if resx == self.tgt.fatRegPass:
                                        self._flushTestResultLog('( PASS ) -- ' + filename + '\n')
                                        break
                                    elif resx == self.tgt.fatRegFail:
                                        self._flushTestResultLog('( FAIL ) -- ' + filename + '\n')
                                        break
                                time.sleep(0.5)
                            break
                        ##############################################################
                        deltaTime_load = time.clock() - deltaTimeStart_load
                        if (deltaTime_load > self.tgt.loadAppTimeout):
                            time.sleep(1)
                            break
                        time.sleep(0.5)
                        ##############################################################
            self.setButtonProperty("runTestCases", uidef.kButtonColor_White, 'Run Test Cases')
            #self.flushContentOnMainPrintWin()
        else:
            self.showInfoMessage('Loader Error', 'You need to set Loader EXE first.')

    def _saveTestResult( self ):
        self.updateBoardSN()
        resFilename = os.path.join(self.exeTopRoot, 'bin', self.mcuDevice + "_" + self.mcuBoard + "_" + self.boardSN + "_test_result_" + time.strftime('%Y-%m-%d_%H.%M.%S',time.localtime(time.time())) + '.txt')
        with open(resFilename, 'w+') as fileObj:
            fileObj.write("\r\n-----------case result log--------------\r\n")
            fileObj.write(self.caseResultLog)
            fileObj.write("\r\n-----------case print log---------------\r\n")
            fileObj.write(self.recvPrintBuf)
            fileObj.close()

    def task_loadTestCases( self ):
        while True:
            if self.isLoadTestCasesTaskPending:
                self._loadTestCases()
                self._saveTestResult()
                self.isLoadTestCasesTaskPending = False
            time.sleep(1)
