from PyQt5 import uic,QtCore
from PyQt5.QtWidgets import QMainWindow
from datetime import datetime


class Ui_CellsMushroom(QMainWindow):

    def __init__(self,mainForm,connection):
        self.count = 1000
        self.dictMushrooms = dict()
        self.dictCount = dict()
        super().__init__()
        uic.loadUi('ui\CellsMushroom.ui', self)  

        self.con = connection
        self.cursor = self.con.cursor()

        self.main=mainForm

        self.setDateNow()
        self.pushButton.clicked.connect(self.newInfo)

        results = self.cursor.execute("""SELECT Id,Name,CountMushroom FROM mushroom 
                                      inner join price_mushroom on price_mushroom.IdMushroom = mushroom.Id
                                      Group by Id,Name,CountMushroom 
                                      Having max(DateCost) = DateCost""").fetchall()
        print((results))
        for result in results:
            
            Name=str(result[1])
            Name=Name.replace('(', '') 
            Name=Name.replace(')', '') 
            Name=Name.replace(',', '') 
            self.comboBox.addItem(Name[0::1]) 

            self.dictMushrooms.update({Name:result[0]})
            self.dictCount.update({Name:result[2]})
            getCount = self.cursor.execute(f"SELECT Sum(Count) FROM store_mushroom where store_mushroom.IdMushroom={result[0]}").fetchall()
            print(getCount[0][0])
            #self.dictCount.update({Name:result[0]})

            self.comboBox.currentTextChanged.connect(self.setCells)
            self.spinBox.valueChanged.connect(self.setCells)

    def setCells(self):
        if(self.comboBox.count!=0):
            mushroom = self.comboBox.currentText()
            costMushroom = self.spinBox.value()
            self.doubleSpinBox.setValue(costMushroom*self.dictCount[mushroom])

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
        getMoney = self.doubleSpinBox.value()

        results = self.cursor.execute("SELECT * FROM cells_mushroom ").fetchall()
        if(len(results)):
            id = int((self.cursor.execute("SELECT max(Id) FROM cells_mushroom").fetchall())[0][0]) +1
        else: id = 0

        if(mushroom !="" and costMushroom !=0 and dateSetCost !="",getMoney !=0.0 ):
            
            if dateSetCost.day()<10 :
                day="0"+str(dateSetCost.day())
            else: day=dateSetCost.day()

            if dateSetCost.month()<10 :
                month="0"+str(dateSetCost.month())
            else: month=dateSetCost.month()

            self.cursor.execute(f"""INSERT INTO cells_mushroom (Id, IdMushroom,CountMushroom,DateRealize,MoneyAbandon)
                                   VALUES ({id},"{mushroom}","{costMushroom}","{day}.{month}.{dateSetCost.year()}","{getMoney}")""")
            
            self.main.setRowsCellsMushrooms()

            self.close()
        else:
            self.label_5.setText("Не все, требуемые поля заполнены")

class Ui_CellsMushroomEdit(QMainWindow):

    def __init__(self,mainForm,connection,Id):
        self.count = 1000
        self.dictMushrooms = dict()
        self.dictCount = dict()
        super().__init__()
        uic.loadUi('ui\CellsMushroom.ui', self)  

        self.Id = Id

        self.con = connection
        self.cursor = self.con.cursor()

        self.main=mainForm

        self.pushButton.clicked.connect(self.newInfo)

        results = self.cursor.execute("""SELECT Id,Name,CountMushroom FROM mushroom 
                                        inner join price_mushroom on price_mushroom.IdMushroom = mushroom.Id
                                        Group by Id,Name,CountMushroom 
                                        Having max(DateCost) = DateCost""").fetchall()
        print((results))
        for result in results:
                
            Name=str(result[1])
            Name=Name.replace('(', '') 
            Name=Name.replace(')', '') 
            Name=Name.replace(',', '') 
            self.comboBox.addItem(Name[0::1]) 

            self.dictMushrooms.update({Name:result[0]})
            self.dictCount.update({Name:result[2]})
            getCount = self.cursor.execute(f"SELECT Sum(Count) FROM store_mushroom where store_mushroom.IdMushroom={result[0]}").fetchall()
            print(getCount[0][0])
            #self.dictCount.update({Name:result[0]})

            self.comboBox.currentTextChanged.connect(self.setCells)
            self.spinBox.valueChanged.connect(self.setCells)

        results = self.cursor.execute(f"""SELECT mushroom.Name,CountMushroom,DateRealize,MoneyAbandon FROM cells_mushroom join  
                                      mushroom on mushroom.Id  = cells_mushroom.IdMushroom where cells_mushroom.Id={self.Id} """).fetchall()

        for result in results:
            self.comboBox.setCurrentText(result[0])
            self.spinBox.setValue(int(result[1]))
            self.setDate(result[2])
            self.doubleSpinBox.setValue(float(result[3]))

    def setCells(self):
        if(self.comboBox.count!=0):
            mushroom = self.comboBox.currentText()
            costMushroom = self.spinBox.value()
            self.doubleSpinBox.setValue(costMushroom*self.dictCount[mushroom])

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
        getMoney = self.doubleSpinBox.value()

        id = self.Id

        if(mushroom !="" and costMushroom !=0 and dateSetCost !="",getMoney !=0.0 ):
            
            if dateSetCost.day()<10 :
                day="0"+str(dateSetCost.day())
            else: day=dateSetCost.day()

            if dateSetCost.month()<10 :
                month="0"+str(dateSetCost.month())
            else: month=dateSetCost.month()

            self.cursor.execute(f"""UPDATE cells_mushroom SET IdMushroom = '{mushroom}', CountMushroom = '{costMushroom}',
                                DateRealize = '{day}.{month}.{dateSetCost.year()}', MoneyAbandon="{getMoney}"
                                where Id = {id};""")
            
            self.main.setRowsCellsMushrooms()

            self.close()
        else:
            self.label_5.setText("Не все, требуемые поля заполнены")
