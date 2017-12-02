import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget,\
        QLabel, QDesktopWidget, QHBoxLayout, QVBoxLayout, QGridLayout


class ModelLayout(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pass

    def center(self):
        rec = self.frameGeometry()
        cent = QDesktopWidget().availableGeometry().center()
        rec.moveCenter(cent)
        self.move(rec.topLeft())


class AbsoluteLayout(ModelLayout):
    
    def initUI(self):
        label1 = QLabel("Zetcode", self)
        label2 = QLabel("tutorials", self)
        label3 = QLabel("for", self)

        label1.move(0, 0)
        label2.move(100, 100)
        label3.move(200, 200)

        self.setGeometry(0, 0, 500, 500)
        self.center()
        self.show()


class BoxLayout(ModelLayout):

    def initUI(self):
        
        button1 = QPushButton("OK")
        button2 = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(0.5)
        hbox.addWidget(button1)
        hbox.addWidget(button2)

        vbox = QVBoxLayout()
        vbox.addStretch(0)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


        self.setGeometry(0, 0, 300, 300)
        self.center()
        self.show()


class GridLayout(ModelLayout):

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        names = ["C", "B", "", "Close",
                 "7", "8", "9", "/",
                 "4", "5", "6", "*",
                 "1", "2", "3", "-",
                 "0", ".", "=", "+"
                ]

        positions = [(i, j) for i in range(5) for j in range(4)]

        for position, name in zip(positions, names):
            if name == "":
                continue

            button = QPushButton(name)
            grid.addWidget(button, *position)

        self.setGeometry(0, 0, 300, 300)
        self.center()
        self.show()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # e1 = AbsoluteLayout()
    # e2 = BoxLayout()
    e3 = GridLayout()
    sys.exit(app.exec_())
