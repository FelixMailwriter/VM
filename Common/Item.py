#-*- coding:utf-8 -*-
from PyQt4 import QtGui
import base64
class Item:
    '''
    Класс описывает продаваемые предметы
    '''

    def __init__(self, item_id, name, price, pic):
        self.id=item_id
        self.name=name
        self.price=price
        self.icon=self._getIcon(pic)
        
    def _getIcon(self, pic):
        qpixmap=QtGui.QPixmap()
        if pic is not None:
            picBytes = base64.b64decode(pic)
            qpixmap.loadFromData(picBytes)
        return qpixmap     
   
    def __str__(self):
        s="Id=%s, Name=%s" %(str(self.id),  self.name)#, self.imgPath)
        return s
    
    def __eq__(self, other):
        return self.id==other.id 
    
    def __gt__(self, other):
        return self.id>other.id 
    