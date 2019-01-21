# -*- coding:utf-8 -*-
from PyQt4 import QtCore
from threading import Thread

class SensorListener(QtCore.QThread):

    def __init__(self, sensorPin, callback, listenDuration=3000, delayStart=0, listenFreq=5):
        QtCore.QThread.__init__(self)
        self.sensorPin = sensorPin  # прослушиваемый Pin
        self.callback = callback  # функция обратного вызова
        self.listenDuration = listenDuration  # Продолжительность цикла прослушивания
        self.delayStart = delayStart  # задержка перед запуском прослушивания
        self.ListenFreq = listenFreq  # Частота опроса


    def run(self):
        print "Слушам датчик %s" % (self.sensorPin)
        self.msleep(self.delayStart)
        count_of_toggles = 0
        state = False
        duration = 0
        while duration < self.listenDuration:
            if state != self.sensorPin.getSignal():
                state = not state
                count_of_toggles += 1
            else:
                duration = duration + self.ListenFreq
                self.msleep(self.ListenFreq)
        print 'TimeOut датчика прослушивания. Срабатываний {}'.format(count_of_toggles/2)
        self.callback(count_of_toggles/2)


    # def run(self):
    #     print "\nСлушам датчик %s" % (self.sensorPin)
    #     cycle = 0
    #     self.msleep(self.delayStart)
    #     while cycle < self.cycles:
    #         duration = 0
    #         count_of_toggles = 0
    #         state = self.sensorPin.getSignal()
    #         while duration < self.cycleDuration:
    #             if state != self.sensorPin.getSignal():
    #                 state = not state
    #                 count_of_toggles += 1
    #                 if count_of_toggles / 2 == self.qty_of_shoot:
    #                     print '\nСрабатывание датчика %s. Выход из потока прослушивания' % (self.sensorPin)
    #                     self.callback(True)
    #                     return
    #             else:
    #                 duration = duration + self.ListenFreq
    #                 self.msleep(self.ListenFreq)
    #         cycle += 1
    #     print 'TimeOut датчика прослушивания %s. Выход из потока'
    #     self.callback(False)