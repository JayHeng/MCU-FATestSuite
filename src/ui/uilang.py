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
                      "     2. Support J-LINK SWD \n\n"

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
}