#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024 NXP
# All rights reserved.
# 
# SPDX-License-Identifier: BSD-3-Clause

import sys
import os

kMenuPosition_File     = 0x0
kMenuPosition_Edit     = 0x1
kMenuPosition_View     = 0x2
kMenuPosition_Tools    = 0x3
kMenuPosition_Window   = 0x4
kMenuPosition_Help     = 0x5

kRevision_1_0_0_en =  "【v1.0.0】 \n" + \
                      "  Feature: \n" + \
                      "     1. Support i.MXRT7xx \n" + \
                      "     2. Support J-LINK SWD \n" + \
                      "     3. Support multiple cases (.srec) detection and load-to-run  \n" + \
                      "     4. Support UART result (magic log) checking \n\n"

kRevision_1_1_0_en =  "【v1.1.0】 \n" + \
                      "  Feature: \n" + \
                      "     1. Support user config (jlink settings, magic log format, recv interval, process timeout) \n\n"

kRevision_1_2_0_en =  "【v1.2.0】 \n" + \
                      "  Feature: \n" + \
                      "     1. Support delay time in UART result (magic log) \n" + \
                      "  Improvement: \n" + \
                      "     1. Can refresh COM port list via 'Reset Test Result' button \n" + \
                      "     2. Kill jlink process to fix stable issue \n\n"

kRevision_1_3_0_en =  "【v1.3.0】 \n" + \
                      "  Feature: \n" + \
                      "     1. Add custom device/board option \n" + \
                      "     2. Can save test result into text file automatically \n" + \
                      "  Improvement: \n" + \
                      "     1. Tool path can contain spaces \n\n"

kMsgLanguageContentDict = {
        'homePage_title':                     ['Home Page'],
        'homePage_info':                      ['https://github.com/JayHeng/MCU-FATestSuite.git \n'],
        'aboutAuthor_title':                  ['About Author'],
        'aboutAuthor_author':                 [u"Author: 痞子衡 \n"],
        'aboutAuthor_email1':                 ['Email: jie.heng@nxp.com \n'],
        'aboutAuthor_email2':                 ['Email: hengjie1989@foxmail.com \n'],
        'aboutAuthor_blog':                   [u"Blog: 痞子衡嵌入式 https://www.cnblogs.com/henjay724/ \n"],
        'revisionHistory_title':              ['Revision History'],
        'revisionHistory_v1_0_0':             [kRevision_1_0_0_en],
        'revisionHistory_v1_1_0':             [kRevision_1_1_0_en],
        'revisionHistory_v1_2_0':             [kRevision_1_2_0_en],
        'revisionHistory_v1_3_0':             [kRevision_1_3_0_en],
}