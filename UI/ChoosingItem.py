# -*- coding:utf-8 -*-
from PyQt4.Qt import QObject
from PyQt4 import QtCore, QtGui, uic


class ChoosingItemWindow(QObject):
    '''
    Класс описывает главную форму приложения. 
    '''


    def __init__(self, magazines, payment):
        QObject.__init__(self)
        self.window = uic.loadUi("UIForms//ChoosingItem.ui")
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ItemButtonDict=self.getItemButtonDict(magazines)   # Кнопки и надписи формы и назначенные им предметы
        self.payment=payment                                    # Сумма, введенная пользователем
        self.fillMainForm() 
      
        
    def getItemButtonDict(self, magazines):
        ibdict={}
        itemButton=ItemButton(1, magazines[1].item, self.window.Button_1, self.window.label_1)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem)       
        ibdict[1]= itemButton 
        
        itemButton=ItemButton(2, magazines[2].item, self.window.Button_2, self.window.label_2)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[2]= itemButton        
        
        itemButton=ItemButton(3, magazines[3].item, self.window.Button_3, self.window.label_3)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[3]= itemButton 
        
        itemButton=ItemButton(4, magazines[4].item, self.window.Button_4, self.window.label_4)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[4]= itemButton
                 
        itemButton=ItemButton(5, magazines[5].item, self.window.Button_5, self.window.label_5)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[5]= itemButton         
        
        itemButton=ItemButton(6, magazines[6].item, self.window.Button_6, self.window.label_6)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[6]= itemButton
        
        return ibdict
     
        
    def fillMainForm(self):
        for i in self.ItemButtonDict: 
            button=self.ItemButtonDict[i].button
            label=self.ItemButtonDict[i].label
            item=self.ItemButtonDict[i].item           
            if item is None: #.price==0:
                button.setIcon(QtGui.QIcon("img//Items//NoItem.jpg"))
                text=""
                button.setEnabled(False)
            else:
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

    def __init__(self, btnId, item, button, label):
        QObject.__init__(self)
        self.btnId=btnId
        self.item=item
        self.button=button
        self.label=label
        
    def sellItem(self):
        self.emit(QtCore.SIGNAL("SellItem"), self.item)        
        