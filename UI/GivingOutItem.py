# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject
from PyQt4 import QtCore, uic
from PyQt4.QtGui import QPixmap
import gettext

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
        self.connect(self.givingOutWindow.btn_OutSensSim, QtCore.SIGNAL("clicked()"), self.outSensClick)  #test remove
        self.givingOutWindow.lbl_msg.setText(_(u"Wait for delivery..."))
        label=QPixmap('../Resources/Forms/ScanBrelok/Success.png')
        self.givingOutWindow.lbl_result.setPixmap(label)
    
    
    def fail(self):
        self.givingOutWindow.lbl_msg.setText(_(u"Delivery error. Call techsupport, please."))
        label=QPixmap('../Resources/Forms/ScanBrelok/Failure.png')
        self.givingOutWindow.lbl_result.setPixmap(label)
        QtCore.QTimer.singleShot(5000, self.givingOutWindow, QtCore.SLOT("close()"))
        
        
     
# ================ test ======================   
    def engSensClick(self):
        self.emit(QtCore.SIGNAL("EngSendClick"))
    
    def outSensClick(self):
        self.emit(QtCore.SIGNAL("OutSensorClick"))