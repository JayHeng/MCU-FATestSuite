#!/usr/bin/env python

# Copyright 2024 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys, os

cpu = 'MIMXRT798'

jlinkDevice     = 'MIMXRT798S_M33_0'
jlinkInterface  = 'SWD'
jlinkSpeedInkHz = 4000

uartRecvInterval = 0.5  # seconds

fatLogStart = 'FAT FW Start'
fatLogPass  = 'FAT FW Pass'
fatLogFail  = 'FAT FW Fail'

fatRegAddr  = 0x50062FE0
fatRegStart = 0x5A
fatRegPass  = 0xA7
fatRegFail  = 0x9F

loadAppTimeout = 5.0  # seconds
waitAppTimeout = 30.0 # seconds


