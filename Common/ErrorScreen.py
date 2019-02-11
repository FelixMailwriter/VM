# -*- coding:utf-8 -*-
import os
from PyQt4 import QtCore, uic, QtGui
from PyQt4.Qt import QObject
import Common.Settings as Settings

class ErrorScreen(QObject):

    def __init__(self, message, closeIdle=5000):
        QObject.__init__(self)
        path = os.path.abspath("UIForms/errorWindow.ui")
        self.window = uic.loadUi(path)
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        desktop = QtGui.QApplication.desktop()
        self.window.move(desktop.availableGeometry().center()-self.window.rect().center())
        
        global _
        _ = Settings._
        
        self.window.btn_close.clicked.connect(self._closeWindow)
        self.window.label.setText(message)
        self.window.btn_close.setText(_(u'Close'))
        
        QtCore.QTimer.singleShot(closeIdle, self._closeWindow)
        
    def setMessageText(self, message):
        self.window.label.setText(message)
    
    def setWindowTitle(self, title):
        self.window.setWindowTitle(title)  
        
    def _closeWindow(self):
        self.emit(QtCore.SIGNAL('ErrorWindowClosing'))
        self.window.close()  