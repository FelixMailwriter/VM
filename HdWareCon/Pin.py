# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import logging
GPIO.setmode(GPIO.BCM)


class Pin(object):
    '''
    Класс определяет PIN в разъеме GPIO платы Raspberry
    direction - направление подключения (IN-прием, OUT-передача)
    num - номер PIN на разъеме GPIO
    '''

    def __init__(self, num, direction, state=0):
        global logger
        logger = logging.getLogger(__name__)

        self.num = num
        self.state = state
        self.direction = direction
         #Конфигурируем пин на вход или на выход
        if self.direction=='IN':
           GPIO.setup(self.num, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        elif self.direction=='OUT':
           GPIO.setup(self.num, GPIO.OUT)
        logger.info('Pin %s сконфигурирован на %s' % (self.num, self.direction))
        #print u'Pin %s сконфигурирован на %s' % (self.num, self.direction)


    def enable(self):
        if self.direction == 'OUT':
            GPIO.output(self.num, True)
            self.state = 1
            logger.info('На PIN %s установлена 1' % (self.num))
            #print 'На PIN %s установлена 1' % (self.num)
        else:
            logger.info('Подать напряение невозможно: PIN  сконфигурирован на вход')
            #print 'Подать напряение невозможно: PIN  сконфигурирован на вход'


    def disable(self):
        if self.direction == 'OUT':
            #print 'PIN %s установлен 0' % (self.num)
            logger.info('PIN %s установлен 0' % (self.num))
            GPIO.output(self.num, False)
            self.state=0


    def getSignal(self):
        if self.direction == 'IN':
            self.state = GPIO.input(self.num)
            logger.info('С PIN ', self.num, ' считан сигнал: {}\n'.format(self.state))
            #print 'С PIN ', self.num, ' считан сигнал: {}\n'.format(self.state)
        return self.state


    def setSignal(self, signal):
        #print 'На сенсоре', self.num, 'установлен', signal
        logger.info('На сенсоре', self.num, 'установлен', signal)
        self.state = signal
        GPIO.output(self.num, signal)


    def toggle(self):
        if self.direction == 'OUT':
            self.state = not self.state
            GPIO.output(self.num,  self.state)


    def __str__(self):
        return 'Pin№ %s Direction=%s State=%s' % (self.num, self.direction, self.state)




