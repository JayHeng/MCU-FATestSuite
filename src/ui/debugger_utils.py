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

kMCU_REGISTER_ADDR = 0x50062FE0

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
        self.jlinkDir = os.path.expandvars(args[3])
        self.jlinkcmdPath = args[4]
        self.quitCommand = 'q'
        self.argsList = [self.jlinkDir, '-device', self.core, '-if', self.interface, '-speed', self.speed]
        self.commandPath = os.path.join(self.jlinkcmdPath, 'jlink_temporary_cmd.jlink')

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
                print("Unknown exception: %s" % e)

    ##
    # @brief Reset the target.
    #
    def reset(self):
        """Reset the target"""
        status = True
        # Prepare cmd and arg
        commandArgs = []
        args = 'r' + '\r\n' + 'h'
        commandArgs = self.getJlinkCmdArg(args)
        # Execute the command.
        try:
            process = subprocess.Popen(commandArgs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as e:
            print("Unknown exception: %s" % e)
            status = False
        #self.deleteJlinkCmdFile()

        return status

    ##
    # @brief Read the memory.
    #
    def readMem32(self, addr=kMCU_REGISTER_ADDR):
        """Read the memory"""
        status = True
        # Prepare cmd and arg
        numItems = 0x1
        memCmd = 'mem32'
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
                hexResult = self.getHexByte(strResult)
                strResult = commandOutputs[resOffset+2:resOffset+4]
                hexResult = (hexResult << 8) + self.getHexByte(strResult)
                strResult = commandOutputs[resOffset+4:resOffset+6]
                hexResult = (hexResult << 8) + self.getHexByte(strResult)
                strResult = commandOutputs[resOffset+6:resOffset+8]
                hexResult = (hexResult << 8) + self.getHexByte(strResult)
            else:
                status = False
        except Exception as e:
            print("Unknown exception: %s" % e)
            status = False

        self.deleteJlinkCmdFile()

        time.sleep(0.5)
        return status, hexResult

    ##
    # @brief Jump to app.
    #
    def JumpToApp(self, fwFile, sp, pc):
        status = True
        # Prepare cmd and arg
        commandArgs = []
        sp = "%08x" % sp   # must be 8 digits
        pc = "%08x" % pc   # must be 8 digits
        args = 'r' + '\r\n' + 'h' + '\r\n' + 'LoadFile ' + fwFile + '\r\n' + 'wreg MSP ' + sp + '\r\n' + 'wreg PSP ' + sp + '\r\n' + 'SetPC ' + pc + '\r\n' + 'g'
        commandArgs = self.getJlinkCmdArg(args)
        # Execute the command.
        try:
            process = subprocess.Popen(commandArgs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as e:
            print("Unknown exception: %s" % e)
            status = False
        #self.deleteJlinkCmdFile()

        return status
