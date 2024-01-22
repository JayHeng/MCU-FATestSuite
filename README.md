# MCU-FATestSuite
A flexible FAT tool based on Python3.7+PyQt5.15, it can do flexible FA tests for NXP MCU (i.MXRT...) | 恩智浦MCU板卡出厂验收测试(FAT)一站式工具 

### 待解决问题

当在工作者线程里(thread) 调用 QT textEdit 控件的 append() 方法更新显示控件时会提示如下错误，并且程序运行可能会闪退

```
QObject::connect: Cannot queue arguments of type 'QTextCursor'
(Make sure 'QTextCursor' is registered using qRegisterMetaType().)
```
