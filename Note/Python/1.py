import sys
from PyQt5.QtWidgets import QApplication, QWidget,\
        QToolTip, QPushButton, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication
# 继承Qwidget类
class Example(QWidget):

    def __init__(self):
        # 使用父类的定义函数
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口的位置（前两个）和大小
        self.setGeometry(0, 0, 500, 500)

        # 移动到正中
        self.center()

        # 设置窗口标题为”Icon”
        self.setWindowTitle("PyQt5 测试程序")

        # 窗口的图标为“web”
        self.setWindowIcon(QIcon("web.jpg"))

        # 设置提示框字体
        QToolTip.setFont(QFont("SansSerif", 10))

        # 给主窗口生成一个提示框
        self.setToolTip("这里是主窗口")

        # 在主窗口上创建一个按钮
        btn = QPushButton("关闭", self)
        
        # 改变按钮大小和位置
        btn.resize(btn.sizeHint())
        btn.move(200, 400)
        
        btn.setToolTip("点击关闭窗口")

        # 点击信号 连接到 quit 方法槽
        btn.clicked.connect(QCoreApplication.instance().quit)

        self.show()

    # 关闭一个QWidget时 会触发closeEvent事件，这里复写这个方法 
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "关闭确认", "真的要离开?",\
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 移动至中心的函数
    def center(self):
        # 获取窗口矩形尺寸
        rec = self.frameGeometry()
        # 计算屏幕中心
        cent = QDesktopWidget().availableGeometry().center()
        # 将矩形中心移至计算的屏幕中心
        rec.moveCenter(cent)
        # 最后将主窗口的左上角与矩形的左上角对齐
        self.move(rec.topLeft())


if __name__ == "__main__":

    # 创建一个QApplication 每个都必须有
    app = QApplication(sys.argv)

    e = Example()

    # 结束自动清除
    sys.exit(app.exec_())
