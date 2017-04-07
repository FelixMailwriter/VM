# -*- coding:utf-8 -*-
from abc import abstractmethod
class DB(object):
    '''
    Абстрактный класс, наследники которого реализуют считывание данных из разных источников: файл, XML, SQL...
    '''

    #__metaclass__ = ABCMeta
    @abstractmethod
    def getItemsMap(self):
        raise NotImplementedError