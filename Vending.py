# -*- coding:utf-8 -*-
from PyQt4.Qt import QObject
from PyQt4 import QtCore
import time
import HdWareCon.RB as RB
from UI.ScanBrelok import ScanBrelok
from UI.FinishWindow import FinishWindow
from UI.ChoosingItem import ChoosingItemWindow
from UI.ReceiveCash import ReceiveCash
from UI.GivingOutItem import GivingOutItem
from Common.Logs import LogEvent
import BDL.BDCon as BDCon
import KP.KPManager as KP
import Common.Settings as Settings
from Errors import Errors


class Vending(QObject):
    
    def __init__(self, payment):
        QObject.__init__(self)
        
        global _
        _= Settings._
        
        self.DbType='SQLDB'
        self.dbProvider=self._getDbProvider(self.DbType)  #Подключение к выбранной БД
            
        self.rb=RB.RB(self.dbProvider)                    # Экземпляр Raspberry
                                                                             
        self.connect(self.rb, QtCore.SIGNAL("ScanFinished"), self.scanFinishHandler)
        self.connect(self.rb, QtCore.SIGNAL("WriteFinished"), self.writeFinishHandler)
        ######
        #self._initKP('NV-9')                               #Инициализация купюроприемника
        
        self.payment=payment                               # Сумма, введенная пользователем

    def _getDbProvider(self, dbType):
        try:
            dbConnector= BDCon.BDCon(dbType)#('TestDB')
            dbProvider=dbConnector.dbContext               #Экземпляр подключенной базы данных  
            return dbProvider
        except:
            message=_(u"Database connection error")
            print message
            raise Exception(message)
            return              
        
    def _initKP(self, kpmodel):
        try:
            self.kpInitilaser=KP.KPInitilaser(kpmodel)                           #Инициализация купюроприемника
            self.kpInitilaser.start()
            self.kpInstance=self.kpInitilaser.getKPInstance()                  #Ссылка на купюроприемник
        except KP.KPErrorException as e:
            print e.value
            raise Exception(_(u'Hardware error'))
            return             
        self.connect(self.kpInitilaser, QtCore.SIGNAL('Init finished'), self._setKPInstance)
    
    def _setKPInstance(self, kpInstance):
        if kpInstance is None:
            message=_(u"Notereceiver initialization error. Code:001")
            print message
            raise Exception(message)
            return              
        self.kpInstance=kpInstance
    
    def start(self):
        self.scanBrelokWindow=ScanBrelok()
        self.connect(self.scanBrelokWindow, QtCore.SIGNAL("ScanBrelok"), self.rb.scanBrelok)
        self.connect(self.scanBrelokWindow, QtCore.SIGNAL("SimulateScanOK"), self.simScan)################### del
        #self.connect(self.rb.gpioSocket.programmator.QtCore.SIGNAL("ScanOK"), self.simScan)
        self.scanBrelokWindow.window.show()
        
    def scanFinishHandler(self, result):
        if result:
            self.selektItem()
        else:
            self.scanBrelokWindow.scanFail()

    def selektItem(self):
        self.choosingItemWindow = ChoosingItemWindow(self.payment, self.dbProvider)     # окно выбора предмета
        self.connect(self.choosingItemWindow, QtCore.SIGNAL("ItemSelected"), self.paymentStart)
        self.connect(self.choosingItemWindow, QtCore.SIGNAL("TimeOutPage"), self.endApp)
        self.scanBrelokWindow.window.close()

    def paymentStart(self, item):
        while self.kpInitilaser.isRunning():
            time.sleep(1)
        if self.payment>=item.price:
            self.giveOutItem(item)
            return
        self.itemId=item
        self.receiveCashWindow=ReceiveCash(self.payment, item, self.dbProvider, self.kpInstance)
        self.connect(self.receiveCashWindow, QtCore.SIGNAL("PaymentCancelled"), self.paymentCancelled)
        self.connect(self.receiveCashWindow, QtCore.SIGNAL("GiveOutItem"), self.giveOutItem)
        self.connect(self.receiveCashWindow, QtCore.SIGNAL("TimeOutPage"), self.endApp)
        self.connect(self.receiveCashWindow, QtCore.SIGNAL("PaymentChange"), self._changePayment)
        self.connect(self.receiveCashWindow, QtCore.SIGNAL("TimeOutPage"), self.endApp)
        self.receiveCashWindow.receiveCashWindow.show()
        
    def _changePayment(self, payment):
        self.payment=payment 
    
    def paymentCancelled(self, payment):
        self.payment=payment
        self.choosingItemWindow = ChoosingItemWindow(self.payment, self.dbProvider)
        self.connect(self.choosingItemWindow, QtCore.SIGNAL("ItemSelected"), self.paymentStart)
        self.connect(self.choosingItemWindow, QtCore.SIGNAL("TimeOutPage"), self.endApp)
        self.choosingItemWindow.window.show()             

    def giveOutItem(self, item):
        self.givingOutItem=GivingOutItem()
        self.connect(self.rb, QtCore.SIGNAL("OutingEnd"), self.givingOutHandler)
        
        #Убрать после тестов
        self.connect(self.givingOutItem, QtCore.SIGNAL("EngSendClick"), self.engSensClick)
        self.connect(self.givingOutItem, QtCore.SIGNAL("OutSensorClick"), self.outSensClick)#############################
        self.connect(self.givingOutItem, QtCore.SIGNAL("SimulateWriteOK"), self.simWrite)#############################
        ###-------------------
        self.connect(self.givingOutItem, QtCore.SIGNAL("TimeOutPage"), self.endApp)
        self.givingOutItem.givingOutWindow.show()        
        self.rb.giveOutItem(item)

    def givingOutHandler(self, result, magazin, item):
        if result:
            #Запись в БД факта продажи
            self.dbProvider.sellItem(magazin, item, self.payment)
            #self.writeBrelokWindow=WriteBrelok()
            #self.connect(self.writeBrelokWindow, QtCore.SIGNAL("WriteBrelok"), self.writeBrelok)
            #self.connect(self.writeBrelokWindow, QtCore.SIGNAL("SimulateWriteOK"), self.simWrite)
            #self.connect(self.writeBrelokWindow, QtCore.SIGNAL("TimeOutPage"), self.endApp)
            #self.writeBrelokWindow.window.show() 
            self.rb.writeBrelok()
        else:
            #Запись в лог о провале продажи
            logMessages=[]
            logEvent=LogEvent('Critical', 'Vending', 'Item %s have not been given' %(str(item.name)))
            logMessages.append(logEvent)
            self.dbProvider.writeLog(logMessages)
            self.givingOutItem.fail()
                    
    def writeFinishHandler(self, result):
        self.givingOutItem.givingOutWindow.close()
        if result:
            self.finishWindow=FinishWindow()
            self.connect(self.finishWindow, QtCore.SIGNAL("FinishProc"), self.endApp)
            #self.writeBrelokWindow.window.close()
            self.finishWindow.window.show()
        else:
            #self.writeBrelokWindow.writeFail()
            message=_(u'Key writing is failed. Call the techsupport.') 
            errormsg=Errors(message)

    def endApp(self):
        self.emit(QtCore.SIGNAL('End working'))
        print 'Программа закончила работу'        
                
    #========== TEST =================

    def engSensClick(self):
        activMag=self.rb.gpioSocket.activeMagazin
        if activMag is None: return
        eng=activMag.magEng
        eng.sensorPin.setSignal(1)
    
    def outSensClick(self):
        self.rb.gpioSocket.getOutSensor.setSignal(1)
    
    def simScan(self):
        currSig=self.rb.gpioSocket.programmator.pinScanOK.getSignal()
        self.rb.gpioSocket.programmator.pinScanOK.setSignal(not currSig)
        
    def simWrite(self):
        self.rb.gpioSocket.programmator.pinWriteOK.setSignal(1)

        

    
        
            