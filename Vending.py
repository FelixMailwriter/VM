# -*- coding:utf-8 -*-
from PyQt4.Qt import QObject
from PyQt4 import QtCore
import HdWareCon.RB as RB
from UI.ScanBrelok import ScanBrelok
from UI.WriteBrelok import WriteBrelok
from UI.FinishWindow import FinishWindow
from UI.ChoosingItem import ChoosingItemWindow
from UI.ReceiveCash import ReceiveCash
from UI.GivingOutItem import GivingOutItem


class Vending(QObject):
    '''
    Класс приложения
    '''

    def __init__(self, payment):
        QObject.__init__(self)
        self.rb=RB.RB()                                                                     # Экземпляр Raspberry
        self.connect(self.rb, QtCore.SIGNAL("ScanFinished"), self.scanFinishHandler)
        self.connect(self.rb, QtCore.SIGNAL("WriteFinished"), self.writeFinishHandler)
        self.item=None  
        self.payment=payment                                                                # Сумма, введенная пользователем
    
    def start(self):
        self.scanBrelokWindow=ScanBrelok()
        self.connect(self.scanBrelokWindow, QtCore.SIGNAL("ScanBrelok"), self.scanBrelok)
        self.connect(self.scanBrelokWindow, QtCore.SIGNAL("SimulateScanOK"), self.simScan)
        self.scanBrelokWindow.window.show()
        
    def scanBrelok(self):
        self.rb.scanBrelok()                      

    def itemSelected(self, item):
        self.item=item
        self.receiveCashWindow=ReceiveCash(self.payment, item)
        self.connect(self.receiveCashWindow, QtCore.SIGNAL("PaymentCancelled"), self.paymentCancelled)
        self.connect(self.receiveCashWindow, QtCore.SIGNAL("GiveOutItem"), self.giveOutItem)
        self.connect(self.receiveCashWindow, QtCore.SIGNAL("ReceiveMoneyTimeout"), self.restart)
        self.receiveCashWindow.receiveCashWindow.show()
        
    def paymentCancelled(self, payment):
        self.payment=payment
        self.choosingItemWindow = ChoosingItemWindow(self.rb.gpioSocket.magazines.copy(), self.payment)
        self.connect(self.choosingItemWindow, QtCore.SIGNAL("ItemSelected"), self.itemSelected)
        self.choosingItemWindow.window.show()             

    def giveOutItem(self, itemId):
        self.receiveCashWindow.receiveCashWindow.close()
        self.givingOutItem=GivingOutItem()
        self.connect(self.rb, QtCore.SIGNAL("OutingEnd"), self.givingOutHandler)
        self.connect(self.givingOutItem, QtCore.SIGNAL("EngSendClick"), self.engSensClick)
        self.connect(self.givingOutItem, QtCore.SIGNAL("OutSensotClick"), self.outSensClick)
        self.givingOutItem.givingOutWindow.show()        
        self.rb.giveOutItem(itemId)

    def givingOutHandler(self, result):
        if result:
            self.givingOutItem.givingOutWindow.close()
            self.writeBrelokWindow=WriteBrelok()
            self.connect(self.writeBrelokWindow, QtCore.SIGNAL("WriteBrelok"), self.writeBrelok)
            self.connect(self.writeBrelokWindow, QtCore.SIGNAL("SimulateWriteOK"), self.simWrite)
            self.writeBrelokWindow.window.show() 
        else:
            self.givingOutItem.fail()
          
    def scanFinishHandler(self, result):
        if result:
            self.selektItem()
        else:
            self.scanBrelokWindow.scanFail()                        

    def writeBrelok(self):
        self.rb.writeBrelok()
            
    def writeFinishHandler(self, result):
        if result:
            self.writeBrelokWindow.window.close()
            self.finishWindow=FinishWindow()
            self.connect(self.finishWindow, QtCore.SIGNAL("FinishProc"), self.endApp)
            self.finishWindow.window.show()
        else:
            self.writeBrelokWindow.writeFail() 
    
    def selektItem(self):
        self.choosingItemWindow = ChoosingItemWindow(self.rb.gpioSocket.magazines.copy(),
                                                      self.payment)     # окно выбора предмета
        #self.choosingItemWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.connect(self.choosingItemWindow, QtCore.SIGNAL("ItemSelected"), self.itemSelected)
        self.scanBrelokWindow.window.close()
        self.choosingItemWindow.window.show()
        
    def endApp(self):
        self.emit(QtCore.SIGNAL('End working'))
        print 'Программа закончила работу'    
        
    def restart(self):
        self.receiveCashWindow.receiveCashWindow.close()
        self.emit(QtCore.SIGNAL('Restart'))
                
    #========== TEST =================

    def engSensClick(self):
        activMag=self.rb.gpioSocket.activeMagazin
        if activMag is None: return
        eng=activMag.magEng
        eng.sensorPin.setSignal(1)
    
    def outSensClick(self):
        self.rb.gpioSocket.getOutSensor.setSignal(1)
    
    def simScan(self):
        self.rb.gpioSocket.programmator.pinScanOK.setSignal(1)
        
    def simWrite(self):
        self.rb.gpioSocket.programmator.pinWriteOK.setSignal(1)
        

    
        
            