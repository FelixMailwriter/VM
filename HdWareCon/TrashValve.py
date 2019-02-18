# -*- coding:utf-8 -*-
import logging
import time
from PyQt4 import QtCore
from PyQt4.Qt import QObject
from HdWareCon.Pin import Pin
from SensorListener import SensorListener
import Common.Error as Error
import Common.Settings as Settings

import logging

class TrashValve(QObject):

    def __init__(self, pins):  # keytype):
        QObject.__init__(self)

        global _
        _ = Settings._

        global logger
        logger = logging.getLogger(__name__)

        self.powerPin = Pin (pins['EngPw'], 'OUT')
        self.pinOpen = Pin (pins['Open'], 'IN')
        self.pinClose = Pin (pins['Close'], 'IN')

        self.init()

        logger.info('Trash valve has been created.')


    def init(self):
        logger.info("Start initialisation")
        #If valve is not closed
        if self.isOpen():  # Closing the valve
            logger.info('Closing the valve')
            self.close()


    def isOpen(self):
        return self.pinClose.getSignal()


    def isClosed(self):
        return self.pinOpen.getSignal()


    def open(self):
        self.powerPin.enable()
        logger.info('Opening started')
        closeListener = SensorListener(self.pinOpen, "TrashValveOpen", 300, 4000)
        self.connect(closeListener, QtCore.SIGNAL("TrashValveOpen"), self._openHandler)
        closeListener.start()


    def _openHandler(self, result):
        if result:
            self.emit(QtCore.SIGNAL("TrashValveOpen"))
        else:
            logger.critical("Trash valve is not open. Timeout.")
            err_level = Error.ErrorLevel.CRITICAL
            err_source = Error.ErrorSource.HARDWARE
            msg = _(u"Trash valve wasn't open by timeout.")
            err = Error.Error(err_level, err_source, msg)
            self.emit(QtCore.SIGNAL("HardwareFailed"), err)

        self.powerPin.disable()
        logger.info('Opening stopped')


    def close(self):
        self.powerPin.enable()
        logger.info('Closing started')
        closeListener = SensorListener(self.pinClose, "TrashValveClosed", 300, 4000)
        self.connect(closeListener, QtCore.SIGNAL("TrashValveClosed"), self._closeHandler)
        closeListener.start()


    def _closeHandler(self, result):
        if result:
            self.emit(QtCore.SIGNAL("TrashValveClosed"))
        else:
            logger.critical("Trash valve is not close. Timeout.")
            err_level = Error.ErrorLevel.CRITICAL
            err_source = Error.ErrorSource.HARDWARE
            msg = _(u"Trash valve wasn't closed by timeout.")
            err = Error.Error(err_level, err_source, msg)
            self.emit(QtCore.SIGNAL("HardwareFailed"), err)

        self.powerPin.disable()
        logger.info('Closing stopped')


