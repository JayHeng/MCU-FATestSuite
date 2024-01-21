# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class faTesterWin
###########################################################################

class faTesterWin ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"MCU FA Test Suite", pos = wx.DefaultPosition, size = wx.Size( 861,520 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        self.m_menubar = wx.MenuBar( 0 )
        self.m_menu_file = wx.Menu()
        self.m_menuItem_exit = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_file.Append( self.m_menuItem_exit )

        self.m_menubar.Append( self.m_menu_file, u"File" )

        self.m_menu_edit = wx.Menu()
        self.m_menubar.Append( self.m_menu_edit, u"Edit" )

        self.m_menu_view = wx.Menu()
        self.m_menubar.Append( self.m_menu_view, u"View" )

        self.m_menu_tools = wx.Menu()
        self.m_menubar.Append( self.m_menu_tools, u"Tools" )

        self.m_menu_window = wx.Menu()
        self.m_menubar.Append( self.m_menu_window, u"Window" )

        self.m_menu_help = wx.Menu()
        self.m_menuItem_homePage = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"Home Page", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_help.Append( self.m_menuItem_homePage )

        self.m_menuItem_aboutAuthor = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"About Author", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_help.Append( self.m_menuItem_aboutAuthor )

        self.m_menuItem_revisionHistory = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"Revision History", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_help.Append( self.m_menuItem_revisionHistory )

        self.m_menubar.Append( self.m_menu_help, u"Help" )

        self.SetMenuBar( self.m_menubar )

        bSizer_win = wx.BoxSizer( wx.VERTICAL )

        wSizer_func = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        bSizer_setup = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook_targetSetup = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_panel_targetSetup = wx.Panel( self.m_notebook_targetSetup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        wSizer_targetSetup = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_staticText_mcuDevice = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, u"MCU Device:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
        self.m_staticText_mcuDevice.Wrap( -1 )

        wSizer_targetSetup.Add( self.m_staticText_mcuDevice, 0, wx.ALL, 5 )

        m_choice_mcuDeviceChoices = [ u"i.MXRT7xx" ]
        self.m_choice_mcuDevice = wx.Choice( self.m_panel_targetSetup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), m_choice_mcuDeviceChoices, 0 )
        self.m_choice_mcuDevice.SetSelection( 0 )
        wSizer_targetSetup.Add( self.m_choice_mcuDevice, 0, wx.ALL, 5 )

        self.m_staticText_mcuBoard = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, u"MCU Board:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
        self.m_staticText_mcuBoard.Wrap( -1 )

        wSizer_targetSetup.Add( self.m_staticText_mcuBoard, 0, wx.ALL, 5 )

        m_choice_mcuBoardChoices = [ u"FOWLP324-EVK_Rev.A" ]
        self.m_choice_mcuBoard = wx.Choice( self.m_panel_targetSetup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), m_choice_mcuBoardChoices, 0 )
        self.m_choice_mcuBoard.SetSelection( 0 )
        wSizer_targetSetup.Add( self.m_choice_mcuBoard, 0, wx.ALL, 5 )

        self.m_staticText_testLoader = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, u"Test Loader:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
        self.m_staticText_testLoader.Wrap( -1 )

        wSizer_targetSetup.Add( self.m_staticText_testLoader, 0, wx.ALL, 5 )

        m_choice_testLoaderChoices = [ u"J-Link SWD", u"MCU-Link SWD", u"ROM UART ISP" ]
        self.m_choice_testLoader = wx.Choice( self.m_panel_targetSetup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ), m_choice_testLoaderChoices, 0 )
        self.m_choice_testLoader.SetSelection( 0 )
        wSizer_targetSetup.Add( self.m_choice_testLoader, 0, wx.ALL, 5 )

        self.m_filePicker_setLoaderExe = wx.FilePickerCtrl( self.m_panel_targetSetup, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 236,-1 ), wx.FLP_DEFAULT_STYLE )
        wSizer_targetSetup.Add( self.m_filePicker_setLoaderExe, 0, wx.ALL, 5 )

        self.m_staticText_null0Setup = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0 )
        self.m_staticText_null0Setup.Wrap( -1 )

        wSizer_targetSetup.Add( self.m_staticText_null0Setup, 0, wx.ALL, 5 )

        self.m_button_detectTestCases = wx.Button( self.m_panel_targetSetup, wx.ID_ANY, u"Detect Test Cases", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        wSizer_targetSetup.Add( self.m_button_detectTestCases, 0, wx.ALL, 5 )

        self.m_staticText_null1Setup = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,-1 ), 0 )
        self.m_staticText_null1Setup.Wrap( -1 )

        wSizer_targetSetup.Add( self.m_staticText_null1Setup, 0, wx.ALL, 5 )

        self.m_staticText_null2Setup = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0 )
        self.m_staticText_null2Setup.Wrap( -1 )

        wSizer_targetSetup.Add( self.m_staticText_null2Setup, 0, wx.ALL, 5 )

        self.m_button_runTestCases = wx.Button( self.m_panel_targetSetup, wx.ID_ANY, u"Run Test Cases", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        wSizer_targetSetup.Add( self.m_button_runTestCases, 0, wx.ALL, 5 )

        self.m_staticText_null3Setup = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 20,-1 ), 0 )
        self.m_staticText_null3Setup.Wrap( -1 )

        wSizer_targetSetup.Add( self.m_staticText_null3Setup, 0, wx.ALL, 5 )

        self.m_staticText_null4Setup = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0 )
        self.m_staticText_null4Setup.Wrap( -1 )

        wSizer_targetSetup.Add( self.m_staticText_null4Setup, 0, wx.ALL, 5 )

        self.m_button_resetTestResult = wx.Button( self.m_panel_targetSetup, wx.ID_ANY, u"Reset Test Result", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        wSizer_targetSetup.Add( self.m_button_resetTestResult, 0, wx.ALL, 5 )

        self.m_staticText_null5Setup = wx.StaticText( self.m_panel_targetSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 240,1 ), 0 )
        self.m_staticText_null5Setup.Wrap( -1 )

        wSizer_targetSetup.Add( self.m_staticText_null5Setup, 0, wx.ALL, 5 )


        self.m_panel_targetSetup.SetSizer( wSizer_targetSetup )
        self.m_panel_targetSetup.Layout()
        wSizer_targetSetup.Fit( self.m_panel_targetSetup )
        self.m_notebook_targetSetup.AddPage( self.m_panel_targetSetup, u"Target Setup", False )

        bSizer_setup.Add( self.m_notebook_targetSetup, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_notebook_portSetup = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_panel_portSetup = wx.Panel( self.m_notebook_portSetup, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        wSizer_portSetup = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_staticText_null0Setup = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 23,1 ), 0 )
        self.m_staticText_null0Setup.Wrap( -1 )

        wSizer_portSetup.Add( self.m_staticText_null0Setup, 0, wx.ALL, 5 )

        self.m_staticText_comPort = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, u"COM Port:", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
        self.m_staticText_comPort.Wrap( -1 )

        wSizer_portSetup.Add( self.m_staticText_comPort, 0, wx.ALL, 5 )

        m_choice_comPortChoices = []
        self.m_choice_comPort = wx.Choice( self.m_panel_portSetup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_choice_comPortChoices, 0 )
        self.m_choice_comPort.SetSelection( 0 )
        wSizer_portSetup.Add( self.m_choice_comPort, 0, wx.ALL, 5 )

        self.m_staticText_null1Setup = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 15,1 ), 0 )
        self.m_staticText_null1Setup.Wrap( -1 )

        wSizer_portSetup.Add( self.m_staticText_null1Setup, 0, wx.ALL, 5 )

        self.m_staticText_null2Setup = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 23,1 ), 0 )
        self.m_staticText_null2Setup.Wrap( -1 )

        wSizer_portSetup.Add( self.m_staticText_null2Setup, 0, wx.ALL, 5 )

        self.m_staticText_baudrate = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, u"Baudrate:", wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
        self.m_staticText_baudrate.Wrap( -1 )

        wSizer_portSetup.Add( self.m_staticText_baudrate, 0, wx.ALL, 5 )

        m_choice_baudrateChoices = [ u"57600", u"115200" ]
        self.m_choice_baudrate = wx.Choice( self.m_panel_portSetup, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_choice_baudrateChoices, 0 )
        self.m_choice_baudrate.SetSelection( 1 )
        wSizer_portSetup.Add( self.m_choice_baudrate, 0, wx.ALL, 5 )

        self.m_staticText_null3Setup = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0 )
        self.m_staticText_null3Setup.Wrap( -1 )

        wSizer_portSetup.Add( self.m_staticText_null3Setup, 0, wx.ALL, 5 )

        self.m_button_open = wx.Button( self.m_panel_portSetup, wx.ID_ANY, u"Open", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        wSizer_portSetup.Add( self.m_button_open, 0, wx.ALL, 5 )

        self.m_staticText_null4Setup = wx.StaticText( self.m_panel_portSetup, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 240,1 ), 0 )
        self.m_staticText_null4Setup.Wrap( -1 )

        wSizer_portSetup.Add( self.m_staticText_null4Setup, 0, wx.ALL, 5 )


        self.m_panel_portSetup.SetSizer( wSizer_portSetup )
        self.m_panel_portSetup.Layout()
        wSizer_portSetup.Fit( self.m_panel_portSetup )
        self.m_notebook_portSetup.AddPage( self.m_panel_portSetup, u"Port Setup", False )

        bSizer_setup.Add( self.m_notebook_portSetup, 1, wx.EXPAND |wx.ALL, 5 )


        wSizer_func.Add( bSizer_setup, 1, wx.EXPAND, 5 )

        bSizer_testResult = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook_testResult = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_panel_testResult = wx.Panel( self.m_notebook_testResult, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        wSizer_testResult = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_textCtrl_resWin = wx.TextCtrl( self.m_panel_testResult, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,390 ), wx.TE_MULTILINE|wx.TE_RICH2 )
        wSizer_testResult.Add( self.m_textCtrl_resWin, 0, wx.ALL, 5 )


        self.m_panel_testResult.SetSizer( wSizer_testResult )
        self.m_panel_testResult.Layout()
        wSizer_testResult.Fit( self.m_panel_testResult )
        self.m_notebook_testResult.AddPage( self.m_panel_testResult, u"Case Test Result", False )

        bSizer_testResult.Add( self.m_notebook_testResult, 1, wx.EXPAND |wx.ALL, 5 )


        wSizer_func.Add( bSizer_testResult, 1, wx.EXPAND, 5 )

        bSizer_recvLog = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook_recvLog = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_panel_recvLog = wx.Panel( self.m_notebook_recvLog, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        wSizer_recvLog = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_textCtrl_printWin = wx.TextCtrl( self.m_panel_recvLog, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 220,390 ), wx.TE_MULTILINE|wx.TE_RICH2 )
        wSizer_recvLog.Add( self.m_textCtrl_printWin, 0, wx.ALL, 5 )


        self.m_panel_recvLog.SetSizer( wSizer_recvLog )
        self.m_panel_recvLog.Layout()
        wSizer_recvLog.Fit( self.m_panel_recvLog )
        self.m_notebook_recvLog.AddPage( self.m_panel_recvLog, u"Recv Log from COM Port", False )

        bSizer_recvLog.Add( self.m_notebook_recvLog, 1, wx.EXPAND |wx.ALL, 5 )


        wSizer_func.Add( bSizer_recvLog, 1, wx.EXPAND, 5 )


        bSizer_win.Add( wSizer_func, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer_win )
        self.Layout()
        self.m_statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.callbackClose )
        self.Bind( wx.EVT_MENU, self.callbackExit, id = self.m_menuItem_exit.GetId() )
        self.Bind( wx.EVT_MENU, self.callbackShowHomePage, id = self.m_menuItem_homePage.GetId() )
        self.Bind( wx.EVT_MENU, self.callbackShowAboutAuthor, id = self.m_menuItem_aboutAuthor.GetId() )
        self.Bind( wx.EVT_MENU, self.callbackShowRevisionHistory, id = self.m_menuItem_revisionHistory.GetId() )
        self.m_choice_mcuDevice.Bind( wx.EVT_CHOICE, self.callbackSetMcuDevice )
        self.m_choice_mcuBoard.Bind( wx.EVT_CHOICE, self.callbackSetMcuBoard )
        self.m_choice_testLoader.Bind( wx.EVT_CHOICE, self.callbackSetTestLoader )
        self.m_filePicker_setLoaderExe.Bind( wx.EVT_FILEPICKER_CHANGED, self.callbackSetLoaderExe )
        self.m_button_detectTestCases.Bind( wx.EVT_BUTTON, self.callbackDetectTestCases )
        self.m_button_runTestCases.Bind( wx.EVT_BUTTON, self.callbackRunTestCases )
        self.m_button_resetTestResult.Bind( wx.EVT_BUTTON, self.callbackResetTestResult )
        self.m_button_open.Bind( wx.EVT_BUTTON, self.callbackOpenUart )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def callbackClose( self, event ):
        event.Skip()

    def callbackExit( self, event ):
        event.Skip()

    def callbackShowHomePage( self, event ):
        event.Skip()

    def callbackShowAboutAuthor( self, event ):
        event.Skip()

    def callbackShowRevisionHistory( self, event ):
        event.Skip()

    def callbackSetMcuDevice( self, event ):
        event.Skip()

    def callbackSetMcuBoard( self, event ):
        event.Skip()

    def callbackSetTestLoader( self, event ):
        event.Skip()

    def callbackSetLoaderExe( self, event ):
        event.Skip()

    def callbackDetectTestCases( self, event ):
        event.Skip()

    def callbackRunTestCases( self, event ):
        event.Skip()

    def callbackResetTestResult( self, event ):
        event.Skip()

    def callbackOpenUart( self, event ):
        event.Skip()


