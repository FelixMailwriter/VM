# -*- coding:utf-8 -*-
from PyQt4.Qt import QObject
from PyQt4 import QtCore
from HdWareCon.Pin import Pin
import time


class PgVizit(QtCore.QThread):
    
    '''
    Класс описывает сущность программатора брелоков
    '''
    
    def __init__(self, socketProgrammator):
        QtCore.QThread.__init__(self)
        print 'Инициализация программатора'
        self.typeOperation=''
        self.pinScan=Pin(socketProgrammator["ProgrammatorScan"], "OUT")
        self.pinScanOK=Pin(socketProgrammator["ProgrammatorScanOK"], "IN")
        self.pinWrite=Pin(socketProgrammator["ProgrammatorWrire"], "OUT")
        self.pinWriteOK=Pin(socketProgrammator["ProgrammatorWriteOK"], "IN")
        
        self.scanOKListener=ProgrammatorPinListener(self.pinScanOK, "ScanFinished", 0, 10000, 100)
        self.connect(self.scanOKListener, QtCore.SIGNAL("ScanFinished"), self.scanFinishHandler)
        
        self.writeOKListener=ProgrammatorPinListener(self.pinWriteOK, "WriteFinished", 0, 10000, 100)
        self.connect(self.writeOKListener, QtCore.SIGNAL("WriteFinished"), self.writeFinishHandler)
        
        self.QTQ_SCAN_TRYING=1
        self.QTY_WRITE_TRYING=1
        self.scanTrying=self.QTQ_SCAN_TRYING
        self.writeTrying=self.QTY_WRITE_TRYING
        self.reset()
        print 'Инициализация программатора выполнена'
        
    def reset(self):
        print 'Инициализация программатора'
        self.pinScan.enable() #программатор срабатывает по низкому уровню
        self.pinWrite.enable()
        
    def run(self):
        if self.typeOperation=='Scan':
            self.scan(False)
        if self.typeOperation=='Write':
            self.write(False)
        
    def scan(self, result=False):
        if result:             
            self.emit(QtCore.SIGNAL("ScanFinished"), True)
            #self.pinScan.enable() #выкл программатор. Программатор срабатывает по низкому уровню
            return
        if self.scanTrying>0:# and not self.scanOKListener.isRunning():
            print 'Включение программатора на сканирование. Попытка %s' %(-(self.scanTrying-6))
            self.scanOKListener.start()
            self.pinScan.disable() #вкл программатор. Программатор срабатывает по низкому уровню
            #self.msleep(500)
        else:
            self.scanTrying=self.QTQ_SCAN_TRYING
            self.pinScan.enable()
            self.emit(QtCore.SIGNAL("ScanFinished"), False)

             
    def scanFinishHandler(self, result):

        if self.scanOKListener.isRunning():
            self.scanOKListener.wait()
    
        self.pinScan.enable()
        time.sleep(1)
    
        if result:
            self.scan(result)
        else:
            self.scanTrying-=1            
            self.scan(result)
  
  
    def write(self, result=False):
        if result:             
            self.emit(QtCore.SIGNAL("WriteFinished"), True)
            return
        if self.writeTrying>0:
            print 'Включение программатора на запись. Попытка %s' %(-(self.writeTrying-6))
            self.writeOKListener.start()
            self.pinWrite.disable()
            #self.msleep(500)
        else:
            self.writeTrying=self.QTY_WRITE_TRYING
            self.emit(QtCore.SIGNAL("WriteFinished"), False)


    def writeFinishHandler(self, result):
        if self.writeOKListener.isRunning():
            self.writeOKListener.wait()
    
        self.pinWrite.enable()
        time.sleep(1)
    
        if result:
            self.write(result)
        else:
            self.writeTrying-=1            
            self.write(result)   
    
      
class ProgrammatorPinListener(QtCore.QThread):
    

    def __init__(self, sensorPin, eventName, delayStart=0, listenDuration=10000, listenFreq=5, proofPing=3):
        QtCore.QThread.__init__(self)
        self.sensorPin=sensorPin                # прослушиваемый Pin
        self.delayStart=delayStart              # задержка перед запуском прослушивания
        self.listenDuration=listenDuration      # Продолжительность прослушивания
        self.ListenFreq=listenFreq              # Частота опроса
        self.eventName=eventName                # имя генерируемого события
        self.proofPing=proofPing*2              # количество срабатываний датчика для успешного завершения операции
        self.currentState = False               # текущее состояние датчика
    
    def run(self):
        print "Слушам датчик %s" %(self.sensorPin)
        threshold=0
        self.msleep(self.delayStart)
        while threshold<self.listenDuration:
            if self.sensorPin.getSignal()!=self.currentState:
                self.currentState= not self.currentState
                print 'State changed', self.currentState
                self.proofPing=self.proofPing-1
            
            if self.proofPing<=0:
                print 'Срабатывание датчика %s. Выход из потока прослушивания' %(self.sensorPin)
                self.emit(QtCore.SIGNAL("%s" %(self.eventName)), True)
                return
            else:
                threshold=threshold+self.ListenFreq
                self.msleep(self.ListenFreq)
        self.emit(QtCore.SIGNAL("%s" %(self.eventName)), False)
        print 'TimeOut датчика прослушивания %s. Выход из потока' %(threshold) 
        
