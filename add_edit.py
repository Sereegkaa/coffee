from ui_add_edit import Ui_AddEditCoffeeForm
from PyQt6.QtWidgets import QDialog
import sqlite3


class AddEditCoffeeForm(QDialog):
    def __init__(self, coffee_id=None):
        super().__init__()
        self.ui = Ui_AddEditCoffeeForm()
        self.ui.setupUi(self)
        self.coffee_id = coffee_id
        if coffee_id:
            self.load_data()

        self.saveBtn.clicked.connect(self.save_data)

    def load_data(self):
        con = sqlite3.connect("release/data/coffee.sqlite")
        cur = con.cursor()
        row = cur.execute("SELECT name, roast, ground, description, price, volume FROM coffee WHERE id = ?",
                          (self.coffee_id,)).fetchone()
        con.close()
        if row:
            self.nameEdit.setText(row[0])
            self.roastEdit.setText(row[1])
            self.groundCheck.setChecked(bool(row[2]))
            self.descEdit.setText(row[3])
            self.priceSpin.setValue(row[4])
            self.volumeSpin.setValue(row[5])

    def save_data(self):
        name = self.nameEdit.text()
        roast = self.roastEdit.text()
        ground = int(self.groundCheck.isChecked())
        desc = self.descEdit.text()
        price = self.priceSpin.value()
        volume = self.volumeSpin.value()

        con = sqlite3.connect("release/data/coffee.sqlite")
        cur = con.cursor()
        if self.coffee_id:
            cur.execute('''UPDATE coffee
                           SET name=?, roast=?, ground=?, description=?, price=?, volume=?
                           WHERE id=?''',
                        (name, roast, ground, desc, price, volume, self.coffee_id))
        else:
            cur.execute('''INSERT INTO coffee(name, roast, ground, description, price, volume)
                           VALUES (?, ?, ?, ?, ?, ?)''',
                        (name, roast, ground, desc, price, volume))
        con.commit()
        con.close()
        self.accept()
