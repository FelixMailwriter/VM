# -*- coding:utf-8 -*-

from HdWareCon.MagEng import MagEng
from HdWareCon.Pin import Pin

class Magazin():
    '''
    Класс описывает сущность магазина предметов. 
    Включает в себя мотор привода, датчик наличия предметов и тип предметов
    '''

    def __init__(self, num, pinEngPower, pinEngSensor, pinEmptySensor, itemId):
        print 'Инициализация магазина№ %s' %(num)
        self.num=num                                        #Номер магазина
        self.magEng=MagEng(pinEngPower, pinEngSensor)       #Двигатель магазина
        self.emptySensor=pinEmptySensor                     #Датчик опорожнения магазина
        self.itemId=itemId                                  #Id экземпляра предмета, загруженного в магазин
        print 'Инициализация магазина№ %s выполнена' %(num)
        
    def reset(self):
        print 'Инициализация магазина№ %s' %(self.num)
        MagEng.reset(self)
        print 'Инициализация магазина№ %s выполнена' %(self.num)    
       
    def isEmpty(self, defaultVal):
        if defaultVal==None:
            return Pin.getSignal(self.emptySensor)
        else: return defaultVal
        
    def giveOutItem(self, item):
        if item.id==self.itemId:
            print 'Магазин %s Начало выдачи предмета %s' %(self.num, str(item))
            self.magEng.motorRotate()
            return self
        return None
    
    def stopOutingItem(self):
        self.magEng.stopEngine()
        print 'Мотор остановлен'
        
    def __str__(self):
        return 'Магазин№%s EngPwPin= %s  EngSensorPin= %s  EmptySensorPin= %d Item= %s'\
            %(self.num, self.magEng.engPin, self.magEng.sensorPin, self.emptySensor, str(self.itemId))



        
        