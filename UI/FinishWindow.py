# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject
from PyQt4 import QtCore, uic
from PyQt4.QtGui import QPixmap
import gettext

class FinishWindow(QObject):

    '''
    Класс описывает финальное окно приложения
    '''
    def __init__(self):
        QObject.__init__(self)
        path=os.path.abspath("UIForms//FinishWindow.ui")
        self.window = uic.loadUi(path)
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self._setLabels()
        QtCore.QTimer.singleShot(5000, self.finish)
        label=QPixmap('./Resources/Forms/ScanBrelok/Success.png')
        self.window.lbl_pix.setPixmap(label)
        
    def finish(self):
        self.window.close()
        self.emit(QtCore.SIGNAL("FinishProc"))
        
    def _setLabels(self):
        
        self.window.label.setText(_(u"The key was written successfully"))
        self.window.label_2.setText(_(u"Thanks for purchase"))
        