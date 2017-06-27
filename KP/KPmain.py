# -*- coding:utf-8 -*-

import serial
import crcmod
import time
from crc import CRC
from KP import KPNV9

if __name__ == '__main__':
    kp=KPNV9()

    kp.receiveNote()


