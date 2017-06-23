# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject
from PyQt4 import QtCore, uic, QtGui
import Common.Settings as Settings
from Errors import Errors

class GivingOutItem(QObject):
    '''
    Класс описывает окно выдачи предмета
    '''
    def __init__(self):
        QObject.__init__(self)
        path=os.path.abspath("UIForms//GivingOutItem.ui")
        self.givingOutWindow = uic.loadUi(path)
        self.givingOutWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        desktop=QtGui.QApplication.desktop()
        self.givingOutWindow.move(desktop.availableGeometry().center()-self.givingOutWindow.rect().center())
        
        global _
        _= Settings._
        
        self.connect(self.givingOutWindow.btn_OutSensSim, QtCore.SIGNAL("clicked()"), self.outSensClick)  #test remove
        self.givingOutWindow.lbl_msg.setText(_(u"Wait for delivery..."))
    
    
    def fail(self):
        self.errWindow=Errors(u"Delivery error. Call techsupport, please.")
        self.connect(self.errWindow, QtCore.SIGNAL('ErrorWindowClosing'), self._backToTitlePage)
        self.errWindow.window.show()
        self.givingOutWindow.hide()

    def _backToTitlePage(self):
        self.emit(QtCore.SIGNAL("TimeOutPage"), self.givingOutWindow)        
        
     
# ================ test ======================   
    
    def outSensClick(self):
        self.emit(QtCore.SIGNAL("OutSensorClick"))