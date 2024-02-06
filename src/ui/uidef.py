
# Copyright 2024 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import wx
import sys, os

kMcuDevice_Custom    = 'CustomDevice'
kMcuDevice_iMXRT700  = 'i.MXRT7xx'

kMcuDevice_v1_0      = [kMcuDevice_iMXRT700]
kMcuDevice_v1_3      = [kMcuDevice_iMXRT700, kMcuDevice_Custom]
kMcuDevice_Latest    = kMcuDevice_v1_3

kMcuBoard_Custom     = 'CustomBoard'
kMcuBoard_RT700_EVK1 = 'FOWLP324-EVK_Rev.A'
kMcuBoard_RT700_EVB1 = 'WLCSP256-EVB_Rev.A'
kMcuBoard_RT700_EVB2 = 'MAPBGA400-EVB_Rev.A'

kMcuBoardList_Custom     = [kMcuBoard_Custom]
kMcuBoardList_iMXRT700   = [kMcuBoard_RT700_EVK1, kMcuBoard_RT700_EVB1, kMcuBoard_RT700_EVB2]

kAdvancedSettings_Tool             = 0

kButtonColor_Yellow = wx.YELLOW
kButtonColor_White  = wx.WHITE
kButtonColor_Green  = wx.GREEN
