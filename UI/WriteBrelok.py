# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject
from PyQt4 import QtCore, uic

class WriteBrelok(QObject):
    '''
    Класс описывает окно записи брелка
    '''


    def __init__(self):
        QObject.__init__(self)
        path=os.path.abspath("UIForms//WriteBrelok.ui")
        self.window = uic.loadUi(path)
        self.window.lbl_write.hide()
        self.window.lbl_fail.hide()
        self.connect(self.window.btn_write, QtCore.SIGNAL("clicked()"), self.writeHandler)
        self.connect(self.window.btn_simWriteOk, QtCore.SIGNAL("clicked()"), self.writeOKHandler) #Test
        
    def writeHandler(self):
        self.window.btn_write.setEnabled(False)
        self.window.label.hide()
        self.window.label_2.hide()
        self.window.lbl_write.show()
        self.window.lbl_fail.hide()
        self.emit(QtCore.SIGNAL("WriteBrelok"))

    def writeFail(self):
        self.window.label.show()
        self.window.label_2.show()
        self.window.lbl_write.hide()
        self.window.lbl_fail.show()
        QtCore.QTimer.singleShot(2000, self.refresh)

    def refresh(self):
        self.window.label.show()
        self.window.label_2.show()
        self.window.lbl_write.hide()
        self.window.lbl_fail.hide()
        self.window.btn_write.setEnabled(True)

#=====TEST=====
    
    def writeOKHandler(self):
        self.emit(QtCore.SIGNAL("SimulateWriteOK"))
        
        
