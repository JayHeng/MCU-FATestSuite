#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import json
from . import uidef
from . import uivar

g_exeTopRoot = None
g_hasSubWinBeenOpened = False
g_cfgFilename = None
g_toolCommDict = {'mcuDevice':None,
                  'mcuBoard':None,
                  'boardSN':None,
                  'testLoader':None,
                  'loaderExe':None,
                 }

def initVar(cfgFilename):
    global g_hasSubWinBeenOpened
    global g_cfgFilename
    global g_toolCommDict

    g_hasSubWinBeenOpened = False
    g_cfgFilename = cfgFilename
    if os.path.isfile(cfgFilename):
        cfgDict = None
        with open(cfgFilename, 'r') as fileObj:
            cfgDict = json.load(fileObj)
            fileObj.close()

        g_toolCommDict = cfgDict["cfgToolCommon"][0]
    else:
        g_toolCommDict = {'mcuDevice':0,
                          'mcuBoard':"",
                          'boardSN':"TRxxxxxxxx",
                          'testLoader':0,
                          'loaderExe':None,
                         }


def deinitVar(cfgFilename=None):
    global g_cfgFilename
    if cfgFilename == None and g_cfgFilename != None:
        cfgFilename = g_cfgFilename
    with open(cfgFilename, 'w') as fileObj:
        global g_toolCommDict
        cfgDict = {
            "cfgToolCommon": [g_toolCommDict]
        }
        json.dump(cfgDict, fileObj, indent=1)
        fileObj.close()

def getAdvancedSettings( group ):
    if group == uidef.kAdvancedSettings_Tool:
        global g_toolCommDict
        return g_toolCommDict
    else:
        pass

def setAdvancedSettings( group, *args ):
    if group == uidef.kAdvancedSettings_Tool:
        global g_toolCommDict
        g_toolCommDict = args[0]
    else:
        pass

def getRuntimeSettings( ):
    global g_hasSubWinBeenOpened
    global g_exeTopRoot
    return g_hasSubWinBeenOpened, g_exeTopRoot

def setRuntimeSettings( *args ):
    global g_hasSubWinBeenOpened
    if args[0] != None:
        g_hasSubWinBeenOpened = args[0]
    try:
        global g_exeTopRoot
        if args[1] != None:
            g_exeTopRoot = args[1]
    except:
        pass
