#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os, time
import pyocd
from pyocd.core.exceptions import ProbeError
from pyocd.core.helpers import ConnectHelper

##
# @brief pyOCD debugger class.
#
class PyocdDebugger():

    ##
    # @brief Initialize the debugger.
    #
    def __init__(self):
        pass

    def getJlinkUid(self):
        jlinkUid = []
        try:
            connected_probes = ConnectHelper.get_all_connected_probes(blocking=False)
        except ProbeError as exc:
            connected_probes = []
        for probe in connected_probes:
            if probe.description.find('J-Link') != -1:
                jlinkUid.append(probe.unique_id)
        return jlinkUid
