# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject, QStringList
from PyQt4 import QtCore, uic

class ScanBrelok(QObject):
    '''
    Класс описывает окно сканирования брелка клиента
    '''


    def __init__(self):
        path=os.path.abspath("UIForms//ScanBrelok.ui")
        QObject.__init__(self)
        self.window = uic.loadUi(path)
        self._setLang()
        self.window.lbl_fail.hide()
        self.window.lbl_scan.hide()
        self.connect(self.window.btn_scan, QtCore.SIGNAL("clicked()"), self.scanHandler)
        self.connect(self.window.btn_ScanOK, QtCore.SIGNAL("clicked()"), self.scanOKHandler) #Test
        self.window.cmbx_lang.currentIndexChanged.connect(self._setLabels)
        self._setLabels()
    
    def _setLang(self):
        #cmbx=QComboBox()
        LangList=QStringList()
        LangList.append(u'English')
        LangList.append(u'Русский')
        LangList.append(u'Украiньська')
        self.window.cmbx_lang.addItems(LangList)
        name=str(u'English')
        index=self.window.cmbx_lang.findText(name)
        self.window.cmbx_lang.setCurrentIndex(index) 
    
    def _setLabels(self):
        self.window.lbl_pressBtnScan1.setText(tr(u'Press the button \"Scan\"'))
        self.window.lbl_pressBtnScan2.setText(u'and enclose your key to the scanner')
        self.window.lbl_scan.setText(u'Scanning...')
        self.window.lbl_fail.setText(u'Scanning failed')
        self.window.btn_scan.setText(u'Scan')

        
                               
    def scanHandler(self):
        self.window.btn_scan.setEnabled(False)
        self.window.label.hide()
        self.window.label_2.hide()
        self.window.lbl_scan.show()
        self.window.lbl_fail.hide()
        self.emit(QtCore.SIGNAL("ScanBrelok"))
         
    
    def scanFail(self):
        self.window.label.show()
        self.window.label_2.show()
        self.window.lbl_scan.hide()
        self.window.lbl_fail.show()
        QtCore.QTimer.singleShot(2000, self.refresh)

    def refresh(self):
        self.window.label.show()
        self.window.label_2.show()
        self.window.lbl_scan.hide()
        self.window.lbl_fail.hide()
        self.window.btn_scan.setEnabled(True)    
        
    #======TEST======
    def scanOKHandler(self):
        self.emit(QtCore.SIGNAL("SimulateScanOK"))    