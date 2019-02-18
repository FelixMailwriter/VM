# -*- coding:utf-8 -*-

from PyQt4 import QtGui
import sys
#import Vending
import logging
from VendingManager import VendingManager



if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    filehandler = logging.FileHandler('logs.log')
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(filehandler)

    app=QtGui.QApplication(sys.argv)
  
    VM=VendingManager()
    sys.exit(app.exec_())
    
