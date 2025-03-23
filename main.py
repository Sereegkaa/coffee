import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.load_data()

    def load_data(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        con.close()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels([
            "ID", "Название", "Обжарка", "Молотый/Зерно", "Описание", "Цена", "Объем"
        ])

        for row, record in enumerate(result):
            for col, item in enumerate(record):
                display = "Молотый" if col == 3 and item else "В зёрнах" if col == 3 else str(item)
                self.tableWidget.setItem(row, col, QTableWidgetItem(display))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
