# -*- coding:utf-8 -*-
from PyQt4.Qt import QObject
from PyQt4 import QtCore, QtGui, uic
import base64
import BDL.BDCon as BDCon
from Errors import Errors


class ChoosingItemWindow(QObject):
    '''
    Класс описывает форму выбора предметов для продажи. 
    '''


    def __init__(self, payment, DbType):
        QObject.__init__(self)
        try:
            dbConnector= BDCon.BDCon(DbType)
            self.dbContext=dbConnector.dbContext                #Экземпляр подключенной базы данных  
        except:
            self.message=Errors(u'Ошибка подключения к базе данных')
            self.message.window.setWindowTitle(u'Ошибка')
            self.message.window.show()
            return
        self.window = uic.loadUi("UIForms//ChoosingItem.ui")
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.itemsList=self.dbContext.getSelledtItems()
        
        self.ItemButtonDict=self.getItemButtonDict()            # Кнопки и надписи формы и назначенные им предметы
        self.payment=payment                                    # Сумма, введенная пользователем
        self.fillMainForm() 
      
    def getItemButtonDict(self):
        if len(self.itemsList)==0:
            self.message=Errors(u'Ошибка подключения к базе данных')
            self.message.window.setWindowTitle(u'Ошибка')
            self.message.window.show()
            return            
        ibdict={}
        itemButton=ItemButton(1, self.itemsList, self.window.Button_1, self.window.label_1)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem)       
        ibdict[1]= itemButton 
        
        itemButton=ItemButton(2, self.itemsList, self.window.Button_2, self.window.label_2)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[2]= itemButton        
        
        itemButton=ItemButton(3, self.itemsList, self.window.Button_3, self.window.label_3)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[3]= itemButton 
        
        itemButton=ItemButton(4, self.itemsList, self.window.Button_4, self.window.label_4)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[4]= itemButton
                 
        itemButton=ItemButton(5, self.itemsList, self.window.Button_5, self.window.label_5)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[5]= itemButton         
        
        itemButton=ItemButton(6, self.itemsList, self.window.Button_6, self.window.label_6)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[6]= itemButton
        
        return ibdict
     
        
    def fillMainForm(self):
        for i in self.ItemButtonDict: 
            button=self.ItemButtonDict[i].button
            label=self.ItemButtonDict[i].label
            itemId=self.ItemButtonDict[i].itemId           
            if itemId==0:
                button.setIcon(QtGui.QIcon("img//Items//NoItem.jpg"))
                text=""
                button.setEnabled(False)
            else:
                qpixmap=QtGui.QPixmap()
                if pic is not None:
                    picBytes = base64.b64decode(pic)
                    qpixmap.loadFromData(picBytes)                
                
                
                button.setIcon(QtGui.QIcon(item.img)) 
                text="%s" %(item.price)
                QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), self.ItemButtonDict[i].sellItem)
            label.setText(text)        
    
    def payItem(self, item):
        self.emit(QtCore.SIGNAL("ItemSelected"), item)
        self.window.close()
        
        
        
class ItemButton(QObject):
    '''
    Класс описывает структуру, связывающую кнопку предмета на главной форме и предмет, закрепленный за ней
    '''

    def __init__(self, btnId, itemsList, button, label):
        QObject.__init__(self)
        if btnId<=len(itemsList):
            buttonContext=itemsList[btnId-1]
            self.btnId=btnId
            self.itemId=buttonContext[0]
            self.button=button
            self.label=buttonContext[1]
        else:
            self.itemId=0
       
    def sellItem(self):
        self.emit(QtCore.SIGNAL("SellItem"), self.item)        
        