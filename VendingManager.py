# -*- coding:utf-8 -*-
from PyQt4.Qt import QObject
from PyQt4 import QtCore
import Vending


class VendingManager(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._start()
        
    def _start(self):
        #self.vending=None
        self.vending=Vending.Vending(0)
        self._connectionSignals()
        self.vending.start()
            
    def _connectionSignals(self):
        self.connect(self.vending, QtCore.SIGNAL('Restart'), self._start)
        self.connect(self.vending, QtCore.SIGNAL('End working'), self._start)