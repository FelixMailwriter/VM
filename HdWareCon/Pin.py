# -*- coding:utf-8 -*-
#import RPi.GPIO as GPIO
#GPIO.setmode(BCM)
class Pin(object):
    '''
    Класс определяет PIN в разъеме GPIO платы Raspberry
    direction - направление подключения (IN-прием, OUT-передача)
    num - номер PIN на разъеме GPIO
    '''

    def __init__(self, num, direction, state=0):
        self.num=num
        self.state=state
        self.direction=direction
        #Конфигурируем пин на вход или на выход
        #if self.direction=='IN': 
        #    GPIO.setup(self.num, GPIO.IN)
        #    GPIO.setup(self.num, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
        #elif self.direction=='OUT':
        #    GPIO.setup(self.num, GPIO.OUT)
        #    GPIO.setup(self.num, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
        print u'Pin %s сконфигурирован на %s' %(self.num, self.direction)
    
    def enable(self):
        if self.direction=='OUT':
        #    GPIO.output(self.num,True)
            self.state=1
            print 'На PIN %s установлена 1' %(self.num)
        else: print 'Подать напряение невозможно: PIN  сконфигурирован на вход'
        
    def disable(self):
        if self.direction=='OUT':        
            print 'PIN %s установлен 0' %(self.num)
        #    GPIO.output(self.num, False)
        #    self.state=0
            
    def setSignal(self, signal):
        print 'На сенсоре' , self.num, 'установлен', signal
        self.state=signal
        
            
    def getSignal(self):
        if self.direction=='IN':
        #    self.state=GPIO.input(self.num)
            print 'С PIN ',self.num,' считан сигнал: ',self.state
        return self.state
                    
    def __str__(self):
        return 'Pin№ %s Direction=%s State=%s' %(self.num, self.direction, self.state)               

                     
                    
            
