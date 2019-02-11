# -*- coding:utf-8 -*-
from enum import Enum

class Error (object):

    def __init__(self, errorlevel, errorsource, msg):
        object.__init__(self)

        self.errorlevel = errorlevel
        self.errorsource = errorsource
        self.msg = msg


class ErrorLevel(Enum):
    CRITICAL = 1
    IMPORTANT = 2
    WARNING = 3
    INFO = 4
    OK = 5


class ErrorSource(Enum):
    PRINTER = 1
    CASHRECEIVER = 2
    PROGRAMMATOR = 3
    ITEMBOX = 4
    HARDWARE = 5
    DATABASE = 6
    SOFTWARE = 7
