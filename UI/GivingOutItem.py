# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject
from PyQt4 import QtCore, uic

class GivingOutItem(QObject):
    '''
    Класс описывает окно выдачи предмета
    '''
    def __init__(self):
        QObject.__init__(self)
        path=os.path.abspath("UIForms//GivingOutItem.ui")
        self.givingOutWindow = uic.loadUi(path)
        self.givingOutWindow.btn_continue.setEnabled(False)
        #self.connect(self.givingOutWindow.btn_EngSensSim, QtCore.SIGNAL("clicked()"), self.engSensClick) #test remove
        self.connect(self.givingOutWindow.btn_EngSensSim, QtCore.SIGNAL("clicked()"), self.outSensClick)  #test remove
        self.givingOutWindow.lbl_msg.setText(u"Ожидайте выдачи...")
    
    
    def fail(self):
        self.givingOutWindow.lbl_msg.setText(u"Ошибка выдачи. Обратитесь в техподдержку.")
        QtCore.QTimer.singleShot(5000, self.givingOutWindow, QtCore.SLOT("close()"))
        
        
     
# ================ test ======================   
    def engSensClick(self):
        self.emit(QtCore.SIGNAL("EngSendClick"))
    
    def outSensClick(self):
        self.emit(QtCore.SIGNAL("OutSensorClick"))