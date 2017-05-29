# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject
from PyQt4 import QtCore, uic
from PyQt4.QtGui import QPixmap
from PyQt4.QtCore import QTimer
import Common.Settings as Settings

class GivingOutItem(QObject):
    '''
    Класс описывает окно выдачи предмета
    '''
    def __init__(self):
        QObject.__init__(self)
        path=os.path.abspath("UIForms//GivingOutItem.ui")
        self.givingOutWindow = uic.loadUi(path)
        self.givingOutWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.givingOutWindow.btn_continue.setEnabled(False)
        
        self.timer=QTimer()                                                     #Таймер возврата на титульную страницу
        self.timer.timeout.connect(self._backToTitlePage)
        self.timer.start(30000)
        
        global _
        _= Settings._
        
        #self.connect(self.givingOutWindow.btn_EngSensSim, QtCore.SIGNAL("clicked()"), self.engSensClick) #test remove
        self.connect(self.givingOutWindow.btn_OutSensSim, QtCore.SIGNAL("clicked()"), self.outSensClick)  #test remove
        self.givingOutWindow.lbl_msg.setText(_(u"Wait for delivery..."))
        label=QPixmap('./Resources/Forms/ScanBrelok/Success.png')
        self.givingOutWindow.lbl_result.setPixmap(label)
    
    
    def fail(self):
        self.givingOutWindow.lbl_msg.setText(_(u"Delivery error. Call techsupport, please."))
        label=QPixmap('./Resources/Forms/ScanBrelok/Failure.png')
        self.givingOutWindow.lbl_result.setPixmap(label)
        self.timer=QTimer()
        self.timer.timeout.connect(self._backToTitlePage)
        self.timer.start(5000)

    def _backToTitlePage(self):
        self.timer.stop()
        self.emit(QtCore.SIGNAL("TimeOutPage"), self.givingOutWindow)        
        
     
# ================ test ======================   
    def engSensClick(self):
        self.emit(QtCore.SIGNAL("EngSendClick"))
    
    def outSensClick(self):
        self.emit(QtCore.SIGNAL("OutSensorClick"))