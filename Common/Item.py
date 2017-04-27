#-*- coding:utf-8 -*-
from PIL import Image
class Item:
    '''
    Класс описывает продаваемые предметы
    '''

    def __init__(self, item_id, name, price):
        self.id=item_id
        self.name=name
        self.price=price
      
   
    def __str__(self):
        s="Id=%s, Name=%s" %(self.id,  self.name)#, self.imgPath)
        return s
    
    def __eq__(self, other):
        return self.id==other.id 
    
    def __gt__(self, other):
        return self.id>other.id 
    