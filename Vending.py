# -*- coding:utf-8 -*-

import time
from BDL.DataSources import MySQLDB, TestDb
# import HdWareCon.RB as RB
from HdWareCon.GPIO_Socket import GPIO_Socket
from PyQt4.Qt import QObject
from PyQt4 import QtCore
from UI.ScanBrelok import ScanBrelok
from UI.FinishWindow import FinishWindow
from UI.ChoosingItem import ChoosingItemWindow
from UI.ReceiveCash import ReceiveCash
from UI.GivingOutItem import GivingOutItem
from Common.Logs import LogEvent
import KP.KPManager as KP
import Common.Settings as Settings
import Common.Error as Error
import Common.Logs as Logs


class Vending(QObject):

    def __init__(self, payment):
        QObject.__init__(self)

        global _
        _ = Settings._

        self.DbType = 'TestDB'  # SQLDB'

        self.payment = payment  # Сумма, введенная пользователем


    def reset(self):

        # ----- Connect to DataBase -----
        try:
            self.dbProvider = self._getDbProvider(self.DbType)  # Подключение к выбранной БД
        except Exception as e:
            err_level = Error.ErrorLevel.CRITICAL
            err_source = Error.ErrorSource.DATABASE
            msg = _(u"Database connection error")
            err = Error(err_level, err_source, msg)
            self.emit(QtCore.SIGNAL("InitFailed"), err)


        # ----- GPIO Socket  initialization -----
        programmatorPinSettings, \
        magazinesPinSettings, \
        PinGetOutSensor, \
        PinDropOff = self.dbProvider.getGPIOPinSettigs()
        if len(programmatorPinSettings) == 0 or \
            len (magazinesPinSettings) == 0 or \
            PinGetOutSensor == '' or \
            PinDropOff == '':
            self.emit(QtCore.SIGNAL("Reset"), False)
        try:
            self.gpio = GPIO_Socket(programmatorPinSettings,
                                    magazinesPinSettings,
                                    self.magazinItemsMap,
                                    PinGetOutSensor,
                                    PinDropOff
                                    )
        except:
            err_level = Error.ErrorLevel.CRITICAL
            err_source = Error.ErrorSource.SOFTWARE
            msg = _(u"GPIO init error")
            err = Error(err_level, err_source, msg)
            self.emit(QtCore.SIGNAL("InitFailed"), err)

        self.connect(self.gpio, QtCore.SIGNAL("ScanFinished"), self._scanFinishHandler)
        self.connect(self.gpio, QtCore.SIGNAL("WriteFinished"), self._writeFinishHandler)
        self.connect(self.gpio, QtCore.SIGNAL("InitResult"), self._initHandler)

        # Banknote receiver initialization -----
        try:
            self._initKP('NV-9')  # Инициализация купюроприемника
        except:
            pass  # Hardware exception

        # Programmator initialization ----
        try:
            pass  # Programmator init
        except:
            pass  # Hardware exception


    def _getDbProvider(self, dbType):
        # Getting DataBase provider depending on the DataBase type
        if dbType == 'TestDB':
            dbContext = TestDb.TestDb()
        elif dbType == 'SQLDB':
            dbContext = MySQLDB.MySQLDB()
        else:
            raise Exception(u"001")
        return dbContext


    def _initHandler(self, error):
        if error.errorlevel == Error.ErrorLevel.OK:
            return
        self.emit(QtCore.SIGNAL("InitFailed"), error)


    def _initKP(self, kpmodel):
        try:
            self.kpInitilaser = KP.KPInitilaser(kpmodel)  # Инициализация купюроприемника
            self.kpInitilaser.start()
            self.kpInstance = self.kpInitilaser.getKPInstance()  # Ссылка на купюроприемник
        except KP.KPErrorException as e:
            print e.value
            raise Exception(_(u'Hardware error'))
            return
        self.connect(self.kpInitilaser, QtCore.SIGNAL('Init finished'), self._setKPInstance)


    def _setKPInstance(self, kpInstance):
        if kpInstance is None:
            message = _(u"Notereceiver initialization error. Code:001")
            print message
            raise Exception(message)
            return
        self.kpInstance = kpInstance


    def start(self):
        self.scanBrelokWindow = ScanBrelok()
        self.connect(self.scanBrelokWindow, QtCore.SIGNAL("ScanBrelok"), self.gpio.scanBrelok)
        self.connect(self.scanBrelokWindow, QtCore.SIGNAL("SimulateScanOK"), self.simScan)
        self.scanBrelokWindow.window.show()





    def selektItem(self):
        self.choosingItemWindow = ChoosingItemWindow(self.payment, self.dbProvider)  # окно выбора предмета
        self.connect(self.choosingItemWindow, QtCore.SIGNAL("ItemSelected"), self.paymentStart)
        self.connect(self.choosingItemWindow, QtCore.SIGNAL("TimeOutPage"), self.endApp)
        self.scanBrelokWindow.window.close()


    def paymentStart(self, item):
        while self.kpInitilaser.isRunning():
            time.sleep(1)
        if self.payment >= item.price:
            self.giveOutItem(item)
            return
        self.itemId = item
        self.receiveCashWindow = ReceiveCash(self.payment, item, self.dbProvider, self.kpInstance)
        self.connect(self.receiveCashWindow, QtCore.SIGNAL("PaymentCancelled"), self.paymentCancelled)
        self.connect(self.receiveCashWindow, QtCore.SIGNAL("GiveOutItem"), self.giveOutItem)
        self.connect(self.receiveCashWindow, QtCore.SIGNAL("TimeOutPage"), self.endApp)
        self.connect(self.receiveCashWindow, QtCore.SIGNAL("PaymentChange"), self._changePayment)
        self.connect(self.receiveCashWindow, QtCore.SIGNAL("TimeOutPage"), self.endApp)
        self.receiveCashWindow.receiveCashWindow.show()


    def _changePayment(self, payment):
        self.payment = payment


    def paymentCancelled(self, payment):
        self.payment = payment
        self.choosingItemWindow = ChoosingItemWindow(self.payment, self.dbProvider)
        self.connect(self.choosingItemWindow, QtCore.SIGNAL("ItemSelected"), self.paymentStart)
        self.connect(self.choosingItemWindow, QtCore.SIGNAL("TimeOutPage"), self.endApp)
        self.choosingItemWindow.window.show()


    def giveOutItem(self, item):
        self.givingOutItem = GivingOutItem()
        self.connect(self.gpio, QtCore.SIGNAL("OutingEnd"), self.givingOutHandler)

        # Убрать после тестов
        self.connect(self.givingOutItem, QtCore.SIGNAL("EngSendClick"), self.engSensClick)
        self.connect(self.givingOutItem, QtCore.SIGNAL("OutSensorClick"),
                     self.outSensClick)  #############################
        self.connect(self.givingOutItem, QtCore.SIGNAL("SimulateWriteOK"), self.simWrite)  #############################
        ###-------------------
        self.connect(self.givingOutItem, QtCore.SIGNAL("TimeOutPage"), self.endApp)
        self.givingOutItem.givingOutWindow.show()
        self.gpio.giveOutItem(item)


    def givingOutHandler(self, result, magazin, item):
        if result:
            # Запись в БД факта продажи
            self.dbProvider.sellItem(magazin, item, self.payment)
            # self.writeBrelokWindow=WriteBrelok()
            # self.connect(self.writeBrelokWindow, QtCore.SIGNAL("WriteBrelok"), self.writeBrelok)
            # self.connect(self.writeBrelokWindow, QtCore.SIGNAL("SimulateWriteOK"), self.simWrite)
            # self.connect(self.writeBrelokWindow, QtCore.SIGNAL("TimeOutPage"), self.endApp)
            # self.writeBrelokWindow.window.show()
            self.gpio.writeBrelok()
        else:
            # Запись в лог о провале продажи
            logMessages = []
            logEvent = LogEvent('Critical', 'Vending', 'Item %s have not been given' % (str(item.name)))
            logMessages.append(logEvent)
            self.dbProvider.writeLog(logMessages)
            self.givingOutItem.fail()


    def _scanFinishHandler(self, result):
        if result:
            self.selektItem()
        else:
            self.scanBrelokWindow.scanFail()


    def _writeFinishHandler(self, result):
        self.givingOutItem.givingOutWindow.close()
        if result:
            self.finishWindow = FinishWindow()
            self.connect(self.finishWindow, QtCore.SIGNAL("FinishProc"), self.endApp)
            # self.writeBrelokWindow.window.close()
            self.finishWindow.window.show()
        else:
            # self.writeBrelokWindow.writeFail()
            message = _(u'Key writing is failed. Call the techsupport.')
            errormsg = Errors(message)


    '''
    def _timeOutWindowHandler(self, window):
        if window is not None:
            window.close()
        self.emit(QtCore.SIGNAL('Restart'))
    
    def endApp(self):
        self.emit(QtCore.SIGNAL('End working'))
        print 'Программа закончила работу'    
    '''


    def endApp(self):
        self.emit(QtCore.SIGNAL('End working'))
        print 'Программа закончила работу'

        # ========== TEST =================


    def engSensClick(self):
        activMag = self.gpio.gpioSocket.activeMagazin
        if activMag is None: return
        eng = activMag.magEng
        eng.sensorPin.setSignal(1)


    def outSensClick(self):
        self.gpio.gpioSocket.getOutSensor.setSignal(1)


    def simScan(self):
        self.gpio.gpioSocket.programmator.pinScanOK.setSignal(1)


    def simWrite(self):
        self.gpio.gpioSocket.programmator.pinWriteOK.setSignal(1)
