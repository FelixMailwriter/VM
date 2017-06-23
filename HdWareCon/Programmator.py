# -*- coding:utf-8 -*-
from PyQt4.Qt import QObject
from PyQt4 import QtCore
from HdWareCon.Pin import Pin
from HdWareCon.SensorListener import SensorListener
import time


class Programmator(QtCore.QThread):
    
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
        self.scanOKListener=SensorListener(self.pinScanOK, "ScanFinished", 0, 20000, 100)
        self.connect(self.scanOKListener, QtCore.SIGNAL("ScanFinished"), self.scanFinishHandler)
        self.writeOKListener=SensorListener(self.pinWriteOK, "WriteFinished", 0, 20000, 100)
        self.connect(self.writeOKListener, QtCore.SIGNAL("WriteFinished"), self.writeFinishHandler)
        self.QTQ_SCAN_TRYING=1
        self.QTY_WRITE_TRYING=1
        self.scanTrying=self.QTQ_SCAN_TRYING
        self.writeTrying=self.QTY_WRITE_TRYING
        print 'Инициализация программатора выполнена'
        
    def reset(self):
        print 'Инициализация программатора'
        self.pinScan.disable()
        self.pinWrite.disable()
        
    def run(self):
        if self.typeOperation=='Scan':
            self.scan(False)
        if self.typeOperation=='Write':
            self.write(False)
        
    def scan(self, result=False):
        if result:             
            self.emit(QtCore.SIGNAL("ScanFinished"), True)
            return
        if self.scanTrying>0:# and not self.scanOKListener.isRunning():
            print 'Включение программатора на сканирование. Попытка %s' %(-(self.scanTrying-6))
            self.scanOKListener.start()
            self.pinScan.enable()
            #self.msleep(500)
        else:
            self.scanTrying=self.QTQ_SCAN_TRYING
            self.emit(QtCore.SIGNAL("ScanFinished"), False)

             
    def scanFinishHandler(self, result):

        if self.scanOKListener.isRunning():
            self.scanOKListener.wait()
    
        self.pinScan.disable()
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
            self.pinWrite.enable()
            #self.msleep(500)
        else:
            self.writeTrying=self.QTY_WRITE_TRYING
            self.emit(QtCore.SIGNAL("WriteFinished"), False)


    def writeFinishHandler(self, result):
        if self.writeOKListener.isRunning():
            self.writeOKListener.wait()
    
        self.pinWrite.disable()
        time.sleep(1)
    
        if result:
            self.write(result)
        else:
            self.writeTrying-=1            
            self.write(result)   
    
      
        
