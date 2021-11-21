import sys, sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.pushButton.clicked.connect(self.click)

    def click(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM coffee""").fetchall()
        con.close()
        print(result)

        for e in result:
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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
