# -*- coding:utf-8 -*-
from abc import abstractmethod, ABCMeta
from PyQt4.Qt import QObject

class KPInstance():
    #абстрактный класс моделей купюроприемников
    
    __metaclass__ = ABCMeta
    
    def __init__(self):
        #QObject.__init__(self)
        pass
    
    @abstractmethod
    def setup(self):
        raise NotImplementedError
    
    @abstractmethod
    def enable(self):
        raise NotImplementedError
    
    @abstractmethod
    def disable(self):
        raise NotImplementedError 