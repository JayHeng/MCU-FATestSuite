#!/usr/bin/env python

# Copyright 2025 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os

cpu = 'MIMXRT1180'

jlinkDevice     = 'MIMXRT1189XXX8_M33'
jlinkInterface  = 'SWD'
jlinkSpeedInkHz = 4000

uartRecvInterval = 0.5  # seconds

#'FAT FW Start DelayTime=10s'
fatLogStart = 'FAT FW Start'
fatLogPass  = 'FAT FW Pass'
fatLogFail  = 'FAT FW Fail'

# Delay x seconds after getting fatLogPass for some cases
fatLogDelay = ' DelayTime='

fatRegAddr  = 0x00000000 # TBD
fatRegStart = 0x5A
fatRegPass  = 0xA7
fatRegFail  = 0x9F

loadAppTimeout    = 5.0  # seconds
loadAppRetryCount = 3
waitAppTimeout    = 10.0 # seconds


