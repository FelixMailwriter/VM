# -*- coding:utf-8 -*-
from HdWareCon.Pin import Pin
from PyQt4 import QtCore
from PyQt4.Qt import QObject
import logging

class MagEng(QObject):
    '''
    Класс описывает сущность привода магазина продаваемых предметов.
    Управляет мотором и датчиком полного оборота мотора
    '''
    
    def __init__(self, numEngPin, numSensorPin):
        QObject.__init__(self)
        print 'Инициализация мотора'

        self.engPin = Pin(numEngPin, 'OUT')
        self.sensorPin = Pin(numSensorPin, 'IN')
        self.startMotorDelay = 500
        self.sensorDelay = 2000
        self.timeOut = 6000
        print 'Инициализация мотора выполнена'
        
    def reset(self):
        print 'Инициализация мотора магазина'
        self.stopEngine()
        
    def motorRotate(self):
        print 'Мотор стартует'
        self.rotateCycle=RotateCycle(self.engPin, self.sensorPin, self.startMotorDelay, self.sensorDelay, self.timeOut)
        self.connect(self.rotateCycle,QtCore.SIGNAL("stopEngine"), self.stopEngine)
        self.rotateCycle.start()
        
    def stopEngine(self):
        print 'Мотор остановлен Pin=%s' %(self.engPin.num)
        self.engPin.disable()
            
        
        
class RotateCycle(QtCore.QThread):
    '''
    Класс,описывающий сущность оборота мотора
    '''      
    def __init__(self, pinEng, pinSensor, startMotorDelay=0, sensorDelay=2000, timeOut=6000): 
        QtCore.QThread.__init__(self)
        self.pinEng=pinEng
        self.pinSensor=pinSensor
        self.startMotorDelay=startMotorDelay    # задержка запуска мотора
        self.sensorDelay=sensorDelay            # задержка подкл датчика полного оборота
        self.timeOut=timeOut                    # максимальное время работы мотора
        self.freq=10                            # частота опроса датчика оборота
        
    def run(self):
        '''метод запускает мотор после задержки startMotorDelay и затем опрашивает датчик оборота мотора с интервалом 
        self.freq мс.
        При наличии высокого уровня на разъеме генерирует событие для отключения мотора
        Если сигнала с датчика не поступило за время timeOut мотор отключается
        '''
        self.msleep(self.startMotorDelay)
        print 'Мотор стартовал'
        Pin.enable(self.pinEng)
        print 'Задержка перед включением датчика оборота %s' %(self.sensorDelay)
        self.msleep(self.sensorDelay)
        print 'Включение опроса датчика оборота'        
        signal=Pin.getSignal(self.pinSensor)
        threshold=0
        while (not signal) and (threshold<self.timeOut):
            self.msleep(self.freq)
            signal=Pin.getSignal(self.pinSensor)
            threshold=threshold+self.freq
        print 'Мотор останавливается'
        self.emit(QtCore.SIGNAL("stopEngine"))
        print 'выход из потока двигатли %s' %(threshold)
        
 
    
    
