import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, \
    QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QTextEdit

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl1 = QLabel('zetcode', self)
        lbl1.move(0,0)

        lbl2 = QLabel('tutorials', self)
        lbl2.move(35, 40)

        lbl3 = QLabel('for', self)
        lbl3.move(80, 80)


        self.setGeometry(300, 300, 1000, 300)
        self.show()


class Example2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建两个按钮
        ok_btn = QPushButton("OK")
        cancle_btn = QPushButton("Cancel")

        # 创建水平布局,添加拉伸因子,将两个按钮加进去
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_btn)
        hbox.addWidget(cancle_btn)

        # 创建竖直布局,将水平布局放入
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        # 设置主窗口布局
        self.setLayout(vbox)

        self.setGeometry(300, 300, 1000, 300)
        self.show()


class Example3(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']
        positions = [(i, j) for i in range(5) for j in range(4)]

        for position,name in zip(positions, names):
            if name == "":
                continue
            button = QPushButton(name)
            grid.addWidget(button, position[0], position[1])

        self.setGeometry(300, 300, 400, 400)
        self.show()


class Example4(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        title = QLabel("Title")
        author = QLabel("Author")
        review = QLabel("Review")

        title_edit = QLineEdit()
        author_edit = QLineEdit()
        review_edit = QTextEdit()

        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(title_edit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(author_edit, 2, 1)

        grid.addWidget(review, 3, 0)
        # 从第三行到第五行
        grid.addWidget(review_edit, 3, 1, 15, 1)

        self.setGeometry(300, 300, 400, 400)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = Example4()

    sys.exit(app.exec_())