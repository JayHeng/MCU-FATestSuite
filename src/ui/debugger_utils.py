#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os, time
import subprocess

##
# @brief Debugger types for createDebugger()
#
kDebuggerType_JLink = 'jlink'
kDebuggerType_Mbed  = 'mbed'

##
# @brief Create a debugger instance
#
def createDebugger(debuggerType, *args):
    """Create a debugger"""
    if debuggerType == kDebuggerType_JLink:
        return JLinkDebugger(args)
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
        self.unlockDeviceName = None
        self.jlinkDir = os.path.expandvars(args[3])
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

