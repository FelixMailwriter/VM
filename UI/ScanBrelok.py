# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject, QStringList, QPixmap, QIcon
from PyQt4 import QtCore, uic
from PyQt4.QtCore import QTimer
from UI.CheckPass import CheckPass
from ConfigParser import ConfigParser
import Common.Settings as Settings
from Errors import Errors

class ScanBrelok(QObject):
    '''
    Класс описывает окно сканирования брелка клиента
    '''
    
    def __init__(self):
        QObject.__init__(self)
        
        path=os.path.abspath("UIForms//ScanBrelok.ui")
        self.window = uic.loadUi(path)
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        self.translate=Settings.Translate()
        self.settings=self._getSettings()
        self.defaultLanguage=u'Русский'
        
        #self.window.lbl_fail.hide()
        self.window.lbl_scan.hide()
        self.connect(self.window.btn_scan, QtCore.SIGNAL("clicked()"), self.scanHandler)
        self.connect(self.window.btn_ScanOK, QtCore.SIGNAL("clicked()"), self.scanOKHandler) #Test
        self.window.btn_exit.clicked.connect(self._closeApp)
        self.window.cmbx_lang.currentIndexChanged.connect(self._changeLocale)
        self.timer=None
        self.clickCounter=0
        
        self._setLang()
   
    def _setLang(self):
        LangList=QStringList()
        LangList.append(u'English')
        LangList.append(u'Русский')
        LangList.append(u'Română')
        self.window.cmbx_lang.addItems(LangList)
        name=self.defaultLanguage
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
        self.window.lbl_pressBtnScan1.show()
        self.window.lbl_pressBtnScan2.show()
        self.window.lbl_scan.hide()
        #self.window.lbl_fail.hide()
        self.window.btn_scan.setEnabled(True) 
        
        self.window.lbl_pressBtnScan1.setText(_(u'Press the button \"Scan\"'))
        self.window.lbl_pressBtnScan2.setText(_(u'and enclose your key'))
        self.window.lbl_pressBtnScan3.setText(_(u'to the scanner'))
        self.window.lbl_scan.setText(_(u'Scanning...'))
        #self.window.lbl_fail.setText(_(u'Error!'))
        self.window.btn_scan.setText(_(u'Scan'))

    def _changeLocale(self):
        global _
        langCode=''
        lang=self.window.cmbx_lang.currentText()
        if lang==u'Русский':
            langCode='ru_RU'
        elif lang==u'English':
            langCode='en_US'
        elif lang==u'Română':
            langCode='ro_RO'
        self.translate.setLang(langCode)
        _=Settings._
        self._setLabels()        
                                       
    def scanHandler(self):
        self.window.lbl_scan.show()
        self.window.btn_scan.setEnabled(False)
        self.window.lbl_pressBtnScan1.hide()
        self.window.lbl_pressBtnScan2.hide()
        self.window.lbl_pressBtnScan3.hide()
        #self.window.lbl_fail.hide()
        self.emit(QtCore.SIGNAL("ScanBrelok"))
         
    
    def scanFail(self):
        self.window.lbl_scan.hide()
        #self.window.lbl_fail.show()
        #QtCore.QTimer.singleShot(5000, self._setLabels)#self.refresh)
        self.errWindow=Errors(u'Error', 5000)
        self.errWindow.window.show()
        self._setLabels()

    def refresh(self):
        self.window.lbl_pressBtnScan1.show()
        self.window.lbl_pressBtnScan2.show()
        self.window.lbl_scan.hide()
        #self.window.lbl_fail.hide()
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
        
    def _getSettings(self):
        filename='config.ini'
        section='lang'
        parser=ConfigParser()
        parser.read(filename)
        prn_config={}
        if parser.has_section(section):
            items=parser.items(section)
            for item in items:
                prn_config[item[0]]=item[1]
        else:
            self._setDefaultSettings()
        self.defaultLanguage=prn_config['default_lang']
        
    def _setDefaultSettings(self):
        self.defaultLanguage='English'
        
    #======TEST======
    def scanOKHandler(self):
        self.emit(QtCore.SIGNAL("SimulateScanOK"))  
          