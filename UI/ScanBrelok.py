# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject
from PyQt4 import QtCore, uic

class ScanBrelok(QObject):
    '''
    Класс описывает окно сканирования брелка клиента
    '''


    def __init__(self):
        path=os.path.abspath("UIForms//ScanBrelok.ui")
        QObject.__init__(self)
        self.window = uic.loadUi(path)
        self.window.lbl_fail.hide()
        self.window.lbl_scan.hide()
        self.connect(self.window.btn_scan, QtCore.SIGNAL("clicked()"), self.scanHandler)
        self.connect(self.window.btn_ScanOK, QtCore.SIGNAL("clicked()"), self.scanOKHandler) #Test
                        
    def scanHandler(self):
        self.window.btn_scan.setEnabled(False)
        self.window.label.hide()
        self.window.label_2.hide()
        self.window.lbl_scan.show()
        self.window.lbl_fail.hide()
        self.emit(QtCore.SIGNAL("ScanBrelok"))
         
    
    def scanFail(self):
        self.window.label.show()
        self.window.label_2.show()
        self.window.lbl_scan.hide()
        self.window.lbl_fail.show()
        QtCore.QTimer.singleShot(2000, self.refresh)

    def refresh(self):
        self.window.label.show()
        self.window.label_2.show()
        self.window.lbl_scan.hide()
        self.window.lbl_fail.hide()
        self.window.btn_scan.setEnabled(True)    
        
    #======TEST======
    def scanOKHandler(self):
        self.emit(QtCore.SIGNAL("SimulateScanOK"))    