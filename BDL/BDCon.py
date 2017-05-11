# -*- coding:utf-8 -*-

from DataSources import MySQLDB, TestDb
from Errors import Errors
import gettext

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
            self.message=Errors(_(u'There are no items to sell'))
            self.message.window.setWindowTitle(_(u'Message'))
            self.message.window.show()
        
     

    
    
