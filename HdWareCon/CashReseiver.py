# -*- coding:utf-8 -*-
from PyQt4 import QtCore
class MyClass(object):
    '''
    Класс описывает сущность купюроприемника
    '''

    def __init__(self, params):
        self.isActive=False

    def activate(self):
        pass
     
     
     
class CashReceiveCycle(QtCore.QThread):
    '''
    Класс описывает цикл приема суммы денег
    ''' 
    def __init__(self):  
        self.isActive=True
        self.inputSumm=0
        
        
        
        
    