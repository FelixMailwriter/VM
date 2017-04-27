# -*- coding:utf-8 -*-
#import RPi.GPIO as GPIO
#GPIO.setmode(BCM)
from PyQt4 import QtCore
from PyQt4.Qt import QObject
from HdWareCon.Programmator import Programmator
from HdWareCon.Pin import Pin
from HdWareCon.Magazin import Magazin 
from HdWareCon.SensorListener import SensorListener


class GPIO_Socket(QObject):
    '''
    Класс описывает разъем GPIO устройства Raspbery Pi3
    '''

    def __init__(self, programmatorPinSettings, magazinesPinSettings, magazinItemsMap, PinGetOutSensor):
        QObject.__init__(self)
        #GPIO.cleanup()
        #GPIO.setmode(GPIO.BCM)
        self.programmator=self.getProgrammator(programmatorPinSettings)                #Экземпляр программатора
        self.connect(self.programmator, QtCore.SIGNAL("ScanFinished"), self.scanHandler)
        self.connect(self.programmator, QtCore.SIGNAL("WriteFinished"), self.writeHandler)
        #Создаем коллекцию магазинов с инфой о пинах и загруженных предметах
        self.magazines=self.getMagazinesList(magazinesPinSettings, magazinItemsMap)    
        self.getOutSensor= self.getGetOutSensor(PinGetOutSensor)                    #PIN датчика выдачи
        self.activeMagazin=None                                                     # Активный магазин                                                 
        
   
    def getMagazinesList(self, magazinesPinSettings, magazinItemsMap):
        #создаем экземпляр магазина и заносим его в список
        magList={}
        for i in range(1,7):
            magazin=(Magazin(i, magazinesPinSettings[(i,"EngPw")], magazinesPinSettings[(i,"EngSensor")], 
                            magazinesPinSettings[(i,"EmptySensor")],magazinItemsMap[i]))
            print 'Добавлен %s'  %(magazin)
            magList[i]= magazin
        return magList
    
    def getGetOutSensor(self, PinGetOutSensor):
        pin= Pin(PinGetOutSensor, 'IN')
        print 'Датчик выдачи установлен %s' %(pin)
        return pin

    def getProgrammator(self, programmatorPinSettings):
        programmator=Programmator(programmatorPinSettings)
        return programmator             #


    def getExistsItems(self):
        items=set()
        for i in self.magazines:
            item=self.magazines[i].item
            if item.id>0:
                items.add(item)
        return items
    
    def giveOutItem(self, itemId):
        print "GPIO_Socket: Начало выдачи предмета"
        if self.activeMagazin is not None: return  
        for i in self.magazines:
            magazin=self.magazines[i]
            self.activeMagazin=magazin.giveOutItem(itemId) 
            if self.activeMagazin is not None:  
                self.giveOutSensorListener=SensorListener(self.getOutSensor, "ItemOut", 2000, 6000, 5)
                self.connect(self.giveOutSensorListener, QtCore.SIGNAL("ItemOut"), self.itemOutHandler)
                self.giveOutSensorListener.start()
                break

    def itemOutHandler(self, result):
        self.activeMagazin=None
        if result:
            print 'GPIO_Socket: предмет выдан'
        else:
            print 'GPIO_Socket: предмет не выдан'
        self.giveOutSensorListener.wait(100)
        self.emit(QtCore.SIGNAL("OutingEnd"), result)
        
        
    def scanBrelok(self):
        self.programmator.scan()
        
    def writeBrelok(self):
        self.programmator.write()
    
    def scanHandler(self, result):
        self.emit(QtCore.SIGNAL("ScanFinished"), result)
    
    def writeHandler(self, result):
        self.emit(QtCore.SIGNAL("WriteFinished"), result)
    
    
            
    
