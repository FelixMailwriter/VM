# -*- coding:utf-8 -*-
import os
import sys
import locale
from PyQt4.Qt import QObject, QStringList, QPixmap, QIcon
from PyQt4 import QtCore, uic
from PyQt4.QtCore import QTimer
import gettext
from UI.CheckPass import CheckPass

class ScanBrelok(QObject):
    '''
    Класс описывает окно сканирования брелка клиента
    '''
    
    def __init__(self):
        QObject.__init__(self)
        
        path=os.path.abspath("UIForms//ScanBrelok.ui")
        self.window = uic.loadUi(path)
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        self.window.lbl_fail.hide()
        self.window.lbl_scan.hide()
        self.connect(self.window.btn_scan, QtCore.SIGNAL("clicked()"), self.scanHandler)
        self.connect(self.window.btn_ScanOK, QtCore.SIGNAL("clicked()"), self.scanOKHandler) #Test
        self.window.btn_exit.clicked.connect(self._closeApp)
        self.window.cmbx_lang.currentIndexChanged.connect(self._changeLocale)
        self.timer=None
        self.clickCounter=0
        
        self._setLang()
        
    def lang_init(self, loc=''):
        if loc=='':
            _locale, _encoding = locale.getdefaultlocale()  # Default system values
        else:
            _locale=loc
            
        path = os.path.abspath(sys.argv[0])
        d=gettext.textdomain()
        gettext.install(d, unicode=True, codeset='utf-8')
        path = os.path.join(os.path.dirname(path),'locale')
        lang = gettext.translation(d, path, [_locale])

        return lang.ugettext
        
    def _setLang(self):
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
        global _
        lang=self.window.cmbx_lang.currentText()
        if lang==u'Русский':
            _ = self.lang_init('ru_RU')
        elif lang==u'English':
            _ = self.lang_init('en_US')
        elif lang==u'Română':
            _ = self.lang_init('ro_RO')
        self._setLabels()        
                                       
    def scanHandler(self):
        self.window.lbl_scan.show()
        self.window.btn_scan.setEnabled(False)
        self.window.lbl_pressBtnScan1.hide()
        self.window.lbl_pressBtnScan2.hide()
        self.window.lbl_fail.hide()
        self.emit(QtCore.SIGNAL("ScanBrelok"))
         
    
    def scanFail(self):
        self.window.lbl_pressBtnScan1.show()
        self.window.lbl_pressBtnScan2.show()
        self.window.lbl_scan.hide()
        self.window.lbl_fail.show()
        QtCore.QTimer.singleShot(3000, self.refresh)

    def refresh(self):
        self.window.lbl_pressBtnScan1.show()
        self.window.lbl_pressBtnScan2.show()
        self.window.lbl_scan.hide()
        self.window.lbl_fail.hide()
        self.window.btn_scan.setEnabled(True) 
        
    def _closeApp(self):
        if self.timer is None:
            self.timer=QTimer()
            self.timer.timeout.connect(self._resetCounter)
            self.timer.start(7000)
        self.clickCounter+=1
        if self.clickCounter>5:
            self._enterPass()
           
    def _resetCounter(self):
        self.clickCounter=0
        self.timer=None
        
    def _enterPass(self):   
        self.windowPass=CheckPass()
        self.windowPass.window.show()
        
    #======TEST======
    def scanOKHandler(self):
        self.emit(QtCore.SIGNAL("SimulateScanOK"))  
          