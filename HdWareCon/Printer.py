# -*- coding:utf-8 -*-
import PyQt4
from PyQt4 import QtGui
import os



class Printer():
    '''
    Класс описывает сущность Принтера
    '''


    def __init__(self):
        self.dirPath="/home/arama/PrintedChecks"
        if not os.path.isdir(self.dirPath):
            os.mkdir(self.dirPath)
        #self.filename = "/home/print.txt"
        
    def printCheck(self, **params):
        self.makeCheckContext(params)

        
    def makeCheckContext(self, params):
        data=params.get("Data")
        #time=params.get("Time")
        itemName=params.get("ItemName")
        price=params.get("Price")
        context=""
        context+="Дата покупки %s \n" %(data)#, time)
        context+="Название: %s \n" %(itemName)            
        context+="Цена: %s \n" %(price)
        self._printOut(params, context)
        
    def _printOut(self, params, context):
        fileName=params.get("Data")#, params.get("Time")) 
        path=self.dirPath+"/"+fileName
        checkText=QtGui.QTextBrowser()
        checkText.setText(context)        
        with open(path, "w") as checkFile:
            checkFile.write(context)
        printer=QtGui.QPrinter()
        checkText.print_(printer)
        
        
        
