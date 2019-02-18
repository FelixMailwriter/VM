# -*- coding:utf-8 -*-
import logging
import time
from PyQt4 import QtCore
from PyQt4.Qt import QObject
from HdWareCon.Pin import Pin
from SensorListener import SensorListener
import Common.Error as Error
import Common.Settings as Settings


class Programmator(QObject):

    def __init__(self, pins):  # keytype):
        QObject.__init__(self)

        global _
        _ = Settings._

        global logger
        logger = logging.getLogger(__name__)

        self.TRY_COUNT_INIT = 3  # Quantity of initialisation tries
        self.TRY_COUNT_READ_KEY = 5  # Quantity of reading tries
        self.TRY_COUNT_MODE_SWITCH = 5  # Quantity of mode switch tries (read -> write and write -> read)
        self.pinSwitcher = Pin(pins['Button'], 'OUT')  # Mode switch button
        self.ledYellow = Pin(pins['Yellow'], 'IN')
        self.ledGreen = Pin(pins['Green'], 'IN')
        self.pinPower = Pin(pins['Power'], 'OUT')

        logger.info('Programmator has been created.')


    def init(self):
        logger.info("--- Programmator init procedure started ---")

        self.green_work = False  # Flag of green led lighting
        self.yellow_work = False  # Flag of yellow led lighting
        self.green_shoots = 0  # Quantity of blinks of green led

        # Switch the programmator
        self.pinPower.enable()
        time.sleep(1)
        # Press out the main switch button
        self.pinSwitcher.enable()

        # checking if the device works properly

        trycount = 0
        while (trycount < self.TRY_COUNT_INIT):
            #print '\n---- Try init {} ----'.format(trycount)
            logger.info("\n---- Try init {} ----".format(trycount))

            self.pinSwitcher.disable()  # Switch read-mode by pressing main button
            time.sleep(1)
            self.green_work = self.ledGreen.getSignal()
            self.yellow_work = self.ledYellow.getSignal()

            #print 'GreenWork={}; YellowWork={}'.format(self.green_work, self.yellow_work)
            logger.info('GreenWork={}; YellowWork={}'.format(self.green_work, self.yellow_work))
            if self.green_work and self.yellow_work:  # if both green and yellow leds are on
                #print 'Programmator OK'
                logger.info("Proggrammator OK")
                self.pinSwitcher.enable()
                return True
            else:
                trycount += 1
                self.green_work = False
                self.yellow_work = False
                self.pinSwitcher.enable()
                time.sleep(1)

        if trycount >= self.TRY_COUNT_INIT:
            #print 'Programmator failed'
            logger.critical("Proggrammator FAILED")
            err_level = Error.ErrorLevel.CRITICAL
            err_source = Error.ErrorSource.PROGRAMMATOR
            msg = _(u"Programmator init error")
            err = Error.Error(err_level, err_source, msg)
            self.emit(QtCore.SIGNAL("HardwareFailed"), err)


        self.green_work = False
        self.yellow_work = False
        #print '==== Prg init finished ===='
        logger.info('==== Prg init finished ====')


    def readKey(self):
        trycount = 0
        # checking if green led is on. It mustn't light, if it id so - trying to switch it off
        while self.ledGreen.getSignal() and trycount < self.TRY_COUNT_MODE_SWITCH:
            self._buttonClick(self.pinSwitcher, 1)
            trycount += 1
            time.sleep(1)

        # if we couldn't to switch green led off - programmator is broken
        if self.ledGreen and trycount >= self.TRY_COUNT_MODE_SWITCH:
            #print 'Programmator failed in switching on read mode. Restarting...'
            logger.error('Programmator failed in switching on read mode. Restarting...')
            msg = _(u"Programmator failed in switching on read mode.")
            self._demandRestart(msg)


        trycount = 0
        # checkin if yellow led is on during read process. It must be on.
        while trycount < self.TRY_COUNT_READ_KEY and self.ledYellow:
            #print '\n--- Try read {} ---'.format(trycount)
            logger.info('\n--- Try read {} ---'.format(trycount))
            # start thread for counting blinks of green led during 3 sek.
            self.greenled_listener = SensorListener(self.ledGreen, self._set_green_shoots, 3000)
            self.greenled_listener.start()
            self.greenled_listener.wait()
            #print 'Shoots = {}'.format(self.green_shoots)
            logger.info('Shoots = {}'.format(self.green_shoots))
            # green led must blink 1 time per 3 sec. Not more then 3 times
            if self.green_shoots > 1 and self.green_shoots < 3:
                #print 'Read OK'
                logger.info('Key read OK')
                self.emit(QtCore.SIGNAL("ScanFinished"), True)
                return True
            # if it blinks many times - read process has failed
            else:
                self.green_shoots = 0
                trycount += 1
                #print '--------'

        #print 'Read FAILED!!!'
        logger.warning('Read FAILED!!!')
        self.emit(QtCore.SIGNAL("ScanFinished"), False)
        return False


    def prepareForWritingKey(self):
        # prepare programmator for writing process
        trycount = 0
        # green led must be on. If it is not so - trying to switch it on by pressing main button.
        while (not self.ledGreen.getSignal()) and trycount < self.TRY_COUNT_MODE_SWITCH:
            self._buttonClick(self.pinSwitcher, 1)
            trycount += 1
            time.sleep(1)

        if (not self.ledGreen.getSignal()) and trycount >= self.TRY_COUNT_MODE_SWITCH:
            #print 'Programmator failed in switching on write mode. Restarting...'
            logger.error('Programmator failed in switching on write mode. Restarting...')
            msg = _(u"Programmator failed in switching on write mode")
            self._demandRestart(msg)


    def checkWriting(self):
        # after writing yellow led must be off
        #TODO begin checking from here
        if self.ledYellow.getSignal():
            #print 'Writing error'
            logger.error('Key writing error')
            self.emit(QtCore.SIGNAL("WriteFinished"), False) # Writing failed

        # starting thread for counting green led blinks for 1 sek
        self.greenled_listener = SensorListener(self.ledGreen, self._set_green_shoots, 1000)
        self.greenled_listener.start()
        self.greenled_listener.wait()

        # green led must be on, no blinks. If blinks - writinf has failed
        if self.green_shoots == 0 and self.ledGreen.getSignal():
            logger.info("Write checking is successful.")
            self.emit(QtCore.SIGNAL("WriteFinished"), True)
        else:
            logger.error("Write checking is failed. Key was written with error.")
            self.emit(QtCore.SIGNAL("WriteFinished"), False)
        self.green_shoots = 0


    def _demandRestart(self, msg):
        err_level = Error.ErrorLevel.IMPORTANT
        err_source = Error.ErrorSource.PROGRAMMATOR
        err = Error.Error(err_level, err_source, msg)
        logger.warning("Printer restarting")
        self.pinPower.disable()  # Switch off the programmator
        time.sleep(1)
        self.emit(QtCore.SIGNAL("DemandRestart"), err)


    def _buttonClick(self, pin, holdtime=0.5):
        pin.disable()
        time.sleep(holdtime)
        pin.enable()


    def _getPins(self):
        pins = {}
        pins['Button'] = 17
        pins['Yellow'] = 27
        pins['Green'] = 22
        pins['Power'] = 0
        return pins


    def _set_green(self, value):
        self.green_work = value


    def _set_yellow(self, value):
        self.yellow_work = value


    def _set_green_shoots(self, value):
        self.green_shoots = value



