import sys
import db
import sqlite3
from ui.Main import Ui_Main
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    con = sqlite3.connect(f"resources/database/{db.DATABASE_NAME}")

    app = QApplication(sys.argv)
    app.setStyle('windowsvista') 
    ex = Ui_Main(con)
    ex.show()
    sys.exit(app.exec_())
