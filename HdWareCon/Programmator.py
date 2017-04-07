# -*- coding:utf-8 -*-
from PyQt4.Qt import QObject
from PyQt4 import QtCore
from HdWareCon.Pin import Pin
from HdWareCon.SensorListener import SensorListener
import time


class Programmator(QObject):
    
    '''
    Класс описывает сущность программатора брелоков
    '''
    
    def __init__(self, socketProgrammator):
        QObject.__init__(self)
        print 'Инициализация программатора'
        self.pinScan=Pin(socketProgrammator["ProgrammatorScan"], "OUT")
        self.pinScanOK=Pin(socketProgrammator["ProgrammatorScanOK"], "IN")
        self.pinWrite=Pin(socketProgrammator["ProgrammatorWrire"], "OUT")
        self.pinWriteOK=Pin(socketProgrammator["ProgrammatorWriteOK"], "IN")
        self.scanOKListener=SensorListener(self.pinScanOK, "ScanFinished", 0, 3000, 100)
        self.connect(self.scanOKListener, QtCore.SIGNAL("ScanFinished"), self.scanFinishHandler)
        self.writeOKListener=SensorListener(self.pinWriteOK, "WriteFinished", 0, 3000, 100)
        self.connect(self.writeOKListener, QtCore.SIGNAL("WriteFinished"), self.writeFinishHandler)
        self.QTQ_SCAN_TRYING=3
        self.QTY_WRITE_TRYING=3
        self.scanTrying=self.QTQ_SCAN_TRYING
        self.writeTrying=self.QTY_WRITE_TRYING
        print 'Инициализация программатора выполнена'
        
    def reset(self):
        print 'Инициализация программатора'
        self.pinScan.disable()
        self.pinWrite.disable()
        
    def scan(self, result=False):
        if result:             
            self.emit(QtCore.SIGNAL("ScanFinished"), True)
            return
        if self.scanTrying>0 and not self.scanOKListener.isRunning():
            print 'Включение программатора на сканирование. Попытка %s' %(-(self.scanTrying-4))
            self.scanOKListener.start()
            self.pinScan.enable()
            time.sleep(2)
            self.pinScan.disable()
        else:
            self.scanTrying=self.QTQ_SCAN_TRYING
            self.emit(QtCore.SIGNAL("ScanFinished"), False)

             
    def scanFinishHandler(self, result):
        if result:
            self.scan(result)
        else:
            self.scanTrying-=1            
            self.scan(result)
  
  
    def writeFinishHandler(self, result):
        if result:
            self.pinWrite.disable()
            self.write(result)
        else:
            self.writeTrying-=1
            self.write(result)
            
        
    def write(self, result=False):
        if result: 
            self.emit(QtCore.SIGNAL("WriteFinished"), True)
            return
        if self.writeTrying>0 and not self.writeOKListener.isRunning():
            print 'Включение программатора на запись. Попытка %s' %(-(self.writeTrying-4))
            self.writeOKListener.start()
            self.pinWrite.enable()
            time.sleep(2)
            self.pinWrite.disable()
        else:
            self.writeTrying=self.QTY_WRITE_TRYING
            self.emit(QtCore.SIGNAL("WriteFinished"), False)
    
    
      
        
