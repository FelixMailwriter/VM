# -*- coding:utf-8 -*-

import serial
import time
from enum import __repr__
from KP.crc import CRC
from PyQt4 import QtCore
from PyQt4.Qt import QObject
import gettext 

class KPProvider(QObject):


    def __init__(self):
        QObject.__init__(self)
        self.conn=self._getConnection()
        self.crc=CRC()
        self.seq=0x00
        self.devNum=0x00
        self.currencyChannels=[]
        self.payFinish=False
        self.beActive=True
        self.busy=False
        self.timer = None
        self.trycount=1

                
    def disable(self):
        print 'send disable'
        self.beActive=False
        for i in range (0,6):
            if self.busy:
                time.sleep(1)
                continue 
            command=bytearray(1)
            command[0]=0x09
            comm=self._generateCommand(0x01, command)
            if self.conn.isOpen():
                self.conn.write(comm)
                self._reverseSeq 
               
    def receiveNote(self):
        '''
        настройка купюроприемника
        '''  
        self._setup()
        '''
        Прием купюры
        '''
        self.beActive=True
        self.busy=True

        self.trycount=1
        noteReceived=False
        while (not noteReceived and self.trycount<30 and self.beActive):
            data=self._poll()
            packLength=len(data)
            for i in range (0, packLength):
                if data[i]=='f0'.decode('hex'):
                    for p in range (i+1, packLength):
                        if data[p]=='ef'.decode('hex'):
                            channel=int(data[p+1].encode('hex'),16)
                            if not channel==0: 
                                noteReceived=True
                                self._stackingNote(channel)
                                self.trycount=0 
                                noteReceived=False                       
            time.sleep(1)
            self.trycount+=1
        if self.trycount>=30:
            self.busy=False
            self.disable()
            self.emit(QtCore.SIGNAL('ReceiveMoneyTimeout'))
        
    def _stackingNote(self, resChannel):
        print 'Купюра принята по каналу {}'.format(resChannel)
        self.busy=True
        self._poll()        
        for i in range (0,4):
            if self.beActive:
                data=self._poll()
                if (data[3]=='f0'.decode('hex') and data[4]=='cc'.decode('hex')):
                    time.sleep(1)
                elif (data[3]=='f0'.decode('hex') and data[4]=='ee'.decode('hex')):
                    channel=int(data[5].encode('hex'),16)
                    if channel==resChannel:
                        noteValue=self._getNoteValue(channel)
                        print 'Принято {} лей'.format(noteValue)
                        self.emit(QtCore.SIGNAL("Note stacked"), noteValue)
                    else:
                        raise DeviceErrorException(_(u"Error in recognition of note"))
            else: 
                self.busy=False
                break
   
    def _getNoteValue(self, channel):
        return self.currencyChannels[channel-1]

    def _setup(self):
        self.conn.open()
        '''
        Устанавливаем версию протокола
        '''
        if not self._setProtocolVersion():
            raise DeviceErrorException(_(u"Protocol version's setting error"))
            return False

        '''
        Запрашиваем настройки каналов купюр - номиналы по каналам
        '''
        if not self._getCurrencyByChannels():
            raise DeviceErrorException(_(u"Error in request of notes\' channels"))
            return False

        '''
        Очищаем буфер команд
        '''
        data=self._poll()
        pollOK=data[3]
        if not pollOK=='f0'.decode('hex'):    
            raise DeviceErrorException(_(u"Error in notes\' denomination reading"))
            return False

        '''
        Устанавливаем разрешенные каналы приема купюр
        '''
        if not self._setInhibits():
            raise DeviceErrorException(_(u"Error in setting channels of notes receiving"))
            return False
        
        '''
        Включаем купюроприемник
        '''
        if not self._enable():
            raise DeviceErrorException(_(u"Engage procedure error"))
            return False
        
        return True 
    
        '''
        Синхронизация
        '''
        syncOK=self._sync()
        trycount=1
        while ((not syncOK) and (trycount<4)):
            syncOK=self._sync()
            trycount+=1
            time.sleep(1)
        if not syncOK:
            raise DeviceErrorException(_(u"Device synchronization failed"))
            return False       
    
    def _poll(self):
        print '---------------'
        print 'send poll'
        command=bytearray(1)
        command[0]=0x07
        comm=self._generateCommand(0x01, command)
        self.conn.write(comm)
        data=self._getDataFromPort()
        self._reverseSeq()
        return data

    def showRecevedData(self, data):
        print '---------------'
        print 'Reseived data:'
        for i in range(0, len(data)):
            print data[i].encode('hex') 
        print '---------------'   
    
    def _setInhibits(self):#, channels):

        '''
        Варинт оперативного отключения каналов не реализован. Прием ведется по всем каналам
        chBytes=0x00
        for i in range(0,len(channels)):
            tempByte=0x01
            tempByte=tempByte<<channels[i]-1
            chBytes=chBytes|tempByte
        '''
        print '---------------'
        print 'send setInhibits'
        command=bytearray(3)
        command[0]=0x02
        command[1]=0xFF #При реализации оперативного отключения каналов в эти переменные записать
        command[2]=0xFF# chBytes для установки разрешенных каналов приема. Сейчас разрешены все каналы
        comm=self._generateCommand(0x03, command)         
        self.conn.write(comm)
        data=self._getDataFromPort()
        self._reverseSeq()
        if data[3]=='f0'.decode('hex'):
            print 'Inhibits command sent'
            print '---------------'
            return True
        else:
            print 'Inhibits command not sent'
            print '---------------' 
            return False         
        
    def _setProtocolVersion(self):
        print '---------------'
        print 'set protocol version sending'
        command=bytearray(2)
        command[0]=0x06
        command[1]=0x07
        comm=self._generateCommand(0x02, command)
        self.conn.write(comm)
        data=self._getDataFromPort()
        self._reverseSeq()
        if data[3]=='f0'.decode('hex'):
            print 'set protocol version sent'
            print '---------------'
            return True
        else:
            print 'set protocol version not sent'
            print '---------------' 
            return False                 
    
    def _enable(self):
        print '---------------'
        print 'Enable'
        self.beActive=True
        command=bytearray(1)
        command[0]=0x0A
        comm=self._generateCommand(0x01, command) 
        self.conn.write(comm)
        data=self._getDataFromPort()
        self._reverseSeq()
        if data[3]=='f0'.decode('hex'):
            print 'Enabled device'
            print '---------------'
            return True
        else:
            print 'Enable failed'
            print '---------------'
            return False         
            
    def _getCurrencyByChannels(self):
        #self.conn.open()
        print '---------------'
        print 'Get currency by channels'
        command=bytearray(1)
        command[0]=0x05
        comm=self._generateCommand(0x01, command) 
        self.conn.write(comm)
        data=self._getDataFromPort()
        self._reverseSeq()
        if data[3]=='f0'.decode('hex'):
            print 'Receiving currency sucsessful'
            print '---------------'
            time.sleep(1)
            #Получаем список номиналов купюр по каналам
            channelsQTY=int(data[15].encode('hex'))
            endpos=len(data)-2
            startpos=endpos-4*channelsQTY
            for i in range(startpos, endpos,4):
                self.currencyChannels.append(int(data[i].encode('hex'),16))
            return True
        else:
            print 'Receiving currency failed'
            print '---------------'
            return False        
               
    def _getConnection(self):
        for tryConnect in range (1, 11):
            print 'Попытка инициализации купюроприемника: %d' %(tryConnect)
            for i in range(0,10):
                try:
                    conn = serial.Serial()
                    conn.baudrate = 9600
                    conn.port = "/dev/ttyACM%d" % i
                    conn.stopbits=2
                    conn.dsrdtr=1
                    conn.startbits=1
                    conn.parity='N'
                    conn.open()
                    conn.close()
                    return conn
                except serial.serialutil.SerialException :
                    pass
            time.sleep(2)
        raise PortNotFoundException(_(u'Note receiver\'s port is not found')) 
    
    def _getDataFromPort(self, length=6):
        print 'wait for answer...'
        for i in range (1,4):
            try:
                l=self.conn.inWaiting()
                if l>0:
                    data=self.conn.read(l)
                    print 'answer received'
                    print 'data length ' 
                    print len(data)
                    self.showRecevedData(data)
                    return data
                time.sleep(1)                
            except serial.SerialException:
                time.sleep(2)
                i=1
        raise DeviceErrorException(_(u'Devise not responding'))
        #return None   
            
    def _sync(self):
        if (not self.conn.is_open):
            self.conn.open() 
        self.seq=0x00 
        print '---------------'     
        print 'send sync'
        command=bytearray(1)
        command[0]=0x11
        comm=self._generateCommand(0x01, command)
        self.conn.write(comm)
        time.sleep(1)
        data=self._getDataFromPort()
        if data[3]=='f0'.decode('hex'):
            print 'Synk OK'
            print '---------------'
            return True
        else:
            print 'Synk Failed'
            print '---------------'
            return False
    
    def _generateCommand(self, commandlength, command):
        packetLength=len(command)+5
        cmd=bytearray(packetLength)
        cmd[0]=b'\x7F'
        cmd[1]=self.seq
        cmd[2]=commandlength
        for i in range(0, len(command)):
            cmd[i+3]=command[i]
        scmd=buffer(cmd, 1,packetLength-3)
        cmd[packetLength-2], cmd[packetLength-1] =self.crc.getcrc(scmd)
        return cmd 
  
    def _reverseSeq(self):
        pass
        if self.seq==0x00:
            self.seq=0x80
            return
        if self.seq==0x80:
            self.seq=0x00
       
         




            
class PortNotFoundException(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return __repr__(self.value)
    
            
class DeviceErrorException(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return __repr__(self.value)            
            
        