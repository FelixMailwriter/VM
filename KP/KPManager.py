# -*- coding:utf-8 -*-
from PyQt4 import QtCore
from KPNV9 import KPNV9
from KP.KPCommon import KPInstance

class KPConnector(QtCore.QThread):
    #потоковый класс, реализующий процесс подключения и настройки параметров купюроприемника
    def __init__(self):
        QtCore.QThread.__init__(self)
        
        self.kpmodel=None
        self.kpInstance=None
        
    def getKPInstance(self, kpmodel):
        self.kpmodel=kpmodel
        if self.kpmodel=='NV-9':
            self.kpInstance=KPNV9()
            
        if self.kpInstance is not None: # and type(self.kpInstance)==type(KPInstance):
            self.start()
        else:    
            raise Exception ('KP is not found')
        
    def run(self):
        print 'kp initialising start'
        resultSetup=self.kpInstance.setup()
        if not resultSetup:
            self.emit(QtCore.SIGNAL('KPSetup is failed'))
            return
        self.emit(QtCore.SIGNAL('KPSetup is OK'), self.kpInstance)
        
    
    
class KPMoneyGetter(QtCore.QThread):
    #потоковый класс, реализующий процесс получения денег купюроприемником
    def __init__(self, master, kpInstance):
        QtCore.QThread.__init__(self)
        
        self.kpInstance=kpInstance
        self.connect(self.kpInstance, QtCore.SIGNAL('Note stacked'), self._moneyReceived)
        self.connect(master, QtCore.SIGNAL('KPStop'), self.kpInstance.disable)
        
    def run(self):
        self.kpInstance.enable()
    
    def _moneyReceived(self, money):
        print 'KPManager received signal value note'
        self.emit(QtCore.SIGNAL('Money received'), money)
        print 'KPManager seds signal value note'
            
        
        


   
        
        

        
        