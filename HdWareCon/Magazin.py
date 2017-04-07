# -*- coding:utf-8 -*-

from HdWareCon.MagEng import MagEng
from HdWareCon.Pin import Pin

#from Common.Item import Item

class Magazin():
    '''
    Класс описывает сущность магазина предметов. 
    Включает в себя мотор привода, датчик наличия предметов и тип предметов
    '''

    def __init__(self, num, pinEngPower, pinEngSensor, pinEmptySensor, item):
        print 'Инициализация магазина№ %s' %(num)
        self.num=num                                        #Номер магазина
        self.magEng=MagEng(pinEngPower, pinEngSensor)       #Двигатель магазина
        self.emptySensor=pinEmptySensor                     #Датчик опорожнения магазина
        self.item=item                                      #Экземпляр предметов, загруенных в магазин
        print 'Инициализация магазина№ %s выполнена' %(num)
        
    def reset(self):
        print 'Инициализация магазина№ %s' %(self.num)
        MagEng.reset(self)
        print 'Инициализация магазина№ %s выполнена' %(self.num)    
       
    def isEmpty(self, defaultVal):
        if defaultVal==None:
            return Pin.getSignal(self.emptySensor)
        else: return defaultVal
        
    def giveOutItem(self, itemId):
        if itemId==self.item.id:
            print 'Магазин %s Начало выдачи предмета %s' %(self.num, self.item)
            self.magEng.motorRotate()
            return self
        return None
        
    def __str__(self):
        return 'Магазин№%s EngPwPin= %s  EngSensorPin= %s  EmptySensorPin= %s Item= %s'\
            %(self.num, self.magEng.engPin, self.magEng.sensorPin, self.emptySensor, self.item)
     
     
      
        
        
        