# 事件与信号

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget\
        , QVBoxLayout, QSlider, QLCDNumber, QPushButton
from PyQt5.QtCore import Qt, QObject, pyqtSignal


# 创建一个自定义信号
class Communicate(QObject):
    
    closeApp = pyqtSignal()


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
    
        # 创建LCD显示和滑动条,按钮
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)
        but1 = QPushButton("button1")
        but2 = QPushButton("button2")

        # 盒模型布局
        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)
        vbox.addWidget(but1)
        vbox.addWidget(but2)

        # 布局加入主窗口
        self.setLayout(vbox)
        
        # 信号-槽 链接
        sld.valueChanged.connect(lcd.display)
        but1.clicked.connect(self.buttonClicked)
        but2.clicked.connect(self.buttonClicked)

        self.c = Communicate()
        self.c.closeApp.connect(self.close)

        self.setGeometry(0, 0, 400, 400)
        self.center()
        self.show()

    # 重写事件处理函数
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
    
    def buttonClicked(self):
        self.close()

    # 鼠标点击 触发 自定义信号
    def mousePressEvent(self, event):
        self.c.closeApp.emit()
    
    def center(self):
        rec = self.frameGeometry()
        cent = QDesktopWidget().availableGeometry().center()
        rec.moveCenter(cent)
        self.move(rec.topLeft())

if __name__ == "__main__":

    app = QApplication(sys.argv)

    e = Example()

    sys.exit(app.exec_())

