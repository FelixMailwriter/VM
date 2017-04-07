# -*- coding:utf-8 -*-

import os
from PyQt4.QtGui import QPixmap
from DB import DB
from Common.Item import Item

class TestDb(DB):
    '''
    БД для тестов
    '''    
    def __init__(self):
        self.QtyMagazines=6
        DB.__init__(self)
        self.Items={}
       
        
    def getItemsMap(self):
        ItemsMap={}
        item=Item(1,'First', 11,
                  self._getItemIcon(self._getItemImgPath('img//Items//1.jpg')))
        ItemsMap[1]=item
        item=Item(2,'Second',20,
                  self._getItemIcon(self._getItemImgPath('img/Items//2.jpg')))
        ItemsMap[2]=item
        item=Item(3,'Third', 21,
                  self._getItemIcon(self._getItemImgPath('img//Items//3.jpg')))
        ItemsMap[3]=item
        item=Item(4,'Fourth', 51,
                  self._getItemIcon(self._getItemImgPath('img//Items//4.jpg')))
        ItemsMap[4]=item
        item=Item(5,'', 0,
                  self._getItemIcon(self._getItemImgPath('img//Items//NoItem.jpg')))
        ItemsMap[5]=item
        item=Item(6,'', 0,
                  self._getItemIcon(self._getItemImgPath('img//Items//NoItem.jpg')))
        ItemsMap[6]=item
        return ItemsMap                
 
        
    def _getItemIcon(self, path):
        img=QPixmap(path)
        return img

    def _getItemImgPath(self, shortPath):
        path=os.path.abspath(shortPath)
        return path 
        
    
    
