# -*- coding:utf-8 -*-
from PyQt4 import QtCore
from KPNV9 import KPNV9
from KP.KPCommon import KPInstance

class KPHandler(QtCore.QThread):
    def __init__(self, model):
        QtCore.QThread.__init__(self)
        
        self.kpmodel=model
        self.kpInstance=None
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
                
        elif self.command=='stop':
            print self.kpInstance
            if self.kpInstance is not None:
                print 'command disable received!!!'
                self.kpInstance.disable()
        
    def _initial(self):
        if self.kpInstance is None:
            try:
                self._getKPInstance()
            except:
                self.emit(QtCore.SIGNAL('KPSetup is failed'))
                 
        resultSetup=self.kpInstance.setup()
        if not resultSetup:
            self.emit(QtCore.SIGNAL('KPSetup is failed'))
            return
        self.connect(self.kpInstance, QtCore.SIGNAL('Note stacked'), self._moneyReceived)
        self.isInitialised=True
        self.emit(QtCore.SIGNAL('KPSetup is OK'), self.kpInstance)   
              
    def _getKPInstance(self):

        if self.kpmodel=='NV-9':
            self.kpInstance=KPNV9()
            
        if self.kpInstance is not None: # and type(self.kpInstance)==type(KPInstance):
            self.start()
        else:    
            raise Exception ('KP is not found')

    def _moneyReceived(self, money):
        self.emit(QtCore.SIGNAL('Money received'), money)

        
        
   

            
        
        


   
        
        

        
        