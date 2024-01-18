#! /usr/bin/env python

# Copyright (c) 2013 Freescale Semiconductor, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# o Redistributions of source code must retain the above copyright notice, this list
#   of conditions and the following disclaimer.
#
# o Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
# o Neither the name of Freescale Semiconductor, Inc. nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys, os, time
import serial
import pexpect
import subprocess
import serialpexpect
import subprocess
import struct
from pyOCD.board import MbedBoard
import bltestconfig

##
# @brief Debugger types for createDebugger()
#
kDebuggerType_JLink = 'jlink'
kDebuggerType_Mbed = 'mbed'
DEBUG_THIS_MODEL = False
if DEBUG_THIS_MODEL:
    JLINK_FILE_COUNT = 0

##
# @brief Create a debugger instance
#
def createDebugger(debuggerType, *args):
    """Create a debugger"""
    if debuggerType == kDebuggerType_JLink:
        return JLinkDebugger(args)
    elif debuggerType == kDebuggerType_Mbed:
        return MbedDebugger()
    elif debuggerType == None:
        return Debugger()
    else:
        raise DebuggerUsageError("debuggerType %s is unknown" % debuggerType)

##
# @brief Debugger exceptions
#
class DebuggerUsageError(Exception):
    """Debugger exceptions"""

##
# @brief Debugger parent class.
#
# Can be used as-is for no-op debugger.
#
class Debugger:
    """Debugger support"""

    ##
    # @brief Open the debugger.
    #
    def open(self):
        pass

    ##
    # @brief Close the debugger.
    #
    def close(self):
        pass

    ##
    # @brief Reset the target.
    #
    def reset(self):
        pass

    ##
    # @brief unlock the target
    #
    def unlock(self):
        pass

    ##
    # @brief Flash a binary image to the target.
    #
    def flashBinary(self, binFilename):
        pass

##
# @brief JLink debugger class.
#
class JLinkDebugger(Debugger):
    """Jlink debugger support"""

    ##
    # @brief Initialize the debugger.
    #
    def __init__(self, args):
        self.core = args[0]
        self.interface = args[1]
        self.speed = str(args[2])
        self.unlockDeviceName = args[3]
        self.jlinkDir = os.path.expandvars(args[4])
        self.quitCommand = 'q'

        self.argsList = [self.jlinkDir, '-device', self.core, '-if', self.interface, '-speed', self.speed]
        self.commandPath = os.path.join(os.path.dirname(__file__), 'debuggers', 'jlink', 'jlink_temporary_cmd.jlink')
        
    ##
    # @brief Convert str to hex.
    #
    def getHexByte(self, str):
        if str[0].isdigit():
            hex = (ord(str[0]) - ord('0')) << 4
        else:
            hex = (ord(str[0]) - ord('A') + 10) << 4
        if str[1].isdigit():
            hex += ord(str[1]) - ord('0')
        else:
            hex += ord(str[1]) - ord('A') + 10
        return hex

    ##
    # @brief
    #
    def getJlinkCmdArg(self, args):
        # command = os.path.expandvars('%IAR_WORKBENCH%/arm/bin/jlink.exe')
        argsList = self.argsList
        if DEBUG_THIS_MODEL:
            global JLINK_FILE_COUNT
            commandPath = os.path.join(os.path.dirname(__file__), 'debuggers', 'jlink', 'jlink_temporary_cmd_DEBUG'+str(JLINK_FILE_COUNT)+'.jlink')
        else:
            commandPath =  self.commandPath
        if os.path.isfile(commandPath):
            os.remove(commandPath)
        with open(commandPath, 'w') as fileObj:
            fileObj.write(args)
            fileObj.close()
        # commandArgs = [command, argsFile]
        # return commandArgs
        argsList.extend(['-CommandFile', commandPath])
        return argsList

    ##
    # @brief
    #
    def deleteJlinkCmdFile(self):
        # Do not delete Temp files if it is DEBUG mode
        if DEBUG_THIS_MODEL:
            global JLINK_FILE_COUNT
            # commandPath = os.path.join(os.path.dirname(__file__), 'debuggers', 'jlink', 'jlink_temporary_cmd_DEBUG'+str(JLINK_FILE_COUNT)+'.jlink')
            JLINK_FILE_COUNT = JLINK_FILE_COUNT + 1
        else:
            commandPath =  self.commandPath
            if os.path.isfile(commandPath):
                try:
                    os.remove(commandPath)
                except Exception as e:
                    print "Unknown exception: %s" % e

    ##
    # @brief Reset the target.
    #
    def reset(self):
        """Reset the target"""
        commandPath = os.path.join(os.path.dirname(__file__), 'debuggers', 'jlink', 'reset.jlink')
        argsList = self.argsList
        argsList.extend(['-CommandFile', commandPath])
        args = ' '.join(argsList)
        try:
            subprocess.call(args)
            # process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except OSError:
            print('\nReset Error.\n')
        # commandOutputs = process.communicate()[0]
        # return commandOutputs

        # test_device = ''
        # debugger_if = ''
        # if bltestconfig.kibble_device != '':
        #     test_device =  ' -device '+ bltestconfig.kibble_device
        # if  bltestconfig.debugger_if != '':
        #     debugger_if = ' -if ' + bltestconfig.debugger_if + ' '
        
        # commandline_device = test_device + debugger_if   
        # command = os.path.expandvars('%IAR_WORKBENCH%/arm/bin/jlink.exe')
        # commandline_args = [commandline_device, os.path.join(os.path.dirname(__file__), 'debuggers', 'jlink', 'reset.jlink')]

        # try:
        #     subprocess.call([command,  commandline_args])
        # except OSError:
        #     print('\nReset Error.\n')
        
#        process = pexpect.spawn(command, commandline_args)        
        # Sometimes jlink hangs after a reset call, we expect an EOF, if 10 seconds passes a TIMEOUT will occur
        # but we are going to assume the reset happened an continue on with the test
#        expectResult = process.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=20)
#        if (expectResult == 1): # We had a timeout, kill the process
#            process.child_obj.kill()
            

    ##
    # @brief Unlock the target
    #
    def unlock(self):
        """unlock the target"""
        # command = os.path.expandvars('%IAR_WORKBENCH%/arm/bin/jlink.exe')
        # commandPath = [os.path.join(os.path.dirname(__file__), 'debuggers', 'jlink', 'unlock.jlink')]
        args = '{} {}\n{}'.format('unlock', self.unlockDeviceName, self.quitCommand)
        commandArgs = self.getJlinkCmdArg(args)
        process = subprocess.Popen(commandArgs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        commandOutputs = process.communicate()[0]
        print commandOutputs
        # process = pexpect.spawn(command, commandArgs)
        # process.wait()

    def readMem(self, address, itemType, itemNum):
        # Parse result (no sure about the case type of addr returned by jlink)
        hexAddr = "0x%08x" % address   # Address must be 8 digits
        hexNumItems = "0x%x" % itemNum
        if itemType == 'byte':
            memCmd = 'mem8'
            addrLength = 2
        elif itemType == 'halfWord' or itemType == 'short':
            memCmd = 'mem16'
            addrLength = 4
        elif itemType == 'word':
            memCmd = 'mem32'
            addrLength = 8
        else:
            raise ValueError('Invalid itemType parameter.')

        args = '{} {} {}\n{}'.format(memCmd, hexAddr, hexNumItems, self.quitCommand)
        # args = memCmd + ' ' + hexAddr + ' ' + ("0x%x" %numItems) + '\r\n' + 'q'
        commandArgs = self.getJlinkCmdArg(args)
        status = True
        try:
            process = subprocess.Popen(commandArgs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            commandOutputs = process.communicate()[0]
            hexAddr = hexAddr[2:]   # Remove the beginning of the string '0x'
            addrIndex = commandOutputs.find(hexAddr.upper())
            if addrIndex == -1:
                addrIndex = commandOutputs.find(hexAddr.lower())
            if addrIndex != -1:
                resOffset = addrIndex + 11
                strResult = commandOutputs[resOffset:resOffset+addrLength]
                hexResult = int(strResult,16)
            else:
                status = False
        except Exception as e:
            print "Unknown exception: %s" % e
            status = False
        self.deleteJlinkCmdFile()
        time.sleep(0.5)
        return status, hexResult
    ##
    # @brief Read the memory.
    #
    def readMemOneItem(self, addr, itemType):
        """Read the memory"""
        status = True
        # Prepare cmd and arg
        numItems = 0x1

        if itemType == 'byte':
            memCmd = 'mem8'
        elif itemType == 'halfWord':
            memCmd = 'mem16'
        elif itemType == 'word':
            memCmd = 'mem32'
        else:
            raise ValueError('Invalid itemType parameter.')
        
        commandArgs = []
        args = memCmd + ' ' + ("0x%x" %addr) + ' ' + ("0x%x" %numItems) + '\r\n' + 'q'
        commandArgs = self.getJlinkCmdArg(args)

        # Execute the command.
        hexResult = 0
        try:
            process = subprocess.Popen(commandArgs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            #print 'commandOutput:', commandOutputs
            commandOutputs = process.communicate()[0]
            # Parse result (no sure about the case type of addr returned by jlink)
            hexAddr = "%08x" % addr   # Address must be 8 digits
            addrIndex = commandOutputs.find(hexAddr.upper())
            if addrIndex == -1:
                addrIndex = commandOutputs.find(hexAddr.lower())
            if addrIndex != -1:
                resOffset = addrIndex + 11
                strResult = commandOutputs[resOffset:resOffset+2]
                # hexResult = int(strResult, 16)
                hexResult = self.getHexByte(strResult)
                if itemType != 'byte':
                    strResult = commandOutputs[resOffset+2:resOffset+4]
                    hexResult = (hexResult << 8) + self.getHexByte(strResult)
                if itemType == 'word':
                    strResult = commandOutputs[resOffset+4:resOffset+6]
                    hexResult = (hexResult << 8) + self.getHexByte(strResult)
                    strResult = commandOutputs[resOffset+6:resOffset+8]
                    hexResult = (hexResult << 8) + self.getHexByte(strResult)
            else:
                status = False
        except Exception as e:
            print "Unknown exception: %s" % e
            status = False

        self.deleteJlinkCmdFile()

        time.sleep(0.5)
        return status, hexResult

    ##
    # @brief Write the memory.
    #
    def writeMemOneItem(self, addr, value, itemType):
        """Write the memory"""
        status = True
        # Prepare cmd and arg
        if itemType == 'byte':
            memCmd = 'w1'
        elif itemType == 'halfWord':
            memCmd = 'w2'
        elif itemType == 'word':
            memCmd = 'w4'
        else:
            raise ValueError('Invalid itemType parameter.')
        
        commandArgs = []
        args = args = memCmd + ' ' + ("0x%x" %addr) + ' ' + ("0x%x" %value) + '\r\n' + 'q'
        commandArgs = self.getJlinkCmdArg(args)

        # Execute the command.
        try:
            process = subprocess.Popen(commandArgs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as e:
            print "Unknown exception: %s" % e
            status = False

        #self.deleteJlinkCmdFile()

        time.sleep(0.5)
        return status

    ##
    # @brief Write the memory.
    #
    def getPC(self):
        """Get the value of PC register"""
        status = True
        
        commandArgs = []
        args = 'h' + '\r\n' + 'g' + '\r\n' + 'q'
        commandArgs = self.getJlinkCmdArg(args)

        # Execute the command.
        pc = 0
        try:
            process = subprocess.Popen(commandArgs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            commandOutputs = process.communicate()[0]
            
            pcIndex = commandOutputs.find('R15(PC)')
            if pcIndex != -1:
                resOffset = pcIndex + 10
                strResult = commandOutputs[resOffset:resOffset+2]
                hexResult = self.getHexByte(strResult)
                strResult = commandOutputs[resOffset+2:resOffset+4]
                hexResult = (hexResult << 8) + self.getHexByte(strResult)
                strResult = commandOutputs[resOffset+4:resOffset+6]
                hexResult = (hexResult << 8) + self.getHexByte(strResult)
                strResult = commandOutputs[resOffset+6:resOffset+8]
                hexResult = (hexResult << 8) + self.getHexByte(strResult)
                pc = hexResult
            else:
                status = False
        except Exception as e:
            print "Unknown exception: %s" % e
            status = False
        
        #self.deleteJlinkCmdFile()

        return status, pc

##
# @brief Mbed (PyOCD) debugger.
#
class MbedDebugger(Debugger):
    """Mbed PyOCD debugger support"""

    ##
    # @brief Initialize the debugger.
    #
    def __init__(self):
        self._board = None

    ##
    # @brief Choose the mbed board.
    #
    def open(self):
        """Choose the board"""
        if not self._board:
            try:
                print "Unknown exception"
                self._board = MbedBoard.chooseBoard()
                print "Unknown exception1"
                self._board.target.resume()
                print "Unknown exception2"
                time.sleep(0.2)
                print "Unknown exception3"
            #except Exception as e: #python 3
            except Exception,e:#python2
                print "Unknown exception: %s" % e
                #assert None

    ##
    # @brief Uninit the mbed board.
    #
    def close(self):
        """Uninit the board"""
        if self._board:
            self._board.uninit()
            self._board = None

    ##
    # @brief Reset the target.
    #
    def reset(self):
        """Reset the target"""
        self.open()
        try:
            self._board.target.halt()
            time.sleep(0.2)
            self._board.target.reset()
            time.sleep(0.1)
        except Exception as e:
            print "Unknown exception: %s" % e
            self.close()

    ##
    # @brief Read the memory.
    #
    def readMemOneItem(self, addr, itemType):
        """Read the memory"""
        status = True
        # Prepare cmd and arg
        if itemType == 'byte':
            memCmd = 8
        elif itemType == 'halfWord':
            memCmd = 16
        elif itemType == 'word':
            memCmd = 32
        else:
            raise ValueError('Invalid itemType parameter.')

        # Execute the command.
        self.open()
        hexResult = 0
        try:
            hexResult = self._board.target.readMemory(addr, memCmd)
        except Exception as e:
            print "Unknown exception: %s" % e
            self.close()
            status = False

        time.sleep(0.5)
        return status, hexResult

    ##
    # @brief Write the memory.
    #
    def writeMemOneItem(self, addr, value, itemType):
        """Write the memory"""
        status = True
        # Prepare cmd and arg
        if itemType == 'byte':
            memCmd = 8
        elif itemType == 'halfWord':
            memCmd = 16
        elif itemType == 'word':
            memCmd = 32
        else:
            raise ValueError('Invalid itemType parameter.')

        # Execute the command.
        self.open()
        try:
            self._board.target.writeMemory(addr, value, memCmd)
        except Exception as e:
            print "Unknown exception: %s" % e
            self.close()
            status = False

        time.sleep(0.5)
        return status

    ##
    # @brief Flash a binary image to the target.
    #
    def flashBinary(self, binFilename):
        """Flash a binary image to the target"""
        self.reset()
        try:
            self._board.target.halt()
            time.sleep(0.2)
            self._board.flash.flashBinary(binFilename)
        except Exception as e:
            print "Unknown exception: %s" % e
            self.close()
