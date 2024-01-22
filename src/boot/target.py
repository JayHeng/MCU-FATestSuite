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

