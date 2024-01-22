#! /usr/bin/env python

# Copyright 2024 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os

def get_dict_default(d, k, default):
    if not d.has_key(k):
        return default
    else:
        return d[k]

##
# Bootloader target definition.
class Target(object):

    def __init__(self, cpu, **kwargs):
        self.cpu = cpu

        self.jlinkDevice = get_dict_default(kwargs, 'jlinkDevice', None)
        self.jlinkInterface = get_dict_default(kwargs, 'jlinkInterface', None)
        self.jlinkSpeedInkHz = get_dict_default(kwargs, 'jlinkSpeedInkHz', None)

        self.uartRecvInterval = get_dict_default(kwargs, 'uartRecvInterval', None)
        self.fatLogStart = get_dict_default(kwargs, 'fatLogStart', None)
        self.fatLogPass = get_dict_default(kwargs, 'fatLogPass', None)
        self.fatLogFail = get_dict_default(kwargs, 'fatLogFail', None)
        self.fatLogDelay = get_dict_default(kwargs, 'fatLogDelay', None)

        self.fatRegAddr = get_dict_default(kwargs, 'fatRegAddr', None)
        self.fatRegStart = get_dict_default(kwargs, 'fatRegStart', None)
        self.fatRegPass = get_dict_default(kwargs, 'fatRegPass', None)
        self.fatRegFail = get_dict_default(kwargs, 'fatRegFail', None)

        self.loadAppTimeout = get_dict_default(kwargs, 'loadAppTimeout', None)
        self.waitAppTimeout = get_dict_default(kwargs, 'waitAppTimeout', None)



