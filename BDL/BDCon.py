# -*- coding:utf-8 -*-

from DataSources import MySQLDB, TestDb
from Errors import Errors

class BDCon():
    '''
    Класс выполняет подключение к выбранному типу базы данных
    в зависимости от параметра typeDB
    '''

    def __init__(self, path):
        if path=='TestDB':
            self.dbContext=TestDb.TestDb()
        elif path=='SQLDB':
            self.dbContext=MySQLDB.MySQLDB()
        else:
            self.message=Errors(u'Нет предметов к продаже')
            self.message.window.setWindowTitle(u'Сообщение')
            self.message.window.show()
        
     

    
    
