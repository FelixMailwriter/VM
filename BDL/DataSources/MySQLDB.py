# -*- coding:utf-8 -*-

from PyQt4 import QtGui
import mysql.connector
from mysql.connector import Error
import base64
from ConfigParser import ConfigParser
from Errors import Errors
from DB import DB
from Common.Item import Item

class MySQLDB(DB):


    def __init__(self):
        DB.__init__(self)
       
    def getGPIOPinSettigs(self):
        programmatorPinSettings={}
        programmatorPinSettings["ProgrammatorScan"]=9
        programmatorPinSettings["ProgrammatorScanOK"]=21
        programmatorPinSettings["ProgrammatorWrire"]=11
        programmatorPinSettings["ProgrammatorWriteOK"]=17

        magazinesPinSettings={}
        magazinesPinSettings[(1,"EngPw")]=27
        magazinesPinSettings[(1, "EngSensor")]=22
        magazinesPinSettings[(1, "EmptySensor")]=10
              
        magazinesPinSettings[(2,"EngPw")]=12
        magazinesPinSettings[(2, "EngSensor")]=16
        magazinesPinSettings[(2, "EmptySensor")]=5
                 
        magazinesPinSettings[(3,"EngPw")]=6
        magazinesPinSettings[(3, "EngSensor")]=13
        magazinesPinSettings[(3, "EmptySensor")]=19
        
        magazinesPinSettings[(4,"EngPw")]=14
        magazinesPinSettings[(4, "EngSensor")]=15
        magazinesPinSettings[(4, "EmptySensor")]=18
        
        magazinesPinSettings[(5,"EngPw")]=23
        magazinesPinSettings[(5, "EngSensor")]=24
        magazinesPinSettings[(5, "EmptySensor")]=25
               
        magazinesPinSettings[(6,"EngPw")]=8
        magazinesPinSettings[(6, "EngSensor")]=7
        magazinesPinSettings[(6, "EmptySensor")]=12
                 
        PinGetOutSensor=26
        return programmatorPinSettings, magazinesPinSettings, PinGetOutSensor
     
    def getConnection(self):
        conn=None
        dbconfig=self._getDBConfig(filename='config.ini', section='mysql') 
        try:
            conn=mysql.connector.connect(**dbconfig)
                
        except Error as e:
            self._showError(u'Ошибка', u'Ошибка подключения к базе данных')
            print (e)
            
        return conn
                    
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
            self._showError(u'Ошибка', u'Ошибка файла конфигурации БД. Отсутствует секция.')
        return config
    
    def getDataFromDb(self, query):
        conn = cur = None
        try:
            conn=self.getConnection()
            cur=conn.cursor()
            cur.execute(query)
            result = cur.fetchall()            
            return result
        except:
            self._showError(u'Ошибка', u'Ошибка подключения к базе данных')
            
        finally:
            if cur is not None: cur.close()
            if conn is not None: conn.close()  
            
    def insertDataToDB(self, query):
        conn = cur = None
        try:
            conn=self.getConnection()
            cur=conn.cursor()
            cur.execute(query)
            conn.commit()
            return True
            
        except:
            self._showError(u'Ошибка', u'Ошибка подключения к базе данных')
            return False
        finally:
            if cur is not None: cur.close()
            if conn is not None: conn.close() 
        
    def deleteDataFromTable(self, query):
        conn = cur = None
        try:
            conn=self.getConnection()
            cur=conn.cursor()
            cur.execute(query)
            conn.commit()
        except:
            self._showError(u'Ошибка', u'Ошибка подключения к базе данных')
            return False
        finally:
            if cur is not None: cur.close()
            if conn is not None: conn.close()
        return True  
    
    def getItemsMap(self, magQty=6):
        query='Select I.idItem, I.itemName, I.ItemPrice, M.idMagazins from Magazins as M, Items as I' +\
                ' Where M.ItemId=I.idItem'
        result=self.getDataFromDb(query)
        
        itemMap=self._fillMagEmptyItems(magQty)

        for row in result:
            itemId=row[0]
            itemName=row[1]
            itemPrice=row[2]/100.
            magNumber=row[3]
            item=Item(itemId, itemName, itemPrice)
            itemMap[magNumber]=item

        return itemMap
            
    def _fillMagEmptyItems(self, magQty):
        itemMap={}
        for i in range (0, magQty):
            itemId=0
            itemName='Пусто'
            itemPrice=0
            itemIcon=QtGui.QIcon("img//Items//NoItem.jpg")
            item=Item(itemId, itemName, itemPrice, itemIcon)
            itemMap[i]=item
        return itemMap 
            
    def _getIconById(self, pic):
        qpixmap=QtGui.QPixmap()
        if pic is not None:
            picBytes = base64.b64decode(pic)
            qpixmap.loadFromData(picBytes)
        return qpixmap                      

    
    def _showError(self, header, message): 

        self.message=Errors(message)
        self.message.window.setWindowTitle(header)
        self.message.window.show()   