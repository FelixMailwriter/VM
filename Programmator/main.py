# -*- coding:utf-8 -*-

import sys
#from PyQt4 import QtGui
from Pin import Pin
import time
from Programmator import Programmator

if __name__ == '__main__':
    #app = QtGui.QApplication(sys.argv)

    pin = Pin(26, 'OUT')
    pinIn = Pin(19, 'IN')

    pin.setSignal(True)
    time.sleep(1)
    pin.setSignal(False)

    prg = Programmator()


