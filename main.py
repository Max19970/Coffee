import sys
import sqlite3
from UI.addEditCoffeeForm import Ui_Form
from UI.main_ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView


class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.load)
        self.pushButton_2.clicked.connect(self.addEdit)

        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        self.coffee = cur.execute("""SELECT * FROM coffee""").fetchall()
        con.close()

    def load(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        for e in self.coffee:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(e[1]))
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(e[2]))
            self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(e[3]))
            self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(e[4]))
            self.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(e[5]))
            self.tableWidget.setItem(rowPosition, 5, QTableWidgetItem(e[6]))

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

    def addEdit(self):
        self.aE = AddEditWindow(self)
        self.aE.show()


class AddEditWindow(QWidget, Ui_Form):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.rowCount = len(self.parent.coffee)
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(True)
        self.spinBox.setValue(1)
        self.check()
        self.fillContent()
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(self.rowCount + 1)

        self.spinBox.valueChanged.connect(self.check)
        self.spinBox.valueChanged.connect(self.fillContent)

        self.pushButton.clicked.connect(self.insert)
        self.pushButton_2.clicked.connect(self.edit)

    def check(self):
        if self.spinBox.value() <= self.rowCount:
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(True)
        else:
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(False)

    def fillContent(self):
        if self.spinBox.value() <= self.rowCount:
            self.lineEdit.setText(self.parent.coffee[self.spinBox.value() - 1][1])
            self.lineEdit_2.setText(self.parent.coffee[self.spinBox.value() - 1][2])
            self.lineEdit_3.setText(self.parent.coffee[self.spinBox.value() - 1][3])
            self.plainTextEdit.setPlainText(self.parent.coffee[self.spinBox.value() - 1][4])
            self.lineEdit_4.setText(self.parent.coffee[self.spinBox.value() - 1][5])
            self.lineEdit_5.setText(self.parent.coffee[self.spinBox.value() - 1][6])
        else:
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.plainTextEdit.setPlainText('')
            self.lineEdit_4.setText('')
            self.lineEdit_5.setText('')

    def insert(self):
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        cur.execute(f"""INSERT INTO coffee(id, name, roasting, type,
                description, cost, size) VALUES({self.spinBox.value()},
                 '{self.lineEdit.text()}', '{self.lineEdit_2.text()}',
                '{self.lineEdit_3.text()}', '{self.plainTextEdit.toPlainText()}',
                 '{self.lineEdit_4.text()}', '{self.lineEdit_5.text()}')""")
        con.commit()
        self.parent.coffee = cur.execute("""SELECT * FROM coffee""").fetchall()
        self.parent.load()
        con.close()
        self.close()

    def edit(self):
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        cur.execute(f"""UPDATE coffee SET name = '{self.lineEdit.text()}',
        roasting = '{self.lineEdit_2.text()}',
        type = '{self.lineEdit_3.text()}',
        description = '{self.plainTextEdit.toPlainText()}',
        cost = '{self.lineEdit_4.text()}',
        size = '{self.lineEdit_5.text()}'
        WHERE id = {self.spinBox.value()}""")
        con.commit()
        self.parent.coffee = cur.execute("""SELECT * FROM coffee""").fetchall()
        self.parent.load()
        con.close()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
