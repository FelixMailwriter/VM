# -*- coding:utf-8 -*-

import serial
import crcmod
import time
from crc import CRC
from KPProvider import KPProvider

if __name__ == '__main__':
    kp=KPProvider()

    kp.receiveNote()


