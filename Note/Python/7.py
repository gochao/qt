# QWidgets(2) 括像素图（QPixmap）,单行文本框（QLineEdit）和下拉列表框（QComboBox）
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QComboBox,\
    QLabel, QHBoxLayout, QSplitter, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class QPixmapExample(QWidget):
    def __init__(self):
        super().__init__()
        self.ui()

    def ui(self):
        # 像素图（QPixmap）
        pixmap = QPixmap("web.jpg")
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        hbox = QHBoxLayout(self)
        hbox.addWidget(lbl)

        self.setLayout(hbox)
        self.setGeometry(0, 0, 10, 10)
        self.setWindowTitle("QWidget(2)")
        self.show()


class QLineEditExample(QWidget):
    def __init__(self):
        super().__init__()
        # 单行文本框（QLineEdit）
        self.lbl = QLabel("text", self)
        self.lbl.move(50, 100)
        qle = QLineEdit(self)
        qle.setGeometry(50, 120, 200, 30)
        qle.textChanged[str].connect(self.text_changed)

        self.setGeometry(0, 0, 500, 500)
        self.show()

    def text_changed(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()


class QSplitterExample(QWidget):
    def __init__(self):
        super().__init__()
        f1 = QFrame(self)
        f1.setFrameShape(QFrame.StyledPanel)
        f2 = QFrame(self)
        f2.setFrameShape(QFrame.StyledPanel)
        f3 = QFrame(self)
        f3.setFrameShape(QFrame.StyledPanel)

        s1 = QSplitter(Qt.Horizontal)
        s2 = QSplitter(Qt.Horizontal)
        s1.addWidget(f1)
        s1.addWidget(f2)
        s2.addWidget(s1)
        s2.addWidget(f3)

        hbox = QHBoxLayout(self)
        hbox.addWidget(s2)

        self.setGeometry(0, 0, 500, 500)
        self.setLayout(hbox)
        self.show()


class QComboBoxExample(QWidget):
    def __init__(self):
        super().__init__()

        combo = QComboBox(self)
        self.lbl = QLabel(self)

        combo.addItem("haha")
        combo.addItem("lala")
        combo.addItem("hiahia")

        self.lbl.move(50, 50)
        combo.move(50,80)

        combo.activated[str].connect(self.abc)

        self.setGeometry(0, 0, 400, 400)
        self.show()
    def abc(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # e1 = QPixmapExample()
    # e2 = QLineEditExample()
    # e3 = QSplitterExample()
    e4 = QComboBoxExample()
    sys.exit(app.exec())