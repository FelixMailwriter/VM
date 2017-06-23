# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject
from PyQt4 import QtCore, uic
from PyQt4.QtCore import QTimer
import Common.Settings as Settings
from Errors import Errors

class WriteBrelok(QObject):
    '''
    Класс описывает окно записи брелка
    '''


    def __init__(self):
        QObject.__init__(self)
        path=os.path.abspath("UIForms//WriteBrelok.ui")
        self.window = uic.loadUi(path)
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        global _
        _= Settings._
        
        self._setLabels()
        
        self.connect(self.window.btn_write, QtCore.SIGNAL("clicked()"), self.writeHandler)
        self.connect(self.window.btn_simWriteOk, QtCore.SIGNAL("clicked()"), self.writeOKHandler) #Test      
        
    def _setLabels(self):
        self.timer=QTimer()
        self.timer.timeout.connect(self._backToTitlePage)
        self.timer.start(60000)  
               
        self.window.lbl_msg.setText(_(u'The key is given away'))
        self.window.label.setText(_(u'Press \'Next\''))
        self.window.label_2.setText(_(u'and enclose it to the scanner'))
        self.window.lbl_write.setText(_(u'Writing...'))
        self.window.lbl_write.hide()
        #self.window.lbl_fail.setText(_(u'Writing failed!'))
        #self.window.lbl_fail2.setText(_(u'Try again, please.'))
        self.window.btn_write.setText(_(u'Write'))
        self.window.label.show()
        self.window.label_2.show()
        self.window.lbl_write.hide()
        print 'btn_write true'
        self.window.btn_write.setEnabled(True)
        
    def writeHandler(self):
        self.timer.stop()
        #self.timer=QTimer()
        #self.timer.timeout.connect(self._backToTitlePage)
        #self.timer.start(60000)
        self.window.btn_write.setEnabled(False)
        self.window.label.hide()
        self.window.label_2.hide()
        self.window.lbl_write.show()
        self.emit(QtCore.SIGNAL("WriteBrelok"))

    def writeFail(self):
        #self.timer.stop()
        self.window.label.show()
        self.window.label_2.show()
        self.window.lbl_write.hide()
        self.errWindow=Errors(u'Error', 5000)
        self.errWindow.window.show()
        self._setLabels()
        print 'setLabels'
        #self.timer=QTimer()
        #self.timer.timeout.connect(self._backToTitlePage)
        #self.timer.start(60000)

    def _backToTitlePage(self):
        self.timer.stop()
        self.emit(QtCore.SIGNAL("TimeOutPage"), self.window)
#=====TEST=====
    
    def writeOKHandler(self):
        self.emit(QtCore.SIGNAL("SimulateWriteOK"))
        
        
