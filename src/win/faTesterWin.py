# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui\MCU-FATestSuite.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_faTesterWin(object):
    def setupUi(self, faTesterWin):
        faTesterWin.setObjectName("faTesterWin")
        faTesterWin.resize(995, 407)
        self.centralwidget = QtWidgets.QWidget(faTesterWin)
        self.centralwidget.setObjectName("centralwidget")
        self.mcuFrame = QtWidgets.QFrame(self.centralwidget)
        self.mcuFrame.setGeometry(QtCore.QRect(10, 10, 241, 201))
        self.mcuFrame.setAutoFillBackground(False)
        self.mcuFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mcuFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.mcuFrame.setLineWidth(1)
        self.mcuFrame.setObjectName("mcuFrame")
        self.label_mcuDevice = QtWidgets.QLabel(self.mcuFrame)
        self.label_mcuDevice.setGeometry(QtCore.QRect(10, 10, 71, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_mcuDevice.setFont(font)
        self.label_mcuDevice.setObjectName("label_mcuDevice")
        self.comboBox_mcuDevice = QtWidgets.QComboBox(self.mcuFrame)
        self.comboBox_mcuDevice.setGeometry(QtCore.QRect(130, 10, 101, 22))
        self.comboBox_mcuDevice.setObjectName("comboBox_mcuDevice")
        self.comboBox_mcuDevice.addItem("")
        self.label_testCaseLoader = QtWidgets.QLabel(self.mcuFrame)
        self.label_testCaseLoader.setGeometry(QtCore.QRect(10, 40, 111, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_testCaseLoader.setFont(font)
        self.label_testCaseLoader.setObjectName("label_testCaseLoader")
        self.comboBox_testCaseLoader = QtWidgets.QComboBox(self.mcuFrame)
        self.comboBox_testCaseLoader.setGeometry(QtCore.QRect(130, 40, 101, 22))
        self.comboBox_testCaseLoader.setMaxVisibleItems(13)
        self.comboBox_testCaseLoader.setObjectName("comboBox_testCaseLoader")
        self.comboBox_testCaseLoader.addItem("")
        self.comboBox_testCaseLoader.addItem("")
        self.comboBox_testCaseLoader.addItem("")
        self.pushButton_testCaseDetect = QtWidgets.QPushButton(self.mcuFrame)
        self.pushButton_testCaseDetect.setGeometry(QtCore.QRect(50, 80, 141, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_testCaseDetect.setFont(font)
        self.pushButton_testCaseDetect.setObjectName("pushButton_testCaseDetect")
        self.pushButton_testCaseRun = QtWidgets.QPushButton(self.mcuFrame)
        self.pushButton_testCaseRun.setGeometry(QtCore.QRect(50, 120, 141, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_testCaseRun.setFont(font)
        self.pushButton_testCaseRun.setObjectName("pushButton_testCaseRun")
        self.pushButton_clearScreen = QtWidgets.QPushButton(self.mcuFrame)
        self.pushButton_clearScreen.setGeometry(QtCore.QRect(50, 160, 141, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_clearScreen.setFont(font)
        self.pushButton_clearScreen.setObjectName("pushButton_clearScreen")
        self.uartFrame = QtWidgets.QFrame(self.centralwidget)
        self.uartFrame.setGeometry(QtCore.QRect(10, 230, 241, 121))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.uartFrame.setFont(font)
        self.uartFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.uartFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.uartFrame.setObjectName("uartFrame")
        self.label_comPort = QtWidgets.QLabel(self.uartFrame)
        self.label_comPort.setGeometry(QtCore.QRect(30, 20, 61, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(True)
        font.setWeight(75)
        self.label_comPort.setFont(font)
        self.label_comPort.setObjectName("label_comPort")
        self.label_baudrate = QtWidgets.QLabel(self.uartFrame)
        self.label_baudrate.setGeometry(QtCore.QRect(30, 50, 61, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_baudrate.setFont(font)
        self.label_baudrate.setObjectName("label_baudrate")
        self.comboBox_comPort = QtWidgets.QComboBox(self.uartFrame)
        self.comboBox_comPort.setGeometry(QtCore.QRect(100, 20, 111, 22))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.comboBox_comPort.setFont(font)
        self.comboBox_comPort.setObjectName("comboBox_comPort")
        self.comboBox_baudrate = QtWidgets.QComboBox(self.uartFrame)
        self.comboBox_baudrate.setGeometry(QtCore.QRect(100, 50, 111, 22))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.comboBox_baudrate.setFont(font)
        self.comboBox_baudrate.setObjectName("comboBox_baudrate")
        self.comboBox_baudrate.addItem("")
        self.comboBox_baudrate.addItem("")
        self.pushButton_open = QtWidgets.QPushButton(self.uartFrame)
        self.pushButton_open.setGeometry(QtCore.QRect(50, 80, 141, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_open.setFont(font)
        self.pushButton_open.setObjectName("pushButton_open")
        self.resFrame = QtWidgets.QFrame(self.centralwidget)
        self.resFrame.setGeometry(QtCore.QRect(260, 10, 721, 341))
        self.resFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.resFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.resFrame.setObjectName("resFrame")
        self.progressBar_action = QtWidgets.QProgressBar(self.resFrame)
        self.progressBar_action.setGeometry(QtCore.QRect(10, 310, 701, 20))
        self.progressBar_action.setProperty("value", 100)
        self.progressBar_action.setObjectName("progressBar_action")
        self.textEdit_printWin = QtWidgets.QTextEdit(self.resFrame)
        self.textEdit_printWin.setGeometry(QtCore.QRect(10, 230, 701, 71))
        self.textEdit_printWin.setObjectName("textEdit_printWin")
        self.groupBox_testResult = QtWidgets.QGroupBox(self.resFrame)
        self.groupBox_testResult.setGeometry(QtCore.QRect(10, 10, 701, 211))
        self.groupBox_testResult.setObjectName("groupBox_testResult")
        faTesterWin.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(faTesterWin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 995, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        faTesterWin.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(faTesterWin)
        self.statusbar.setObjectName("statusbar")
        faTesterWin.setStatusBar(self.statusbar)
        self.menuHelpAction_homePage = QtWidgets.QAction(faTesterWin)
        self.menuHelpAction_homePage.setObjectName("menuHelpAction_homePage")
        self.menuHelpAction_aboutAuthor = QtWidgets.QAction(faTesterWin)
        self.menuHelpAction_aboutAuthor.setObjectName("menuHelpAction_aboutAuthor")
        self.menuHelpAction_revisionHistory = QtWidgets.QAction(faTesterWin)
        self.menuHelpAction_revisionHistory.setObjectName("menuHelpAction_revisionHistory")
        self.menuHelp.addAction(self.menuHelpAction_homePage)
        self.menuHelp.addAction(self.menuHelpAction_aboutAuthor)
        self.menuHelp.addAction(self.menuHelpAction_revisionHistory)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(faTesterWin)
        self.comboBox_mcuDevice.setCurrentIndex(0)
        self.comboBox_testCaseLoader.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(faTesterWin)

    def retranslateUi(self, faTesterWin):
        _translate = QtCore.QCoreApplication.translate
        faTesterWin.setWindowTitle(_translate("faTesterWin", "MCU FA Test Suite"))
        self.label_mcuDevice.setText(_translate("faTesterWin", "MCU Device:"))
        self.comboBox_mcuDevice.setCurrentText(_translate("faTesterWin", "i.MXRT7xx"))
        self.comboBox_mcuDevice.setItemText(0, _translate("faTesterWin", "i.MXRT7xx"))
        self.label_testCaseLoader.setText(_translate("faTesterWin", "Test Case Loader:"))
        self.comboBox_testCaseLoader.setItemText(0, _translate("faTesterWin", "J-Link SWD"))
        self.comboBox_testCaseLoader.setItemText(1, _translate("faTesterWin", "MCU-Link SWD"))
        self.comboBox_testCaseLoader.setItemText(2, _translate("faTesterWin", "ROM UART ISP"))
        self.pushButton_testCaseDetect.setText(_translate("faTesterWin", "Test Case Detect"))
        self.pushButton_testCaseRun.setText(_translate("faTesterWin", "Test Case Run"))
        self.pushButton_clearScreen.setText(_translate("faTesterWin", "Clear Screen"))
        self.label_comPort.setText(_translate("faTesterWin", "COM Port:"))
        self.label_baudrate.setText(_translate("faTesterWin", "Baudrate:"))
        self.comboBox_baudrate.setItemText(0, _translate("faTesterWin", "57600"))
        self.comboBox_baudrate.setItemText(1, _translate("faTesterWin", "115200"))
        self.pushButton_open.setText(_translate("faTesterWin", "Open"))
        self.groupBox_testResult.setTitle(_translate("faTesterWin", "Test Result"))
        self.menuFile.setTitle(_translate("faTesterWin", "File"))
        self.menuEdit.setTitle(_translate("faTesterWin", "Edit"))
        self.menuView.setTitle(_translate("faTesterWin", "View"))
        self.menuTools.setTitle(_translate("faTesterWin", "Tools"))
        self.menuWindow.setTitle(_translate("faTesterWin", "Window"))
        self.menuHelp.setTitle(_translate("faTesterWin", "Help"))
        self.menuHelpAction_homePage.setText(_translate("faTesterWin", "Home Page"))
        self.menuHelpAction_aboutAuthor.setText(_translate("faTesterWin", "About Author"))
        self.menuHelpAction_revisionHistory.setText(_translate("faTesterWin", "Revision History"))
