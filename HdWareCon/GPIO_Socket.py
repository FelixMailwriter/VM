# -*- coding:utf-8 -*-
#import RPi.GPIO as GPIO
#GPIO.setmode(BCM)
from PyQt4 import QtCore
from PyQt4.Qt import QObject
#from HdWareCon import Programmator_del.Programmator
from Programmator.Vizit import PgVizit 
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
        self.programmator=PgVizit(programmatorPinSettings)                          #Экземпляр программатора
        self.connect(self.programmator, QtCore.SIGNAL("ScanFinished"), self.scanHandler)
        self.connect(self.programmator, QtCore.SIGNAL("WriteFinished"), self.writeHandler)
        #Создаем коллекцию магазинов с инфой о пинах и загруженных предметах
        self.magazines=self.getMagazinesList(magazinesPinSettings, magazinItemsMap)    
        self.getOutSensor= self.getGetOutSensor(PinGetOutSensor)                    #PIN датчика выдачи
        self.activeMagazin=None                                                     # Активный магазин                                                 
        
   
    def getMagazinesList(self, magazinesPinSettings, magazinItemsMap):
        #создаем экземпляр магазина и заносим его в список
        magList={}
        for MagNumber in magazinItemsMap:
            MagItem=magazinItemsMap[MagNumber]
            magazin=(Magazin(MagNumber, magazinesPinSettings[(MagNumber,"EngPw")], magazinesPinSettings[(MagNumber,"EngSensor")], 
                    magazinesPinSettings[(MagNumber,"EmptySensor")],MagItem))
            print 'Добавлен %s'  %(magazin)
            magList[MagNumber]= magazin
        return magList
    
    def getGetOutSensor(self, PinGetOutSensor):
        pin= Pin(PinGetOutSensor, 'IN')
        print 'Датчик выдачи установлен %s' %(pin)
        return pin

    def giveOutItem(self, item):
        print "GPIO_Socket: Начало выдачи предмета %s" %(str(item))
        self.outingItem=item
        if self.activeMagazin is not None: return  
        for i in self.magazines:
            magazin=self.magazines[i]
            self.activeMagazin=magazin.giveOutItem(item) 
            if self.activeMagazin is not None:  
                self.giveOutSensorListener=SensorListener(self.getOutSensor, "Click", 2000, 6000, 5)
                self.connect(self.giveOutSensorListener, QtCore.SIGNAL("Click"), self.itemOutHandler)
                self.giveOutSensorListener.start()
                break

    def itemOutHandler(self, result):
        if result:
            print 'GPIO_Socket: предмет выдан'
            #self.activeMagazin.stopOutingItem()
        else:
            print 'GPIO_Socket: предмет не выдан'
        self.giveOutSensorListener.wait(100)
        self.emit(QtCore.SIGNAL("OutingEnd"), result, self.activeMagazin, self.outingItem)
        self.activeMagazin=None
        
    def scanBrelok(self):
        self.programmator.typeOperation='Scan'
        self.programmator.start()
        
    def writeBrelok(self):
        self.programmator.typeOperation='Write'
        self.programmator.start()
    
    def scanHandler(self, result):
        self.emit(QtCore.SIGNAL("ScanFinished"), result)
    
    def writeHandler(self, result):
        self.emit(QtCore.SIGNAL("WriteFinished"), result)
    
    
            
    
