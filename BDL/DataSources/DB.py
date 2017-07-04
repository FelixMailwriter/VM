# -*- coding:utf-8 -*-
from abc import abstractmethod
class DB(object):
    '''
    Абстрактный класс, наследники которого реализуют считывание данных из разных источников: файл, XML, SQL...
    '''

    #__metaclass__ = ABCMeta
    '''
    @abstractmethod
    def getGPIOPinSettigs(self):
        raise NotImplementedError
    '''
    
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
    
    @abstractmethod
    def getItemsMap(self):
        raise NotImplementedError
    
    @abstractmethod
    def getGPIOHdWSettigs(self):
        raise NotImplementedError
    
    @abstractmethod
    def getDataFromDb(self, query):
        raise NotImplementedError
    
    @abstractmethod
    def insertDataToDB(self, query):
        raise NotImplementedError
    
    @abstractmethod
    def deleteDataFromTable(self, query):
        raise NotImplementedError
    

    
    