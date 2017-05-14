# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject, QStringList, QImage, QPixmap, QIcon
from PyQt4 import QtCore, uic
import gettext
#gettext.install('ru', './locale', unicode=True)
#gettext.install('ro', './locale', unicode=True)
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
        self.window.cmbx_lang.currentIndexChanged.connect(self._changeLocale)
        self._changeLocale()
    
    def _setLang(self):
        #cmbx=QComboBox()
        LangList=QStringList()
        LangList.append(u'English')
        LangList.append(u'Русский')
        LangList.append(u'Română')
        self.window.cmbx_lang.addItems(LangList)
        name=str(u'English')
        index=self.window.cmbx_lang.findText(name)
        self.window.cmbx_lang.setCurrentIndex(index)
        self._setLangIcons() 
        
    def _setLangIcons(self):
        itemcount=self.window.cmbx_lang.count()
        for i in range(0, itemcount+1):
            if self.window.cmbx_lang.itemText(i)==u'English':
                path='./Resources/FlagsIcons/USA.png'
            elif self.window.cmbx_lang.itemText(i)==u'Русский':
                path='./Resources/FlagsIcons/Russia.png'
            elif self.window.cmbx_lang.itemText(i)==u'Română':
                path='./Resources/FlagsIcons/Moldova.png'
            img=QPixmap()
            img.load(path)
            icon=QIcon(img)
            self.window.cmbx_lang.setItemIcon(i,icon) 
                
    
    def _setLabels(self):
        self.window.lbl_pressBtnScan1.setText(_(u'Press the button \"Scan\"'))
        self.window.lbl_pressBtnScan2.setText(_(u'and enclose your key to the scanner'))
        self.window.lbl_scan.setText(_(u'Scanning...'))
        self.window.lbl_fail.setText(_(u'Scanning failed'))
        self.window.btn_scan.setText(_(u'Scan'))

    def _changeLocale(self):
        lang=self.window.cmbx_lang.currentText()
        if lang==u'Русский':
            gettext.install('ru', './locale', unicode=True) 
        elif lang==u'English':
            gettext.install('en', './locale', unicode=True)
        elif lang==u'Română':
            gettext.install('ro', './locale', unicode=True)
        self._setLabels()        
            
        
                               
    def scanHandler(self):
        self.window.btn_scan.setEnabled(False)
        self.window.lbl_pressBtnScan1.hide()
        self.window.lbl_pressBtnScan2.hide()
        self.window.lbl_scan.show()
        self.window.lbl_fail.hide()
        self.emit(QtCore.SIGNAL("ScanBrelok"))
         
    
    def scanFail(self):
        self.window.lbl_pressBtnScan1.show()
        self.window.lbl_pressBtnScan2.show()
        self.window.lbl_scan.hide()
        self.window.lbl_fail.show()
        QtCore.QTimer.singleShot(2000, self.refresh)

    def refresh(self):
        self.window.lbl_pressBtnScan1.show()
        self.window.lbl_pressBtnScan2.show()
        self.window.lbl_scan.hide()
        self.window.lbl_fail.hide()
        self.window.btn_scan.setEnabled(True)    
        
    #======TEST======
    def scanOKHandler(self):
        self.emit(QtCore.SIGNAL("SimulateScanOK"))    