# -*- coding:utf-8 -*-

from DataSources import MySQLDB, TestDb
from enum import __repr__

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
            raise DbConnectionException(u'Тип подключения не существует')
        
     

    
    
