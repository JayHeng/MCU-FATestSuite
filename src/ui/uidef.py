
# Copyright 2024 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import wx
import sys, os

kMcuDevice_Custom    = 'CustomDevice'
kMcuDevice_iMXRT500  = 'MIMXRT500'
kMcuDevice_iMXRT700  = 'MIMXRT700'
kMcuDevice_iMXRT1050 = 'MIMXRT1050'
kMcuDevice_iMXRT1060 = 'MIMXRT1060'
kMcuDevice_iMXRT1180 = 'MIMXRT1180'

kMcuDevice_v1_0      = [kMcuDevice_iMXRT700]
kMcuDevice_v1_3      = [kMcuDevice_iMXRT700, kMcuDevice_Custom]
kMcuDevice_v2_0      = [kMcuDevice_iMXRT500, kMcuDevice_iMXRT700, kMcuDevice_iMXRT1060, kMcuDevice_Custom]
kMcuDevice_v3_0      = [kMcuDevice_iMXRT500, kMcuDevice_iMXRT700, kMcuDevice_iMXRT1050, kMcuDevice_iMXRT1060, kMcuDevice_iMXRT1180, kMcuDevice_Custom]
kMcuDevice_Latest    = kMcuDevice_v3_0

kMcuBoard_Custom     = 'CustomBoard'
kMcuBoardList_Custom     = [kMcuBoard_Custom]

kMcuBoard_RT500_EVK1 = 'EVK_Rev.D_SCH-45800'
kMcuBoardList_iMXRT500   = [kMcuBoard_RT500_EVK1]

kMcuBoard_RT700_EVK1 = 'EVK_Rev.A_SCH-89280'
kMcuBoard_RT700_EVB1 = 'EVB_Rev.A_SCH-89271'
kMcuBoard_RT700_EVB2 = 'EVB_Rev.A_SCH-89790'
kMcuBoardList_iMXRT700   = [kMcuBoard_RT700_EVK1, kMcuBoard_RT700_EVB1, kMcuBoard_RT700_EVB2]

kMcuBoard_RT1050_EVKB0 = 'EVKB_Rev.B_SCH-30168'
kMcuBoardList_iMXRT1050   = [kMcuBoard_RT1050_EVKB0]

kMcuBoard_RT1060_EVK0  = 'EVK_Rev.X2_SCH-31357'
kMcuBoard_RT1060_EVK1  = 'EVK_Rev.A_SCH-31357'
kMcuBoard_RT1060_EVK2  = 'EVK_Rev.A1_SCH-31357'
kMcuBoard_RT1060_EVK3  = 'EVK_Rev.A2_SCH-31357'
kMcuBoard_RT1060_EVKB1 = 'EVKB_Rev.A_SCH-47858'
kMcuBoard_RT1060_EVKB2 = 'EVKB_Rev.B_SCH-47858'
kMcuBoard_RT1060_EVKC1 = 'EVKC_Rev.A_SCH-55539'
kMcuBoard_RT106X_EVK1  = 'EVK_Rev.A1_SCH-50780'
kMcuBoard_RT1060X_OPENART_DUAL = 'OPENART-DUAL_Rev.A_SCH-55323'
kMcuBoard_RT1060_EVB1  = 'EVB_Rev.A_SCH-34758'
kMcuBoardList_iMXRT1060   = [kMcuBoard_RT1060_EVK0, kMcuBoard_RT1060_EVK1, kMcuBoard_RT1060_EVK2, kMcuBoard_RT1060_EVK3,
                             kMcuBoard_RT1060_EVKB1, kMcuBoard_RT1060_EVKB2,
                             kMcuBoard_RT1060_EVKC1,
                             kMcuBoard_RT106X_EVK1,
                             kMcuBoard_RT1060X_OPENART_DUAL,
                             kMcuBoard_RT1060_EVB1]

kMcuBoard_RT1180_EVK0 = 'EVK_Rev.C3_SCH-50577'
kMcuBoardList_iMXRT1180   = [kMcuBoard_RT1180_EVK0]

kAdvancedSettings_Tool             = 0

kTestLoader_Jlink    = 'J-Link'
kTestLoader_CmsisDap = 'CMSIS-DAP'
kTestLoader_RomIsp   = 'ROM ISP UART'

kButtonColor_Yellow = wx.YELLOW
kButtonColor_White  = wx.WHITE
kButtonColor_Green  = wx.GREEN
