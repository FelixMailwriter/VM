# -*- coding:utf-8 -*-
from PyQt4 import QtCore
from KPNV9 import KPNV9

class KPHandler(QtCore.QThread):
    
    def __init__(self, model=''):
        QtCore.QThread.__init__(self)
        
        self.model=model
        self.kpInstance=self._defineKPInstance(self.model)
        
        self.command=None
        self.isInitialised=False
        
    def execCommand(self, command):
        print 'Command %s' %(command)
        self.command=command 
        self.start()
               
    def run(self):
        print 'Command2 %s' %(self.command)
        if self.command=='init':
            self._initial()
            
        elif self.command=='getMoney':
            if self.kpInstance is not None:
                self.kpInstance.enable()
            else:
                self.initial()
                self.kpInstance.enable()
                
    def _initial(self):
        resultSetup=self.kpInstance.setup()
        if not resultSetup:
            self.emit(QtCore.SIGNAL('Init finished'), None)
            return
        self.connect(self.kpInstance, QtCore.SIGNAL('Note stacked'), self._moneyReceived)
        self.isInitialised=True
        self.emit(QtCore.SIGNAL('Init finished'), self.kpInstance)
        
    def _defineKPInstance(self, kpmodel):
        kpInstance=None
        if kpmodel=='NV-9':
            kpInstance=KPNV9()
            #self.kpInstance.setMaster(self)
        
        if kpInstance==None:
            raise Exception ('BanknoteReceiver type error')
        
        return kpInstance
        
    def getKPInstance(self):
        return self.kpInstance
    

    def _moneyReceived(self, money):
        self.emit(QtCore.SIGNAL('Money received'), money)


class KPStopper(QtCore.QThread):
    def __init__(self, kpThread):
        QtCore.QThread.__init__(self) 
        
        self.kpThread=kpThread
        self.kpInstance=self.kpThread.getKPInstance()
           
   
    def run(self):
        while self.kpThread.isRunning():
            self.kpInstance.disable()
            self.sleep(1)

            
        
        


   
        
        

        
        