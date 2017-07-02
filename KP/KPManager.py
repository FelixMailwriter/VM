# -*- coding:utf-8 -*-
from PyQt4 import QtCore
from KPNV9 import KPNV9

class KPInitilaser(QtCore.QThread):
    
    def __init__(self, model=''):
        QtCore.QThread.__init__(self)
        
        self.model=model
        self.kpInstance=self._defineKPInstance(self.model)
        
    def run(self):
        resultSetup=self.kpInstance.setup()
        if not resultSetup:
            self.emit(QtCore.SIGNAL('Init finished'), None)
            return
        self.emit(QtCore.SIGNAL('Init finished'), self.kpInstance)
        
    def _defineKPInstance(self, kpmodel):
        kpInstance=None
        if kpmodel=='NV-9':
            kpInstance=KPNV9()
        
        if kpInstance==None:
            raise Exception ('BanknoteReceiver type error')
        
        return kpInstance

    def getKPInstance(self):
        return self.kpInstance        
    
    
        
class KPMoneyGetter(QtCore.QThread):
    
    def __init__(self, kpInstance):
        QtCore.QThread.__init__(self)
        
        self.kpInstance=kpInstance
        self.connect(self.kpInstance, QtCore.SIGNAL('Note stacked'), self._moneyReceived)
        
    def run(self):
        self.kpInstance.enable()
       
    def _moneyReceived(self, money):
        self.emit(QtCore.SIGNAL('Money received'), money)        

    def getKPInstance(self):
        return self.kpInstance
                

class KPStopper(QtCore.QThread):
    def __init__(self, kpThread):
        QtCore.QThread.__init__(self) 
        
        self.kpThread=kpThread
        self.kpInstance=self.kpThread.getKPInstance()
           
   
    def run(self):
        while self.kpThread.isRunning():
            self.kpInstance.disable()
            self.sleep(1)

   
        


   
        
        

        
        