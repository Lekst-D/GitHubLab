from PyQt5 import uic,QtCore
from PyQt5.QtWidgets import QMainWindow
from datetime import datetime

class Ui_Mushroom(QMainWindow):

    def __init__(self,mainForm,connection):
        self.count = 1000
        super().__init__()
        uic.loadUi('ui\Mushroom.ui', self)  

        self.con = connection
        self.cursor = self.con.cursor()

        self.main=mainForm

        self.setDateNow()
        self.pushButton.clicked.connect(self.newInfo)
    

    def setDateNow(self):
        date_str = datetime.today().strftime('%d.%m.%Y')

        qdate = QtCore.QDate.fromString(date_str, 'dd.MM.yyyy')
        self.dateEdit.setDisplayFormat('dd.MM.yyyy')
        self.dateEdit.setDate(qdate)

    def newInfo(self):

        name = self.lineEdit.text()
        description = self.textEdit.toPlainText()
        timeLife = self.lineEdit_3.text()
        costMushroom = self.doubleSpinBox.value()
        dateSetCost = self.dateEdit.date()

        results = self.cursor.execute("SELECT * FROM mushroom ").fetchall()
        if(len(results)):
            id = int((self.cursor.execute("SELECT max(Id) FROM mushroom").fetchall())[0][0]) +1
        else: id = 0

        if(name !="" and description !="" and timeLife !="" and costMushroom !=""and dateSetCost !=""):
            self.cursor.execute(f"""INSERT INTO mushroom (Id, Name,Description,TimeLife)
                                  VALUES ({id},"{name}","{description}","{timeLife}" )""")
            
            if dateSetCost.day()<10 :
                day="0"+str(dateSetCost.day())
            else: day=dateSetCost.day()

            if dateSetCost.month()<10 :
                month="0"+str(dateSetCost.month())
            else: month=dateSetCost.month()

            self.cursor.execute(f"""INSERT INTO price_mushroom (IdMushroom, CountMushroom,DateCost) 
                                VALUES ({id},"{costMushroom}","{day}.{month}.{dateSetCost.year()}") """)
            
            self.main.setRowsMushrooms()

            self.close()
        else:
            self.label_8.setText("Не все, требуемые поля заполнены")


class Ui_MushroomEdit(QMainWindow):

    def __init__(self,mainForm,connection,Id):
        self.count = 1000
        self.Id=Id
        super().__init__()
        uic.loadUi('ui\Mushroom.ui', self)  

        self.con = connection
        self.cursor = self.con.cursor()

        self.main=mainForm

        
        self.pushButton.clicked.connect(self.newInfo)

        results = self.cursor.execute(f"""SELECT Name,Description,TimeLife,CountMushroom,DateCost FROM 
                                      mushroom join  price_mushroom on mushroom.Id  = price_mushroom.IdMushroom where Id={self.Id} """).fetchall()

        for result in results:
            self.lineEdit.setText(result[0])
            self.textEdit.setText(result[1])
            self.lineEdit_3.setText(result[2])
            self.doubleSpinBox.setValue(float(result[3]))
            #self.dateEdit.setValue(result[5])
            self.setDate(result[4])

        print(Id)

    def setDate(self,date):
        print(date)
        qdate = QtCore.QDate.fromString(date, "dd.MM.yyyy")
        self.dateEdit.setDisplayFormat('dd.MM.yyyy')
        self.dateEdit.setDate(qdate)

    def newInfo(self):

        name = self.lineEdit.text()
        description = self.textEdit.toPlainText()
        timeLife = self.lineEdit_3.text()
        costMushroom = self.doubleSpinBox.value()
        dateSetCost = self.dateEdit.date()

        id = self.Id

        if(name !="" and description !="" and timeLife !="" and costMushroom !=0 and dateSetCost !=""):
            self.cursor.execute(f"""UPDATE mushroom SET Name = '{name}',Description = '{description}',
                                TimeLife = '{timeLife}' where Id = {id};""")

            self.cursor.execute(f"""UPDATE price_mushroom SET CountMushroom = '{costMushroom}',
                                DateCost='{dateSetCost.day()}.{dateSetCost.month()}.{dateSetCost.year()}' where IdMushroom = {id};""")

            self.main.setRowsMushrooms()
            self.main.setRowsKeeperMushrooms()
            self.main.setRowsCellsMushrooms()

            self.close()
        else:
            self.label_8.setText("Не все, требуемые поля заполнены")