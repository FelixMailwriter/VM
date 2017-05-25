# -*- coding:utf-8 -*-
from PyQt4 import QtCore

class SensorListener(QtCore.QThread):
    

    def __init__(self, sensorPin, eventName, delayStart=0, listenDuration=10000, listenFreq=5):
        QtCore.QThread.__init__(self)
        self.sensorPin=sensorPin                # прослушиваемый Pin
        self.delayStart=delayStart              # задержка перед запуском прослушивания
        self.listenDuration=listenDuration      # Продолжительность прослушивания
        self.ListenFreq=listenFreq              # Частота опроса
        self.eventName=eventName                # имя генерируемого события
    
    def run(self):
        print "Слушам датчик %s" %(self.sensorPin)
        threshold=0
        self.msleep(self.delayStart)
        while threshold<self.listenDuration:
            if self.sensorPin.getSignal():
                self.emit(QtCore.SIGNAL("%s" %(self.eventName)), True)
                print 'Срабатывание датчика %s. Выход из потока прослушивания' %(self.sensorPin)
                return
            else:
                threshold=threshold+self.ListenFreq
                self.msleep(self.ListenFreq)
        self.emit(QtCore.SIGNAL("%s" %(self.eventName)), False)
        print 'TimeOut датчика прослушивания %s. Выход из потока' %(threshold) 
