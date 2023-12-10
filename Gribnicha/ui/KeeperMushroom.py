from PyQt5 import uic,QtCore
from PyQt5.QtWidgets import QMainWindow
from datetime import datetime


class Ui_KeeperMushroom(QMainWindow):

    def __init__(self,mainForm,connection):
        self.count = 1000
        self.dictMushrooms = dict()
        super().__init__()
        uic.loadUi('ui\KeeperMushroom.ui', self)  

        self.con = connection
        self.cursor = self.con.cursor()

        self.main=mainForm

        self.setDateNow()
        self.pushButton.clicked.connect(self.newInfo)

        results = self.cursor.execute("SELECT Id,Name FROM mushroom ").fetchall()
        print((results))
        for result in results:
            
            Name=str(result[1])
            Name=Name.replace('(', '') 
            Name=Name.replace(')', '') 
            Name=Name.replace(',', '') 
            self.comboBox.addItem(Name[0::1]) 

            self.dictMushrooms.update({Name:result[0]})

    def setDateNow(self):
        date_str = datetime.today().strftime('%d.%m.%Y')

        qdate = QtCore.QDate.fromString(date_str, 'dd.MM.yyyy')
        self.dateEdit.setDisplayFormat('dd.MM.yyyy')
        self.dateEdit.setDate(qdate)

    def newInfo(self):

        mushroom = self.comboBox.currentText()
        mushroom =int(self.dictMushrooms[mushroom]) 
        costMushroom = self.spinBox.value()
        dateSetCost = self.dateEdit.date()

        results = self.cursor.execute("SELECT * FROM store_mushroom ").fetchall()
        if(len(results)):
            id = int((self.cursor.execute("SELECT max(Id) FROM store_mushroom").fetchall())[0][0]) +1
        else: id = 0

        if(mushroom !="" and costMushroom !=0 and dateSetCost !=""):
            
            if dateSetCost.day()<10 :
                day="0"+str(dateSetCost.day())
            else: day=dateSetCost.day()

            if dateSetCost.month()<10 :
                month="0"+str(dateSetCost.month())
            else: month=dateSetCost.month()

            self.cursor.execute(f"""INSERT INTO store_mushroom (Id, IdMushroom,Count,DateRemain)
                                  VALUES ({id},"{mushroom}","{costMushroom}","{day}.{month}.{dateSetCost.year()}" )""")
            
            self.main.setRowsKeeperMushrooms()

            self.close()
        else:
            self.label_4.setText("Не все, требуемые поля заполнены")

            
class Ui_KeeperMushroomEdit(QMainWindow):

    def __init__(self,mainForm,connection,Id):
        self.count = 1000
        self.dictMushrooms = dict()
        super().__init__()
        uic.loadUi('ui\KeeperMushroom.ui', self)  

        self.Id = Id

        self.con = connection
        self.cursor = self.con.cursor()

        self.main=mainForm

        results = self.cursor.execute("SELECT Id,Name FROM mushroom ").fetchall()
        print((results))
        for result in results:
            
            Name=str(result[1])
            Name=Name.replace('(', '') 
            Name=Name.replace(')', '') 
            Name=Name.replace(',', '') 
            self.comboBox.addItem(Name[0::1]) 

            self.dictMushrooms.update({Name:result[0]})

        results = self.cursor.execute(f"""SELECT mushroom.Name,Count,DateRemain,TimeLife FROM store_mushroom join  
                                      mushroom on mushroom.Id  = store_mushroom.IdMushroom where store_mushroom.Id={self.Id} """).fetchall()

        for result in results:
            self.comboBox.setCurrentText(result[0])
            self.spinBox.setValue(int(result[1]))
            self.setDate(result[2])
        
        self.pushButton.clicked.connect(self.newInfo)

    def setDate(self,date):
        print(date)
        qdate = QtCore.QDate.fromString(date, "dd.MM.yyyy")
        self.dateEdit.setDisplayFormat('dd.MM.yyyy')
        self.dateEdit.setDate(qdate)

    def newInfo(self):

        mushroom = self.comboBox.currentText()
        mushroom =int(self.dictMushrooms[mushroom]) 
        costMushroom = self.spinBox.value()
        dateSetCost = self.dateEdit.date()

        id = self.Id

        if(mushroom !="" and costMushroom !=0.0 and dateSetCost !=""):
            
            if dateSetCost.day()<10 :
                day="0"+str(dateSetCost.day())
            else: day=dateSetCost.day()

            if dateSetCost.month()<10 :
                month="0"+str(dateSetCost.month())
            else: month=dateSetCost.month()

            self.cursor.execute(f"""UPDATE store_mushroom SET IdMushroom = '{mushroom}', Count = '{costMushroom}',
                                DateRemain = '{day}.{month}.{dateSetCost.year()}' where Id = {id};""")

            self.main.setRowsKeeperMushrooms()

            self.close()
        else:
            self.label_4.setText("Не все, требуемые поля заполнены")