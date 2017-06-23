# -*- coding:utf-8 -*-
import os
from PyQt4 import QtCore, uic
from PyQt4.Qt import QObject
import Common.Settings as Settings

class Errors(QObject):

    def __init__(self, message, closeIdle=5000):
        QObject.__init__(self)
        path=os.path.abspath("UIForms/errorWindow.ui")
        self.window=uic.loadUi(path)
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        global _
        _= Settings._
        
        self.window.btn_close.clicked.connect(self.window.close)
        self.window.label.setText(message)
        self.window.btn_close.setText(_(u'Close'))
        
        QtCore.QTimer.singleShot(closeIdle, self.window.close)
        
    def setMessageText(self, message):
        self.window.label.setText(message)
    
    def setWindowTitle(self, title):
        self.window.setWindowTitle(title)    