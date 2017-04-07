# -*- coding:utf-8 -*-
from PyQt4 import QtCore
from KP.KPProvider import KPProvider

class KPManager(QtCore.QThread):


    def __init__(self, receiveCashObj):
        QtCore.QThread.__init__(self)
        
        self.kp=KPProvider()
        self.receiveCashObj=receiveCashObj
        self.connect(self.receiveCashObj, QtCore.SIGNAL("KPStop"), self.stop)
        self.connect(self.kp, QtCore.SIGNAL("Note stacked"), self.enterCash)
        self.connect(self.kp, QtCore.SIGNAL('ReceiveMoneyTimeout'), self.moneyTimeOut)
        
    def run(self):
        self.kp.receiveNote()
        
    def enterCash(self, summa):
        self.emit(QtCore.SIGNAL("Note stacked"), summa)
            
    def stop(self):
        print 'Command STOP sent to the KP'
        self.kp.disable()
        
    def moneyTimeOut(self):
        self.emit(QtCore.SIGNAL('ReceiveMoneyTimeout'))    