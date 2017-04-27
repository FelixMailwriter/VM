# -*- coding:utf-8 -*-
from PyQt4.Qt import QObject
from PyQt4 import QtCore
from enum import __repr__
from datetime import datetime
from HdWareCon.GPIO_Socket import GPIO_Socket
from KP.KPProvider import KPProvider
import BDL.BDCon as BDCon
#from HdWareCon.Printer import Printer

class RB(QObject):
    '''
    Класс описывает сущность платы RasperryPi3
    '''
    
    def __init__(self):
        QObject.__init__(self)
        
        try:
            dbConnector= BDCon.BDCon('SQLDB')#('TestDB')
            self.dbContext=dbConnector.dbContext           #Экземпляр подключенной базы данных  
            
        except BDCon.DbConnectionException:
            raise InitException(u'Ошибка инициализации Raspberry')
        
        programmatorPinSettings, magazinesPinSettings, PinGetOutSensor=self.dbContext.getGPIOPinSettigs()
              
        magazinItemsMap=self.dbContext.getItemsMap()
        self.gpioSocket=GPIO_Socket(programmatorPinSettings=programmatorPinSettings, 
                                    magazinesPinSettings=magazinesPinSettings, 
                                    magazinItemsMap=magazinItemsMap,
                                    PinGetOutSensor=PinGetOutSensor)
        self.connect(self.gpioSocket, QtCore.SIGNAL("OutingEnd"), self.itemOutHandler)
        self.connect(self.gpioSocket, QtCore.SIGNAL("ScanFinished"), self.scanHandler)
        self.connect(self.gpioSocket, QtCore.SIGNAL("WriteFinished"), self.writeHandler)
        #self.printer=Printer()
####        self.kp=KPProvider()

     
    def getExistsItems(self):                           #Опрашивает магазины и возвращает уникальный список предметов
        return self.gpioSocket.getExistsItems()
         
    def giveOutItem(self, itemId):                      #Запускает процедуру выдачи предмета по его id
        print "RB: Начало выдачи предмета"
        self.gpioSocket.giveOutItem(itemId)
        
    def itemOutHandler(self, result):
        if result:
            print "RB: предмет выдан"
        else: 
            print "RB: предмет не выдан"
        self.emit(QtCore.SIGNAL("OutingEnd"), result)
    
    def scanBrelok(self):
        self.gpioSocket.scanBrelok()
        
    def writeBrelok(self):
        self.gpioSocket.writeBrelok()
    
    def scanHandler(self, result):
        self.emit(QtCore.SIGNAL("ScanFinished"), result)
    
    def writeHandler(self, result):
        self.emit(QtCore.SIGNAL("WriteFinished"), result)     
    
    def printCheck(self, item):
        now = datetime.now()
        dateNow=datetime.strftime(now, "%Y.%m.%d %H:%M:%S")
        itemName=item.name
        itemPrice=item.price
        #self.printer.printCheck(Data=dateNow, ItemName=itemName, Price=itemPrice)
        
class InitException(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return __repr__(self.value)   
    
    