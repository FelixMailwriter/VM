# -*- coding:utf-8 -*-
from PyQt4.Qt import QObject
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QIcon
from Common.Item import Item
from Errors import Errors
import gettext

class ChoosingItemWindow(QObject):
    '''
    Класс описывает форму выбора предметов для продажи. 
    '''

    def __init__(self, payment, dbProvider):
        QObject.__init__(self)

        self.dbProvider=dbProvider

        #Получаем сгруппированную таблицу продаваемых предметов (сумма по магазинам по каждому типу предмета) 
        self.itemsForSale=self.dbProvider.getItemsForSale() 
        
        self.window = uic.loadUi("UIForms//ChoosingItem.ui")
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        self.ItemButtonDict=self.getItemButtonDict()                            # Кнопки и надписи формы и назначенные им предметы
        self.payment=payment                                                    # Сумма, введенная пользователем
        self.timer=QTimer()                                                     #Таймер возврата на титульную страницу
        self.timer.timeout.connect(self._backToTitlePage)
        self.timer.start(30000)
        self.fillMainForm() 
      
    def getItemButtonDict(self):
        if len(self.itemsForSale)==0:
            self.message=Errors(_(u'There are no items to sell'))
            self.message.window.setWindowTitle(_(u'Message'))
            self.message.window.show()
            return            
        ibdict={}
        itemButton=ItemButton(1, self.itemsForSale, self.window.Button_1, self.window.label_1)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem)       
        ibdict[1]= itemButton 
        
        itemButton=ItemButton(2, self.itemsForSale, self.window.Button_2, self.window.label_2)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[2]= itemButton        
        
        itemButton=ItemButton(3, self.itemsForSale, self.window.Button_3, self.window.label_3)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[3]= itemButton 
        
        itemButton=ItemButton(4, self.itemsForSale, self.window.Button_4, self.window.label_4)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[4]= itemButton
                 
        itemButton=ItemButton(5, self.itemsForSale, self.window.Button_5, self.window.label_5)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[5]= itemButton         
        
        itemButton=ItemButton(6, self.itemsForSale, self.window.Button_6, self.window.label_6)
        self.connect(itemButton, QtCore.SIGNAL("SellItem"), self.payItem) 
        ibdict[6]= itemButton
        
        return ibdict
     
        
    def fillMainForm(self):
        self._setLabels()
        for i in self.ItemButtonDict: 
            button=self.ItemButtonDict[i].button
            label=self.ItemButtonDict[i].label
            #itemId=self.ItemButtonDict[i].itemId           
            #if itemId==0:
            if self.ItemButtonDict[i].item is None:
                button.setIcon(QtGui.QIcon("img//Items//NoItem.jpg"))
                label.setText=("")
                button.setVisible(False)
            else:
                icon=self.ItemButtonDict[i].item.icon#.dbProvider.getItemPictureById(itemId)
                if icon is not None:
                    button.setIcon(QIcon(icon))
                QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), self.ItemButtonDict[i].sellItem)
   
    def _setLabels(self):
        self.window.lbl_selectModel.setText(_(u'Select the model'))
   
    def payItem(self, item):
        self.timer.stop()
        self.emit(QtCore.SIGNAL("ItemSelected"), item)
        self.window.close()
        
    def _backToTitlePage(self):
        self.emit(QtCore.SIGNAL("TimeOutPage"), self.window) 
                   
class ItemButton(QObject):
    '''
    Класс описывает структуру, связывающую кнопку предмета на главной форме и предмет, закрепленный за ней
    '''

    def __init__(self, btnId, itemsForSale, button, label):
        QObject.__init__(self)
        self.button=button
        self.label=label
        if btnId<=len(itemsForSale):
            buttonContext=itemsForSale[btnId-1]
            self.btnId=btnId
            itemId=buttonContext[0]
            itemName=buttonContext[1]
            itemPrice=buttonContext[2]/100.
            itemIcon=buttonContext[3]
            self.item=Item(itemId, itemName, itemPrice, itemIcon)
            self.label.setText(str(int(itemPrice)))
        else:
            itemId=0
            self.item=None
            self.label.setText('')
       
    def sellItem(self):
        self.emit(QtCore.SIGNAL("SellItem"), self.item)        
        