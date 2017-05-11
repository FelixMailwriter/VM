# -*- coding:utf-8 -*-
from PyQt4 import QtCore
import usb.core
import usb.util
import time
from Common import Item
from enum import __repr__

'''
Принтер через USB в данной реализации работает нестабильно.
Необходима доработка.
'''
class Printer(QtCore.QThread):

    def __init__(self, params):
        QtCore.QThread.__init__(self)
        self.context=params                 #Ссодержимое чека (предметы или строки текста)
        self.dev=None                       #Сыллка на устройство печати
        self.printDevOut=None               #ссылка на канал вывода данных
        self.printDevIn=None                #ссылка на канал получения ответа от устройства
        self.reattach=False                 #Флаг отключения системного драйвера порта
        self.command=None                   #команда принтеру
        self.SEQ=0x20                       #Порядковый номер команды
        self._initial()                     #инициализация устройства
        
    def run(self):                    
        self._printCheck()                   #Печать чека
        self._disconnectDev()               #Отключение устройства
        
    def _printCheck(self):
        
        for checkElem in self.context:
            #Если печатать описание предмета
            if type(checkElem)==Item:
                pass
            #иначе печатаем свободную строку
            else:
                pass
    #Открытие фискального чека
    
    
    #Печать продаваемых товаров
    
    
    #Печать суммы чека
    
    
    #Закрытие фискального чека
    
    def _openFiskCheck(self):
        self._makeCommand(0x30,'1,00000,1')
        self._sendCommand(self.command)
        #data = self.dev.read(self.printDevIn.bEndpointAddress, self.printDevIn.wMaxPacketSize,1000)
        #print data
        self._makeCommand(0x35, '')
        self._sendCommand(self.command)
        #self.msleep(500)
        #data = self.dev.read(self.printDevIn.bEndpointAddress, self.printDevIn.wMaxPacketSize, 1000)
        #print data
        self._makeCommand(0x38, '')
        self._sendCommand(self.command)
        #self.msleep(500)
        #data = self.dev.read(self.printDevIn.bEndpointAddress, self.printDevIn.wMaxPacketSize, 1000)
        #print data
        
        self._disconnectDev()
        
        #self.msleep(600)
        #answer=self._getAnswer()
        #self._checkAnswer(answer)
    
    def _makeCommand(self, commandCode, commandParams):
        self.SEQ+=1
        #paramsLength=0
        #if len(commandParams)>0:
        params=self._getParamsBytes(commandParams)
        paramsLength=len(params)
        packadgeLength=10+paramsLength
        self.command=bytearray(packadgeLength)
        commandLength=4+paramsLength
        #Записываем байты длины строки, номера команды и кода команды
        self.command[0]=0x01
        self.command[1]=commandLength+0x20
        self.command[2]=self.SEQ
        self.command[3]=commandCode
        #Записываем байты строки параметров команды
        pos=4
        for b in params:
            self.command[pos]=b
            pos+=1
        #записываем байт признака конца команды
        self.command[pos]=0x05
        #получаем контрольную сумму
        bcc=self._getBCC(paramsLength)
        #дописываем байты контрольной суммы
        pos+=1
        for i in range(0,4):
            self.command[pos]=bcc[i]
            print 'bcc2={}'.format(bcc[i])
            pos+=1
        #дописываем байт призака конца пакета
        self.command[packadgeLength-1]=0x03
        
        #увеличиваем счетчик номера команды

        for i in self.command:
            print i
    
    def _sendCommand(self, command):
        self.printDevOut.write(command)
        #self.dev.write(self.printDevOut.bEndpointAddress, command, 5000)
        
    def _getAnswer(self):
        answer=self.printDevIn.read_all()
        print answer
            
            
    def _checkAnswer(self, answer):
        pass
        
    def _getBCC(self, paramsLength):
        sum=0
        #получаем сумму байт строки команды + параметров 
        for i in range(1, (paramsLength+5)):
            sum+=self.command[i]
        hexSum=hex(sum)
        #разделяем значения по одной цифре и прибавляем к ней 0x30
        bcc=bytearray(4)
        for i in range (0,4): bcc[i]=0x30
        count=3
        for i in range(len(hexSum)-1, 0, -1):
            if hexSum[i]=='x': break
            bcc[count]=int(hexSum[i],16)+0x30
            count-=1
        return bcc
       
    def _getParamsBytes(self, commandParams):
        seqParamSymbols=[]                  #Параметры, разбитые по символам
        for commparam in commandParams:
            param='{}'.format(commparam)
            for symbol in param:
                seqParamSymbols.append(symbol)
            #seqParamSymbols.append(',')
        lenParamsString=len(seqParamSymbols)
        bytesParam=bytearray(lenParamsString)
        for i in range(0, lenParamsString):
            asciiCode=ord(seqParamSymbols[i])
            if asciiCode>=48 and asciiCode<=57:
                num=int(chr(asciiCode),16)
                bytesParam[i]=num+0x30
            else:
                t=asciiCode
                bytesParam[i]=t
            
            if bytesParam[i]>=30 and bytesParam[i]<=39:
                bytesParam[i]+=0x30
        return bytesParam
        #print bytesParam

    
    def _initial(self):
        self._getPrintDevice()
        self.printDevOut, self.printDevIn=self._connectDev()
        if self.printDevOut==None or self.printDevIn==None:
            raise PrinterHardwareException(u'Printer endpoint setup error')
        
    def _getPrintDevice(self):   #получаем ссылку на устройство печати
    # ищем устройство по коду производителя и коду устройства
        self.dev = usb.core.find(idVendor=0x067b, idProduct=0x2303)
    # если устройство не найдено - 
        if self.dev is None:
            raise PrinterHardwareException(u'Device not found') 
            
        #Если устройство найдено, оключаем системный драйвер
        if self.dev.is_kernel_driver_active(0):
            self.reattach = True
            self.dev.detach_kernel_driver(0)
        self.dev.set_configuration()
                
    def _connectDev(self):       #получаем ссылку на каналы вывода и получения данных        
    # get an endpoint instance
        cfg = self.dev.get_active_configuration()
        intf = cfg[(0,0)]
        #получаем ссылку на канал вывода данных на печать
        epOut = usb.util.find_descriptor(
        intf,
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT) 
        
        #получаем ссылку на канал получения ответа от устройства печати
        epIn= usb.util.find_descriptor(
        intf,
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_IN) 
        
        return epOut, epIn 
    
    def _disconnectDev(self):
        usb.util.dispose_resources(self.dev)    #освобождаем ресурсы устройства

        if self.reattach:                       #подключаем системный драйвер обратно
            self.dev.attach_kernel_driver(0) 
        
# Exceptions

class PrinterHardwareException(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return __repr__(self.value)    
            