# -*- coding:utf-8 -*-

from DB import DB
from Common.Item import Item

class MySQLDB(DB):
    '''
    classdocs
    '''


    def __init__(self):
        DB.__init__(self)
        '''
        Constructor
        '''
        
    def getGPIOHdWSettigs(self):
        programmatorSettings={}
        programmatorSettings["ProgrammatorScan"]=2
        programmatorSettings["ProgrammatorScanOK"]=3
        programmatorSettings["ProgrammatorWrire"]=4
        programmatorSettings["ProgrammatorWriteOK"]=17
        magazinesSettings={}
        magazinesSettings[(1,"EngPw")]=27
        magazinesSettings[(1, "EngSensor")]=22
        magazinesSettings[(1, "EmptySensor")]=10
        item=Item(1,'First', 11.11, 'img//Items//1.jpg')
        magazinesSettings[(1, "Item")]=item  
              
        magazinesSettings[(2,"EngPw")]=9
        magazinesSettings[(2, "EngSensor")]=11
        magazinesSettings[(2, "EmptySensor")]=5
        item=Item(2,'Second',22.22, 'img//Items//2.jpg')
        magazinesSettings[(2, "Item")]=item 
                 
        magazinesSettings[(3,"EngPw")]=6
        magazinesSettings[(3, "EngSensor")]=13
        magazinesSettings[(3, "EmptySensor")]=19
        item=Item(3,'Third', 33.33, 'img//Items//3.jpg')
        magazinesSettings[(3, "Item")]=item 
        
        magazinesSettings[(4,"EngPw")]=14
        magazinesSettings[(4, "EngSensor")]=15
        magazinesSettings[(4, "EmptySensor")]=18
        item=Item(4,'Fourth', 44.44, 'img//Items//4.jpg')
        magazinesSettings[(4, "Item")]=item 
        
        magazinesSettings[(5,"EngPw")]=23
        magazinesSettings[(5, "EngSensor")]=24
        magazinesSettings[(5, "EmptySensor")]=25
        item=Item(0,'',55.55,'')
        magazinesSettings[(5, "Item")]=item  
               
        magazinesSettings[(6,"EngPw")]=8
        magazinesSettings[(6, "EngSensor")]=7
        magazinesSettings[(6, "EmptySensor")]=12
        item=Item(0,'',66.66,'')
        magazinesSettings[(6, "Item")]=item
                 
        mapGetOutSensor=26
        return programmatorSettings, magazinesSettings, mapGetOutSensor 