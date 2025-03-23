import sys
import sqlite3
from ui_main import Ui_MainWindow
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidgetItem, QPushButton
)
from add_edit import AddEditCoffeeForm


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_data()

        self.addButton = QPushButton("Добавить", self)
        self.addButton.move(10, 560)

        self.editButton = QPushButton("Редактировать", self)
        self.editButton.move(120, 560)

        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

    def load_data(self):
        con = sqlite3.connect("release/data/coffee.sqlite")
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

    def add_coffee(self):
        dlg = AddEditCoffeeForm()
        if dlg.exec():
            self.load_data()

    def edit_coffee(self):
        selected = self.tableWidget.currentRow()
        if selected != -1:
            coffee_id = int(self.tableWidget.item(selected, 0).text())
            dlg = AddEditCoffeeForm(coffee_id)
            if dlg.exec():
                self.load_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
