# -*- coding:utf-8 -*-
import os
from PyQt4 import uic
from PyQt4.Qt import QObject
import gettext

class Errors(QObject):

    def __init__(self, message):
        QObject.__init__(self)
        path=os.path.abspath("UIForms/errorWindow.ui")
        self.window=uic.loadUi(path)
        self.window.btn_close.clicked.connect(self.window.close)
        self.window.label.setText(message)
        self.window.btn_close.setText(_(u'Close'))
        
    def setMessageText(self, message):
        self.window.label.setText(message)
    
    def setWindowTitle(self, title):
        self.window.setWindowTitle(title)    