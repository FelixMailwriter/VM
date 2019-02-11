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
        DB.__init__(self)
        self.QtyMagazines=6
        self.Items={}
       
    # def getGPIOPinSettigs(self):
    #     programmatorPinSettings={}
    #     programmatorPinSettings['Button'] = 9
    #     programmatorPinSettings['Yellow'] = 21
    #     programmatorPinSettings['Green'] = 11
    #     programmatorPinSettings['Power'] = 17
    #
    #     magazinesPinSettings={}
    #     magazinesPinSettings[(1,"EngPw")]=27
    #     magazinesPinSettings[(1, "EngSensor")]=22
    #     magazinesPinSettings[(1, "EmptySensor")]=10
    #
    #     magazinesPinSettings[(2,"EngPw")]=12
    #     magazinesPinSettings[(2, "EngSensor")]=16
    #     magazinesPinSettings[(2, "EmptySensor")]=5
    #
    #     magazinesPinSettings[(3,"EngPw")]=6
    #     magazinesPinSettings[(3, "EngSensor")]=13
    #     magazinesPinSettings[(3, "EmptySensor")]=19
    #
    #     magazinesPinSettings[(4,"EngPw")]=14
    #     magazinesPinSettings[(4, "EngSensor")]=15
    #     magazinesPinSettings[(4, "EmptySensor")]=18
    #
    #     magazinesPinSettings[(5,"EngPw")]=23
    #     magazinesPinSettings[(5, "EngSensor")]=24
    #     magazinesPinSettings[(5, "EmptySensor")]=25
    #
    #     magazinesPinSettings[(6,"EngPw")]=8
    #     magazinesPinSettings[(6, "EngSensor")]=7
    #     magazinesPinSettings[(6, "EmptySensor")]=12
    #
    #     PinGetOutSensor=26
    #     return programmatorPinSettings, magazinesPinSettings, PinGetOutSensor
            
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
    
        
    def getIdItemsinMagazinsMap(self, magQty=6):
        # itemMap=self._fillMagEmptyItems(magQty)
        itemMap = {}
        itemMap[1] = 1
        itemMap[2] = 1
        itemMap[3] = 2
        return itemMap
    
    def writeLog(self, logMessages):
