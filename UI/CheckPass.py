# -*- coding:utf-8 -*-
import os
import sys
from PyQt4 import QtCore, uic
from PyQt4.Qt import QObject
from ConfigParser import ConfigParser
from Common.ErrorScreen import Errors

class CheckPass(QObject):
    def __init__(self):
        QObject.__init__(self)
        path=os.path.abspath("UIForms//pass.ui")
        self.window = uic.loadUi(path)
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.config=self._getDBConfig(filename='config.ini', section='security') 
        
        self.window.btn_ok.clicked.connect(self._checkPass)
        
        
    def _getDBConfig(self, **param):
        filename=param['filename']
        section=param['section']
        parser=ConfigParser()
        parser.read(filename)
        config={}
        if parser.has_section(section):
            items=parser.items(section)
            for item in items:
                config[item[0]]=item[1]
        else:
            self._showError(_(u'Error'), _(u'There is errors in the configuration file. No section.'))
        return config       
        
    def _checkPass(self):
        if self.window.le_pass.text()==self.config['pass']:
            sys.exit()
        else:
            self.window.close()
            
    def _showError(self, header, message): 
        self.message=Errors(message)
        self.message.window.setWindowTitle(header)
        self.message.window.show() 
        
        