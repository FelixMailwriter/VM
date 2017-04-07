# -*- coding:utf-8 -*-
from Common.Item import Item
from DataSources import MySQLDB, TestDb
#import DataSources.TestDb as TestDb
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
    
             
        
class DbConnectionException(Exception):
    
    def __init__(self, value):
        self.value=value
        
    def __str___(self):
        return __repr__(self.value)
    
    
