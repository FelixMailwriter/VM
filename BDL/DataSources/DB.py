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
        programmatorPinSettings = {}
        programmatorPinSettings['Button'] = 4
        programmatorPinSettings['Yellow'] = 17
        programmatorPinSettings['Green'] = 27
        programmatorPinSettings['Power'] = 22

        magazinesPinSettings={}
        magazinesPinSettings[(1,"EngPw")] = 10
        magazinesPinSettings[(1, "EngSensor")] = 9
        magazinesPinSettings[(1, "EmptySensor")] = 11

        magazinesPinSettings[(2,"EngPw")] = 5
        magazinesPinSettings[(2, "EngSensor")] = 6
        magazinesPinSettings[(2, "EmptySensor")] = 13

        magazinesPinSettings[(3,"EngPw")] = 19
        magazinesPinSettings[(3, "EngSensor")] = 26
        magazinesPinSettings[(3, "EmptySensor")] = 21

        magazinesPinSettings[(4,"EngPw")] = 20
        magazinesPinSettings[(4, "EngSensor")] = 16
        magazinesPinSettings[(4, "EmptySensor")] = 12

        magazinesPinSettings[(5,"EngPw")] = 7
        magazinesPinSettings[(5, "EngSensor")] = 8
        magazinesPinSettings[(5, "EmptySensor")] = 25

        PinGetOutSensor = 15

        PinTrashValve = {}
        PinTrashValve["EngPw"] = 14
        PinTrashValve["Open"] = 23
        PinTrashValve["Close"] = 24

        #magazinesPinSettings[(6, "EmptySensor")] = 18

        return programmatorPinSettings, magazinesPinSettings, PinGetOutSensor, PinTrashValve
    
    @abstractmethod
    def getItemsMap(self):
        raise NotImplementedError
    
    # @abstractmethod
    # def getGPIOHdWSettigs(self):
    #     raise NotImplementedError
    
    @abstractmethod
    def getDataFromDb(self, query):
        raise NotImplementedError
    
    @abstractmethod
    def insertDataToDB(self, query):
        raise NotImplementedError
    
    @abstractmethod
    def deleteDataFromTable(self, query):
        raise NotImplementedError
    

    
    