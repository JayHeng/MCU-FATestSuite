#!/usr/bin/env python

# Copyright 2024 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os

cpu = 'CustomDevice'

jlinkDevice     = 'MIMXRT798S_M33_0'
jlinkInterface  = 'SWD'
jlinkSpeedInkHz = 4000

uartRecvInterval = 0.5  # seconds

#'FAT FW Start DelayTime=10s'
fatLogStart = 'FAT FW Start'
fatLogPass  = 'FAT FW Pass'
fatLogFail  = 'FAT FW Fail'

# Delay x seconds after getting fatLogPass for some cases
fatLogDelay = ' DelayTime='

fatRegAddr  = 0x50062FE0
fatRegStart = 0x5A
fatRegPass  = 0xA7
fatRegFail  = 0x9F

loadAppTimeout = 5.0  # seconds
waitAppTimeout = 10.0 # seconds


