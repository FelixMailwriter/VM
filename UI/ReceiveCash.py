# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject
from PyQt4 import QtCore, uic
#from KP.KPProvider import KPProvider
from KP.KPManager import KPManager
from Printer.PrnDK350 import Printer, PrinterHardwareException
import Common.Settings as Settings
from PyQt4.QtCore import QTimer
from Common.Logs import LogEvent


class ReceiveCash(QObject):
    '''
    Оплата предмета и выдача чека.
    '''
    def __init__(self, payment, item, dbProvider):
        QObject.__init__(self)
        self.kpManager=KPManager(self)
        self.payment=payment
        self.item=item
        self.dbProvider=dbProvider
        path=os.path.abspath("UIForms//ReceiveCash.ui")      
        self.receiveCashWindow = uic.loadUi(path)
        
        self.timer=QTimer()                                                     #Таймер возврата на титульную страницу
        self.timer.timeout.connect(self._backToTitlePage)
        self.timer.start(60000)
        
        global _
        _= Settings._
        
        self.receiveCashWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.receiveCashWindow.btnContinue.setEnabled(self.item.price<self.payment)
        self.receiveCashWindow.lbl_summa.setText("%s" %(self.payment))
        self.connect(self.receiveCashWindow.btnPay, QtCore.SIGNAL("clicked()"), self.enableKP)
        self.connect(self.receiveCashWindow.btnCancel, QtCore.SIGNAL("clicked()"), self.cancelOperation)
        self.connect(self.receiveCashWindow.btnContinue, QtCore.SIGNAL("clicked()"), self.continueOperation)
        self.connect(self.kpManager, QtCore.SIGNAL("Note stacked"), self.increasePayment)
        #self.connect(self.kpManager, QtCore.SIGNAL('ReceiveMoneyTimeout'), self._exitPayment)
        self._setLabels()
                         
        if (self.payment>=self.item.price):
            self.receiveCashWindow.btnContinue.setEnabled(True)
               
    def _setLabels(self):
        self.receiveCashWindow.lbl1.setText(_(u'Incomming cash'))
        self.receiveCashWindow.btnPay.setText(_(u'Pay'))
        self.receiveCashWindow.lbl_msgNoPayOut.setText(_(u'Mashine does not give any odd money'))
        self.receiveCashWindow.btnCancel.setText(_(u'Cancel'))
        self.receiveCashWindow.btnContinue.setText(_(u'Next'))
        
        self.receiveCashWindow.labelItem.setPixmap(self.item.icon)
        self.receiveCashWindow.labelPrice.setText("%s" %(int(self.item.price)))
        if self.payment==0:
            paymentText="0"
        else:
            paymentText="%s" %(int(self.payment))
        self.receiveCashWindow.lbl_summa.setText(paymentText)       
        
    def enableKP(self):
        self.receiveCashWindow.btnPay.setEnabled(False)
        self.kpManager.start()
            
    def increasePayment(self, summa):
        self.timer.start(60000)
        self.payment+=summa
        self.dbProvider.writeBanknote(summa)
        self.emit(QtCore.SIGNAL('PaymentChange'), self.payment)
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
        self.timer.stop()
        try:
            #self._printCheck()
            t=0
        except PrinterHardwareException as e:
            events=[]
            log=LogEvent()
            log.sourse='Printer'
            log.priority='Hight'
            log.message='Printer is not ready'
            events.append(log)
            self.dbProvider.writeLog(events)
        finally:            
            self.emit(QtCore.SIGNAL("GiveOutItem"), self.item)
        
    def _printCheck(self):
        check=[]
        if self.payment==0:
            return
        overpay=self.payment-self.item.price
        if overpay>0:
            rec=dict(Text=self.item.name, Price=self.item.price, TaxCode='A')
            check.append(rec)
            rec=dict(Text='Alte venituri', Price=overpay, TaxCode='A')
            check.append(rec)
        elif overpay<0:
            self.item.name='Error in payment for '+self.item.name
            rec=dict(Text=self.item.name, Price=self.payment, TaxCode='A')
            check.append(rec)
        else:
            rec=dict(Text=self.item.name, Price=self.payment, TaxCode='A')
            check.append(rec)                     
        
        printer=Printer()
        logMessages=printer.checkStatus()
        self.dbProvider.writeLog(logMessages)
        printer.run(check, 'Fisk')
   
    def _backToTitlePage(self):
        self.timer.stop()
        self.emit(QtCore.SIGNAL("KPStop"))                            #Останов купюроприемника
        #self._printCheck()
        self.emit(QtCore.SIGNAL("TimeOutPage"), self.receiveCashWindow) 
                
    def _exitPayment(self):
        if self.payment==0:
            return
        self.item.name='Error in payment for '+self.item.name
        self.item.price=self.payment
        #self._printCheck()

        

    
        