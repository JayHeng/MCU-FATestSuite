#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os, time
import pylink
from pylink.errors import JLinkException

kMCU_REGISTER_ADDR = 0x50062FE0

##
# @brief JLink debugger class.
#
class PylinkDebugger():
    """Jlink debugger support"""

    ##
    # @brief Initialize the debugger.
    #
    def __init__(self, *args):
        self.jlink = pylink.JLink()
        self.core = args[0]
        self.interface = args[1]
        self.speed = args[2]

    def getJlinkUid(self):
        jlinkUid = []
        try:
            connected_probes = self.jlink.connected_emulators()
        except:
            connected_probes = []
        print(connected_probes)
    ##
    # @brief Jump to app.
    #
    def JumpToApp(self, serialNum, fwFile, sp, pc, addr=kMCU_REGISTER_ADDR):
        status = True

        # Open a connection to your J-Link.
        self.jlink.open(serialNum)
        # Connect to the target device.
        self.jlink.connect(self.core, verbose=True)
        self.jlink.set_speed(self.speed)
        if self.interface == 'SWD':
            self.jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        elif self.interface == 'JTAG':
            self.jlink.set_tif(pylink.enums.JLinkInterfaces.JTAG)

        return status


