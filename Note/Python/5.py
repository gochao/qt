# 对话框
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,\
    QInputDialog, QLineEdit, QFrame, QColorDialog, QFontDialog,\
    QLabel, QFileDialog, QTextEdit
from PyQt5.QtGui import QColor

class DialogExample(QWidget):
    def __init__(self):
        super().__init__()
        self.btn = QPushButton("Dialog", self)
        self.le = QLineEdit(self)
        self.ui()

    def ui(self):
        self.setGeometry(0, 0, 300, 300)
        self.setWindowTitle("Dialog")
        self.show()

        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showdialog)

        self.le.move(100, 100)

    def showdialog(self):
        text, ok = QInputDialog.getText(self, "myDialog", "enter your name")
        if ok:
            self.le.setText(str(text))


class ColorExample(QWidget):
    def __init__(self):
        super().__init__()
        self.btn = QPushButton("ColorDialog", self)
        self.frm = QFrame(self)
        self.ui()

    def ui(self):
        self.setGeometry(0, 0, 300, 300)
        self.setWindowTitle("ColorDialog")

        col = QColor(0, 0, 0)

        self.btn.move(20, 20)
        self.btn.clicked.connect(self.dialogshow)

        self.frm.setStyleSheet("QWidget {background-color:%s}" % col.name())
        self.frm.setGeometry(50, 50, 50, 50)

        self.show()

    def dialogshow(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.frm.setStyleSheet("QWidget {background-color:%s}" % col.name())


class FontExample(QWidget):
    def __init__(self):
        super().__init__()
        self.btn = QPushButton("Font-set", self)
        self.txt = QTextEdit()
        self.ui()

    def ui(self):
        self.btn.move(100, 100)
        self.btn.clicked.connect(self.fontdialog)

        self.lbl.move(200, 200)

        self.setGeometry(0, 0, 300, 300)
        self.show()

    def fontdialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.lbl.setFont(font)


class FileExample(QWidget):
    def __init__(self):
        super().__init__()
        self.btn = QPushButton("File", self)
        self.txt = QTextEdit("Files", self)
        self.ui()

    def ui(self):
        self.btn.move(100, 100)
        self.btn.clicked.connect(self.filedialog)

        self.txt.move(100, 200)

        self.setGeometry(0, 0, 400, 400)
        self.show()

    def filedialog(self):
        fname = QFileDialog.getOpenFileName(self, "Open file" ,"/home")
        if fname[0]:
            f = open(fname[0], 'r')
        with f:
            data = f.read()
            self.txt.setText(data)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # e1 = DialogExample()
    # e2 = ColorExample()
    # e3 = FontExample()
    e4 = FileExample()
    sys.exit(app.exec_())