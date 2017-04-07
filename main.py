# -*- coding:utf-8 -*-

from PyQt4 import QtGui
import sys
#import Vending
from VendingManager import VendingManager



if __name__ == '__main__':
    
    app=QtGui.QApplication(sys.argv)
  
    VM=VendingManager()
    sys.exit(app.exec_())
    
