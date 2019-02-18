# -*- coding:utf-8 -*-
import os
from PyQt4.Qt import QObject
from PyQt4 import QtCore, uic
from PyQt4.QtCore import QTimer
import datetime
from ConfigParser import ConfigParser
from Printer.PrnDK350 import Printer
import Vending
import Common.Settings as Settings
import Common.Error as Error
from Common.ErrorScreen import Errors


class VendingManager(QObject):

    def __init__(self):
        self.defaultLocale = 'ru_RU'
        self.translate = Settings.Translate()
        self.translate.setLang(self.defaultLocale)

        global _
        _ = Settings._

        QObject.__init__(self)
        path = os.path.abspath("UIForms//errorWindow.ui")
        self.window = uic.loadUi(path)
        self.cashInBox = 0
        self.getCashInBoxTimer = QTimer()
        self.getCashInBoxTimerIdle, self.setCashInBoxTimerIdle = self._getTimesCashIncome()
        print 'Start income cash after {}'.format(self.getCashInBoxTimerIdle)
        print 'Start outcome cash after {}'.format(self.setCashInBoxTimerIdle)
        self.getCashInBoxTimer.timeout.connect(self._getCashInBox)
        self.getCashInBoxTimer.start(self.getCashInBoxTimerIdle * 1000)

        self._start()


    def _getTimesCashIncome(self):
        filename = 'config.ini'
        section = 'printer'
        parser = ConfigParser()
        parser.read(filename)
        prn_config = {}
        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                prn_config[item[0]] = item[1]
        else:
            self._showError(u'Ошибка', u'Ошибка файла конфигурации. Отсутствует секция принтера.')
            message = _(u"Printer error. Device is not ready")
            self.errormsg = Errors(message, 60000)
            self.connect(self.errormsg, QtCore.SIGNAL('ErrorWindowClosing'), self._start)

        TimeZReport = prn_config['time_zreport'].split(':')

        startHour = int(TimeZReport[0])
        startMinutes = int(TimeZReport[1])

        timeGap = datetime.timedelta(minutes=int(prn_config['incomerest_timegap']))

        startTime = datetime.datetime.now().replace(hour=startHour, minute=startMinutes, second=0,
                                                    microsecond=0) - timeGap / 2
        if startTime <= datetime.datetime.now():
            startTime = datetime.datetime.now() + datetime.timedelta(days=1)
            startTime = startTime.replace(hour=startHour, minute=startMinutes, second=0, microsecond=0) - timeGap / 2
        timeToStart = startTime - datetime.datetime.now()
        return timeToStart.total_seconds(), timeGap.total_seconds()


    def _start(self):
        self.vending = Vending.Vending(0)
        self._connectionSignals()
        try:
            self.vending.reset()
        except Exception as e:
            message = _(u"Device doesn't work\n")
            message += _(u"Code: ") + e.message
            self.errormsg = Errors(message, 60000)
            self.errormsg.window.show()
            self.connect(self.errormsg, QtCore.SIGNAL('ErrorWindowClosing'), self._start)
            return

        self.vending.start()


    def _connectionSignals(self):
        self.connect(self.vending, QtCore.SIGNAL('Restart'), self._start)
        self.connect(self.vending, QtCore.SIGNAL('End working'), self._start)
        self.connect(self.vending, QtCore.SIGNAL("HardwareFailed"), self._hardwareErrorHandler)


    def _getCashInBox(self):
        print 'Stop inbox timer'
        self.getCashInBoxTimer.stop()
        self.stopApp()
        printer = Printer()
        print 'Remeber cash'
        self.cashInBox = printer.getDayMoney()
        printer.printXReport('2')
        print 'Set outcome timer on %d' % (self.setCashInBoxTimerIdle)
        self.setCashInBoxTimer = QTimer()
        self.setCashInBoxTimer.timeout.connect(self._setCashInBox)
        self.setCashInBoxTimer.start(self.setCashInBoxTimerIdle * 1000)


    def _setCashInBox(self):
        print 'Stop outbox timer'
        self.setCashInBoxTimer.stop()
        printer = Printer()
        print 'Writing cash %s' % (self.cashInBox)
        printer.setDayMoney(self.cashInBox)
        self.getCashInBoxTimerIdle, self.setCashInBoxTimerIdle = self._getTimesCashIncome()
        print 'Reset timers'
        print 'Set outcome timer on %d' % (self.getCashInBoxTimerIdle)
        self.getCashInBoxTimer.timeout.connect(self._getCashInBox)
        self.getCashInBoxTimer.start(self.getCashInBoxTimerIdle * 1000)
        self.window.close()
        print 'starting app'
        self._start()


    def stopApp(self):
        print 'stopping app'
        self.vending.scanBrelokWindow.window.close()
        self.vending = None
        self.window.label.setText(_(u'Device is in service. Please, wait.'))
        self.window.btn_close.setEnabled(False)
        self.window.show()

    def _hardwareErrorHandler(self, err):
        if err.errorlevel == Error.ErrorLevel.CRITICAL:
            pass # stop processing
        else:
            pass #write log