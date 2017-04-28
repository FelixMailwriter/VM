# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject
from PyQt4 import QtCore, QtGui, uic
#from KP.KPProvider import KPProvider
from KP.KPManager import KPManager
from Printer.PrnDK350 import Printer 

class ReceiveCash(QObject):
    '''
    Оплата предмета и выдача чека.
    '''
    def __init__(self, payment, item):
        QObject.__init__(self)
        #self.kp=KPProvider()
        self.kpManager=KPManager(self)
        self.payment=payment
        self.item=item
        path=os.path.abspath("UIForms//ReceiveCash.ui")       
        self.receiveCashWindow = uic.loadUi(path)
        self.receiveCashWindow.btnContinue.setEnabled(self.item.price<self.payment)
        self.receiveCashWindow.lbl_summa.setText("%s" %(self.payment))
        self.connect(self.receiveCashWindow.btnPay, QtCore.SIGNAL("clicked()"), self.enableKP)
        self.connect(self.receiveCashWindow.btnCancel, QtCore.SIGNAL("clicked()"), self.cancelOperation)
        self.connect(self.receiveCashWindow.btnContinue, QtCore.SIGNAL("clicked()"), self.continueOperation)
        self.connect(self.kpManager, QtCore.SIGNAL("Note stacked"), self.increasePayment)
        self.connect(self.kpManager, QtCore.SIGNAL('ReceiveMoneyTimeout'), self._exitPayment)
        self.paintForm()
        if (self.payment>=self.item.price):
            self.receiveCashWindow.btnContinue.setEnabled(True)
               
    
    def paintForm(self):
        #self.receiveCashWindow.labelItem.setPixmap(QtGui.QPixmap(self.item.img))
        self.receiveCashWindow.labelItem.setPixmap(self.item.icon)
        self.receiveCashWindow.labelPrice.setText("%s" %(self.item.price))
        if self.payment==0:
            paymentText=""
        else:
            paymentText="%s" %(self.payment)
        self.receiveCashWindow.lbl_summa.setText(paymentText)
 
    def enableKP(self):
        self.receiveCashWindow.btnPay.setEnabled(False)
        self.kpManager.start()
            
    def increasePayment(self, summa):
        self.payment+=summa
        #Вставить процедуру записи лога в БД
        self.receiveCashWindow.lbl_summa.setText("%s" %(self.payment))
        if (self.payment>=self.item.price):
            self.receiveCashWindow.btnContinue.setEnabled(True)
            self.emit(QtCore.SIGNAL("KPStop"))                        #Останов купюроприемника
        else:
            self.receiveCashWindow.btnContinue.setEnabled(False)

              
    def cancelOperation(self):
        self.emit(QtCore.SIGNAL("PaymentCancelled"), self.payment)
        self.receiveCashWindow.close()
        self.emit(QtCore.SIGNAL("KPStop"))                            #Останов купюроприемника
        
    def continueOperation(self):
        self.emit(QtCore.SIGNAL("GiveOutItem"), self.item)
        self._printCheck()
        
    def _printCheck(self):
        check=[]
        rec=dict(Text=self.item.name, Price=self.item.price, TaxCode='A')
        check.append(rec)
        overpay=self.payment-self.item.price
        if overpay>0:
            rec=dict(Text='Alte venituri', Price=overpay, TaxCode='A')
            check.append(rec)            
        prn=Printer.printCheck(check)
        prn.run()
        
    def _exitPayment(self):
        self.emit(QtCore.SIGNAL('ReceiveMoneyTimeout'))
        
    
    
        