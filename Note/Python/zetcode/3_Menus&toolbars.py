from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon
import sys


# 继承的类是QMainWindow,包含状态栏,菜单栏,工具栏
class Example1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # 设置状态栏信息
        # 状态栏提示是对组件的说明或帮助
        self.statusBar().showMessage("Ready")

        self.setGeometry(300, 300, 1000, 200)
        self.setWindowTitle("statusbar")
        self.show()


# 菜单栏
# 菜单栏里有一个file菜单
# file菜单里有有一个exit_action的QAction
# 这个QAcion有图标,有快捷键,和状态栏说明
class Example2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # 创建一个退出动作,赋予图标,快捷键,状态说明
        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip("退出")
        # 动作触发信号,连接到退出槽
        exit_action.triggered.connect(qApp.quit)

        # 调用状态栏,使它创建
        self.statusBar()

        # 在菜单栏创建一个菜单
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exit_action)

        self.setGeometry(300,300, 1000, 200)
        self.show()



class Example3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个退出动作,赋予图标,快捷键,状态说明
        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip("退出")
        # 动作触发信号,连接到退出槽
        exit_action.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('tuichu')
        self.toolbar.addAction(exit_action)


        self.setGeometry(300, 300, 1000, 200)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = Example3()

    sys.exit(app.exec_())