# -*- coding:utf-8 -*-
from abc import abstractmethod
class DB(object):
    '''
    Абстрактный класс, наследники которого реализуют считывание данных из разных источников: файл, XML, SQL...
    '''

    #__metaclass__ = ABCMeta
    
    @abstractmethod
    def getGPIOPinSettigs(self):
        raise NotImplementedError
    
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
    

    
    