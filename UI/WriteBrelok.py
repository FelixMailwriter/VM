# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject
from PyQt4 import QtCore, uic
from PyQt4.QtGui import QPixmap
from PyQt4.QtCore import QTimer
import Common.Settings as Settings

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
        self.window.lbl_write.hide()
        self.window.lbl_fail.hide()
        self.window.lbl_fail2.hide()
        self.connect(self.window.btn_write, QtCore.SIGNAL("clicked()"), self.writeHandler)
        self.connect(self.window.btn_simWriteOk, QtCore.SIGNAL("clicked()"), self.writeOKHandler) #Test
        label=QPixmap('./Resources/Forms/ScanBrelok/Success.png')
        #self.window.lbl_success.setPixmap(label)
        label=QPixmap('./Resources/Forms/ScanBrelok/Failure.png')
        #self.window.lbl_fail_2.setPixmap(label) 
        self.timer=QTimer()
        self.timer.timeout.connect(self._backToTitlePage)
        self.timer.start(60000)        
       
        
    def _setLabels(self):
        self.window.lbl_msg.setText(_(u'The key is given away'))
        self.window.label.setText(_(u'Press \'Next\''))
        self.window.label_2.setText(_(u'and enclose it to the scanner'))
        self.window.lbl_write.setText(_(u'Writing...'))
        self.window.lbl_fail.setText(_(u'Writing failed!'))
        self.window.lbl_fail2.setText(_(u'Try again, please.'))
        self.window.btn_write.setText(_(u'Write'))
        #self.window.lbl_success.show()
        #self.window.lbl_fail_2.hide()        
        self.window.label.show()
        self.window.label_2.show()
        self.window.lbl_write.hide()
        self.window.lbl_fail.hide()
        self.window.lbl_fail2.hide()
        self.window.btn_write.setEnabled(True)
        
    def writeHandler(self):
        self.timer.stop()
        self.timer=QTimer()
        self.timer.timeout.connect(self._backToTitlePage)
        self.timer.start(60000)
        self.window.btn_write.setEnabled(False)
        #self.window.lbl_success.show()
        #self.window.lbl_fail_2.hide()
        self.window.label.hide()
        self.window.label_2.hide()
        self.window.lbl_write.show()
        self.window.lbl_fail.hide()
        self.window.lbl_fail2.hide()
        self.emit(QtCore.SIGNAL("WriteBrelok"))

    def writeFail(self):
        self.timer.stop()
        #self.window.lbl_success.hide()
        #self.window.lbl_fail_2.show()       
        self.window.label.show()
        self.window.label_2.show()
        self.window.lbl_write.hide()
        self.window.lbl_fail.show()
        self.window.lbl_fail2.show()
        QtCore.QTimer.singleShot(5000, self._setLabels)
        self.timer=QTimer()
        self.timer.timeout.connect(self._backToTitlePage)
        self.timer.start(60000)

    def _backToTitlePage(self):
        self.timer.stop()
        self.emit(QtCore.SIGNAL("TimeOutPage"), self.window)
#=====TEST=====
    
    def writeOKHandler(self):
        self.emit(QtCore.SIGNAL("SimulateWriteOK"))
        
        
