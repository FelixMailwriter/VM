# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject
from PyQt4 import QtCore, uic

class FinishWindow(QObject):

    '''
    Класс описывает финальное окно приложения
    '''


    def __init__(self):
        QObject.__init__(self)
        path=os.path.abspath("UIForms//FinishWindow.ui")
        self.window = uic.loadUi(path)
        QtCore.QTimer.singleShot(5000, self.finish)
        
    def finish(self):
        self.window.close()
        self.emit(QtCore.SIGNAL("FinishProc"))
        