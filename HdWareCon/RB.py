# -*- coding:utf-8 -*-
from PyQt4.Qt import QObject
from PyQt4 import QtCore
from HdWareCon.GPIO_Socket import GPIO_Socket
from KP.KPProvider import KPProvider
#from HdWareCon.FilePrinter import Printer

class RB(QObject):
    '''
    Класс описывает сущность платы RasperryPi3
    '''
    
    def __init__(self, dbProvider):
        QObject.__init__(self)
        
        self.dbProvider=dbProvider
        
        programmatorPinSettings, magazinesPinSettings, PinGetOutSensor=self.dbProvider.getGPIOPinSettigs()
        
        #Получаем коллекцию магазинов с закрепленными за ними предметами      
        self.magazinItemsMap=self.dbProvider.getIdItemsinMagazinsMap()
        
        self.gpioSocket=GPIO_Socket(programmatorPinSettings=programmatorPinSettings, 
                                    magazinesPinSettings=magazinesPinSettings, 
                                    magazinItemsMap=self.magazinItemsMap,
                                    PinGetOutSensor=PinGetOutSensor)
        self.connect(self.gpioSocket, QtCore.SIGNAL("OutingEnd"), self.itemOutHandler)
        self.connect(self.gpioSocket, QtCore.SIGNAL("ScanFinished"), self.scanHandler)
        self.connect(self.gpioSocket, QtCore.SIGNAL("WriteFinished"), self.writeHandler)

        self.kp=KPProvider()

     
    def giveOutItem(self, item):                      #Запускает процедуру выдачи предмета по его id
        print "RB: Начало выдачи предмета %s" %(str(item))
        self.gpioSocket.giveOutItem(item)
        
    def itemOutHandler(self, result, magazin, item):
        if result:
            print "RB: предмет выдан"
        else: 
            print "RB: предмет не выдан"
        self.emit(QtCore.SIGNAL("OutingEnd"), result, magazin, item)
    
    def scanBrelok(self):
        self.gpioSocket.scanBrelok()
        
    def writeBrelok(self):
        self.gpioSocket.writeBrelok()
    
    def scanHandler(self, result):
        self.emit(QtCore.SIGNAL("ScanFinished"), result)
    
    def writeHandler(self, result):
        self.emit(QtCore.SIGNAL("WriteFinished"), result)     
  
   
    
    