# -*- coding:utf-8 -*-
#import RPi.GPIO as GPIO
#GPIO.setmode(BCM)
from PyQt4 import QtCore
from PyQt4.Qt import QObject
from HdWareCon.Pin import Pin
from HdWareCon.Magazin import Magazin
from TrashValve import TrashValve
from HdWareCon.SensorListener import SensorListener
from Programmator.Programmator import Programmator
import Common.Error as Error
import Common.Settings as Settings


class GPIO_Socket(QObject):
    '''
    Класс описывает разъем GPIO устройства Raspbery Pi3
    '''

    def __init__(self, programmatorPinSettings, magazinesPinSettings,
                 magazinItemsMap, PinGetOutSensor, PinTrashValve):
        QObject.__init__(self)
        #GPIO.cleanup()
        #GPIO.setmode(GPIO.BCM)
        global _
        _ = Settings._

        self.prgRestartsCounter = 0

        self.programmatorPinSettings = programmatorPinSettings

        self.programmator = self._getProgrammator(programmatorPinSettings)  #Экземпляр программатора

        self.programmator.init()

        self.trashValve = self._getTrashValve(PinTrashValve) # Заслонка сброса
        
        #Создаем коллекцию магазинов с инфой о пинах и загруженных предметах
        self.magazines = self._getMagazinesList(magazinesPinSettings, magazinItemsMap)
        self.getOutSensor = self._getGetOutSensor(PinGetOutSensor)   # Pin датчика выдачи
        self.activeMagazin = None                                   # Активный магазин


   
    def _getMagazinesList(self, magazinesPinSettings, magazinItemsMap):
        #создаем экземпляр магазина и заносим его в список
        magList = {}
        for MagNumber in magazinItemsMap:
            MagItem = magazinItemsMap[MagNumber]
            magazin = (Magazin(MagNumber, magazinesPinSettings[(MagNumber,"EngPw")], magazinesPinSettings[(MagNumber,"EngSensor")],
                    magazinesPinSettings[(MagNumber,"EmptySensor")],MagItem))
            print 'Добавлен %s'%(magazin)
            magList[MagNumber] = magazin
        return magList


    def _getGetOutSensor(self, PinGetOutSensor):
        pin= Pin(PinGetOutSensor, 'IN')
        print 'Датчик выдачи установлен %s' %(pin)
        return pin


    def _getProgrammator(self, programmatorPinSettings):
        programmator = Programmator(programmatorPinSettings)
        self.connect(self.programmator, QtCore.SIGNAL("HardwareFailed"), self._hardwareFaledHandler)
        self.connect(self.programmator, QtCore.SIGNAL("ScanFinished"), self.scanHandler)
        self.connect(self.programmator, QtCore.SIGNAL("WriteFinished"), self.writeHandler)
        self.connect(self.programmator, QtCore.SIGNAL("DemandRestart"), self._prgRestart)
        return programmator


    def _getTrashValve(self, PinTrashValve):
        trashValve = TrashValve(PinTrashValve)


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


    def _hardwareFaledHandler(self, err):
        self.emit(QtCore.SIGNAL("HardwareFailed"), err)


    def _prgRestart(self, err):
        if self.prgRestartsCounter >= 3:
            err_level = Error.ErrorLevel.CRITICAL
            err_source = Error.ErrorSource.PROGRAMMATOR
            msg = _(u"Programmator failed")
            err = Error.Error(err_level, err_source, msg)
            self.emit(QtCore.SIGNAL("HardwareFailed"), err)
        else:
            self.prgRestartsCounter += 1
            self.emit(QtCore.SIGNAL("HardwareFailed"), err)
            self.programmator.init()


    def scanHandler(self, result):
        self.emit(QtCore.SIGNAL("ScanFinished"), result)
    
    def writeHandler(self, result):
        self.emit(QtCore.SIGNAL("WriteFinished"), result)
    
    
            
    
