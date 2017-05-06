# -*- coding:utf-8 -*-

from PyQt4 import QtGui
import mysql.connector as DbConnector
from mysql.connector import Error
import base64
from ConfigParser import ConfigParser
from Errors import Errors
from DB import DB
from datetime import datetime


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
            conn=DbConnector.connect(**dbconfig)        
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
    
    def getDataFromDb(self, query, type='all'):
        conn = cur = None
        try:
            conn=self.getConnection()
            cur=conn.cursor()
            cur.execute(query)
            if type=='all':
                result = cur.fetchall()
            if type=='one':
                result=cur.fetchone()            
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
    
    def getIdItemsinMagazinsMap(self, magQty=6):
        query='Select idMagazins, ItemId from Magazins Where ItemQTY>0'
        result=self.getDataFromDb(query)
        
        #itemMap=self._fillMagEmptyItems(magQty)
        itemMap={}
        for row in result:
            magId=row[0]
            itemId=row[1]
            itemMap[magId]=itemId
        return itemMap

    def getItemsForSale(self):
        query='Select M.ItemId, I.ItemName, I.ItemPrice, I.ItemIcon, sum(M.ItemQTY) as summa from Magazins as M'+\
                ' left join Items as I'+\
                ' on M.itemId=I.IdItem'+\
                ' where I.hidden=False'+\
                ' group by M.ItemId'+\
                ' having summa>0'
        itemsList=self.getDataFromDb(query)
        return itemsList
    
    def getItemPictureById(self, itemId):
        query='Select ItemIcon from Items Where idItem=%d' %(itemId)
        result=self.getDataFromDb(query, 'one')
        pic=result[0]
        qpixmap=QtGui.QPixmap()
        if pic is not None:
            picBytes = base64.b64decode(pic)
            qpixmap.loadFromData(picBytes)
        return qpixmap
    
    def writeLog(self, logMessages):#eventType, source, event):
        for logMessage in logMessages:
            priority=logMessage.priority
            source=logMessage.sourse
            event=logMessage.message
            query='Insert into Log (EventType, Source, EventDate, Event)'+\
                ' values (\'%s\', \'%s\', \'%s\', \'%s\')' \
                %(priority, source, str(datetime.now()), event)
            self.insertDataToDB(query) 
    
    def sellItem(self, magazin, item):
        #Уменьшение количества предметов в магазине
        # Получаем текущее количество предметов в магазине
        query='Select ItemQty from Magazins where idMagazins=%d' %(magazin.num)
        result=self.getDataFromDb(query, 'one') 
        if len(result)==0 :
            self._showError(u'Ошибка', u'Ошибка выборки из базы данных')
            return
        qty=int(result[0])-1
        #Обновляем данные в магазине
        query='Update Magazins SET ItemQty=%d where idMagazins=%d' %(qty, magazin.num)
        self.insertDataToDB(query)
        
        #Запись в журнал продаж
        query='Insert into Sales (saleDate, saledItemId, price)'+\
                ' VALUES (\'%s\', %d, %d)' %(datetime.now(), item.id, item.price)
        self.insertDataToDB(query)
               
    def _showError(self, header, message): 

        self.message=Errors(message)
        self.message.window.setWindowTitle(header)
        self.message.window.show()   
        
        